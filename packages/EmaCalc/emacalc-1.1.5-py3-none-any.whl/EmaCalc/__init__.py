"""This package implements a Bayesian probabilistic model for
analysis of Ecological Momentary Assessment (EMA) data.

EMA methodology is used, for example,
to evaluate the effect of any kind of psycho-social-medical intervention,
for example, the subjective performance of hearing aids or other equipment,
in the everyday life of the user or client.

For example, in an EMA study including hearing-aid users,
the participants might be asked to report, at random occasions in their daily life,
which type of activity they are currently engaged in,
or in which type of situation they are currently using their hearing aids.

The participants may also be asked to grade the performance of their current hearing aids,
for one or more perceptual Attributes, e.g., Speech Understanding and/or Sound Comfort.

Thus, EMA records usually include both NOMINAL and ORDINAL data.
Typically, many EMA records are collected from each participant,
but the number of records may vary a lot among respondents.

*** Template scripts:
run_ema.py
run_sim.py

*** Main Modules:
ema_data: defines classes EmaFrame, EmaDataSet, with read / write functions for EMA data,
    and some functions to show the distribution of raw data.

ema_model: defines class EmaModel as a probabilistic model for EMA data
    and a variational learning algorithm for all model parameters.

ema_group: defines class EmaGroupModel defining probabilistic model for
    ONE population and a group of EMA respondents recruited from that population.

ema_respondent: defines class EmaRespondentModel including recorded data and parameters
    for ONE EMA respondent.

ema_display: classes and functions to display analysis results

ema_display_format: functions formatting plots and tables with analysis results

ema_base: defines help class EmaParamBase defining internal properties and methods
    for accessing all model parameters.

*** Reference:
A Leijon, Petra von Gablenz, Inga Holube, Jalil Taghia and Karolina Smeds (2023):
Bayesian Analysis of Ecological Momentary Assessment (EMA) Data Collected in Adults
Before and After Hearing Rehabilitation.
Frontiers in Digital Health, 5(1100705). doi: 10.3389/fdgth.2023.1100705

*** Version History:
* Version 1.1.5:
2025-05-23, Bugfix in ema_data._check_required_columns, _match_string_label.
            Extended user-friendly checks for typos.

* Version 1.1.3 == 1.1.4:
2025-03-21, new module ema_repr: ema_base.EmaRepr(reprlib.Repr) for pretty-printing repr()
            requires Python >= 3.12.
2025-03-18, Minor bug fix in ema_simulation.
            User-friendly checks for minor typos in input parameters.

* Version 1.1.2:
2024-06-27, Clarified Situation-profile plot labels, table headings, and file names.
            Generate difference tables for both PRIMARY and SECONDARY situation dimensions.

* Version 1.1.1:
2024-02-13, minor bug fix

* Version 1.1.0:
2024-02-04, allow population estimates to be displayed within any selected group dimension(s),
            averaged across other group dimension(s).
2024-01-30, credible differences only between categories in SECONDARY situation dimension(s),
            within each category plotted on x-axis, if more than one situation dimensions.

* Version 1.0.2:
2023-09-10, bugfix in ema_display.py. Update for Pandas groupby with version >= 2.1.

* Version 1.0.1:
2023-06-09, modified modules ema_thresholds and ema_latent to avoid numerical error in some extreme cases,
            and minor related changes in ema_simulation.

* Version 1.0.0:
2023-05-17, EmaModel.initialize(...) using n_participants_per_comp instead of max_n_comp.
2023-04-23, Respondent group specifications moved to ema_data.EmaFrame.
            EmaDataSet.load() signature changed: can find group category(-ies) in file path.
            EmaDataSet.save() signature changed: can save data in one single file,
                or in separate files, by group and / or participant

* Version 0.9.6:
Include range percentile plots and tables by groups, to show group differences

* Version 0.9.5:
Show observed and model-predicted attribute grade-counts,
    as requested by one reviewer of Frontiers (2023) paper.

Changed ema_base parameter extraction -> n_parameters == model degrees of freedom,
i.e., NO redundant model parameters.
This leads to a slight change of arbitrary scale zero point:
    If restrict_thresholds == True: one middle response threshold always forced -> zero,
    even for odd number of response categories.
    (Previous versions: mid-point of middle interval -> zero, if odd number of categories.)

Allow user to set number of samples for calculating population result displays.

* Version 0.9.4:
ema_display_format: Fixed filename bug that caused crash when running under Windows

* Version 0.9.3:
Ordinal rating scale may be tied to more than one Attribute.
changed names scenario -> situation,
'subject' -> 'participant',
'population_individual' -> 'random_individual'

* Version 0.9.2:
ema_data: improved optional overview of input data
ema_base: fixed numerical underflow problem in case of extreme response patterns.

* Version 0.9.1: Using Pandas DataFrame storage for input data, and all table results

* Version 0.8.3: changed ema_group classes to avoid unnecessary data transfer to Pool multi-processes

* Version 0.8.2: allow use multiprocessing.Pool for subjects in parallel

* Version 0.8.1: separate complete GMM for each group model,
    with mixture weights and components implemented in ema_group.EmaGroupModel

* Version 0.8: Improved variational approximation, less factorized,
    using joint q(xi_n, zeta_n) for EmaRespondentModel

* Version 0.7.2: Separate random Generators for each EmaRespondentModel

* Version 0.7.1: Minor updates:
    Allow seed for random generators, for reproducible numerical results
    Improved user control of simulated experiment, see script run_sim
    Minor change to ema_model.EmaRespondentModel.adapt_xi method

* Version 0.7:
2021-12-20, allow display of NAP effect measure of Attribute-Rating differences for
    individual participants, with point estimates and confidence intervals.
2021-12-17, display aggregated Attribute effects weighted by Scenario probabilities
2021-12-15, ema_model.EmaRespondentModel calculates individual Average Attribute Ratings, if desired.

* Version 0.6:
2021-12-08, allow user control of model restriction:
            restrict_attribute: sensory-variable location average forced -> 0.
            restrict_threshold: response-threshold median forced -> 0.

* Version 0.5.1: Minor update:
2021-11-25, allow EMA study with NO Attributes, i.e., ONLY Scenario probability profile(s)
2021-12-02, Minor fix: Attribute location == 0 given FIRST Scenario category
            regardless of regression_effect specification. (NO GOOD! Changed in v. 0.6)

* Version 0.5:
2021-10-12, Crude version, based on CountProfileCalc-2021, and PairedCompCalc (on PyPi),
2021-11-24, Functional beta version tested with simulated and (some) real data.
"""
__name__ = 'EmaCalc'
__version__ = '1.1.5'

__all__ = ['__version__', 'run_ema', 'run_sim']
