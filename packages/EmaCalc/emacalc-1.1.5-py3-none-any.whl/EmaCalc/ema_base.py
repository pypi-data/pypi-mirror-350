"""General utility classes and functions for internal EmaCalc use.

Defines class
EmaParamBase --- container for common properties used by all model classes
    specifying the indexing of separate types of model parameters,
    calculating logprob for observed data, given tentative model parameters.

NOTE: To make the model identifiable, some restriction is necessary.
The zero point on the attribute scale is otherwise arbitrary,
if both latent-variable locations and response thresholds are freely variable.

This behavior is user-controlled by initialization arguments
restrict_attribute and restrict_threshold.

The model is also slightly restricted by a weakly informative prior,
for numerical stability in case of extreme response patterns,
e.g., aLL ratings in the highest ordinal category.


*** Version history:
* Version 1.1.5:
2025-05-23, deleted global EMA_BASE, because it does not work with pickle.load()

* Version 1.1.3:
2025-03-28, use ema_base.EMA_BASE as package-global constant object
2025-03-21, using ema_repr.EmaObject as superclass
2025-03-11, user-friendly check for input typos

* Version 1.0.2:
2023-09-10, update for Pandas groupby.transform(sum) -> ('sum') for future default change

* Version 1.0.1:
2023-06-10, minor cleanup in _make_prior, no effect on results

* Version 0.9.6:
2023-04-02, new access functions situation_prob_df, attribute_theta_df yielding pandas result

* Version 0.9.5:
2022-11-28, changed _theta_map() to define attribute theta directly from effect parameters
            depending on restrict_attribute setting.
            One beta parameter less, if restrict_attribute is True.
            EmaParamBase._restrict_attr() no longer needed.
2022-11-19, threshold calculations done by class methods in module ema_thresholds

* Version 0.9.3:
2022-08-12, allowing ordinal scale tied to more than one attribute
2022-08-02, changed EmaParamBase properties specifying index slices
2022-07-21, xi parameters stored in order (alpha, beta, eta) parameter groups
2022-07-15, separate beta_slices, eta_slices;
            to allow threshold parameters tied to more than one attribute
2022-07-13, changed all names involving scenario -> situation

* Version 0.9.2:
2022-06-12, response-threshold mapping functions
    mapped_width(), d_mapped_width_d_eta(), and mapped_width_inv()
    slightly modified to be safe against numerical underflow.
    Global PRIOR_PSEUDO_RESPONDENT slightly modified, with no apparent effect on result.

* Version 0.9:
2022-03-17, use Pandas CategoricalDtype instances in EmaFrame situation_dtypes and attributes
2022-03-18, use Pandas DataFrame for EMA data in EmaDataSet, to allow many input file formats

* Version 0.8.1
2022-02-28, changed class name -> EmaParamBase
2022-02-23, GMM comp moved to ema_model.EmaGroupModel, separate GMM for each group

* Version 0.7.1
2022-01-11, _make_prior with log normalized uniform scenario prob

* Version 0.7
2022-01-02, minor cleanup _make_prior: ONLY scalar precision shape for GMM components

* Version 0.6
2021-12-03, user-definable prior inter-individual variance for reference parameters
2021-12-05, testing ways to set hyper-prior
2021-12-06, boolean properties restrict_attribute, restrict_threshold of EmaParamBase
            for user-specified model restriction
2021-12-08, minor checks against numerical overflow

* Version 0.5.1
2021-11-26, allow ZERO Attributes, i.e., empty emf.attribute_grades
2021-12-01, cleanup some doc comments
2021-12-02, Attribute sensory location fixed == 0. for first Scenario category
            regardless of regression_effect specification.

* Version 0.5
2021-11-24, first published beta version
"""
# *** Use only K - 1 alpha params for each phase, no redundant parameters?
# *** e.g., with only alpha differences stored in xi ?
# *** use one beta parameter for sum(all traits), and remaining for trait differences?
#       for better covariance structure with independent xi parameters

import numpy as np
from itertools import chain
from collections import namedtuple
from scipy.special import logit, expit
from scipy.special import logsumexp, softmax
import logging
import pandas as pd

from EmaCalc.ema_repr import EmaObject
from EmaCalc.gauss_gamma import GaussianRV
# from EmaCalc.ema_thresholds import ThresholdsOld  # for backward compatibility
from EmaCalc.ema_thresholds import ThresholdsFree, ThresholdsMidFixed

# from EmaCalc.ema_display import aggregate_situation_prob  # ********* for TEST

# ------------------------------------------------------
__version__ = "2025-05-23"

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # *** TEST

PRIOR_PSEUDO_RESPONDENT = 0.5  # seems to work OK
# = hyperprior total pseudo-count re ONE real respondent
# = prior GaussianRV.mean.learned_weight for all GMM components.
# This value is NOT critical for Occam's Razor behavior.

PRIOR_PARAM_SCALE = 1.
# = main hyperprior scale of most Gaussian model parameters,
# defined in LatentNormal d-prime (probit) units for attribute parameters,
# rescaled if the LatentLogistic (logistic) model is used for latent variables.
# This prior may have effect on the Occam's Razor function:
# small values may allow several active GMM components with small variance,
# but experiments suggest the prior value is not critical.

# *** 2023-05-16, tested with PRIOR_PARAM_SCALE = 0.3:
# *** Too small, -> some GMM population-model comp. with only ONE member.

PRIOR_PREC_A = PRIOR_PSEUDO_RESPONDENT / 2
# = GaussianRV precision shape for ALL parameters

# PRIOR_PREC_A_THRESHOLDS = 4 * PRIOR_PREC_A
# *** Allow user to set smaller prior variance for threshold parameters ?
# *** 2023-05-13 TESTED, does not make clear difference to GMM number of components.

PRIOR_PREC_B = PRIOR_PARAM_SCALE**2 / 2
# = GaussianRV precision inv_scale for MOST EmaModel parameters
# -> allows very small precision <=> large inter-individual variance
# -> mode of prior component-element variance = PRIOR_PREC_B /(PRIOR_PREC_A + 1) approx= PRIOR_PREC_B


# ------------------------------------------------------- Help classes
AttributeSlice = namedtuple('AttributeSlice', ['beta_slice', 'eta_slice'])


class Slicer:
    """Help class to create consecutive slices for parts of parameter vector
    """
    def __init__(self, start=0):
        self.start = start

    def slice(self, length):
        """Create a new slice object tight after previous slice
        :param length: desired slice size
        :return: a slice object
        """
        stop = self.start + int(length)
        sl = slice(self.start, stop)
        self.start = stop  # for next call
        return sl


