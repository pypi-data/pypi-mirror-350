"""This module defines classes and methods for simulated EMA study
with group(s) of respondents drawn at random from population(s)
with specified inter-individual distributions of all model parameters.

The simulations can generate artificial data with the same structure
as a real experiment.


*** Main Module Classes:

EmaSimPopulation: defines distribution of model parameters
    for probabilities of one or more SITUATIONS, in one or more Situation Dimensions,
    and one or more perceptual ATTRIBUTE latent-variable locations
    in ONE (sub-)population of potential participants.

EmaSimExperiment: defines a complete EMA experiment,
    generates simulated responses by participants in one or more groups,
    sampled from EmaSimPopulation instance(s).
    The EMA data layout is defined by an ema_data.EmaFrame instance,
    defining Situation dimensions and categories, and
    defining discrete ordinal response scales for each Attribute.

EmaSimSubject = superclass for subject properties

SubjectBradley: single subject with Attribute ratings determined by
    the LatentLogistic-Terry-Luce (BTL) model, assuming standard Logistic latent variable,
    i.e., with st.dev. approx= 1.8

SubjectThurstone: single subject with Attribute ratings determined by
    the LatentNormal Case V model, assuming standard Gaussian latent variable,
    i.e., with st.dev. = 1.

EmaSimGroup: container for EmaSimSubject instances
    drawn at random from an EmaSimPopulation instance.


*** Main Class Methods:

EmaSimPopulation.gen_group(...)
    draws a group of simulated participants at random from the simulated Population.

EmaSimExperiment.gen_dataset(...)
    generates am ema_data.EmaDataSet instance with simulated EMA records
    for one or more groups of simulated participants.
    All records can be saved to file(s) using the EmaDataSet.save(...) method.

*** Usage example: See script run_sim.py

*** Version History:
* Version 1.1.5:
2025-05-24, remove global EMA_FRAME.
            Keep ref to EmaFrame instance as property in EmaSimPopulation, as v. 1.1.2.

* Version 1.1.3-4:
2025-03-30, global EMA_FRAME instance for all sim objects
2025-03-21, using ema_base.EmaObject as common superclass, with pretty-printing repr()
2025-03-09, New error class EmaSimInputError.
            EmaSimPopulation: user-friendly check of input typing errors
            Check EmaSimExperiment groups for consistency. Bug detected by Frederic Marmel Febr 2025

* Version 1.0.1:
2023-05-31, EmaSimPopulation.gen_group.gen_tau() simplified to use only ema_thresholds module functions,
    instead of ema_threshold classes

* Version 0.9.4:
2022-11-22, allow EmaSimPopulation settings restrict_attribute, restrict_threshold
            with same effects as in ema_model.EmaModel
2022-11-19, adapted to use ema_thresholds.Thresholds

* Version 0.9:
2022-03-21, adapted to use Pandas in EmaFrame and EmaDataSet

* Version 0.7.1:
2022-01-19, module function set_sim_seed to ensure reproducibility
2022-01-19, EmaSimSubject.rvs methods defined here, to ensure reproducibility
2022-01-06, EmaSimPopulation.response_width_mean to control individual decision thresholds
2022-01-05, minor cleanup EmaSimExperiment

* Version 0.5.1:
2021-11-25, allow experiment with NO Attributes

* Version 0.5:
2021-11-14, copied and modified PairedCompCalc -> EmaCalc
2021-11-16, first functional version
2021-11-21, rather extensively tested
"""
# *** store true EmaSimSubject, EmaSimPopulation properties as pd.DataFrame instances ? *****

# **** specify separate Attribute variance for each Situation dimension ????
# **** separate inter-individual attribute variance jointly for all situation_dtypes,
# **** plus variance for independent variations across situation_dtypes???

import numpy as np
import pandas as pd
import logging

from EmaCalc.ema_repr import EmaObject
from EmaCalc.ema_data import EmaDataSet
from EmaCalc.ema_thresholds import mapped_tau, mapped_tau_inv

from EmaCalc import ema_latent


RNG = np.random.default_rng()
# = default module-global random generator
# may be modified via function set_sim_seed

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # test


class EmaSimInputError(RuntimeError):
    """Any kind of input mismatch.
    """


