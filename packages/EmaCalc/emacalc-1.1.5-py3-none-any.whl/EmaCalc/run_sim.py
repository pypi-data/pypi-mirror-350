"""This script simulates an Ecological Momentary Assessment (EMA) study.
Collects all simulated EMA records in files,
as if the data had been gathered in a real experiment,
and runs the analysis.

A simulated experiment may include
one or more Groups of participants randomly drawn from separate Population(s),
with each participant performing several simulated EMA recordings.
Each EMA record includes
(1) a nominal SITUATION, specified in one or more Situation Dimensions,
(2) ordinal ratings of zero, one or more perceptual ATTRIBUTE(s).


*** Usage:
For first demo: Just run this script and look at the generated data files and the results.
NOTE: This simulated experiment is NOT a serious example of a real study.
It was designed mainly to illustrate some possibilities of the EmaCalc package.

For planning an EMA study:
Copy and edit this script and run it for any desired simulation.

Given some anticipated true effect-sizes in the population characteristics,
the simulation will indicate whether these effects can be reliably demonstrated
in a planned study, given the limited number of participants,
and the limited number of EMA recordings by each participant.


*** Version history:
* Version 1.1.0:
2024-02-04, New argument for EmaDisplay.show(..., group_factors=[...],...),
            to show population differences within SELECTED subset of group "dimensions".
            New argument to EmaFrame.setup(..., population_weights)
            defining relative weights to merge population results across OTHER group "dimensions".
2024-01-30, new format arguments in EmaDisplay.show(...) for user control of plot styles.

* Version 1.0.0:
2023-05-17, EmaModel.initialize(..., n_participants_per_comp, ...) defines initial number of GMM components.
            Parameter max_n_comp no longer used.
2023-04-23, Adapted to simplified group-key representation in ema_data.EmaFrame.
            NOTE: changed signatures EmaFrame.setup(), EmaDataSet.load(), and .save().

* Version 0.9.3:
2022-08-17, minor cleanup adapting to minor changes in some package modules.

* Version 0.9.1:
2022-04-04, all result tables generated and saved as Pandas DataFrame instances
2022-03-27, NAP and mean-grades results directly from raw data in ema_data.EmaDataSet
2022-03-21, using Pandas DataFrame format in EmaDataSet, allowing many input file formats

* Version 0.7.1:
2022-01-19, allow set_random_seed for exactly reproducible results

* Version 0.7: minor update to include new calculation and display functions

* Version 0.6:
2021-12-08, tested methods for restrict_attribute, restrict_threshold

* Version 0.5:
2021-11-16, first functional version
2021-11-21, cleaned and tested beta version
"""
# -------- __main__ check to prevent multiprocessor sub-tasks to re-run this script
if __name__ == '__main__':
    import numpy as np
    from pathlib import Path
    import logging
    import datetime as dt
    import pickle

    from EmaCalc.ema_simulation import EmaSimPopulation, EmaSimExperiment
    from EmaCalc.ema_simulation import SubjectThurstone, SubjectBradley

    from EmaCalc.ema_data import EmaFrame, EmaDataSet
    from EmaCalc.ema_model import EmaModel
    from EmaCalc.ema_display import EmaDisplaySet
    from EmaCalc import ema_logging, __version__
    from EmaCalc.ema_display_format import harmonize_ylim

    # ------------ (optional) Set simulator random seed for reproducible data generation
    # from EmaCalc.ema_simulation import set_sim_seed
    # set_sim_seed(12345)  # for reproducible results. ONLY FOR TEST OR DEMO

    # ------------------------ Set up working directory and result logging:
    # timestamp_result = True  # New result folder for each run, to prevent over-writing
    timestamp_result = False  # Repeated runs will over-write existing results

    work_path = Path.home() / 'Documents' / 'EMA_sim'  # or whatever...
    data_path = work_path / 'data'  # or whatever
    result_path = work_path / 'result'  # or whatever

    model_file = 'test_ema_model.pkl'  # saved model file
    experiment_file = 'test_ema_experiment.pkl'  # saved EmaSimExperiment

    if timestamp_result:
        t = dt.datetime.now()
        result_path = result_path.with_name(result_path.name +
                                            f'-{t.year}-{t.month:02}-{t.day:02}-{t.hour:02}{t.minute:02}')

    ema_logging.setup(save_path=result_path,
                      log_file='run_sim_log.txt')  # to save the log file

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    logger.info(f'*** Running EmaCalc version {__version__} ***')

    # ------ 1: Define Experimental Framework: Situations, Attributes, and Groups

    emf = EmaFrame.setup(situations={'Phase': ('',),  # Test phase(s), only one unlabelled
                                     'HA': ('A', 'B'),  # two Hearing-aid programs
                                     'CoSS': [f'C{i}' for i in range(1, 8)],  # Seven CoSS categories
                                     },
                         phase_key='Phase',
                         attributes={'Speech': ['Very Hard',
                                                'Hard',
                                                'Easy',
                                                'Very Easy',
                                                'Perfect'],
                                     'Comfort': ['Bad',
                                                 'Not Good',
                                                 'Not Bad',
                                                 'Good']},
                         groups = {'Age': ['young', 'old'],
                                   'Gender': ['F', 'M'],
                                   },   # -> FOUR distinct possible populations / groups
                         population_weights={('old', 'M'): 2.,
                                             ('old', 'F'): 2.,
                                             }  # default = 1. for other populations
                         )
    # NOTE: situations and attributes and group keys and category labels will be parts of result file names,
    # so they can include only characters allowed in file names.

    # NOTE: situations and attributes are always analyzed as Categorical variables,
    # even if the categories / grades are defined by numeric values.
    # The rank order of attribute grades is defined by the order as listed here, from worst to best,
    # not by, e.g., alphabetical or numerical order of the grade labels.

    # NOTE: if EQUAL grades are used for more than one attribute,
    # the model still assumes separate rating scales for each attribute.
    # However, if grade sequences are IDENTICAL objects for more than one attribute,
    # the model uses the SAME rating scale for those attributes.

    # Response thresholds are always estimated separately for each participant.

    # NOTE: population_weights are needed only if results are to be shown separately
    # for only one or a few of Group Dimensions, averaging across categories in other Group Dimensions.
    # In this example, we define population Age = old to be twice as large as Age = young,
    # both for Gender = M and Gender = F.
    # Each element of population_weights must specify one category in each predefined Group Dimension.

    # --------------- Define Population(s) to be simulated:

    # Not necessarily normalized probability-mass arrays
    pop0_situation_prob = np.ones((2, 7))  # with HA = A, B

    # pop0_situation_prob.shape == emf.situation_shape
    # OR == emf.situation_shape[1:] if emf.situation_shape[0] == 1, i.e., only one phase

    # --------- Population mean for Attribute 'Speech', in subject_class scale units

    pop0_speech_mean = np.array([[0., 0., 0., 0., 0., 0., 0.],     # with 'HA' = 'A'
                                 [3., 3., 3., 0., -3., -3., -3]])  # with 'HA' = 'B'
    pop0_speech_mean[1] += 0.5  # add mean difference between HA (B - A)
    pop0_comfort_mean = pop0_speech_mean[[1, 0], :]  # opposite pattern to 'Speech'

    pop_0 = EmaSimPopulation(emf,
                             situation_prob=pop0_situation_prob,
                             attribute_mean={'Speech': pop0_speech_mean,
                                             'Comfort': pop0_comfort_mean},
                             log_situation_std=0.,  # inter-individual standard deviation of log prob
                             attribute_std=1.0,  # inter-individual standard deviation of attribute locations
                             response_width_mean=1.5,  # response interval width in subject_class units
                             log_response_width_std=0.3,  # inter-individual random threshold variations
                             # subject_class=SubjectBradley,  # default, logistic latent variable
                             id='Pop0'
                             )
    # Optionally, define other populations here,
    pop1_situation_prob = pop0_situation_prob
    pop1_speech_mean = np.array([[0., 0., 0., 0., 0., 0., 0.],     # with 'HA' = 'A'
                                 [0., 0., 0., 0., 0., 0., 0.]])  # with 'HA' = 'B'
    pop1_speech_mean[0] -= 1.  # add fixed difference between HA (B - A)
    pop1_speech_mean[1] += 1.  # add fixed difference between HA (B - A)
    pop1_comfort_mean = pop1_speech_mean[[1, 0], :]  # opposite pattern to 'Speech'
    # pop1_comfort_mean = pop0_comfort_mean  # SAME as pop0
    pop_1 = EmaSimPopulation(emf,
                             situation_prob=pop1_situation_prob,
                             attribute_mean={'Speech': pop1_speech_mean,
                                             'Comfort': pop1_comfort_mean},
                             log_situation_std=0.,  # inter-individual standard deviation of log prob
                             attribute_std=0.5,  # inter-individual standard deviation of attribute traits
                             response_width_mean=1.5,  # response interval width in subject_class units
                             log_response_width_std=0.3,  # inter-individual random threshold variations
                             # subject_class=SubjectBradley,  # default
                             id='Pop1'
                             )
    # with SAME EmaFrame, but different situation_prob and/or mean Attribute values

    # ------------------ Generate Experiment with one Group of participants sampled from each Population:
    ema_exp = EmaSimExperiment(emf,
                               groups={('old', 'F'): pop_0.gen_group(n_participants=10),
                                       ('young', 'F'): pop_1.gen_group(n_participants=20),
                                       ('old', 'M'): pop_0.gen_group(n_participants=10),
                                       # ('young', 'M'): pop_1.gen_group(n_participants=15)
                                       })  # Example: Same true population properties for both 'Gender' categories.
    # NOTE: each group keys MUST be a tuple of one category from each group dimension,
    # as defined in EmaFrame.setup().
    # However, the experiment might include fewer groups than all possible ones.
    # In this example, the potential group ('young', 'M') was arbitrarily omitted from the simulated experiment.
    # Simulated data are generated only for THREE participant groups, although there are FOUR true populations.
    # Of course, this makes the data set un-balanced, NOT recommended for a real study.

    logger.info(f'ema_exp= {ema_exp}')
    # ema_exp defines TRUE parameter values for Population(s) and all participants in each Group

    # -------- (Optional) Save EmaSimExperiment instance with true parameter values
    data_path.mkdir(parents=True, exist_ok=True)
    with (data_path / experiment_file).open('wb') as f:
        pickle.dump(ema_exp, f)
    logging.info(ema_exp.__class__.__name__ + ' saved to file ' + str(data_path / experiment_file))

    # ------------------------- Generate EMA data for all participants in all Groups:

    ds = ema_exp.gen_dataset(min_ema=30,    # min n of EMA records per participant
                             max_ema=70)    # max n of EMA records per participant
    # = a complete EmaDataSet instance with simulated EMA records for all participants

    # Optionally, save all data in a directory tree with data files
    file_format = 'csv'  # 'xlsx', or other format that Pandas can handle
    ds.save(data_path, fmt=file_format,
            # join_groups=False,    # default: groups in separate directories
            # join_groups=True,     # One large file for all simulated participants.
            # participant='file',   # default: one separate file for each participant
            # participant='ID',     # name of column for participant ID, needed if several in one file
            allow_over_write=True   # default: new simulation run -> same file names
            )
    logging.info('Simulated EMA data saved in ' + str(data_path) + f' as {file_format} file(s)')

    # ----------------- (Optional) show mean grades and NAP results for all participants

    mean_grades = ds.attribute_grade_mean(groupby=('HA', 'CoSS'))
    mean_grades.save(result_path / 'Attribute_mean_grades.txt', float_format='%.2f')
    # mean_grades.save(result_path / 'Attribute_mean_grades.csv')  # for input to other analysis
    logger.info(f'Attribute_mean_grades saved in {result_path}')

    # nap = ds.nap_table(sit='HA', nap_cat=['A', 'B'], groupby=('CoSS',))  # grouped results
    nap = ds.nap_table(sit='HA', nap_cat=['A', 'B'], p=0.95)  # overall, all CoSS categories
    # high NAP>0.5 means B is better than A
    # default aggregated across other situation dimensions
    nap_file = 'NAP_HA_B-A'
    nap.save(result_path / (nap_file + '.txt'), float_format='%.2f')  # pretty-formatted by Pandas
    # nap.save(result_path / (nap_file + '.tex'), float_format='%.2f')  # for import to LaTeX doc.
    # nap.save(result_path / (nap_file + '.csv'), sep='\t')  # tab-delimited text, for input to other program
    # nap.save(result_path / (nap_file + '.xlsx'))  # for further Excel analysis
    logger.info(f'NAP results saved in {result_path}')

    # ------------------------------- Learn Analysis Model from simulated data set:

    # -------- (Test) re-loading simulated data from saved files (optional):
    logging.info('Simulated EMA data re-loaded from ' + str(data_path) + f' as {file_format} files')
    ds = EmaDataSet.load(emf, data_path, fmt=file_format,
                         participant='file',  # file name -> participant ID;
                         # participant='ID',  # Column Header in each file
                         path_groups=['Age', 'Gender'], # groups defined in path string
                         # path_groups=None,    # One data column for each Group Dimension
                         )
    # NOTE: path_groups are used only for Group Dimensions that are NOT specified in a data column.
    # In this example, directory paths include substrings like 'Age_old', 'Gender_M', etc.

    logger.info(f'Using data ds=\n{ds}')

    # Model ordinal-regression effects of situations on each Attribute:
    # regression_effects = ['HA',     # main linear regression effect only
    #                       'CoSS',   # main linear regression effect only
    #                       # 'Phase',  # if there are several phase categories
    #                       ]
    regression_effects = [('HA', 'CoSS')  # joint effects, main AND interaction
                          # 'Phase',  # if there are several phase categories
                          ]
    # NOTE: A regression_effects element may include any combination of situation dimensions, BUT
    # including ALL interactions -> many model parameters,
    # possibly -> less reliable estimation for each parameter.

    # In this example: ['HA', 'CoSS'] -> 2 + (7 - 1) = 8 regression-effect parameters
    #                ['CoSS', 'HA'] -> 7 + (2 - 1) = 8 regression-effect parameters
    #                [('HA', 'CoSS')] -> 2 * 7 = 14 regression-effect parameters

    emm = EmaModel.initialize(ds, effects=regression_effects,
                              # n_participants_per_comp=10,   # default
                              # restrict_attribute=False,     # default
                              # restrict_threshold=True,      # default
                              # latent_class='logistic',      # default
                              )
    # n_participants_per_comp = initial number of participants per mixture component in population model
    # restrict_attribute=True -> force attribute mean location at zero
    # restrict_threshold=True -> force one mid-scale response threshold at zero
    #   for each respondent and each sample of each attribute.
    # latent_class = 'logistic' ("logit" model) OR 'normal' ("probit" model)

    ll = emm.learn(max_hours=2., max_minutes=0.)
    logger.info(f'*** Data log-likelihood = {ll[-1]:.1f}, indicating model fit to data. ***')
    # *** Recommend re-run model learning with same data set a couple of times, use best-fitting model result.

    emm.prune()  # keep only active mixture components

    # -------- Save learned EmaModel instance (optional):
    with (work_path / model_file).open('wb') as f:
        pickle.dump(emm, f)

    # ------------------------------- generate all result displays:

    emd = EmaDisplaySet.show(emm,
                             situations=['CoSS',  # CoSS probabilities, aggregated across HA
                                         ('CoSS', 'HA'),  # CoSS probabilities, conditional on HA
                                         ('HA', 'CoSS'),  # HA probabilities, conditional on CoSS
                                         ],
                             attributes=[('Speech', 'CoSS'),    # Speech, main effect of CoSS
                                         ('Speech', 'HA'),      # Speech, main effect of HA
                                         ('Speech', ('CoSS', 'HA')),    # joint effect of both
                                         ('Comfort', ('CoSS', 'HA'))],  # joint effect of both
                             grade_counts=['Speech',  # total 'Speech' grade-counts, sum across HA and CoSS
                                           ('Speech', 'HA'),    # 'Speech' grade-counts, separated by HA
                                           ('Comfort', 'HA')],
                             group_factors=['Age', 'Gender',
                                            ('Age', 'Gender')],
                             # -> main effects in Dimensions 'Age', 'Gender', and in both combined
                             random_individual=True,    # random individual in population
                             population_mean=True,      # population mean
                             participants=False,        # individual results: True -> MANY plots and tables
                             grade_thresholds=True,     # True -> median response thresholds in attribute plots
                             percentiles=[2.5, 25, 50, 75, 97.5],   # in profile plots and tables
                             credibility_limit=0.7,     # minimum credibility in difference tables
                             mpl_params={'figure.max_open_warning': 0,  # suppress warning
                                         'figure.autolayout': True,    # -> tight layout
                                         'axes.labelsize': 'x-large'},  # -> matplotlib.rcParam
                             # mpl_style='my_style_sheet',
                             # ... any other ema_display.FMT or ema_display_format.FMT settings
                             )
    # NOTE: joint (=interaction) effects are correct only if included in EmaModel regression effects

    # ------------------------------- (optionally) edit display elements, if desired
    for gf in emd.group_factors.values():
        for g_disp in gf.groups.values():
            harmonize_ylim([g_disp.population_mean.attributes[('Speech', ('CoSS', 'HA'))].plot.ax,
                            g_disp.random_individual.attributes[('Speech', ('CoSS', 'HA'))].plot.ax,
                            g_disp.population_mean.attributes[('Comfort', ('CoSS', 'HA'))].plot.ax,
                            g_disp.random_individual.attributes[('Comfort', ('CoSS', 'HA'))].plot.ax
                            ])
            harmonize_ylim([g_disp.population_mean.situations[('CoSS', 'HA')].plot.ax,
                            g_disp.random_individual.situations[('CoSS', 'HA')].plot.ax,
                            ])

    # ------------------------------- save all result displays
    emd.save(result_path,
             figure_format='pdf',
             table_format='txt',
             float_format='%.2f')

    # (optionally) save in other format(s), too:
    # emd.save(result_path,
    #          table_format='xlsx',  # for input to other package
    #          float_format='%.4f',  # any other parameters for Pandas table-writer function
    #          index=True,   # needed by Pandas.to_excel in some cases
    #          )
    # emd.save(result_path,
    #          table_format='csv',  # for input to other package
    #          float_format='%.4f',  # any other parameters for Pandas table-writer function
    #          sep='\t'  # -> tab-delimited
    #          )

    logging.info(f'All result displays saved in {result_path}')

    logging.shutdown()