# ------------------------------------------------------------------
class EmaParamBase(EmaObject):
    """Container for common properties of ema_model.EmaModel and its sub-models.

    Each individual parameter distribution is represented by
    a large set of samples, stored as property EmaRespondentModel.xi, with
    xi[s, :] = s-th sample of the parameter vector for ONE respondent.

    All model classes share mapping properties defined here,
    for extracting parameter subsets of three different types
    from a xi array of parameter vectors.
    Parameter types are stored consecutively in order (alpha, beta, eta)
    """
    def __init__(self, emf, effects,
                 rv_class,
                 thr,
                 theta_map,
                 alpha_slices,
                 attribute_slices,
                 tied_scales,
                 comp_prior,
                 restrict_attribute=False,
                 restrict_threshold=False):
        """
        :param emf: single ema_data.EmaFrame instance,
        :param effects: iterable with regression-effect terms for attribute regression
            effects[i] = single key in emf.situation_dtypes.keys() or tuple of such keys
        :param rv_class: latent sensory variable class, defined in module ema_latent,
            defining the distribution as either logistic or normal (Gaussian).
        :param thr: class defining threshold calculations, defined in module ema_thresholds,
        :param theta_map: fixed 2D array to extract latent-variable location samples from xi array
        :param alpha_slices: list of slice objects, such that
            xi[:, alpha_slices[t]] = alpha = log-likelihood for situations in t-th test phase
        :param attribute_slices: list of AttributeSlice objects, ordered like emf.attribute_dtypes,
            with attribute_slices[i] = (beta_slice, eta_slice), such that
            xi[:, beta_slice] = beta = regression-effect parameters for i-th Attribute
            xi[:, eta_slice] = eta = threshold parameters for i-th Attribute
        :param tied_scales: list of indices into attribute_slices,
            to allow more than one attribute to use SAME ordinal scale
        :param comp_prior: single gauss_gamma.GaussianRV instance,
            prior for ALL GMM components in ema_group.PopulationModel instance
        :param restrict_attribute: (optional) boolean switch
            to force restriction on attribute sensory-variable location mean across situations
        :param restrict_threshold: (optional) boolean switch
            to force restriction on middle response-threshold location
        """
        self.emf = emf
        self.effects = effects
        self.rv_class = rv_class
        self.thr = thr
        self.theta_map = theta_map
        self.alpha_slices = alpha_slices
        self.attribute_slices = attribute_slices
        self.tied_scales = tied_scales
        self.comp_prior = comp_prior
        self.restrict_attribute = restrict_attribute  # needed? already defined in theta_map
        self.restrict_threshold = restrict_threshold  # needed? already defined by class thr

    def rrepr(self, r, level):
        """recursive repr function for EmaObject that has only ONE instance,
            but may be referenced in several other Ema class instances
            **** create only ONE GLOBAL instance ? **********
            """
        with np.printoptions(threshold=20, edgeitems=2):
            return super().rrepr(r, level) + '<at ' + hex(id(self)) + '>'  # *** TESTing for multiproc

    # def __repr__(self):
    #     return (self.__class__.__name__ + '(' +
    #             '\n\t'.join(f'{k}= {repr(v)},'
    #                         for (k, v) in self.__dict__.items()) +
    #             '\n\t)')

    @classmethod
    def initialize(cls, emf, effects, rv_class,
                   restrict_attribute=False,
                   restrict_threshold=False):
        """Assign all parameter-extraction properties, and
        prior mixture components as GaussianRV objects with correct size.
        :param emf: single ema_data.EmaFrame instance,
            defining the experiment structure.
        :param effects: iterable with regression-effect terms for attribute regression
            effects[i] = single key in emf.situation_dtypes.keys() or tuple of such keys
        :param rv_class: latent variable class, defined in ema_latent,
            defining its distribution as either logistic or normal.
        :param restrict_attribute: (optional) boolean switch
            to force restriction on attribute sensory-variable locations
        :param restrict_threshold: (optional) boolean switch
            to force restriction on response-threshold locations
        :return: a cls instance

        Result: all properties initialized
        NOTE: xi parameter slices in order: all alpha, all beta, all eta
        """
        _check_effects(emf, effects)
        effects = [e_i if type(e_i) is tuple else (e_i,)
                   for e_i in effects]
        # = list of requested regression effects of situation categories
        # to be estimated for their influence on Attribute responses.
        # Each element MUST be a tuple with one or more situation key(s).

        # Define mapping indices from rows of xi array to its parts:
        n_phases = emf.situation_shape[0]
        n_situations = np.prod(emf.situation_shape[1:], dtype=int)  # within each phase
        slice_gen = Slicer()  # creating adjacent slice objects
        alpha_slices = [slice_gen.slice(n_situations)
                        for _ in range(n_phases)]
        # = list of slice objects, such that
        # xi[:, alpha_slices[t]] = alpha = log-likelihood for situations in t-th test phase
        # i.e., n_phases slices with equal lengths, for all test phases.

        theta_map = _theta_map(emf, effects, restrict_attribute)
        # = fixed 2D array to extract latent-variable location samples from xi array
        # by method attribute_theta(...)

        n_beta = theta_map.shape[0]
        # = number of regression-effect parameters, same for every Attribute
        n_attributes = len(emf.attribute_dtypes)
        beta_slices = [slice_gen.slice(n_beta)
                       for _ in range(n_attributes)]
        # = list of slice objects, such that
        # xi[:, beta_slices[i]] = beta = effect parameters for i-th attribute, such that
        # latent-variable location theta = np.dot(beta, theta_map)

        if restrict_threshold:
            thr = ThresholdsMidFixed
        else:
            thr = ThresholdsFree
        # Number of eta parameters depends on class thr
        unique_slices = {scale_id: slice_gen.slice(thr.n_param(len(scale.categories)))
                         for (scale_id, scale) in emf.ordinal_scales.items()}

        eta_slices = [unique_slices[scale_id]
                      for scale_id in emf.attribute_scales.values()]
        # = list of slice objects, such that
        # xi[:, eta_slices[i]] = eta = threshold parameters for i-th attribute, such that
        # response thresholds tau = thr.tau(eta)
        # Some thresholds may be identical for more than one attribute
        attribute_slices = [AttributeSlice(beta, eta)
                            for (beta, eta) in zip(beta_slices,
                                                   eta_slices)]
        # *** attribute_slices as dict instead ?
        tied_scales = None
        if len(attribute_slices) > len(unique_slices):
            attribute_keys = list(emf.attribute_scales.keys())
            tied_scales = [[attribute_keys.index(a_key) for a_key in a_keys]
                           for a_keys in emf.scale_attributes.values()]
        # tied_scales[s] = list of attribute indices a_i, such that
        # attribute_slices[a_i].eta_slice is eta_slices[s],
        # allowing same eta parameters to be used for more than one attribute

        n_parameters = slice_gen.start  # no more slices needed
        comp_prior = _make_prior(n_parameters,
                                 alpha_slices,
                                 attribute_slices,
                                 rv_class)
        # = single GaussianRV instance, prior for ALL GMM components,
        # fixed throughout the VI learning procedure.
        logger.debug(f'PRIOR_PSEUDO_RESPONDENT = {PRIOR_PSEUDO_RESPONDENT:.3f}; ' +
                     f'PRIOR_PARAM_SCALE = {PRIOR_PARAM_SCALE:.3f}; ' +
                     f'PRIOR_PREC_A = {PRIOR_PREC_A:.3f}; ' +
                     f'PRIOR_PREC_B = {PRIOR_PREC_B:.3f}')
        logger.debug(f'comp_prior.prec.a = '
                     + np.array_str(comp_prior.prec.a,
                                    precision=3))
        logger.debug('comp_prior.prec.b = '
                     + np.array_str(comp_prior.prec.b,
                                    precision=5))
        logger.debug('mode{1 / comp_prior.prec}= '
                     + np.array_str(comp_prior.prec.mode_inv(),
                                    precision=5))
        return cls(emf, effects, rv_class,
                   thr,
                   theta_map,
                   alpha_slices,
                   attribute_slices,
                   tied_scales,
                   comp_prior,
                   restrict_attribute,
                   restrict_threshold)

    @property
    def n_parameters(self):  # *** needed ?
        if len(self.attribute_slices) > 0:
            return max(a_slice.eta_slice.stop
                       for a_slice in self.attribute_slices)
        else:
            return self.alpha_slices[-1].stop

    # def beta_0_size(self):  # needed only for old _restrict_attr
    #     """number of effect parameters for FIRST effect term
    #     :return: n_beta = scalar
    #
    #     NOTE: remaining effect terms are relative to first effect.
    #     """
    #     return np.prod([len(self.emf.situation_dtypes[sc_i].categories)
    #                     for sc_i in self.effects[0]],
    #                    dtype=int)

    def situation_prob(self, xi):
        """Extract probability-mass for situations, given parameters,
        used mainly by ema_display
        :param xi: 2D array with parameter samples
        :return: u = mD array with situation probability-mass within each phase,
            u[s, k0, k1, k2, ...] = s-th sample of P[(k1, k2,...)-th situation | phase k0]
            sum u[s, k0] == 1., for all s and k0

        2022-02-15, check for underflow
        """
        n_sc = self.alpha_slices[-1].stop
        alpha = xi[:, :n_sc].reshape((xi.shape[0], self.emf.n_phases, -1))
        alpha -= np.amax(alpha, axis=-1, keepdims=True)
        too_small = np.all(alpha < np.log(np.finfo(float).tiny), axis=-1)
        n_underflow = np.sum(too_small)
        if n_underflow > 0:
            logger.warning(f'situation_prob: {n_underflow} alpha samples too small. '
                           + 'Should not happen. Maybe too few responses?')
            logger.debug(f'alpha[too_small, :] = {alpha[too_small]}')
        u = np.exp(alpha)
        # avoid nan after normalization, should not be needed !
        u /= np.sum(u, axis=-1, keepdims=True)  # normalize within each Phase
        return u.reshape((-1, *self.emf.situation_shape))

    def situation_prob_df(self, xi, groupby=None, sample_head='_sample'):
        """Extract probability-mass for situations, given parameters,
        used mainly by ema_display
        :param xi: 2D array with parameter samples
        :param groupby: (optional) tuple with situation key(s) to be included.
            If undefined, include ALL situation dimensions as defined in self.emf
        :param sample_head: (optional) level name of sample index
        :return: ds = pandas Series object
            with a MultiIndex with levels (sample_head, *groupby),
            containing the CONDITIONAL probability for categories in groupby[0], given other groupby cases,
            aggregated across situation dimensions NOT included in groupby.
        """
        u = self.situation_prob(xi)
        # u[s, k0, k1, k2, ...] = s-th sample of conditional P[(k1, k2,...)-th situation | phase k0]
        # following -> *** separate module function aggregate_situation_prob ? ******
        df_index = pd.MultiIndex.from_product([range(len(u)),
                                               *[sit_dtype.categories
                                                 for sit_dtype in self.emf.situation_dtypes.values()]],
                                              names=[sample_head, *self.emf.situation_dtypes.keys()])
        if groupby is None:
            return pd.Series(u.reshape((-1,)), index=df_index)
        else:
            u /= u.shape[1]
            # u[s, k0, k1, k2, ...] = s-th sample of prob-mass P[(k0, k1, k2,...)-th situation]
            df = pd.Series(u.reshape((-1,)), index=df_index)
            df = df.groupby(level=[0, *groupby], sort=False, group_keys=True).sum()
            # **** needed only if len(groupby) > 1
            if len(groupby) > 1:
                # scale to CONDITIONAL prob for categories in groupby[0], given other dimensions
                df = df / df.groupby(level=[0, *groupby[1:]],
                                     sort=False, group_keys=True).transform('sum')
                # CHECK: df.groupby(level=[0, *groupby[1:]], sort=False).sum() == 1., in all groups
            return df

    def attribute_theta(self, xi, a):
        """Extract location of latent sensory variable, for ONE given attribute
        used only by ema_display
        :param xi: 2D array with parameter sample vectors
            xi[s, :] = s-th parameter sample vector
        :param a: attribute key = one of self.emf.attribute_grades.keys()
        :return: theta = mD array, with
            theta[s, k0, k1, ...] = s-th sample of
                attribute location, given the (k0, k1, ...)-th situation.
        """
        a_index = list(self.emf.attribute_dtypes.keys()).index(a)
        beta_slice = self.attribute_slices[a_index].beta_slice
        # *** attribute_slices as dict instead ?
        beta = xi[..., beta_slice]
        return np.dot(beta, self.theta_map).reshape((-1, *self.emf.situation_shape))

    def attribute_theta_df(self, xi, a, groupby=None, sample_head='_sample'):
        """Extract location of latent sensory variable, for ONE given attribute,
        given each situation category in selected situation dimension(s).
        Used mainly by ema_display
        :param xi: 2D array with parameter sample vectors
            xi[s, :] = s-th parameter sample vector
        :param a: attribute key = one of self.emf.attribute_grades.keys()
        :param groupby: (optional) tuple with situation key(s) to be included.
            If undefined, include ALL situation dimensions as defined in self.emf
        :param sample_head: (optional) level name of sample index
        :return: ds = pandas Series object
            with a MultiIndex with levels (sample_head, *groupby),
            containing the Attribute value samples for each category in groupby situation dimension(s),
            aggregated across all OTHER situation_dtypes not included in groupby,
            weighted by AVERAGE situation probabilities in those dimensions.
        """
        theta = self.attribute_theta(xi, a)
        # theta[s, k0, k1, ...] = s-th sample of attribute location, in (k0, k1, ...)-th situation.
        df_index = pd.MultiIndex.from_product([range(len(theta)),
                                               *[sit_dtype.categories
                                                 for sit_dtype in self.emf.situation_dtypes.values()]],
                                              names=[sample_head, *self.emf.situation_dtypes.keys()])
        theta_ds = pd.Series(theta.reshape((-1,)), index=df_index)
        if groupby is None:
            return theta_ds
        else: # weighted average across situation dimensions not included
            aggregate_by = list(set(self.emf.situation_dtypes.keys()) - set(groupby))
            # = OTHER situation dimensions to be aggregated out
            u = self.situation_prob_df(xi, sample_head=sample_head)  # *** use array access ??? ***
            # u = Series object with same MultiIndex as theta_ds),
            # containing the CONDITIONAL probability for categories in situation_dtypes[1:]
            # given Phase category in situation_dtypes[0]
            u = u / len(u.index.levels[1])
            # u = absolute prob.mass for each sample and situation category
            # w_cond = u / u.groupby(level=[0, *groupby], sort=False).transform(sum)
            # # = CONDITIONAL prob.mass for categories in aggregate_by, GIVEN each category in groupby
            w_av = u.groupby(level=[0, *aggregate_by],
                             sort=False, group_keys=True).transform('sum')
            # = AVERAGE prob.mass for categories in aggregate_levels
            # = same as ema_display.aggregate_situation_theta
            # -> slightly less variability than w_cond
            theta_ds = theta_ds * w_av  # w_cond  # ???
            return theta_ds.groupby(level=[0, *groupby], sort=False, group_keys=True).sum()

    def attribute_tau(self, xi, a):
        """Extract response thresholds for ONE given attribute,
        EXCEPT fixed extreme limits at -inf, +inf.
        Used only by ema_display
        :param xi: 2D array with parameter sample vectors
            xi[s, :] = s-th parameter sample vector
        :param a: attribute key = one of self.emf.attribute_grades.keys()
        :return: tau = 2D array, with
            tau[s, l] = s-th sample of UPPER limit of l-th response interval,
                EXCEPT the last at +inf
                tau.shape[-1] == len(self.emf.attribute_grades[a]) - 1
        """
        a_index = list(self.emf.attribute_dtypes.keys()).index(a)
        eta_slice = self.attribute_slices[a_index].eta_slice
        eta = xi[..., eta_slice]
        return self.thr.tau(eta)[..., 1:-1]

    # ---------------------- methods for logprob calculation:

    def situation_logprob(self, xi, situation_count):
        """Situation logprob given tentative parameter array
        Used by ema_respondent.EmaRespondentModel.adapt().
        :param xi: 1D or 2D array of tentative parameter samples
        :param situation_count: 2D array with response counts,
            situation_count[k0, k] = number of responses
            in k-th <=> (k1, k2, ...)-th situation category at k0-th test phase,
            using flattened index for situation dimensions 1,2,....
        :return: ll = scalar or 1D array
            ll[...] = ln P{situation_count | xi[..., :]}
            ll.shape == xi.shape[:-1]
        """
        def sit_lp(alpha):
            """
            :param alpha: non-normalized log-prob-mass for ONE test phase
            :return: lp = 1D or 2D array
                lp[..., k] = log P{visit k-th situation | alpha[..., :] }
                normalized as sum_k exp(lp[..., k]) == 1.
            """
            return alpha - logsumexp(alpha, axis=-1, keepdims=True)
        # -------------------------------------------------------
        return sum(np.dot(sit_lp(xi[..., alpha_ind]), z_t)
                   for (z_t, alpha_ind) in zip(situation_count,
                                               self.alpha_slices))

    def d_situation_logprob(self, xi, situation_count):
        """Gradient of situation_logprob,
        to be concatenated with d_rating_logprob(...)
        :param xi: 1D or 2D array of tentative parameter samples
        :param situation_count: 2D array with response counts
            situation_count[k0, k] = number of responses
            in k-th <=> (k1, k2, ...)-th situation category at k0-th test phase,
            using flattened index for situation dimensions 1,2,....
        :return: list of 1D or 2D arrays ll_t, with
            ll_t[..., j] = d ln P{situation_count[t] | xi[..., :]} / d xi[..., j_t]
                for j_t-th alpha parameter in t-th test phase
            ll_t.shape[-1] == situation_count.shape[-1]
        """
        def d_sit_lp(alpha):
            """Gradient of sit_lp(alpha)
           :param alpha: non-normalized log-prob-mass for ONE test phase
            :return: d_lp = 1D or 2D array with
                d_lp[..., k] = log P{visit k-th situation | alpha[..., :] }
                d_lp.shape == alpha.shape
            """
            return np.eye(alpha.shape[-1]) - softmax(alpha[..., None, :], axis=-1)
            # -------------------------------------------------------------------

        # return [np.einsum('k, ...kj -> ...j',  # ******* use dot or @?
        #                   z_t, d_sit_lp(xi[..., alpha_ind]))
        return [np.dot(z_t, d_sit_lp(xi[..., alpha_ind]))
                for (z_t, alpha_ind) in zip(situation_count,
                                            self.alpha_slices)]

    def rating_logprob(self, xi, rating_count):
        """Rating logprob given tentative parameter array
        Used by ema_respondent.EmaRespondentModel.adapt().
        :param xi: 1D or 2D array of tentative parameter samples
        :param rating_count: list of 2D arrays with response counts
            rating_count[i][l, k] = number of responses for i-th ATTRIBUTE,
            at l-th ordinal level, given the k-th <=> (k0, k1, k2, ...)-th situation
        :return: ll = scalar or 1D array
            ll[...] = log P{rating_count | xi[..., :]}
            ll.shape == xi.shape[:-1]
        """
        def rating_lp(beta, eta):
            """log-prob for ONE attribute
            :param beta: 1D or 2D array with effect params
            :param eta: 1D or 2D array with threshold params
            :return: lp = 2D or 3D array with
                lp[..., l, k] = ln P{l-th grade | k-th situation, beta, eta}
            """
            return self.rv_class.log_cdf_diff(*self.cdf_args(beta, eta))
        # --------------------------------------------------------------
        # ll_y = sum(np.einsum('lk, ...lk -> ...',
        #                      y_i, lp_i)
        return sum(np.sum(y_i * rating_lp(xi[..., beta_ind], xi[..., eta_ind]),
                          axis=(-2, -1))
                   for (y_i, (beta_ind, eta_ind)) in zip(rating_count,
                                                         self.attribute_slices)
                   )

    def d_rating_logprob(self, xi, rating_count):
        """Gradients of rating_logprob(...),
        for each separate group of parameters,
        to be concatenated with d_situation_logprob(...)
        :param xi: 1D or 2D array of tentative parameter samples
        :param rating_count: list of 2D arrays with response counts
            rating_count[i][l, k] = number of responses for i-th ATTRIBUTE,
            at l-th ordinal level, given the k-th <=> (k0, k1, k2, ...)-th situation
        :return: d_ll = list of 1D or 2D arrays d_ll_beta, and d_ll_eta, with elements
            d_ll_beta[a][..., j] = d ln P{rating_count[a] | xi[..., :]} / d beta_a[..., j]
                w.r.t. effect parameters beta_a for a-th attribute
            d_ll_eta[t][..., j] = d ln P{rating_count[a] | xi[..., :]} / d eta_t[..., j]
                w.r.t. threshold parameters eta for t-th attribute scale
                (each set of scale thresholds may be tied to one or several attributes)
            d_ll elements ordered as groups of parameters in parameter array xi
        """
        # *** separate calculations for d ll / d theta and d_ll / d tau ? ***
        # *** In the logistic model, d ll / d theta is independent of the interval width tau_high - tau_low
        # *** This was utilized in the similar model in ItemResponseCalc
        d_ll_beta = []
        d_ll_eta = []
        for (y_i, (beta_ind, eta_ind)) in zip(rating_count,
                                              self.attribute_slices):
            beta = xi[..., beta_ind]
            eta = xi[..., eta_ind]
            (dlp_low, dlp_high) = self.rv_class.d_log_cdf_diff(*self.cdf_args(beta, eta))
            d_ll_beta.append(np.einsum('...lk, lk, jk -> ...j',
                                       dlp_low + dlp_high, y_i, - self.theta_map))
            # tensordot 2 steps?

            d_tau_d_eta = self.thr.d_tau(eta)
            d_ll_eta.append(np.einsum('...lk, lk, ...lj -> ...j',  # *** use dot , matmul ?
                                      dlp_low, y_i, d_tau_d_eta[..., :-1, :])
                            +
                            np.einsum('...lk, lk, ...lj -> ...j',
                                      dlp_high, y_i, d_tau_d_eta[..., 1:, :]))
        # all d_ll_beta, d_ll_eta elements have equal shape[:-1]
        # i.e., can be concatenated along axis=-1

        # if some eta scales tied to more than one attribute, sum those d_ll_eta elements:
        if self.tied_scales:
            d_ll_eta = [sum(d_ll_eta[i]
                            for i in tied_attribute_ind)
                        for tied_attribute_ind in self.tied_scales]
        # join into one list, elements to be concatenated by caller:
        return d_ll_beta + d_ll_eta

    def cdf_args(self, beta, eta):
        """Extract arguments for logprob calculation for ONE attribute
        :param beta: 1D or 2D array with beta parameter sample for given attribute
            beta[..., k] = ...-th sample of k-th regression-effect parameter
        :param eta: 1D or 2D array with threshold parameter sample for given attribute
            eta[..., l] = ...-th sample of l-th parameter
        :return: tuple (arg_low, arg_high) with 2D or 3D array args for probabilistic model,
            such that
            P[ l-th response | ...-th parameter sample, k-th situation ] =
            = rv_class.cdf(arg_high[..., l, k]) - rv_class.cdf(arg_low[..., l, k])
        """
        theta = np.dot(beta, self.theta_map)
        # theta[..., k] = ...-th sample of latent-variable location, given k-th situation
        # tau = response_thresholds(eta)  # INCL extreme -Inf, +Inf limits
        tau = self.thr.tau(eta)  # INCL extreme -Inf, +Inf limits
        a = tau[..., :-1, None] - theta[..., None, :]  # lower interval limits
        b = tau[..., 1:, None] - theta[..., None, :]  # upper interval limits
        return a, b

    def restrict(self, xi):
        """Adjust mean log situation-prob -> 0; -> no change of situation-prob.
        :param xi: ref to 2D array of sample parameter vectors
        :return: None
        Result: xi modified in place
            tau and associated theta samples modified by same amount
        """
        for sit_slice in self.alpha_slices:
            d = logsumexp(xi[:, sit_slice], axis=-1, keepdims=True)
            # logger.debug(f'xi situation restrict d: mean={np.mean(d):.3}; std={np.std(d):.3}; '
            #              + f'max={np.amax(d):.3}; min={np.amin(d):.3}')
            xi[:, sit_slice] -= d
        # version <= 0.9.4:
        # for (beta_slice, eta_slice) in self.attribute_slices:
        #     # beta = xi[..., beta_slice]
        #     # eta = xi[..., eta_slice]
        #     theta = np.dot(xi[..., beta_slice], self.theta_map)
        #     # tau = response_thresholds(xi[..., eta_slice])[..., 1:-1]
        #     tau = self.thr.tau(xi[..., eta_slice])[..., 1:-1]
        #     if self.restrict_attribute:
        #         d = np.mean(theta, axis=-1, keepdims=True)
        #     elif self.restrict_threshold:
        #         d = np.median(tau, axis=-1, keepdims=True)
        #     else:
        #         d = 0.
        #     # d = random offset to be zero-ed out with no effect on log-likelihood
        #     n_beta_0 = self.beta_0_size()  # **** only first regression-effect ! *****
        #     # = number of mean-location-controlling beta parameters = first part of beta_slice
        #     b0_slice = slice(beta_slice.start,
        #                      beta_slice.start + n_beta_0)
        #     # = beta slice only for FIRST regression effect term
        #     xi[:, b0_slice] -= d
        #     # eta = tau_inv(tau - d)  # **********************
        #     eta = self.thr.tau_inv(tau - d)
        #     xi[:, eta_slice] = eta
        # if self.restrict_attribute:
        #     self._restrict_attribute(xi)

    # def _restrict_attribute(self, xi):
    #     """Force mean(theta) -> 0, and adjust thresholds correspondingly
    #     :param xi: ref to 2D array of sample parameter vectors
    #     :return: None
    #     Result: xi modified in place
    #         tau and associated theta samples modified by same amount
    #     NOTE: theta and tau adjusted equally, for each attribute,
    #     so the threshold scales MUST be UNIQUE for each attribute,
    #     i.e., self.tied_scale == False
    #     """
    #     if self.tied_scales:
    #         logger.error('Cannot restrict attribute means with scale(s) tied to more than one attribute')
    #         # *** should not happen, checked earlier
    #     for (beta_slice, eta_slice) in self.attribute_slices:
    #         # beta = xi[..., beta_slice]
    #         # eta = xi[..., eta_slice]
    #         theta = np.dot(xi[..., beta_slice], self.theta_map)
    #         tau = self.thr.tau(xi[..., eta_slice])[..., 1:-1]
    #         d = np.mean(theta, axis=-1, keepdims=True)
    #         # d = random offset to be zero-ed out with no effect on log-likelihood
    #         n_beta_0 = self.beta_0_size()  # **** only first regression-effect ! *****
    #         # = number of mean-location-controlling beta parameters = first part of beta_slice
    #         b0_slice = slice(beta_slice.start,
    #                          beta_slice.start + n_beta_0)
    #         # = beta slice only for FIRST regression effect term
    #         xi[:, b0_slice] -= d
    #         # eta = tau_inv(tau - d)  # **********************
    #         eta = self.thr.tau_inv(tau - d)
    #         xi[:, eta_slice] = eta

    # ------------------------------------ Help methods for ema_respondent.initialize():
    def initialize_xi(self, z, y):
        """Initialize individual parameter vector, given observed counts
        :param z: 2D array with
            z[k0, k] = number of EMA records at k0-th test phase
            in k-th <=> (k1, k2, ...)-th situation, EXCL. k0= test phase
        :param y: list of 2D arrays,
            y[i][l, k] = number of responses at l-th ordinal level for i-th ATTRIBUTE question
            given k-th <=> (k0, k1, k2, ...)-th situation (INCL. k0 = test phase)
        :return: xi = 1D array with all parameters,
            ordered by parameter sub-types (alpha, beta, eta) as defined by self
        """
        alpha = list(_initialize_situation_param(z))
        eta = [_initialize_rating_eta(y_i, self.thr)
               for y_i in y]
        # beta = [_initialize_rating_beta(y_i, eta_i, self.theta_map)
        #         for (y_i, eta_i) in zip(y, eta)]
        beta = [_initialize_rating_beta(y_i, self.thr.tau(eta_i), self.theta_map)
                for (y_i, eta_i) in zip(y, eta)]
        if self.tied_scales:  # ****************** sum y instead ! ****************
            eta = [sum(eta[i] for i in tied_attribute_ind)
                   for tied_attribute_ind in self.tied_scales]
        for eta_scale in eta:
            eta_scale -= np.sum(eta_scale)
        # just in case _initial_rating_eta yields non-zero values
        # order as alpha[0], alpha[1],..., beta[0], beta[1], ..., eta[0], eta[1],...
        return np.concatenate([*chain(alpha, beta, eta)])