# ------------------ module functions
def set_sim_seed(seed=None):
    """Set module-global RNG with given seed.
    To be called by user BEFORE any other work,
    to achieve reproducible results.
    :param seed: (optional) integer
    :return: None
    """
    global RNG
    RNG = np.random.default_rng(seed)
    if seed is not None:
        logger.warning(f'*** Using seed={seed} -> reproducible results.')


# --------------------------------------- subject response models
class EmaSimSubject(EmaObject):
    """Simulate one individual participant in an EMA data-collection experiment.
    Superclass for either SubjectBradley or SubjectThurstone
    """
    def __init__(self, sc_prob, a_theta, a_tau):  # lapse_prob=0.):
        """
        :param sc_prob: mD array with (non-normalized) conditional Situation probability
            sc_prob[k0, k1, k2,...] propto Prob (k1, k2, ...)-th situation, GIVEN k0-th Phase
            sc_prob.shape == emf.situation_shape
        :param a_theta: dict with (a_key, a_theta) elements, where
            a_key = a string identifying ONE Attribute among emf.attribute_grades.keys()
            a_theta[k0, k1, ...] = mD array with mean of latent sensory variable for Attribute a_key,
        :param a_tau: dict with (a_key, thr) elements, where
            tnr[l] = UPPER interval limit for l-th ordinal response,
            NOT INCLUDING extreme -inf, +inf limits
        """
        # *** store properties as pd.Series objects ? ******
        self.sc_prob = sc_prob
        self.a_theta = a_theta
        self.a_tau = a_tau

    def rrepr(self, r, level):
        with np.printoptions(threshold=20, edgeitems=2, precision=3):
            return super().rrepr(r, level)

    def attribute_theta(self, a, emf, groupby=None):
        """Present location of latent sensory variable, for ONE given attribute,
        given each situation category in selected situation dimension(s).
        :param a: attribute key = one of self.a_theta.keys()
        :param emf: EmaFrame object common for population and experiment
        :param groupby: (optional) tuple with situation key(s) to be included.
            If undefined, include ALL situation dimensions as defined in sit_keys
        :return: ds = pandas Series object
            with a MultiIndex with levels groupby,
            containing the mean attribute value for each category in groupby situation dimension(s),
            aggregated across all OTHER situation_dtypes not included in groupby,
            weighted by AVERAGE situation probabilities in those dimensions.
        """
        # *** would be slightly easier if properties were already stored as pd.Series objects
        theta = self.a_theta[a]
        ds_index = pd.MultiIndex.from_product([[0],
                                               *[sit_dtype.categories
                                                 for sit_dtype in emf.situation_dtypes.values()]],
                                              names=[0, *emf.situation_dtypes.keys()])
        # incl an extra index level to allow use of aggregate_attribute_theta
        theta_ds = pd.Series(theta.reshape((-1,)), index=ds_index)
        if groupby is None:
            return theta_ds.droplevel(0)  # skip the single-category level 0
        else:
            u = pd.Series(self.sc_prob.reshape((-1,)), index=ds_index)
            return aggregate_situation_theta(theta_ds, u, groupby).droplevel(0)

    def gen_ema_records(self, emf, min_ema, max_ema):
        """Generate a sequence of EMA records at random
        using response properties of self.
        :param emf: ema_data.EmaFrame instance
        :param min_ema: min random number of EMA records per Phase
        :param max_ema: max random number of EMA records per Phase
        :return: ema_df = a pd.DataFrame instance containing simulated EMA results,
            stored according to given emf.
            One column for each Situation dimension and each Attribute.
            One row for each simulated EMA record.
            Number of records randomly drawn with
            min_ema <= ema_df.shape[0] < max_ema
        """
        def situation_index(sit_p, sit_shape):
            """Generate ONE random situation index tuple, NOT including Phase index
            :param sit_p: 1D probability-mass array for all situations, EXCEPT Phase
            :param sit_shape: tuple with situation_shape EXCEPT Phase dimension
            :return: ind = index tuple; len(ind) = len(sc_shape)
             """
            sit_ind = RNG.choice(len(sit_p), p=sit_p)  # linear random index
            return np.unravel_index(sit_ind, shape=sit_shape)

        def situation_dict(sit_ind):
            """Convert index tuple to situation dict
            """
            return {sit_key: sit_dtype.categories[i]
                    for (i, (sit_key, sit_dtype)) in zip(sit_ind,
                                                         emf.situation_dtypes.items())}
        # -------------------------------------------------------

        ema_list = []
        # = list of dicts, one for each simulated EMA record
        sit_shape_phase = emf.situation_shape[1:]
        sit_prob_phase = self.sc_prob.reshape((self.sc_prob.shape[0], -1))
        for (i, p) in enumerate(sit_prob_phase):
            n_rec = RNG.integers(min_ema, max_ema)
            for _ in range(n_rec):
                sit_index = (i, *situation_index(p, sit_shape_phase))
                a_grades = self.gen_attr_grades(emf, sit_index)
                ema_list.append(situation_dict(sit_index) | a_grades)
        cat_dtypes = emf.situation_dtypes | emf.attribute_dtypes  # ****** needed ?
        return pd.DataFrame.from_records(ema_list).astype(cat_dtypes)

    def gen_attr_grades(self, emf, sit_index):
        """Generate random ordinal Attribute grades in given Situation
        :param emf: external ema_data.EmaFrame object defining experimental layout
        :param sit_index: index tuple defining ONE situation for this record,
            including index in ALL situation dimensions
        :return: a_grades = dict with elements (a, grade)
        """
        def rvs_grade(th, tau):
            """Generate a random grade index for ONE attribute in ONE situation
            :param th: scalar location of latent variable in the given situation
            :param tau: 1D threshold array for this attribute,
                NOT INCLUDING extreme -inf, +inf limits
            :return: scalar integer index of given rating
            """
            x = self.rvs(th)  # done by sub-class
            return np.sum(x > tau)
        # -------------------------------------------------------
        return {a: emf.attribute_dtypes[a].categories[rvs_grade(a_th[sit_index],
                                                                self.a_tau[a])]
                for (a, a_th) in self.a_theta.items()}

    @staticmethod
    def rvs(loc, size=None):
        """Abstract method, implemented by sub-class.
        Draw random variables from self
         :param loc: scalar or array-like location
         :param size: (optional) size of result
         :return: x = scalar or array
             x.shape == loc.shape, if no size is given
         """
        raise NotImplementedError

    # def lapse(self):  # *** future ???
    #     """Generate True with prob = self.lapse_prob
    #     """
    #     return uniform.rvs(0, 1.) < self.lapse_prob
    #
    # def lapse_response(self):
    #     """Generate a random result, disregarding latent variable and threshold parameters
    #     :return: scalar integer
    #         in {-n_difference_grades, ...,-1, +1,..., + n_difference_grades}, if forced_choice
    #         in {-n_difference_grades+1, ...,0, ...,  + n_difference_grades-1}, if not forced_choice
    #         i.e., excluding 0 if self.emf.forced_choice
    #     """
    #     n_response_limits = len(self.response_thresholds)
    #     # if self.emf.forced_choice:
    #     if self.response_thresholds[0] == 0.:  # forced_choice
    #         return ((-1 if uniform.rvs() < 0.5 else +1) *
    #                 randint.rvs(low=1, high=n_response_limits + 1))
    #
    #     else:
    #         return randint.rvs(low=-n_response_limits,
    #                            high=n_response_limits + 1)
    #


