"""This module defines a class for individual participant parameter model
to be part of an ema_group.EmaGroupModel instance,
which is part the main Bayesian probabilistic model of EMA data.

Individual parameter distributions are approximated by sampling.
The population mixture model is common prior for all individuals in
the participant group recruited from the same population.

*** Class Defined here:

EmaRespondentModel: Distribution of individual parameter vector
    assumed to determine the observed EMA data from ONE respondent,
    including, in each EMA record,
    (1) a nominal (possibly multidimensional) Situation category, and
    (2) ordinal Ratings for zero, one, or more perceptual Attributes.
    The parameter distribution is represented by an array xi with many samples.
    The sample distributions are independent across EmaRespondentModel instances,
    so instances may be adapt-ed in parallel processes.

*** Version History:
* Version 1.1.5:
2025-05-22, still no stored base property,
            instead supplied as argument when needed in methods
            attribute_grade_count, rvs_grade_count, just like adapt

* Version 1.1.3
2025-03-29, cleanup EmaRespondentModel: no id, base, prior properties
2025-03-21, using ema_repr.EmaObject as superclass

* Version 1.0.0:
2023-05-01, EmaRespondentModel.rvs_grade_count() reverted to old method from Frontiers paper.
            Alternative method from v.0.9.5 sometimes incorrect.
2023-04-26, corrected bug in EmaRespondentModel.rvs_grade_count(), in case multiple Phase-s
            Private property EmaRespondentModel._rng, using sampler rng, for reproducibility.

* Version 0.9.5:
2023-03-11, rvs_grade_count() uses model-PREDICTED situation count profiles,
            -> greater variability, compared to earlier OBSERVED counts for each situation
2023-03-03, new methods EmaRespondentModel.attribute_grade_count() and .rvs_grade_count()

* Version 0.9.3:
2022-07-27, changed module name ema_subject -> ema_respondent
            EmaSubjectModel -> EmaRespondentModel
2022-07-20, moved _initialize xi -> ema_base, for same reason
2022-07-19, moved logprob calc -> ema_base, to hide parameter indexing details there
2022-07-xx, minor update for notation change: scenario -> situation

* Version 0.9.2:
2022-06-15, EmaSubjectModel methods mean_attribute_grades, nap_diff deleted.
            Replaced by ema_data.EmaDataSet.(mean_attribute_table, nap_table).

2022-06-15, new _initialize_rating_eta(y); changed _initialize_rating_theta(y, eta)
            tested initial response thresholds crudely based on response counts

2022-05-21, EmaSubjectModel.cdf_arg: check for too small response interval,
            that might cause numerical underflow in case of many missing data

* Version 0.8.3:
2022-03-08, minor cleanup logging to work in multiprocessing

* Version 0.8.2: prepared for multi-processing subject adapt() in parallel processes
2022-03-03, EmaSubjectModel methods mean_zeta, mean_zeta_mom no longer needed

* Version 0.8.1: minor cleanup of comments and logger output

* Version 0.8
2022-02-12, Changed VI factorization for better approximation,
    with individual indicators conditional on parameter samples,
    defining variational q(zeta_n, xi_n) = q(zeta_n | xi_n) q(xi_n)
"""
import multiprocessing
import logging

import numpy as np
from scipy.optimize import minimize
import pandas as pd

from samppy import hamiltonian_sampler as ham
from samppy.sample_entropy import entropy_nn_approx as entropy

from EmaCalc.ema_repr import EmaObject
from EmaCalc.ema_base import PRIOR_PARAM_SCALE


# -------------------------------------------------------------------
__ModelVersion__ = "2025-05-22"

DITHER_PARAM_SCALE = 0.1 * PRIOR_PARAM_SCALE
# -> initial dithering of point-estimated individual parameters

N_SAMPLES = 1000
# = number of parameter vector samples in each EmaRespondentModel instance

logger = logging.getLogger(__name__)
# logger does NOT inherit parent handlers, when this module is running as child process
if multiprocessing.current_process().name != "MainProcess":
    # restore a formatter like ema_logging, only for console output
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('{asctime} {name}: {message}',
                                           style='{',
                                           datefmt='%H:%M:%S'))
    logger.addHandler(console)