# ---------------------------------------- Other support functions:

def _initialize_situation_param(z):
    """Crude initial estimate of situation logprob parameters
    :param z: 2D array with situation counts
        z[t, k] = n EMA records in k-th <-> (k1, k2,...)-th situation
            in t-th test phase
    :return: alpha = 2D array
        alpha[t, k] = log prob of k-th situation at t-th test phase
        alpha.shape == (z.shape[0], z[0].size)
    """
    p = z + PRIOR_PSEUDO_RESPONDENT
    p /= np.sum(p, axis=-1, keepdims=True)
    return np.log(p)


def _initialize_rating_eta(y, thr):
    """Crude initial estimate of threshold-defining parameters for ONE attribute question
    :param y: 2D rating_count array,
        y[l, k] = number of responses at l-th ordinal level,
        given the k-th <-> (k0, k1, ...)-th situation category
    :param thr: Thresholds subclass, to determine number of eta parameters
    :return: eta = 1D array of eta parameters, defining thresholds as
        tau = ema_base.response_thresholds(eta)
        eta.shape == y.shape[:1]
    Method: set eta parameters to match observed relative freq of all rating grades
        as if theta = 0.
    OR just set all eta == 0.
    """
    # p = np.sum(y, axis=-1) + JEFFREYS_CONC
    # p /= np.sum(p)
    # return mapped_width_inv(p)
    # *** This method seems to improve the first LL,
    # but sometimes give worse or same long-term result
    return np.zeros(thr.n_param(len(y)))  # original simple method