class SubjectThurstone(ema_latent.LatentNormal, EmaSimSubject):
    """Simulate a subject using the LatentNormal Case V choice model.
    """
    @staticmethod
    def rvs(loc, size=None):
        """Draw random sample(s) from self
        :param loc: scalar or array-like location
        :param size: (optional) size of result
        :return: x = scalar or array
            x.shape == loc.shape, if no size is given
        """
        loc = np.asarray(loc)
        if size is None:
            size = loc.shape
        return loc + RNG.standard_normal(size=size)


class SubjectBradley(ema_latent.LatentLogistic, EmaSimSubject):
    """Simulate one individual participant in a paired-comparison experiment.
    The subject responds using the LatentLogistic-Terry-Luce choice model,
    with parameters defined in the log domain.
    """
    @staticmethod
    def rvs(loc, size=None):
        """Draw random variables from self
        :param loc: scalar or array-like location
        :param size: (optional) size of result
        :return: x = scalar or array
            x.shape == loc.shape
        """
        return RNG.logistic(loc, size=size)


# -------------------------------------------------------------------------
class EmaSimPopulation(EmaObject):
    """Defines a simulated population
    from which groups of random test participants can be generated
    for a simulated EMA experiment.

    The population instance defines distributions for
    one or more nominal Situation categories, and
    zero, one or more perceptual Attributes, given any Situation.

    Each Situation is a combination of one category from each Situation Dimension.
    """
    def __init__(self, emf,
                 situation_prob,
                 attribute_mean=None,
                 log_situation_std=0.,
                 attribute_std=0.,
                 response_width_mean=None,  # -> subject_class.scale
                 log_response_width_std=0.,
                 lapse_prob_range=(0., 0.),  # ******* not used ******
                 subject_class=SubjectBradley,
                 restrict_attribute=False,
                 restrict_threshold=True,
                 id=''):
        """
        :param emf: ema_data.EmaFrame instance defining Situations and Attributes
        :param situation_prob: array-like multi-dim, with
            situation_prob[k0, k1,...] prop.to probability of (k1, k2,...)-th situation,
            GIVEN the k0-th test phase category, even if only one phase category.
            situation_prob.shape must correspond to shape of emf.situation_dtypes.
        :param attribute_mean: (optional) dict or iterable with elements (a_key, a_mean), where
            a_key is string id of a rated perceptual attribute,
            a_mean is an mD array with
            a_mean[k0, k1, ...] = latent-variable mean for attribute a_key, in subject_class scale units,
            given the (k0, k1,...)-th Situation category, i.e.,
            a_mean.shape == situation_prob.shape, for all attributes.
        :param log_situation_std: (optional) inter-individual standard deviation of
            log probabilities for each situation category.
        :param attribute_std: (optional) scalar inter-individual standard deviation of all attribute parameters
        :param response_width_mean: (optional) mean width of response intervals,
            in subject_class scale units
        :param log_response_width_std: (optional) scalar standard deviation of log(response-interval-width)
        :param lapse_prob_range: (optional) tuple (min, max) probability of random lapse response
        :param subject_class: (optional) subject probabilistic model for generating responses
        :param restrict_attribute: (optional) boolean switch
            to force mean attribute location == 0., mean across situations
        :param restrict_threshold: (optional) boolean switch
            to force ONE mid-range response-threshold == 0.
        :param id: (optional) string label, used as prefix in all generated subject names
        """
        # *** store situation_prob, attribute_mean as pd.Series objects ? ******
        # global EMA_FRAME  # v 1.1.3, reverted.
        # EMA_FRAME = emf
        self.emf = emf  # save emf ref here, too, although same for all subpopulations
        # *** send emf as arg when needed ? ***
        situation_prob = np.asarray(situation_prob)
        if emf.situation_shape[0] == 1 and emf.situation_shape[1:] == situation_prob.shape:
            situation_prob = situation_prob[None, ...]
        if emf.situation_shape != situation_prob.shape:
            raise RuntimeError('situation_prob.shape must agree with EmaFrame situation_dtypes')
        self.situation_prob = situation_prob
        for (i, sc_i) in enumerate(self.situation_prob):
            self.situation_prob[i] /= np.sum(sc_i)
            # = normalizes conditional probabilities, for each phase
        self.log_situation_std = log_situation_std

        if attribute_mean is None:
            attribute_mean = dict()  # NO attributes
        else:
            attribute_mean = dict(attribute_mean)
        self._match_attribute_keys(attribute_mean)  # ensure they agree with self.emf
        for (a, a_mean) in attribute_mean.items():
            if (emf.situation_shape[0] == 1
                    and emf.situation_shape[1:] == a_mean.shape):
                attribute_mean[a] = attribute_mean[a][None, ...]
        assert all(a_mean.shape == emf.situation_shape
                   for a_mean in attribute_mean.values()), 'attribute_mean.shape must match situation_shape'
        if restrict_attribute and emf.tied_response_scales:
            restrict_attribute = False
            logger.warning('*** Cannot use restrict_attribute=True with tied response scales')
        if restrict_attribute and restrict_threshold:
            restrict_attribute = False  # ONLY ONE restriction allowed
            logger.warning(f'Only ONE restriction allowed: using restrict_threshold={restrict_threshold}')
        self.restrict_attribute = restrict_attribute
        self.restrict_threshold = restrict_threshold
        if self.restrict_attribute:
            attribute_mean = {a: a_mean - np.mean(a_mean)
                              for (a, a_mean) in attribute_mean.items()}
        self.attribute_mean = attribute_mean
        self.attribute_std = attribute_std
        if response_width_mean is None:
            response_width_mean = subject_class.scale
        self.response_width_mean = response_width_mean
        # if self.restrict_threshold:
        #     self._thr = ThresholdsMidFixed
        # else:
        #     self._thr = ThresholdsFree
        # self._eta = _init_eta(response_width_mean, self._thr)
        self.log_response_width_std = log_response_width_std
        # = inter-individual std around self._eta
        self.lapse_prob_range = lapse_prob_range
        self.subject_class = subject_class
        self.id = id   # needed only as prefix in participant names

    def rrepr(self, r, level):
        with np.printoptions(threshold=20, edgeitems=2, precision=3):
            return super().rrepr(r, level)

    # def __repr__(self):
    #     return (f'{self.__class__.__name__}(\n\t' +
    #             ',\n\t'.join(f'{key}={repr(v)}'
    #                          for (key, v) in vars(self).items()) +
    #             '\n\t)')

    def _match_attribute_keys(self, attr_dict):
        """Ensure attribute dict keys match with EmaFrame definition.
        Changed in place if needed and possible
        :param attr_dict: dict with (a_key, array) items
        :return: None
        """
        a_keys_old = list(attr_dict.keys())  # list because keys may change in iteration
        a_keys_new = [self.emf.match_attribute_key(a_k) for a_k in a_keys_old]
        for (ak_new, ak_old) in zip(a_keys_new, a_keys_old):
            if ak_new != ak_old:
                attr_dict[ak_new] = attr_dict.pop(ak_old)
                logger.warning(f'Attribute label {ak_old} changed to {ak_new}.')
        if set(attr_dict.keys()) != set(self.emf.attribute_dtypes.keys()):
            raise EmaSimInputError('attribute_mean must define same attributes as EmaFrame')

    @property
    def n_attributes(self):
        return len(self.attribute_mean)

    def gen_group(self, n_participants=1):
        """Create a group of simulated-subject instances randomly drawn from self,
        with properties suitable for a planned experiment.
        :param n_participants: number of randomly drawn participants from self
        :return: single EmaSimGroup instance, containing generated participants,
            each with properties drawn from self.
        """
        def gen_sc_prob():  # *** -> general local self.method ? ****
            sc_p = np.exp(np.log(self.situation_prob) +
                          self.log_situation_std *
                          RNG.standard_normal(size=self.emf.situation_shape))
            for (i, sc_i) in enumerate(sc_p):
                sc_p[i] /= np.sum(sc_i)
                # normalized conditional probabilities, for each phase
            return sc_p

        def gen_attr():
            theta = self.attribute_std * RNG.standard_normal(size=(self.n_attributes,
                                                                   *self.emf.situation_shape))
            # theta[i, ...] = random offset of location for i-th attribute of s-th subject
            return {a: th_mean + th_d
                    for ((a, th_mean), th_d) in zip(self.attribute_mean.items(),
                                                    theta)}

        def gen_tau():
            """Random threshold parameters for each attribute
            """
            def tau(n_levels):  #, thr):
                """Calc response thresholds
                :param n_levels: integer number of response intervals
                :return: t = 1D array with INNER interval limits, i.e.,
                    t[m] = UPPER interval limit for m-th ordinal response
                    t.shape == (n_levels - 1,)
                """
                t = self.response_width_mean * (np.arange(n_levels - 1) + 1. - n_levels / 2)
                # n_eta = thr.n_param(n_levels)  # Old version <= 1.0.0
                # eta = thr.tau_inv(t) + self.log_response_width_std * RNG.standard_normal(size=n_eta)
                # # incl. random variations of log interval width in mapped [0, 1] range
                # tau_OLD = thr.tau(eta)[1:-1]  # EXCL (-inf, +inf) extremes
                # *** new method without using specific threshold classes
                n_half = n_levels // 2 - 1
                if self.restrict_threshold:
                    t -= t[n_half]  # t[n_half] forced -> 0
                w = mapped_tau_inv(t)
                w *= np.exp(self.log_response_width_std * RNG.standard_normal(size=len(w)))
                t = mapped_tau(w)[1:-1]  # EXCL (-inf, +inf) extremes
                if self.restrict_threshold:
                    t -= t[n_half]  # t[n_half] forced -> 0
                return t

            # ----------------------------------------------------
            # if self.restrict_threshold:  # ******** not needed
            #     thr = ThresholdsMidFixed
            # else:
            #     thr = ThresholdsFree  # ******
            # thr = None  # ****** not needed any more
            scale_tau = {s_id: tau(len(scale.categories))  # , thr)
                         for (s_id, scale) in self.emf.ordinal_scales.items()}
            # = scale thresholds, possibly used for more than one attribute
            return {a: scale_tau[s_id]
                    for (a, s_id) in self.emf.attribute_scales.items()}
            # --------------------------------------------------------------------
        return EmaSimGroup(self,
                           {self.id + f'_S{i}': self.subject_class(sc_prob=gen_sc_prob(),
                                                                   a_theta=gen_attr(),
                                                                   a_tau=gen_tau())
                            for i in range(n_participants)})

    def situation_prob_mean(self, groupby=None):
        """Mean situation probabilities as pd.Series
        :param groupby: (optional) tuple with situation key(s) to be included.
            If undefined, include ALL situation dimensions as defined in self.emf
        :return: ds = pandas Series object
            with a (Multi)Index with one level for each situation dimension in groupby,
            containing the CONDITIONAL probability for categories in groupby[0], given other groupby cases,
            aggregated across all situation dimensions NOT included in groupby.
        """
        u = self.situation_prob
        # u[k0, k1,...] = P[(k1, k2,...)-th situation | phase k0], already normalized
        ds_index = pd.MultiIndex.from_product([[0], *[sit_dtype.categories
                                                 for sit_dtype in self.emf.situation_dtypes.values()]],
                                              names=['', *self.emf.situation_dtypes.keys()])
        # incl an extra "sample" index level to allow using same aggregate_situation_prob
        ds = pd.Series(u.reshape((-1,)), index=ds_index)
        if groupby is None:
            return ds.droplevel(0) # skip the single-category level 0
        else:
            return aggregate_situation_prob(ds, groupby).droplevel(0)

    def situation_prob_rvs(self, groupby=None, n_samples=1, sample_head='_sample'):
        """Extract samples of probability-mass for situations
        :param groupby: (optional) tuple with situation key(s) to be included.
            If undefined, include ALL situation dimensions as defined in self.emf
        :param sample_head: (optional) level name of sample index
        :return: ds = pandas Series object
            with a MultiIndex with levels (sample_head, *groupby),
            containing the CONDITIONAL probability for categories in groupby[0], given other groupby cases,
            aggregated across situation dimensions NOT included in groupby.

        Method: copied from ema_base.situation_prob_df
        """
        u = np.exp(np.log(self.situation_prob) +
                      self.log_situation_std *
                      RNG.standard_normal(size=(n_samples, *self.emf.situation_shape)))
        # u[s, k0, k1,...] propto s-th sample of P[(k1, k2,...)-th situation | phase k0]
        u = u.reshape((*u.shape[:1], -1))
        # u[s, k0, k] = propto s-th sample of prob of k-th <-> (k0, k1,...)-th situation
        u /= np.sum(u, axis=-1, keepdims=True)
        # u[s, k0, k] = s-th sample of conditional P[k-th <-> (k1, k2,...)-th situation | phase k0]
        ds_index = pd.MultiIndex.from_product([range(len(u)),
                                               *[sit_dtype.categories
                                                 for sit_dtype in self.emf.situation_dtypes.values()]],
                                              names=[sample_head, *self.emf.situation_dtypes.keys()])
        ds = pd.Series(u.reshape((-1,)), index=ds_index)
        if groupby is None:
            return ds
        else:  # ***** -> function aggregate_situation_prob
            return aggregate_situation_prob(ds, groupby)

    def attribute_theta_mean(self, a, groupby=None):
        """Extract mean location of latent sensory variable, for ONE given attribute,
        given each situation category in selected situation dimension(s).
        :param a: attribute key = one of self.emf.attribute_grades.keys()
        :param groupby: (optional) tuple with situation key(s) to be included.
            If undefined, include ALL situation dimensions as defined in self.emf
        :return: ds = pandas Series object
            with a MultiIndex with levels groupby,
            containing the mean attribute value for each category in groupby situation dimension(s),
            aggregated across all OTHER situation_dtypes not included in groupby,
            weighted by AVERAGE situation probabilities in those dimensions.
        """
        theta = self.attribute_mean[a]
        df_index = pd.MultiIndex.from_product([[0],
                                               *[sit_dtype.categories
                                                 for sit_dtype in self.emf.situation_dtypes.values()]],
                                              names=[0, *self.emf.situation_dtypes.keys()])
        # incl an extra index level to allow use of aggregate_attribute_theta
        theta_ds = pd.Series(theta.reshape((-1,)), index=df_index)
        if groupby is None:
            return theta_ds.droplevel(0) # skip the single-category level 0
        else:
            u = self.situation_prob
            u = pd.Series(u.reshape((-1,)), index=df_index)
            return aggregate_situation_theta(theta_ds, u, groupby).droplevel(0)

    def attribute_theta_rvs(self, a, groupby=None, n_samples=1, sample_head='_sample'):
        """Extract location of latent sensory variable, for ONE given attribute,
        given each situation category in selected situation dimension(s).
        :param a: attribute key = one of self.emf.attribute_grades.keys()
        :param groupby: (optional) tuple with situation key(s) to be included.
            If undefined, include ALL situation dimensions as defined in self.emf
        :param sample_head: (optional) level name of sample index
        :return: ds = pandas Series object
            with a MultiIndex with levels (sample_head, *groupby),
            containing the Attribute value samples for each category in groupby situation dimension(s),
            aggregated across all OTHER situation_dtypes not included in groupby,
            weighted by AVERAGE situation probabilities in those dimensions.

        Method: same as ema_base.attribute_theta_df(...)
        """
        th_mean = self.attribute_mean[a]
        th_std = self.attribute_std
        theta = th_std * RNG.standard_normal(size=(n_samples, *th_mean.shape)) + th_mean
        # theta[s, k0, k1,...] = s-th sample of attribute attr, given (k0, k1,...)-th situation
        ds_index = pd.MultiIndex.from_product([range(len(theta)),
                                               *[sit_dtype.categories
                                                 for sit_dtype in self.emf.situation_dtypes.values()]],
                                              names=[sample_head, *self.emf.situation_dtypes.keys()])
        theta_ds = pd.Series(theta.reshape((-1,)), index=ds_index)
        if groupby is None:
            return theta_ds
        else:  # -> separate aggregate function
            u_ds = self.situation_prob_rvs(n_samples=n_samples, sample_head=sample_head)
            return aggregate_situation_theta(theta_ds, u_ds, groupby)
            # # TEST for comparison:
            # aggregate_by = list(set(self.emf.situation_dtypes.keys()) - set(groupby))
            # # = OTHER situation dimensions to be aggregated out
            # u = self.situation_prob_rvs(n_samples=n_samples, sample_head=sample_head)
            # # u = Series object with same MultiIndex as theta_ds),
            # # containing the CONDITIONAL probability for categories in situation_dtypes[1:]
            # # given Phase category in situation_dtypes[0]
            # u = u / len(u.index.levels[1])
            # # u = absolute prob.mass for each sample and situation category
            # w_av = u.groupby(level=[0, *aggregate_by],
            #                  sort=False, group_keys=True).transform(sum)
            # # = AVERAGE prob.mass for categories in aggregate_by
            # # = same as ema_display.aggregate_situation_theta
            # theta_ds = theta_ds * w_av
            # return theta_ds.groupby(level=[0, *groupby], sort=False, group_keys=True).sum()


