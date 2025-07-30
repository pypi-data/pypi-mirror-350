"""This module defines a Bayesian probabilistic model of EMA data.
The model is learned using observed EMA recordings from all participants,
stored in an ema_data.EmaDataSet instance.

This model version uses a mixture of Gaussian distributions
for the parameter vectors in each population of potential respondents,
represented by one group of participants.
A separate GMM is learned for each population.

Individual parameter distributions are approximated by sampling.
The population mixture model is common prior for all individuals in
the group recruited from the same population.

The model can NOT use Bayesian sequential learning.
It must be trained in a single run from a single batch of EMA data,
which is usually quite sufficient for practical applications.

However, its learn(...) method can be called several times,
in case learning stopped before reaching convergence.

*** Class Overview:

EmaModel: Defines posterior distributions of situation probabilities,
    and locations of latent variables for perceptual attribute(s),
    learned from EMA data in an ema_data.EmaDataSet instance.
    The EMA study may include data from different groups of participants,
    represented by an ema_group.EmaGroupModel instance for each population / participant group.

ema_group.EmaGroupModel: Defines a GMM for ONE population,
    and contains all individual response-probability models,
    implemented by an ema_respondent.EmaRespondentModel instance for each participant,
    in ONE group of test participants, assumed recruited from the SAME population.

ema_respondent.EmaRespondentModel: Distribution of individual parameter vector
    assumed to determine the observed EMA data for ONE participant.
    Each EMA record specifies
    (1) a nominal (possibly multidimensional) Situation category, and
    (2) ordinal Ratings for zero, one, or more subjective Attributes.
    The parameter distribution is represented by an array xi with many samples.

ema_base.EmaParamBase: common properties defining
    indexing into array of parameter vectors, and
    a prior GaussianRV instance for all GMM components in all groups.

*** Model Theory: The present model is theoretically similar to
the model of the PairedCompCalc package, partly described in
A. Leijon, M. Dahlquist, and K. Smeds (2019):
Bayesian analysis of paired-comparison sound quality ratings. JASA 146(5):3174–3183.

EXCEPT for the present use of a mixture model for the population(s).

Detailed math documentation is presented in
A. Leijon, P. von Gablenz, I. Holube, J. Taghia, and K. Smeds.
Bayesian analysis of ecological momentary assessment (EMA) data
collected in adults before and after hearing rehabilitation.
Frontiers in Digital Health, 5(1100705), 2023.

*** Version History:
* Version 1.1.5:
2025-05-23, Cannot use global ema_base.EMA_BASE object! Does not work with pickle.load().
            EmaModel.initialize calls EmaParamBase.initialize instead.

* Version 1.1.3:
2025-03-29, initialize global ema_base.EMA_BASE object for use in all modules
2025-03-21, using ema_repr.EmaObject as superclass

* Version 1.1.0:
2024-02-04, new method EmaModel.gen_population_models,
            allowing ema_display to show results for any combination of group "dimensions".
            E.g., if population/group dimensions are ('Age', 'Gender'),
            show only for 'Age' categories, as a weighed average across 'Gender' categories.

* Version 1.0.2:
2023-09-07, EmaModel.initialize: default n_participant_per_comp=10, for faster learning

* Version 1.0.1:
2023-06-10, EmaModel.initialize changed argument rv_class ->  latent_class = 'logistic' or 'normal'

* Version 1.0.0:
2023-05-17, EmaModel.initialize(...) using n_participants_per_comp instead of max_n_comp.

* Version 0.9.3:
2022-08-20, ensure restrict_attributes=False, in case tied response scales
2022-06-xx, adapted to use pandas.DataFrame storage in ema_data.

* Version 0.8.3:
2022-03-08, minor cleanup

* Version 0.8.1
2022-02-26, cleanup logger output, cleanup comments
2022-02-26, class def EmaGroupModel -> module ema_group, EmaRespondentModel -> ema_respondent
2022-02-26, complete separate GMM for each group, GMM components -> EmaGroupModel property comp

* Version 0.8
2022-02-12, Changed VI factorization for better approximation,
    with individual indicators conditional on parameter samples,
    defining variational q(zeta_n, xi_n) = q(zeta_n | xi_n) q(xi_n)

* Version 0.7.2
2022-01-31, Different random Generator for each EmaRespondentModel sampler, spawned from same seed

* Version 0.7.1
2022-01-30, NO module-global random Generator object here
2022-01-30, seed input to EmaModel.initialize, for reproducible results
2022-01-29, random.Generator argument to EmaRespondentModel.initialize
2022-01-11, minor update EmaRespondentModel.adapt_xi, restrict_xi

* Version 0.7:
2021-12-15, new method EmaRespondentModel.mean_attribute_grade
2021-12-20, new method EmaRespondentModel.nap_diff, calculate NAP distance

* Version 0.6:
2021-12-06, Allow user control switches: restrict_attribute OR restrict_threshold
2021-12-08, restrict_attribute: sensory-variable location average forced -> 0.
            restrict_threshold: response-threshold median forced -> 0.

* Version 0.5:
2021-11-03, first functional version
2021-11-04, removed EmaGroupModel.initialize_weights and EmaRespondentModel.initialize_weights
2021-11-05, Hamiltonian sampler -> EmaRespondentModel property -> better stepsize optimization
2021-11-07, store EmaParamBase object as property, so it gets pickled automatically
2021-11-18, cleanup comments
"""
import datetime as dt
import logging