def _initialize_rating_beta(y, tau, theta_map):
    """Crude initial estimate of regression-effect parameters for ONE attribute question
    :param y: 2D rating_count array,
        y[l, k] = number of responses at l-th ordinal level,
        given the k-th <-> (k0, k1, ...)-th situation category
    :param tau: 1D array with threshold parameters, incl extreme -inf + inf
    :return: beta = array of sensory-variable locations theta, such that
        theta approx = np.dot(beta, theta_map),
        theta[k] = estimated location of latent variable,
        given the k-th <-> (k0, k1, ...)-th situation category
    """
    expit_tau = expit(tau)
    typical_theta = logit((expit_tau[:-1] + expit_tau[1:]) / 2)
    # = back-transformed midpoints in each response interval
    # typical_theta[l] = theta given l-th response
    p = y + PRIOR_PSEUDO_RESPONDENT
    p /= np.sum(p, axis=0, keepdims=True)
    theta = np.dot(typical_theta, p)
    # = typical (midpoint) locations, given y
    beta = np.linalg.lstsq(theta_map.T, theta, rcond=None)[0]
    # -> theta approx = np.dot(beta, theta_map),
    return beta


def _make_prior(n_parameters,
                alpha_slices,
                attribute_slices,
                rv_class):
    """Create hyperprior for parameter distribution in the total population
    :param n_parameters: total number of parameters
    :param alpha_slices: list with index slice for each situation phase
    :param attribute_slices: list with one AttributeSlice tuple for each attribute
    :return: single GaussianRV instance
    """
    prec_a = PRIOR_PREC_A  # * np.ones(n_parameters)  # still scalar, same for all elements
    prec_b = PRIOR_PREC_B * np.ones(n_parameters)
    for (b_slice, e_slice) in attribute_slices:
        prec_b[b_slice] *= rv_class.scale**2
        # prec_a[e_slice] *= 100.  # ****** temp fix just for TEST
        # ************* TEST reduce prior threshold-parameter variance, no
    loc = np.zeros(n_parameters)
    # for a_slice in alpha_slices:
    #     loc[a_slice] = - np.log(a_slice.stop - a_slice.start)  # not needed
    return GaussianRV.initialize(loc=loc,
                                 learned_weight=PRIOR_PSEUDO_RESPONDENT,
                                 prec_a=prec_a,
                                 prec_b=prec_b)