# logger.setLevel(logging.DEBUG)  # *** TEST
# ham.logger.setLevel(logging.DEBUG)  # *** TEST sampler


# -------------------------------------------------------------------
class EmaRespondentModel(EmaObject):
    """Container for EMA response-count data for ONE respondent,
    and a sampled approximation of the individual parameter distribution.

    Individual parameter distributions are approximated by a large set of samples
    stored as property xi, with
    self.xi[s, :] = s-th sample vector of parameters,
    with subsets of parameter types (alpha, beta, eta)
    as defined in common ema_base.EmaParamBase object
    """
    def __init__(self, situation_count, rating_count, xi, rng):  # reduced in v 1.1.3
        """
        :param situation_count: 2D array with response counts
            situation_count[k0, k] = number of responses
            in k-th <=> (k1, k2, ...)-th situation category at k0-th test phase,
            using flattened index for situation dimensions 1,2,....
            NOTE: ema_data.EmaFrame always stores test phase as first situation dimension.
        :param rating_count: list of 2D arrays with response counts
            rating_count[i][l, k] = number of responses for i-th ATTRIBUTE,
            at l-th ordinal level, given the k-th <=> (k0, k1, k2, ...)-th situation
        :param xi: 2D array with parameter sample vector(s)
            xi[s, j] = s-th sample of j-th individual parameter,
                concatenated by parameter sub-types as defined in base.
        :param rng: random Generator object for sampler
        """
        # *** v. 1.1.3: prior and base as arg to self.adapt(), not stored as properties
        # self.base = base  # removed in v 1.1.3
        self.situation_count = situation_count
        self.rating_count = rating_count
        self.xi = xi
        self._sampler = ham.HamiltonianSampler(x=self.xi,
                                               fun=self._neg_ll,
                                               jac=self._grad_neg_ll,
                                               epsilon=0.2,
                                               n_leapfrog_steps=10,     # = default
                                               min_accept_rate=0.8,     # = default
                                               max_accept_rate=0.95,    # = default
                                               rng=rng
                                               )
        # keeping sampler properties across learning iterations
        # self.prior = prior   # removed in v 1.1.3
        self.ll = None  # space for log-likelihood result from self.adapt()

    @property
    def _rng(self):
        return self._sampler._rng

    def rrepr(self, r, level):
        with np.printoptions(threshold=20, edgeitems=2, precision=3):
            return super().rrepr(r, level)

    @classmethod
    def initialize(cls, base, ema_df, rng):
        """Create model from recorded data
        :param base: common ema_base.EmaParamBase object
        :param ema_df: a pandas.DataFrame object for ONE respondent
        :param rng np.random.Generator for sampler use
        :return: a cls instance
        """
        z = base.emf.count_situations(ema_df).reshape((base.emf.n_phases, -1))
        # z[k0, k] = number of EMA records at k0-th test phase
        # in k-th <=> (k1, k2, ...)-th situation, EXCL. k0= test phase
        y = [base.emf.count_grades(a, ema_df)
             for a in base.emf.attribute_dtypes.keys()]
        # y[i][l, k] = number of attribute_grades at l-th ordinal level for i-th ATTRIBUTE question
        # given k-th <=> (k0, k1, k2, ...)-th situation (INCL. k0= test phase)
        xi = base.initialize_xi(z, y)
        # dither to N_SAMPLES:
        xi = xi + DITHER_PARAM_SCALE * rng.standard_normal(size=(N_SAMPLES, len(xi)))
        # return cls(base, z, y, xi, rng)
        return cls(z, y, xi, rng)

    def _kl_div_zeta(self, prior):
        """KLdiv for indicator variables zeta re prior
        = KLdiv{q(zeta | self.xi) || p(zeta | prior.mix_weight)}
        using current variational q(xi, zeta) = q(zeta | xi) q(xi)
        :param prior: ref to EmaGroupModel instance containing self
        :return: kl = scalar E{ ln q(zeta | self.xi) - ln p(zeta | prior.mix_weight)}

        Method: Leijon doc eq:VIlowerBoundCalc
        """
        w = prior.mean_conditional_zeta(self.xi)
        # w[c, s] = E{zeta_c | self.xi[s, :]} Leijon doc eq:ProbZetaGivenXi
        return np.sum(np.mean(w * (np.log(w + np.finfo('float').tiny)  # avoid log(0.) = nan
                                   - prior.mix_weight.mean_log[:, None]),
                              axis=1))

    def adapt(self, s_name, base, prior):
        """Adapt parameter distribution self.xi
        to stored EMA count data, given the current self.w
        and the current estimate of population GMM components self.prior.comp.
        :param s_name: respondent id, for logger output
        :param base: ref to common ema_base.EmaParamBase instance for logprob calc
        :param prior: ref to caller's PopulationModel instance
        :return: self, to send result via map() or Pool.imap()

        Result: Updated self.xi, and
            self.ll = E{ ln p(self.situation_count, self.rating_count | self.xi) }_q(xi)
                - E{ ln q(xi) / prior_p(xi) }_q(xi)
                - KLdiv( q(zeta | xi) || p(zeta | prior.mix_weight)
        """
        # find MAP point first:
        # lp_0 = - np.mean(self._neg_ll(self.xi), axis=0)  # ****** ref for test
        xi_0 = np.mean(self.xi, axis=0)
        res = minimize(fun=self._neg_ll,
                       jac=self._grad_neg_ll,
                       args=(base, prior),
                       x0=xi_0)
        if res.success:
            xi_map = res.x.reshape((1, -1))
        else:
            raise RuntimeError(f'{s_name}: MAP search did not converge: '
                               + 'res= ' + repr(res))
        if len(self.xi) != N_SAMPLES:
            # run sampler starting from x_map
            self._sampler.x = xi_map
        else:
            # we have sampled before, start from those samples
            self._sampler.x = self.xi + xi_map - xi_0
        # **** ------------------------------------- test effect of MAP
        # lp_1 = - np.mean(self._neg_ll(self._sampler.x), axis=0)  # ***** test after MAP adjustment
        # print(f'adapt: Subj {s_name}: MAP adjustment: d_lp = {lp_1 - lp_0:.3f}')
        # -----------------------------------------------------
        self._sampler.args = (base, prior)
        self._sampler.safe_sample(n_samples=N_SAMPLES, min_steps=2)
        logger.debug(f'{s_name}: sampler.epsilon= {self._sampler.epsilon:.3f}. '
                     + f'accept_rate= {self._sampler.accept_rate:.1%}. '
                     + f'n_steps= {self._sampler.n_steps}')
        self.xi = self._sampler.x
        # self.base.restrict(self.xi)
        base.restrict(self.xi)
        # adjust for modified xi:
        self._sampler.U = self._sampler.potential(self._sampler.x)
        # Calc log-likelihood contribution with final xi samples:
        lp_xi = - np.mean(self._sampler.U)  # after base.restrict
        # lp_xi = E_xi{ ln p(data | xi) + self.prior.logpdf(xi) }
        h_xi = entropy(self.xi)
        # approx = - E{ ln q(xi) }
        # kl_zeta = self._kl_div_zeta(self.prior)
        kl_zeta = self._kl_div_zeta(prior)
        self.ll = lp_xi + h_xi - kl_zeta
        logger.debug(f'{s_name}: adapt: ll={self.ll:.3f}; '
                     + f'(lp_xi={lp_xi:.3f}; '
                     + f'h_xi= {h_xi:.3f}. '
                     + f'-kl_zeta= {-kl_zeta:.3f})')
        self.ll = lp_xi + h_xi - kl_zeta
        return self

    def _neg_ll(self, xi, base, prior):
        """Objective function for self.adapt_xi
        :param xi: 1D or 2D array of candidate parameter vectors
        :return: neg_ll = scalar or 1D array
            neg_ll[...] = - ln P{ self.situation_count, self.rating_count | xi[..., :]}
                    - ln p(xi[..., :] | prior)
            neg_ll.shape == xi.shape[:-1]
        """
        # return - self.prior.logpdf(xi) - self.logprob(xi, base)
        return - prior.logpdf(xi) - self.logprob(xi, base)

    def _grad_neg_ll(self, xi, base, prior):
        """Gradient of self._neg_ll w.r.t. xi
        :param xi: 1D or 2D array of candidate parameter vectors
        :return: dll = scalar or 1D array
            dll[..., j] = d _neg_ll(xi[..., :]) / d xi[..., j]
            dll.shape == xi.shape
        """
        # return - self.prior.d_logpdf(xi) - self.d_logprob(xi, base)
        return - prior.d_logpdf(xi) - self.d_logprob(xi, base)

    def logprob(self, xi, base):
        """log likelihood of EMA count data, given parameters xi
        :param xi: 1D or 2D array of candidate parameter vectors
        :return: ll = scalar or 1D array
            ll[...] = ln P{ self.situation_count, self.rating_count | xi[..., :]}
            ll.shape == xi.shape[:-1]
        """
        # ll_z = self.base.situation_logprob(xi, self.situation_count)
        # ll_y = self.base.rating_logprob(xi, self.rating_count)
        ll_z = base.situation_logprob(xi, self.situation_count)
        ll_y = base.rating_logprob(xi, self.rating_count)

        # ----------- any rating_logprob = -inf -> ll_y == NaN
        if np.any(np.isnan(ll_y)):
            logger.warning('EmaRespondentModel.logprob: Some ll_y == NaN. Should never happen!')
        return ll_z + ll_y

    def d_logprob(self, xi, base):
        """Gradient of self.logprob(xi)
        :param xi: 1D or 2D array with candidate parameter vectors
        :return: d_ll = 1D or 2D array
            d_ll[..., j] = d ln P{ self.situation_count, self.attribute_grades | xi[..., :]} / d xi[..., j]
            d_ll.shape == xi.shape
        """
        # d_ll_z = self.base.d_situation_logprob(xi, self.situation_count)
        # # = list of arrays with shapes concatenable along axis=-1
        # d_ll_y = self.base.d_rating_logprob(xi, self.rating_count)
        # # = list of arrays with shapes concatenable along axis=-1
        d_ll_z = base.d_situation_logprob(xi, self.situation_count)
        # = list of arrays with shapes concatenable along axis=-1
        d_ll_y = base.d_rating_logprob(xi, self.rating_count)
        # = list of arrays with shapes concatenable along axis=-1
        return np.concatenate(d_ll_z + d_ll_y, axis=-1)

    def rvs(self, size=N_SAMPLES):
        # re-sample if size != len(self.xi) ???
        return self.xi