class EmaSimGroup(EmaObject):
    """Group of test participants drawn from a given population
    """
    def __init__(self, pop, participants):
        """
        :param pop: an EmaSimPopulation instance,
            from which participants have been drawn at random
        :param participants: dict with items (s_id, s_sim)
            s_id = string id for the subject
            s_sim = an EmaSimSubject instance
        """
        self.pop = pop
        self.participants = participants

    # def __repr__(self):  # *********** -> rrepr(self, level)
    #     # n_ema = sum(s_df.shape[0] for s_df in self.participants.values())
    #     return (self.__class__.__name__ + '('
    #             + f'\n\tpop={repr(self.pop)}'
    #             + f'\n\tparticipants= dict with {len(self.participants)} simulated participants)')


# -------------------------------------------------------------------------
class EmaSimExperiment(EmaObject):
    """Defines a simulated EMA data-collection experiment,
    with one or more groups of simulated participants, with
    each group generated from an EmaSimPopulation instance.

    Method gen_dataset() generates a complete ema_data.EmaDataSet instance
    with EMA records for all participants in all groups.

    The experimental procedure is defined by
    emf = an ema_data.EmaFrame instance
    """
    def __init__(self, emf, groups):
        """
        :param emf: EmaFrame instance, defining experimental parameters
        :param groups: dict with elements (g_id, g_sim),
            g_id is a tuple with one or several group-category labels,
                one for each element in emf.group_head()
            g_sim = an EmaSimGroup instance
        """
        # global EMA_FRAME
        # EMA_FRAME = emf
        self.emf = emf
        group_keys = [emf.match_group_key(g) for g in groups.keys()]
        for (gk_new, gk_old) in zip(group_keys, groups.keys()):
            if gk_new != gk_old:
                groups[gk_new] = groups.pop(gk_old)
                logger.warning(f'Group key {gk_old} changed to {(gk_new,)} to match EmaFrame.')
        self.groups = groups

    # def __repr__(self):
    #     return (f'{self.__class__.__name__}(\n\t' +
    #             ',\n\t'.join(f'{key}={repr(v)}'
    #                          for (key, v) in vars(self).items()) +
    #             '\n\t)')

    def gen_dataset(self, min_ema=3, max_ema=50):
        """Generate a complete EmaDataSet instance for this experiment,
        with one or more groups of participants.
        :param min_ema: min random number of EMA records in each Phase
        :param max_ema: max random number of EMA records in each Phase
        :return: a single EmaDataSet instance
        """
        emd = {g: {s_id: s.gen_ema_records(self.emf, min_ema, max_ema)
                   for (s_id, s) in g_sim.participants.items()}
               for (g, g_sim) in self.groups.items()}
        return EmaDataSet(self.emf, emd)