def _check_effects(emf, effects):
    """Check that all effects refer to unique situation keys
    :param emf: ema_data.EmaFrame instance
    :param effects: list with regression-effect specifications
        effects[i] = single key in emf.situation_dtypes.keys(), OR tuple of such keys
    :return: None
    Result: raise RuntimeError if incorrect effects
    """
    def _match_effect(effect_item):
        """Match one effect item to be consistent with emf situations
        :param effect_item: situation key or tuple of situation keys
        :return: eff_new <- eff corrected if needed and possible
        """
        if isinstance(effect_item, tuple):
            return tuple(emf.match_situation_key(eff_k)
                         for eff_k in effect_item)
        else:
            return emf.match_situation_key(effect_item)
    # ------------------------------------------------

    for (i, e_i) in enumerate(effects):
        e_new = _match_effect(e_i)
        if e_new != e_i:
            logger.warning(f'*** Regression effect {e_i} changed to {e_new}')
            effects[i] = e_new
    effect_keys = sum((list(e_i) if type(e_i) is tuple else [e_i]
                      for e_i in effects), start=[])
    # = flat list with all situation keys from effects
    if len(set(effect_keys)) != len(effect_keys):
        raise RuntimeError('situation keys can occur only ONCE in regression_effects')
    # for e_i in effect_keys:
    #     if e_i not in emf.situation_dtypes.keys():
    #         raise RuntimeError(f'regression effect key {e_i} is not a situation key')
    for sit_key in emf.situation_dtypes.keys():
        if len(emf.situation_dtypes[sit_key].categories) > 1 and sit_key not in effect_keys:
            logger.warning(f'situation dimension {repr(sit_key)} to be disregarded in regression?')