# ------------------------------------- display functions
    def attribute_grade_count(self, base, a, groupby=None):
        """Collect table of ordinal grade counts for ONE attribute,
        for this participant, optionally subdivided by situation.
        Similar to ema_data.EmaDataSet.attribute_grade_count()
        :param base: ref to common ema_base.EmaParamBase object
        :param a: selected attribute key
        :param groupby: (optional) single situation dimension or list of such keys
            for which separate attribute-counts are calculated.
            Counts are summed across any OTHER situation dimensions.
        :return: if groupby is defined:
            a pd.DataFrame object with all grade counts,
            with one row for each (*groupby) combination
            and one column for each grade category
            if groupby is empty: a pd.Series with sum of all grade counts
        """
        # emf = ema_base.EMA_BASE.emf  # ******** does not work after pickle.load() ? *********
        emf = base.emf
        a_ind = list(emf.attribute_scales.keys()).index(a)
        sit_index = pd.MultiIndex.from_product([sit_dtype.categories
                                                for sit_dtype in emf.situation_dtypes.values()],
                                               names=emf.situation_dtypes.keys())
        a_grades = emf.ordinal_scales[emf.attribute_scales[a]].categories
        df = pd.DataFrame(self.rating_count[a_ind].T,
                          index=sit_index, columns=a_grades)
        df.columns.set_names(a, inplace=True)
        if groupby is None:
            return df.sum()
        else:
            return df.groupby(level=groupby, sort=False, group_keys=True).sum()

    def rvs_grade_count(self, base, a, groupby=None, sample_head='_Sample'):
        """Calculate sampled model-predicted distribution of response counts
        for comparison with observed count histograms.
        :param base: ref to common ema_base.EmaParamBase object
        :param a: key for selected attribute
        :param groupby: (optional) single situation key (dimension) or list of such keys
            for which separate attribute-counts are calculated.
            Counts are summed across any OTHER situation dimensions.
        :param sample_head: (optional) header name for sample index
        :return: a pd.DataFrame object with all grade counts,
            with one row for each (sample, *groupby) multi-index combination
            and one column for each grade category.
        """
        # *** use total observed count to estimate situation-count distribution !
        # base = ema_base.EMA_BASE
        emf = base.emf
        a_index = list(emf.attribute_dtypes.keys()).index(a)
        if groupby is None:
            groupby = []
        elif isinstance(groupby, str):
            groupby = [groupby]
        # theta = self.base.attribute_theta(self.xi, a)  # v 1.1.3
        theta = base.attribute_theta(self.xi, a)  # v 1.1.5
        # theta[s, k0, k1,...] = s-th sample of attribute a, given (k0, k1,...)-th situation
        theta_shape = theta.shape
        theta = theta.reshape((theta_shape[0], -1))
        # theta[s, k] = s-th sample of attribute a, given k-th <=> (k0, k1,...)-th situation
        # tau = self.base.attribute_tau(self.xi, a)
        tau = base.attribute_tau(self.xi, a)
        tau = np.concatenate((np.full((tau.shape[0], 1), -np.inf),
                              tau,
                              np.full((tau.shape[0], 1), np.inf)), axis=-1)
        # tau[s, l] = s-th sample of l-th median rating threshold for attribute a
        arg_low = tau[..., :-1, None] - theta[..., None, :]
        # a[s, l, k] = lower interval limits for l-th category in k-th situation
        arg_high = tau[..., 1:, None] - theta[..., None, :]  # upper interval limits
        # lp = self.base.rv_class.log_cdf_diff(arg_low, arg_high)
        lp = base.rv_class.log_cdf_diff(arg_low, arg_high)
        p_response = np.exp(lp).transpose((0, 2, 1))
        # p[s, k, l] = s-th sample of prob of l-th response in k-th situation
        # p_sit = self.base.situation_prob(self.xi)
        # # p_sit[s, k0, k1, ...] = s-th sample of CONDITIONAL prob for (k1,...)-th situation, given k0 (Phase)
        # p_sit /= p_sit.shape[1]  # equal weight for all Phase-s
        # # p_sit[s, k0, k1,...] = s-th sample of prob for k-th <-> (k0, k1,...)-th situation
        # p_sit = p_sit.reshape((len(p_sit), -1))
        # # p_sit[s, k] = s-th sample of prob for k-th situation, across ALL attributes
        # c_tot = np.sum(self.rating_count[a_index])
        # # c_tot = total count across all situations
        # c_sit_all = self._rng.multinomial(c_tot, p_sit)
        # c_sit_all[s, k] = s-th sample of PREDICTED count in k-th situation across ALL attributes
        # *** This gives WRONG result in case the attribute is relevant only in some situation,
        # *** E.g., in the IHAB study, attribute Involvement has responses only in CoSS=C2.
        c_sit = np.sum(self.rating_count[a_index], axis=0)
        # c_sit[k] = total OBSERVED count of responses in k-th situation for THIS attribute!
        # *** This is the method used in the Frontiers paper!
        n_count = self._rng.multinomial(c_sit, pvals=p_response)
        # n_count[s, k, l] = s-th sample of counts in l-th grade category in k-th situation
        df_index = pd.MultiIndex.from_product([range(len(n_count)),
                                               *[sit_dtype.categories
                                                 for sit_dtype in emf.situation_dtypes.values()]],
                                              names=[sample_head, *emf.situation_dtypes.keys()])
        a_grades = emf.ordinal_scales[emf.attribute_scales[a]].categories
        df = pd.DataFrame(n_count.reshape((-1, n_count.shape[-1])),
                          index=df_index, columns=a_grades)
        df.columns.set_names(a, inplace=True)
        return df.groupby(level=[0, *groupby], sort=False, group_keys=True).sum()