import numpy as np

from EmaCalc.dirichlet import JEFFREYS_CONC
# = Jeffreys prior concentration for Dirichlet distribution
# **** Use reference prior conc approx = 1/K instead for the Dirichlet (Berger-2009)?

from EmaCalc.ema_repr import EmaObject
from EmaCalc.ema_base import EmaParamBase
from EmaCalc.ema_group import EmaGroupModel, PopulationModel
from EmaCalc.ema_latent import LatentLogistic, LatentNormal


# -------------------------------------------------------------------
__ModelVersion__ = "2025-05-23"

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # *** TEST


# ------------------------------------------------------------------
class EmaModel(EmaObject):
    """Defines probability distributions of EMA recordings
    for all populations from which participants were recruited,
    and for all participants in each group,
    given all included EMA data,
    as collected in one ema_data.EmaDataSet instance.

    Model parameters define estimated probabilities for nominal SITUATIONS,
    and estimated distributions of latent variables that determine ordinal subjective ratings
    on given ATTRIBUTE questions.
    The latent variables have continuous values on an INTERVAL scale, as defined by the model,
    although all subjective Attribute ratings are discrete on ORDINAL scales.

    Each ATTRIBUTE latent-variable location may depend on one or more situation dimensions,
    as estimated by an ordinal regression model,
    including main and interaction effects as requested by the user.

    The model allows for the possibility that different respondents
    might interpret and use the ordinal rating scales in different ways,
    by including separate response-threshold parameters for each individual.

    The model allows for the possibility that each respondent
    might use different response thresholds for each Attribute question,
    even if the response alternatives are expressed by the same words.

    However, the researcher may also set up the ema_data.EmaFrame object such that
    the model presumes identical response thresholds for separate Attributes.
    """
    def __init__(self, base, groups, rng):
        """
        :param base: unique EmaParamBase object, used by all model parts
        :param groups: dict with EmaGroupModel instances, stored as
            groups[group] = one EmaGroupModel instance, where
                group = dict key = tuple (cat0, cat1, ...), one catx from each group dimension
            groups[group].participants[s_id] = an EmaRespondentModel instance, where
            s_id is a key identifying the participant.
        :param rng: random Generator object
        """
        self.base = base   # NEEDED! pickle.load() cannot find global ema_base.EMA_BASE
        self.groups = groups
        self.rng = rng

    @classmethod
    def initialize(cls, ds, effects,
                   max_n_comp=None,
                   n_participants_per_comp=10,
                   latent_class='logistic',
                   restrict_attribute=False,
                   restrict_threshold=True,
                   seed=None):
        """Create a crude initial model from all available EMA data.
        :param ds: a single ema_data.EmaDataSet instance with all EMA data for analysis
        :param effects: iterable with desired estimated effects of situation on attribute attribute_grades.
            Each effect element = a key in ds.emf.situation_dtypes, or a tuple of such keys.
        :param max_n_comp: Not used, only for compatibility warning
        :param n_participants_per_comp: (optional) expected number participants per mixture component
            -> initial n_comp = n_participants // n_participants_per_comp
            The number of actually used components may be reduced during VI learning.
        :param latent_class: (optional) string label for latent sensory random variable
        :param restrict_attribute: (optional) boolean switch
            to force restriction on attribute sensory-variable locations
        :param restrict_threshold: (optional) boolean switch
            to force restriction on response-threshold locations
        :param seed: (optional) integer to get reproducible random sequences
        :return: a cls instance
        """
        ds.ensure_complete()
        # -> removed participant with no EMA records and group with no participants
        if max_n_comp is not None:
            logger.warning(f'Version >= 1.0: max_n_comp no longer used. Set n_participants_per_comp instead.')
        n_participants_per_comp = max(2, n_participants_per_comp)
        if restrict_attribute and ds.emf.tied_response_scales:
            restrict_attribute = False
            logger.warning('*** Cannot use restrict_attribute=True with tied response scales')
        if restrict_attribute and restrict_threshold:
            restrict_attribute = False  # ONLY ONE restriction allowed
            logger.warning(f'Only ONE restriction allowed: using restrict_threshold={restrict_threshold}')
        if not (restrict_attribute or restrict_threshold):
            logger.warning('Either restrict_attribute or restrict_threshold '
                           + 'should be True, to avoid artificial variance!')
        if latent_class.lower() in {'logistic', 'logit'}:  # *** use difflib here?
            rv_class = LatentLogistic
        elif latent_class.lower() in {'normal', 'gaussian', 'probit'}:
            rv_class = LatentNormal
        else:
            raise RuntimeError(f'Unknown label latent_class = ' + repr(latent_class))
        # base = ema_base.initialize(ds.emf, effects, rv_class,
        #                            restrict_attribute=restrict_attribute,
        #                            restrict_threshold=restrict_threshold)  # v 1.1.3
        base = EmaParamBase.initialize(ds.emf, effects, rv_class,
                                       restrict_attribute=restrict_attribute,
                                       restrict_threshold=restrict_threshold)  # v 1.1.5
        seed_seq = np.random.SeedSequence(seed)
        rng = np.random.default_rng(seed_seq)
        # = main Generator for all random numbers, EXCEPT EmaRespondentModel instances
        # Same rng for all EmaGroupModel instances, but separate for EmaRespondentModel-s
        group_seeds = seed_seq.spawn(len(ds.groups))
        groups = {g: EmaGroupModel.initialize(n_participants_per_comp, base, g_data, g_seed, rng)
                  for ((g, g_data), g_seed) in zip(ds.groups.items(),
                                                   group_seeds)}
        logger.info('EmaModel initialized with ' +
                    f'{len(groups)} group(s); ' +
                    f'{base.n_parameters} model parameters / participant;\n\t' +
                    f'restrict_attribute = {restrict_attribute}; ' +
                    f'restrict_threshold = {restrict_threshold};' +
                    f'\n\tn_participants_per_comp={n_participants_per_comp}; ' +
                    f'latent_class = ' + repr(latent_class) + '.'
                    )
        if seed is None:
            logger.debug(f'*** Using seed={seed}')
        else:
            logger.warning(f'*** Using seed={seed} -> reproducible results.')
        return cls(base, groups, rng)

    # ------------------------------------------ General VI learn algorithm:
    def learn(self,
              min_iter=10,
              min_step=0.1,
              max_iter=np.inf,
              max_hours=0.,
              max_minutes=0.,
              callback=None):
        """Learn all individual and population parameter distributions
        from all observed EMA data stored in self.groups[...].participants[...],
        using Variational Inference (VI).

        This method adapts a population GMM in each EmaGroupModel instance,
        and a sampled approximation of parameter distribution in all EmaRespondentModel instances.

        VI maximizes a lower bound to the total log-likelihood of all observed data.
        The resulting sequence of log-likelihood values is guaranteed to be non-decreasing,
        except for minor random variations caused by the sampling.

        :param min_iter: (optional) minimum number of learning iterations
        :param min_step: (optional) minimum data log-likelihood improvement,
                 over the latest min_iter iterations,
                 for learning iterations to continue.
        :param max_iter: (optional) maximum number of iterations, regardless of result.
        :param max_hours = (optional) maximal allowed running time, regardless of result.
        :param max_minutes = (optional) maximal allowed running time, regardless of result.
        :param callback: (optional) function to be called after each iteration step.
            If callable, called as callback(self, log_prob)
            where log_prob == scalar last achieved value of VI log-likelihood lower bound
        :return: log_prob = list of log-likelihood values, one for each iteration.

        Result: updated all properties of
        self.groups[...].pop_gmm properties comp, mix_weight
        self.groups[...].participants[...].xi = parameter sample array
        """
        if max_hours == 0. and max_minutes == 0.:
            max_minutes = 30.
        logger.info('Learning the model. Might take some time! '
                    + f'Max {max_hours:.0f} hours + {max_minutes:.0f} minutes.')
        min_iter = np.max([min_iter, 1])
        end_time = dt.datetime.now() + dt.timedelta(hours=max_hours,
                                                    minutes=max_minutes)
        # = last allowed time to start new VI iteration
        log_prob = []
        while (len(log_prob) <= min_iter
               or (log_prob[-1] - log_prob[-1 - min_iter] > min_step
                   and (len(log_prob) < max_iter)
                   and (dt.datetime.now() < end_time))):
            log_prob.append(self.adapt())
            if callable(callback):
                callback(self, log_prob[-1])
            logger.info(f'Done {len(log_prob)} iterations; data_LL = {log_prob[-1]:.2f}')
        if dt.datetime.now() >= end_time:
            logger.warning('Learning stopped at time limit, possibly not yet converged')
        if len(log_prob) >= max_iter:
            logger.warning('Learning stopped at max iterations, possibly not yet converged')
        return log_prob

    def prune(self, min_weight=JEFFREYS_CONC):
        """Prune model to keep only active profile clusters
        :param min_weight: scalar, smallest accepted value for sum individual weight
        :return: None
        Result: all groups pruned with same criterion
        """
        for (g_name, g_model) in self.groups.items():
            # logger.info(f'Pruning group {g_name}:')
            g_model.prune(g_name, min_weight)

    def adapt(self):
        """One VI adaptation step for all groups
        :return: ll = scalar VI lower bound to data log-likelihood,
            incl. negative contributions for parameter KLdiv re priors
        """
        return sum(g_model.adapt(g_name)
                   for (g_name, g_model) in self.groups.items())

    def gen_population_models(self, gf):  # *** new in v.1.1.0
        """Generator of all population models that matches requested group_factor(s)
        :param gf: tuple with one or more group "dimension" labels, as defined in self.base.emf
        :return: iterator yielding tuples (g_label, g_model), where
            g_label = tuple of group category labels, one for each given "dimension"
                in the order as given in gf
            g_model = an ema_group.PopulationModel instance for the corresponding subpopulation, OR
                an ema_group.EmaGroupModel (incl. participants).

        NOTE: IF gf does not include ALL group "dimension" defined in current EmaFrame,
        g_model is a weighed average across models in all OTHER "dimensions".
        """
        for g_label in self.base.emf.gen_population_keys_in_factor(gf):
            g_keys = list(self.base.emf.gen_matching_group_keys(dict(zip(gf, g_label))
                                                                ))
            # = key tuples with order as used in self.groups.keys()
            g_keys = list(filter(lambda gk: gk in self.groups.keys(), g_keys))
            # filtered, because some of the possible group categories may not exist
            if len(g_keys) == 1:
                yield g_label, self.groups[g_keys[0]]  # no merging needed
                # NOTE: complete ema_group.EmaGroupModel instance, including all Participants
            elif len(g_keys) > 1:
                g_weights = self.base.emf.population_model_weights(g_keys)
                # len(g_weights) == len(g_keys)
                g_models = [self.groups[g_k].pop_gmm for g_k in g_keys]
                # NOTE: only ema_group.PopulationMddel instances, without Participants
                yield g_label, PopulationModel.merge(g_models, g_weights)
            # else StopIteration automatically


# ------------------------------------------------- TEST:
# if __name__ == '__main__':