def _theta_map(emf, effects, restrict_attr):
    """Create 2D array for extraction of attribute locations
    from parameter vector samples
    :param emf: ema_data.EmaFrame instance,
        defining the analysis model structure.
    :param effects: iterable with regression-effect specifications
        effects[i] = tuple with one or more key(s) from emf.situation_dtypes.keys()
    :param restrict_attr: boolean switch
        to force mean theta across situations -> 0., regardless of beta
    :return: th = 2D array, such that
        theta[..., :] = np.dot(beta[..., :], th) is ...-th sample of attribute location
            in the :-th <=> (k0, k1, ...)-th situation, with
        beta[..., j] = xi[:, attr_slice][..., j] is the j-th regression effect parameter,
        and xi is the array of row parameter-vector samples.
    """
    def theta_one(effect):
        """Make theta_map part for ONE effect term
        :param effect: tuple of one or more situation keys
        :return: mD array th, with
            th[j, k0, k1, ...] = j-th effect given (k0, k1, ...)-th situation
            th[j, 0, 0, ...] = 0, in 0-th reference situation.
            th.shape == (size_effect, *emf.situation_shape), where
            size_effect = size of category array defined by effect.
        """
        beta_shape = tuple(len(emf.situation_dtypes[sc_i].categories) for sc_i in effect)
        # = situation_shape, for this effect term
        beta_ndim = len(beta_shape)
        beta_size = int(np.prod(beta_shape))
        t = np.eye(beta_size).reshape((beta_size, *beta_shape))
        if restrict_attr or effect != effects[0]:
            t = t[1:]
            # if restrict_attr: only relative effects re. first category, delete first
            # else: include absolute theta intercept parameter only in FiRST effect term,
            # with same influence on theta in all effect terms
        # expand t.ndim to number of situation dimensions:
        t = t.reshape(t.shape + tuple(np.ones(len(emf.situation_dtypes) - beta_ndim,
                                              dtype=int)
                                      ))
        ax_0 = range(1, 1 + len(beta_shape))
        ax_new = tuple(list(emf.situation_dtypes).index(e_i) + 1
                       for e_i in effect)
        t = np.moveaxis(t, ax_0, ax_new)
        return t + np.zeros(emf.situation_shape)
    # ---------------------------------------------------------------
    th = np.concatenate([theta_one(e_tuple)
                         for e_tuple in effects],
                        axis=0)
    th = th.reshape((th.shape[0], -1))  # keep as 2D for simplicity
    if restrict_attr:
        th -= np.mean(th, axis=-1, keepdims=True)
        # forcing mean(theta) -> 0., regardless of regression beta parameters
    return th