# ------------------------------------------------ module support functions
def aggregate_situation_prob(ds, groupby):
    """Aggregate conditional situation probabilities
    :param ds: pd.Series with (Multi)Index with levels = [0, *situation_keys]
        with CONDITIONAL probabilities for categories in situation_keys[1:], given situation_keys[0] = Phase
    :param groupby: tuple with situation key(s) to be included in result
    :return: ds = pandas Series object
        with a MultiIndex with levels (sample_head, *groupby),
        containing the CONDITIONAL probability for categories in groupby[0], given other groupby cases,
        aggregated across situation dimensions NOT included in groupby.
    """
    # **** generalize this for sampled data or NO sample index *** ?
    ds = ds / ds.index.levshape[1]
    # = unconditional prob for each category in situation_keys, for ALL dimensions INCL Phase
    ds = ds.groupby(level=[0, *groupby], sort=False, group_keys=True).sum()
    if len(groupby) > 1:
        # rescale to CONDITIONAL prob for categories in groupby[0], given other dimensions
        ds = ds / ds.groupby(level=[0, *groupby[1:]],
                             sort=False, group_keys=True).transform('sum')
        # CHECK: df.groupby(level=[0, *groupby[1:]], sort=False).sum() == 1., in all groups
    return ds


def aggregate_situation_theta(theta_ds, u_ds, groupby):
    """Aggregate attribute locations given for each situation category
    by averaging across situations NOT included in result.
    :param theta_ds: pd.Series with (Multi)Index with levels = [0, *situation_keys]
        with attribute locations in each category of situation_keys
    :param u_ds: pd.Series with same (Multi)Index as theta_ds,
        with CONDITIONAL probabilities for situations in situation_keys[1:], given situation_keys[0] = Phase
    :param groupby: tuple with situation key(s) to be included in result
    :return: ds = pandas Series object
        with a MultiIndex with levels (sample_head, *groupby),
        containing the CONDITIONAL probability for categories in groupby[0], given other groupby cases,
        aggregated across situation dimensions NOT included in groupby.
    """
    situation_keys = theta_ds.index.names[1:]
    # = situation dimensions in order as defined in EmaFrame
    aggregate_by = list(set(situation_keys) - set(groupby))
    # = OTHER situation dimensions to be aggregated out
    # u = self.situation_prob_rvs(n_samples=n_samples, sample_head=sample_head)
    # # u = Series object with same MultiIndex as theta_ds),
    # # containing the CONDITIONAL probability for categories in situation_dtypes[1:]
    # # given Phase category in situation_dtypes[0]
    u_ds = u_ds / len(u_ds.index.levels[1])
    # u = absolute prob.mass for each sample and situation category
    w_av = u_ds.groupby(level=[0, *aggregate_by],
                        sort=False, group_keys=True).transform('sum')
    # = AVERAGE prob.mass for categories in aggregate_by
    theta_ds = theta_ds * w_av
    return theta_ds.groupby(level=[0, *groupby], sort=False, group_keys=True).sum()