# ------------------------------------------------- TEST:
if __name__ == '__main__':
    # from scipy.optimize import approx_fprime, check_grad

    from ema_data import EmaFrame
    from ema_latent import LatentLogistic

    print('*** Testing some ema_base module functions ')
    emf = EmaFrame.setup(situations={'CoSS': [f'C{i}' for i in range(1, 8)],
                                     'Viktigt': ('Lite',
                                                 'Ganska',
                                                 'Mycket'),
                                     # 'Test': (None, None),
                                     'HA': ('A', 'B')
                                     }, attributes={'Speech': ('Difficult',
                                                               'Normal',
                                                               'Easy'),
                                                    'Quality': ('Bad', 'Good')
                                                    })

    # print('emf=\n', emf)

    # Testing restrictions (both cannot be true, but both may be False):
    restrict_threshold = False   # False
    restrict_attribute = True   # False
    print(f'restrict_attribute= {restrict_attribute}; restrict_threshold= {restrict_threshold}')
    main_theta = {'Phase': [0.],
                  'CoSS': 0.1 * np.arange(len(emf.situation_dtypes['CoSS'].categories)),
                  'Viktigt': np.array([-1., 0., 1.]),
                  'HA': np.array([0., 1.])
                  }
    # = only main effects, additive
    regr_effects = ['HA', ('CoSS', 'Viktigt')]
    # regr_effects = [('CoSS', 'Viktigt'), 'HA']

    # effect_HA = np.array([-1., 1.])
    # effect_CoSS = 0.1 * np.arange(len(emf.situation_dtypes['CoSS']))
    # effect_Vikt = np.array([-1., 0., 1.])
    true_theta = main_theta['CoSS'][:, None] + main_theta['Viktigt']
    true_theta = true_theta[..., None] + main_theta['HA']
    true_theta = true_theta[None, ...]  # only one phase
    # stored like emf.situation_dtypes
    # true_theta[t, c, v, h] = theta in t-th phase, c-th CoSS, v-th Vikt, h-th HA

    theta_HA = main_theta['HA']
    beta_HA = theta_HA[1:] - theta_HA[0]  # rel. first HA
    theta_CoSS_Vikt = main_theta['CoSS'][:, None] + main_theta['Viktigt']
    theta_CoSS_Vikt = theta_CoSS_Vikt.reshape((-1,))
    beta_CoSS_Vikt = theta_CoSS_Vikt[1:] - theta_CoSS_Vikt[0]  # rel. first CoSS_Vikt case
    if restrict_attribute:
        # only relative beta differences:
        beta_all = np.concatenate((beta_HA, beta_CoSS_Vikt))
        true_theta -= np.mean(true_theta) # force mean theta -> 0.
    else:
        # include absolute theta for HA:
        beta_all = np.concatenate((theta_HA + theta_CoSS_Vikt[0], beta_CoSS_Vikt))
    # for regr_effects = ['HA', ('CoSS', 'Viktigt')]
    # beta_all = np.concatenate((theta_CoSS_Vikt.reshape((-1)), beta_HA))
    # for regr_effects = [('CoSS', 'Viktigt'), 'HA']

    if restrict_threshold:
        thr = ThresholdsMidFixed
    else:
        thr = ThresholdsFree
    eta = [np.zeros(thr.n_param(len(r_cat.categories)))
           for r_cat in emf.attribute_dtypes.values()]

    alpha = np.zeros(emf.situation_shape).reshape((-1))
    print(f'len(alpha)= {len(alpha)}')
    print('; '.join(f'{a}: len(beta)= {len(beta_all)}'
                    for a in emf.attribute_dtypes.keys())
          )
    print('; '.join(f'{a}: len(eta)= {len(eta_a)}'
                    for (a, eta_a) in zip(emf.attribute_dtypes.keys(),
                                          eta)
                    )
          )

    # xi = np.concatenate((lp_situations, *beta_eta))
    xi = np.concatenate((alpha,
                         np.tile(beta_all, len(emf.attribute_dtypes)),
                         *eta))
    print(f'n_parameters= {len(xi)}')
    xi = xi[None, :]
    print(f'xi= {xi}')

    p_base = EmaParamBase.initialize(emf, regr_effects, rv_class=LatentLogistic,
                                     restrict_threshold=restrict_threshold,
                                     restrict_attribute=restrict_attribute)
    print('p_base= ', p_base)
    print(f'p_base.n_parameters = {p_base.n_parameters}')
    print(f'p_base.theta_map.shape= {p_base.theta_map.shape}')

    print('\n*** Testing param extraction methods ***')

    for (phase, alpha_slice) in zip(emf.situation_dtypes[emf.phase_key].categories,
                                    p_base.alpha_slices):
        print(f'{emf.phase_key}= {phase}: xi[:, alpha_slice].shape= ', xi[:, alpha_slice].shape)
    # for (phase, alpha) in zip(emf.situation_dtypes[emf.phase_key], p_base.situation_logprob(xi)):
    #     print(f'{emf.phase_key}= {phase}: prob-mass=\n', np.exp(alpha))
    print(f'\nemf.situation_shape= {emf.situation_shape}')
    # for (a, beta_slice) in zip(emf.attribute_grades.keys(),
    #                            p_base.beta_slices):
    # for (a, a_slice) in p_base.attribute_slices.items():
    for (a, (beta_slice, eta_slice)) in zip(emf.attribute_dtypes.keys(),
                                            p_base.attribute_slices):
        print(f'\nAttribute {a}.beta_slice: {beta_slice}')
        print(f'\nAttribute {a}: xi[:, beta_slice]={xi[:, beta_slice]}')

    for a in emf.attribute_dtypes.keys():
        theta = p_base.attribute_theta(xi, a)
        print(f'\nAttribute {a}: theta.shape={theta.shape}.')
        sc_dim_0 = 'Phase'
        sc_dim_1 = 'CoSS'
        theta = theta.reshape((-1, *emf.situation_shape))  # *** just for testing
        for (sc_0, theta_0, true_theta_0) in zip(emf.situation_dtypes[sc_dim_0].categories,
                                                 theta[0], true_theta):
            print(f'\t{sc_dim_0}= {sc_0}:')
            for (sc_1, theta_1, true_theta_1) in zip(emf.situation_dtypes[sc_dim_1].categories,
                                                     theta_0, true_theta_0):
                print(f'\t\t{sc_dim_1}= {sc_1}: theta=\n', theta_1)
                print(f'\t\t{sc_dim_1}= {sc_1}: true_theta=\n', true_theta_1)

    for a in emf.attribute_dtypes.keys():
        tau = p_base.attribute_tau(xi, a)
        print(f'\nAttribute {a}: tau.shape={tau.shape}. tau=\n', tau)

    xi[0, 0:2] = 2.
    print('\n***Testing situation_prob')
    p_ds = p_base.situation_prob_df(xi, groupby=('Viktigt',))
    print('situation prob.=\n',p_ds)
    print('\n***Testing attribute_theta:')
    th_ds = p_base.attribute_theta_df(xi, a='Speech')
    print(th_ds)
    p_ds = p_base.situation_prob_df(xi)
    print('situation prob.=\n',p_ds)
    th_ds = p_base.attribute_theta_df(xi, a='Speech', groupby=('CoSS',))
    print('Speech=\n', th_ds)


