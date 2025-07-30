"""This module defines classes to access and store recorded EMA data,
and methods and functions to read and write such data.

Each EMA Record includes nominal and ordinal elements, defining
* a participant ID label,
* a SITUATION specified by nominal category in ONE or MORE Situation Dimension(s),
* ordinal RATING(s) for ZERO, ONE, or MORE perceptual ATTRIBUTE(s) in the current situation.
* (optionally) group category label(s) for this participant

*** Class Overview:

EmaFrame: defines study layout and category labels of data in each EMA Record.
    EmaFrame properties can also define selection criteria
    for a subset of data to be included for analysis.

EmaDataSet: container of all EMA data to be used as input for statistical analysis.

*** File Formats:

Data may be stored in various table-style file formats allowed by package pandas,
e.g., xlsx, csv, odt, etc.
Each data file may include EMA records from ONE or SEVERAL participants,
from ONE or SEVERAL groups.

The participant id may be stored in a designated column of the table,
or the file name may be used as participant id,
or (in Excel-type files) the participant may be identified by the sheet name.

Group category(-ies) may be defined in table column(s),
OR defined by sub-string(s) in the absolute path for each file.

A collected EMA data set can be saved in various file formats, similar to input files.

*** Input Data Files:

All input files from an experiment must be stored in ONE directory tree.

If a group dimension is specified by the file path, the path must include a sub-string
combining the group dimension and ONE allowed category,
for example, 'Age_old', if the group dimension 'Age' has allowed categories 'young' and 'old'.

Each participant in the same group MUST have a unique participant ID.

Different files may include data for the same participant,
e.g., results obtained in different test phases,
or simply for additional sets of EMA records from the same participant.

Participants in different groups may have the same participant ID labels,
because the groups are separated anyway,
but normally the participant IDs should be unique across all groups.

*** Example Directory Tree:

Assume we have data files in the following directory structure:
~/ema_study / Age_old / Gender_male, containing files Test_EMA_64.xlsx and Response_Data_LAB_64.xlsx
    with data to be analyzed for group key= ('old', 'male') in group dimensions ('Age', 'Gender').
~/ema_study / Age_old / Gender_female, containing files Test_EMA_64.xlsx and Data_EMA_65.xlsx
~/ema_study / Age_young / Gender_male,  containing files Test_EMA_64.xlsx and EMA_65.xlsx
~/ema_study / Age_young / Gender_female, containing files Test_EMA_64.xlsx and EMA_65.xlsx

Four separate groups may then be defined by dimensions 'Age' and 'Gender',
and the analysis may be restricted to only use data in files with names including 'EMA_64'.

*** Accessing Input Data for Analysis:
*1: Create an EmaFrame object defining the experimental layout, e.g., as:

emf = EmaFrame.setup(situations={'CoSS': [f'C{i}' for i in range(1, 8)],
                                 'Important': ('Slightly', 'Medium', 'Very'),
                                 },  # nominal variables
                     attributes={'Speech': ('Very Hard', 'Fairly Hard', 'Fairly Easy','Very Easy')},
                     groups={'Age': ('young', 'old'),
                             'Gender': ('female', 'male'),
                             'Test': ('EMA_64',)},
        )
NOTE: String CASE is always distinctive, i.e., 'Male' and 'male' are DIFFERENT categories.

*2: Load all test results into an EmaDataSet object:

ds = EmaDataSet.load(emf, path='~/ema_study',
                    fmt='xlsx',
                    participant='sheet',  # xlsx sheet title is used as participant ID
                    path_groups=['Age', 'Gender', 'Test']  # group dimensions identified by file path
                    )
The parameter emf is an EmaFrame object that defines all variables to be analyzed,
and the other arguments specify where these variables are to be found.

The resulting data set includes exactly FOUR combinations of 'Age' and 'Gender',
with an extra dimension 'Test' that has only one allowed category.
The object ds can now be used as input for analysis.

*** Selecting Subsets of Data for Analysis:
It is possible to define a data set using only a subset of the data files in the given directory tree.
For example, assume we want to analyze only TWO groups, old males, and old females,
and only data from group dimension 'Test' with the single category 'EMA_64',
and only responses for Situation dimension 'CoSS'.

Then we must define a new EmaFrame object, and load only a subset of group data:

emf = EmaFrame.setup(situations={'CoSS': [f'C{i}' for i in range(1, 8)],
                                 },  # nominal variables
                     attributes={'Speech': ('Very Hard', 'Fairly Hard', 'Fairly Easy','Very Easy')},
                     groups={'Age': ('old',),
                             'Gender': ('female', 'male'),
                             'Test': ('EMA_64',)}
                    )
ds = EmaDataSet.load(emf, path='~/ema_study',
                    fmt='xlsx',
                    participant='sheet',
                    path_groups=['Age', 'Gender', 'Test'])

In case all input data have been collected in a single file in the data directory,
the file must include columns with header 'Age', 'Gender',
and one column for the participant ID, with header, e.g., 'Test Subject'.
Then the data may be accessed as

ds = EmaDataSet.load(emf, path='~/ema_study',
                    fmt='xlsx',
                    participant='Test Subject',  # column header
                    path_groups=['Test']  # read only file paths including 'Test_EMA_64'
                    )
This data set will include TWO groups named ('old', 'female', EMA_64), and ('old', 'male', EMA_64)


*** Version History:
* Version 1.1.5:
2025-05-22, bugfix in _check_required_columns, match_string_label, for user typing errors
            user-friendly input checks in EmaDataSet display methods

* Version 1.1.3:
2025-03-21, using ema_repr.EmaObject as superclass
2025-03-10, using difflib to check and correct user typing errors, when possible

* Version 1.1.1:
2024-02-13, new argument in EmaDataSet.attribute_grade_mean(..., fill_missing=False),
            True -> include missing row(s) filled with NaN.

* Version 1.1.0:
2024-02-04, new property EmaFrame.population_weights = dict with relative weights to be used
            to merge ema_group.PopulationModel instances across some group "dimensions"
2024-02-02, new EmaFrame methods: gen_population_keys_in_factor, gen_matching_group_keys, population_weights
            providing help for ema_group.PopulationModel.merge method

* Version 1.0.2:
2023-09-10, update for future Pandas groupby input default change

* Version 1.0.0:
2023-04-25, Group categories specified in EmaFrame.setup(...)
            EmaFrame.filter(...) does all data checking.
            EmaDataSet.load(...) allows group category in file path.
            EmaDataSet.save(...) can save separate group/participant files, or one big file.
            EmaDataSet.groups: keys include only group categories, NOT group "dimensions".

* Version 0.9.6:
2023-04-11, bugfix EmaDataSet.join_df, .attribute_count, .attribute_mean

* Version 0.9.4:
2022-11-06: Fix to avoid FutureWarning in EmaDataSet.attribute_grade_mean

* Version 0.9.3:
2022-08-22, EmaDataSet.load(), .save() safer for pandas read, in case empty phase_key
2022-08-16, changed EmaFrame.situations -> situation_dtypes
2022-08-16, changed EmaFrame.attribute_grades -> attribute_dtypes
2022-08-16, new EmaFrame.setup() method, for clarity, separate from __init__
2022-07-27, changed 'subject' -> 'participant'
2022-07-13, renamed EmaFrame.scenarios -> situations, and other methods consistently
2022-07-13, changed EmaDataSet method names: attribute_grade_count, attribute_grade_mean
2022-07-11, minor bugfix in EmaDataSet.attribute_grade_distribution

* Version 0.9.2:
2022-06-16, minor fix in EmaDataSet.mean_attribute_table, nap_table
2022-06-03, changed variable name stage -> phase everywhere
2022-05-21, clearer logger info for valid- and missing-data input

* Version 0.9:
2022-03-17, use Pandas CategoricalDtype instances in EmaFrame situation_dtypes and attributes
2022-03-18, use Pandas DataFrame format in EmaDataSet, to allow many input file formats

* Version 0.8.3:
2022-03-08, minor fix for FileReadError error message

* Version 0.8.1:
2021-02-27, fix EmaDataSet.load(), _gen_group_file_paths(), _groups(), for case NO groupby

* Version 0.5.1:
2021-11-26, EmaDataSet.load warning for input argument problems

* Version 0.5:
2021-10-15, first functional version
2021-11-18, groupby moved from EmaFrame -> EmaDataSet.load
2021-11-20, EmaDataSet.ensure_complete
2021-11-23, Group dir name MUST include both (g_factor, g_cat), e.g., 'Age_old'
2021-11-xx, allow empty attribute_grades
"""
# *** Future:
# *** EmaDataSet.initialize + add method ? load = initialize + add

import numpy as np
from pathlib import Path
import pandas as pd
from difflib import get_close_matches
# from collections import namedtuple
from itertools import product, chain
import logging

from EmaCalc.ema_repr import EmaObject
from EmaCalc.ema_file import ema_gen, Table, FileReadError, FileWriteError
from EmaCalc.ema_nap import nap_pandas

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


class EmaInputError(RuntimeError):
    """Any kind of user-input mismatch.
    """
# ******* separate UnknownLabelError, MisspelledLabelError ?

# ------------------------------------------------------------
# Help classes: Categorical Data Types used in EMA analysis.

# Category labels should preferably be (short) string literals,
# identical to the codes stored in EMA data records.
# Integer labels can also be used, but this can cause some ambiguity:
# Pandas.reader functions might re-interpret labels,
# e.g., string '3' might be read as the number 3.

class _EmaDtype(pd.CategoricalDtype):
    """Abstract superclass"""
    def __repr__(self):
        return self.__class__.__name__ + '('+ repr(list(self.categories.values)) + ')'


class NominalDtype(_EmaDtype):
    def __init__(self, cats):
        """
        :param cats: sequence of string (or integer) labels
        """
        super().__init__(categories=cats, ordered=False)


class OrdinalDtype(_EmaDtype):
    def __init__(self, grades):
        """
        :param grades: sequence of string (or integer) labels
            The "value" of an ordinal grade is determined
            ONLY by the given order, NOT by the sorting value of the grade label:
            With grades=['one', 'zero'], grade 'zero' is higher than grade 'one'
        """
        super().__init__(categories=grades, ordered=True)


# ------------------------------------------------------------
class EmaFrame(EmaObject):
    """Defines variable names and categories of all data elements
    to be analyzed in an EMA study.
    The allowed categories of each EMA variable is stored as a pd.CategoricalDtype instance.
    """
    def __init__(self, situation_dtypes, phase_key, ordinal_scales, attribute_scales,
                 group_dtypes, population_weights=None):
        """
        :param situation_dtypes: dict with elements (dimension, dtype), where
            dimension is a string label identifying one situation "dimension",
            dtype is a NominalDtype defining NOMINAL categories within this dimension.
        :param phase_key: situation key (dimension name) for the test phase,
            which MUST be the FIRST element of situation_dtypes.
        :param ordinal_scales: dict with elements (scale_id: dtype), where
            dtype is a CategoricalDtype defining ORDINAL categories for the scale.
        :param attribute_scales: dict with elements (attribute_key, scale_id), defining
            the scale used by each attribute.
            Note: Separate attributes may use the SAME ordinal scale,
                if so specified by the researcher.
        :param group_dtypes: dict with elements (dimension, dtype), where
            dimension is a string label identifying one grouping "dimension", e.g., 'Age'
            dtype is a NominalDtype defining NOMINAL categories within this dimension.
        :param population_weights: (optional) dict or iterable with elements (group_key, weight value)
            for relative weights of ema_group.PopulationModel instances in case they are merged for display.
            Weights are = 1. for populations that are not explicitly included.
        """
        self.situation_dtypes = situation_dtypes
        self.phase_key = phase_key
        self.ordinal_scales = ordinal_scales
        self.attribute_scales = attribute_scales
        self.group_dtypes = group_dtypes
        if population_weights is None:
            population_weights = dict()
        # ensure population_weights.keys() match with group_dtypes:
        pop_keys = [self.match_group_key(pop_k)
                    for pop_k in population_weights.keys()]
        for (pk_new, pk_old) in zip(pop_keys, population_weights.keys()):
            if pk_new != pk_old:
                population_weights[pk_new] = population_weights.pop(pk_old)
                logger.warning(f'Population key {pk_old} changed to {(pk_new,)}.')
        self.population_weights = population_weights

    # def __repr__(self):  # -> superclass
    #     return (self.__class__.__name__ + '(\n\t\t' +
    #             ',\n\t\t'.join(f'{key}={repr(v)}'
    #                            for (key, v) in vars(self).items()) +
    #             '\n\t\t)')

    @classmethod
    def setup(cls, situations=None, phase_key='Phase', attributes=None,
              groups=None, population_weights=None):
        """Create the EmaFrame object defining all EMA variables to be analyzed.
        :param situations: (optional) dict or iterable with elements (dimension, category_list), where
            dimension is a string label identifying one situation "dimension",
            category_list is an iterable of labels for NOMINAL categories within this dimension.
        :param attributes: (optional) dict or iterable with elements (attribute, grades),
            attribute is string id of a rated perceptual attribute,
            grades is an iterable with ORDINAL categories, strings or integer.
        :param phase_key: (optional) situation key for the test phase, with
            situation_dtypes[phase_key] = list of test phases (e.g., before vs after treatment),
                specified by experimenter, i.e., NOT given as an EMA response
            situation_dtypes[phase_key] is automatically added with a SINGLE value,
            if not already defined in given situation_dtypes.
        :param groups: (optional) dict or iterable with elements (dimension, category_list), where
            dimension is a string label identifying one grouping "dimension", e.g., 'Age' or 'Gender',
            category_list is an iterable of labels for NOMINAL categories within this dimension.
        :param population_weights: (optional) dict or iterable with elements (group_key, weight value)
            for relative weights of ema_group.PopulationModel instances in case they are merged for display.
            Weights are = 1. for populations that are not explicitly included.
        :return: cls instance

        NOTE: situation_dtypes and attribute_grades and groups may define a subset of
            data in input data files, if not all variants are to be analyzed.
            Categories MUST be specified EXACTLY as stored in data files,
            case-sensitive, i.e., 'A', and 'a' are different categories.

            If needed, the EmaDataSet.load(...) method allows
            argument 'converters' to pandas reader function,
            defining a dict with function(s) to make saved data fields agree with pre-defined categories.
            Column headers in the data files may also be re-named, if needed,
            as specified by argument rename_cols to the EmaDataSet.load(...) method.
        """
        if situations is None:
            situations = dict()
        else:
            situations = dict(situations)
        if phase_key not in situations.keys():
            situations[phase_key] = ('',)  # just a single category
        situations = dict((sit, NominalDtype(sit_cats))
                          for (sit, sit_cats) in situations.items())
        # re-order to ensure first situation key == self.phase_key:
        phase_dict = {phase_key: situations.pop(phase_key)}
        situations = phase_dict | situations  # **** requires python >= 3.9

        if attributes is None:
            attributes = dict()
        else:
            attributes = dict(attributes)
        # NOTE: some attributes.values() may be IDENTICAL objects, not only equal.
        ordinal_scales = {id(a_cats): OrdinalDtype(a_cats)
                          for (a, a_cats) in attributes.items()}
        # including only UNIQUE scales, each possibly tied to more than one attribute
        attribute_scales = dict((a, id(a_cats))
                                for (a, a_cats) in attributes.items())
        if groups is None:
            groups = dict()  # {'': ['']}  # Empty?, ONE un-named group with all participants
        groups = dict((g, NominalDtype(g_cats))
                      for (g, g_cats) in groups.items())
        return cls(situations, phase_key, ordinal_scales, attribute_scales,
                   group_dtypes=groups,
                   population_weights=population_weights)

    @property
    def tied_response_scales(self):
        """Some ordinal scale tied to more than one attribute scale"""
        return len(self.ordinal_scales) < len(self.attribute_scales)

    @property
    def attribute_dtypes(self):
        """Mapping attribute key -> dtype object
        :return: dict with elements (a_key, a_dtype),
            where a_dtype is a pd.CategoricalDtype object
        """
        return {a_key: self.ordinal_scales[scale_key]
                for (a_key, scale_key) in self.attribute_scales.items()}

    @property
    def scale_attributes(self):
        """Mapping scale key -> list of attributes sharing the same scale
        i.e., inverse to mapping self.attribute_scales
        :return: dict with elements (s_id, a_keys), such that
            self.ordinal_scales[s_id] is shared by all attributes in a_keys
        """
        return {s_id: [a_key for (a_key, a_scale) in self.attribute_scales.items()
                       if s_id == a_scale]
                for s_id in self.ordinal_scales.keys()}

    @property
    def dtypes(self):
        """
        :return: dict with ALL defined ema variables and their dtypes
        """
        return self.situation_dtypes | self.attribute_dtypes | self.group_dtypes

    @property
    def situation_shape(self):
        """tuple with number of nominal categories for each situation dimension"""
        return tuple(len(sit_dtype.categories)
                     for sit_dtype in self.situation_dtypes.values())

    @property
    def rating_shape(self):
        """tuple with number of ordinal response levels for each attribute
        """
        return tuple(len(r_cat.categories)
                     for r_cat in self.attribute_dtypes.values())

    @property
    def n_phases(self):
        # == situation_shape[0]
        return len(self.situation_dtypes[self.phase_key].categories)

    def group_head(self):
        return tuple(self.group_dtypes.keys())

    def gen_population_keys_in_factor(self, gf):
        """Generator all possible categories within requested group "dimensions"
        :param gf: tuple with one or more group "dimension" keys
        :return: iterator yielding tuples with group category labels, one for each given "dimension"
        """
        if len(self.group_dtypes) == 0:
            return [()]
        else:
            return product(*(self.group_dtypes[gf_k].categories for gf_k in gf))

    def gen_matching_group_keys(self, g_pattern):
        """Generate all possible group categories that match pattern g_label in gf
        :param g_pattern: dict defining ONE selected category for zero, one or more group "dimensions"
            if empty: generate ALL possible group categories
        :return: iterator yielding complete tuples of matching group categories
            in the order defined by self.group_head
        """
        if len(self.group_dtypes) == 0:
            return [()]
        g_keys = product(*([g_pattern[g_dim]] if g_dim in g_pattern.keys()
                           else self.group_dtypes[g_dim].categories
                           for g_dim in self.group_dtypes.keys()))
        return g_keys

    def population_model_weights(self, g_keys):
        """User-defined population weights for subset of population categories
        to be used for merging corresponding ema_group.PopulationModel instances
        :param g_keys: list of tuples, each defining ONE group category,
            i.e., with one category defined for each value in self.groups_dtypes.keys()
            in the correct order.
        :return: list with positive weight values, same length as g_keys
        """
        return np.array([self.population_weights[g] if g in self.population_weights else 1.
                      for g in g_keys])

    def required_vars(self):
        """List of all variable keys that must be specified by input data sets.
        :return:
        """
        return list(chain(self.situation_dtypes.keys(),
                          self.attribute_dtypes.keys(),
                          self.group_dtypes.keys()))

    def filter(self, ema, participant):
        """Check and filter EMA data for ONE participant, to ensure that
        it includes the required columns, with required data types.
        :param ema: a pd.DataFrame instance
        :param participant: a required column name
        :return: a pd.DataFrame instance with complete data
            or an empty DataFrame if no usable EMA records were found
        """
        # *** check and correct for Phase column here ? ***********
        required_col = self.required_vars() + [participant]
        required_dtypes = self.dtypes | {participant: object}
        _check_required_columns(required_col, ema.columns)
        try:
            ema = ema[required_col]
            ema = ema.astype(required_dtypes, errors='raise')
            # *** this accepts NaN, but sets NaN if cell contents not in defined categories ***
            # *** delete rows with NaN not needed? NaNs excluded anyway by DataFrame.value_counts()
        except KeyError as e:
            raise FileReadError(f'Some missing required data column(s). Error {e}')
        except ValueError as e:
            raise FileReadError(f'Incompatible data type. Error {e}')
        return ema

    def count_situations(self, ema):
        """Count EMA situation occurrences for analysis
        :param ema: np.DataFrame instance with all EMA records for ONE respondent,
            with columns including self.situation_dtypes.keys()
        :return: z = mD array with situation_counts
            z[k0, k1,...] = number of recordings in (k0, k1,...)-th situation category
            z.shape == self.situation_shape
        """
        # 2022-05-24, Arne Leijon: verified manually with input data
        z = ema.value_counts(subset=list(self.situation_dtypes.keys()), sort=False)
        # = pd.Series including only non-zero counts, indexed by situation or tuple(situation_dtypes)
        ind = pd.MultiIndex.from_product([sit_dtype.categories
                                          for sit_dtype in self.situation_dtypes.values()])
        z = z.reindex(index=ind, fill_value=0)
        # must reindex to include zero counts
        return np.array(z).reshape(self.situation_shape)

    def count_grades(self, a, ema):
        """Count grade occurrences for given attribute in a given DataFrame instance
        :param a: attribute key
        :param ema: pd.DataFrame instance with all EMA records for ONE respondent,
            with columns including all self.situation_dtypes.keys() and self.attribute_grade.keys()
        :return: y = 2D array with
            y[l, k] = number of responses at l-th ordinal level,
            given k-th <=> (k0, k1, ...)-th situation category
        """
        # 2022-05-24, verified manually with input data
        z = ema.value_counts(subset=[a] + list(self.situation_dtypes.keys()), sort=False)
        ind = pd.MultiIndex.from_product([self.attribute_dtypes[a].categories]
                                         + [sit_dtype.categories
                                            for sit_dtype in self.situation_dtypes.values()])
        z = z.reindex(index=ind, fill_value=0)
        return np.array(z).reshape((ind.levshape[0], -1))

    # ------------------------------------ correcting user typing errors:
    # NOTE: No warnings here, caller must warn if needed.
    def match_group_factor(self, g_factor):
        """Ensure that a tentative user-defined grouping factor (dimension)
        agrees with previous definition.
        :param g_factor: string label
        :return: g_factor_new <- g_factor corrected if needed and possible
        """
        return _match_string_label(g_factor, self.group_dtypes.keys(), 'group_factor')

    def match_group_key(self, g_key):
        """Ensure that a tentative user-defined group key
        is a tuple with group categories exactly matching definition in self.
        :param g_key: tuple (gc_1, ..., gc_K),
            with one selected category gc_i from each group factor in self.group_dtypes
        :return: g_new_key <- g_key corrected if needed and possible
        """
        if not isinstance(g_key, tuple):
            logger.warning(f'Group key {g_key} changed to {(g_key,)}. Must be a tuple.')
            g_key = (g_key,)
        if len(g_key) != len(self.group_dtypes):
            raise EmaInputError(f'group-key tuple must have {len(self.group_dtypes)} labels'
                                + ' to match EmaFrame.')
        g_new_key = tuple(_match_string_label(gk_i, g_cats_i.categories,
                                              'group category')
                          for (gk_i, g_cats_i) in zip(g_key,
                                                      self.group_dtypes.values()))
        return g_new_key

    def match_attribute_key(self, a_key):
        """Ensure that a tentative user-defined Attribute key
        agrees with previous definition.
        :param a_key: string label
        :return: a_key_new <- a_key corrected if needed and possible
        """
        return _match_string_label(a_key, self.attribute_dtypes.keys(), 'attribute')

    def match_situation_key(self, sit_key):
        """Ensure that a tentative user-defined Situation key (= dimension)
        agrees with previous definition.
        :param sit_key: string label
        :return: sit_key_new <- sit_key corrected if needed and possible
        """
        return _match_string_label(sit_key, self.situation_dtypes.keys(),
                                   'situation dimension')


# ------------------------------------------------------------
class EmaDataSet(EmaObject):
    """Container of all input data for one complete EMA study.
    """
    def __init__(self, emf, groups):
        """
        :param emf: an EmaFrame instance
        :param groups: dict with elements (group_id: group_dict), where
            group_id = tuple (g_cat_0, g_cat_1,...), identifying a population
                by one category selected for each group "dimension".
            group_dict = dict with elements (participant_id, ema_df), where
            ema_df = a pd.DataFrame instance with one column for each EMA variable,
            and one row for each EMA record.
            ema_df.shape == (n_records, n SITUATION dimensions + n ATTRIBUTES)
        """
        self.emf = emf
        self.groups = groups

    def rrepr(self, r, level):
        with pd.option_context('display.max_rows', 4,
                               'display.show_dimensions', False):
            return super().rrepr(r, level)

    def __repr__(self):  # ********** -> __str__ ? rrepr() ? *********
        def sum_n_records(g_participants):
            """Total number of EMA records across all participants in group"""
            return sum(len(s_ema) for s_ema in g_participants.values())
        # ---------------------------------------------------------------
        return (self.__class__.__name__ + '(\n\t'
                + f'emf= {self.emf},\n\t'
                + 'groups= {' + '\n\t\t'
                + '\n\t\t'.join((f'{g}: {len(g_participants)} participants '
                                 + f'with {sum_n_records(g_participants)} EMA records in total,')
                                for (g, g_participants) in self.groups.items())
                + '\n\t\t})')

    # *** separate classmethod initialize, method add; load = initialize + add ?
    # *** to allow collecting data from several sources, with different file formats...

    @classmethod
    def load(cls, emf, path, fmt=None,
             participant='file',
             path_groups=None,
             group_join_str='_',
             ema_vars=None, grouping=None,
             **kwargs):
        """Create one class instance with selected data from input file(s).
        :param emf: EmaFrame instance
        :param path: string or Path defining top of directory tree containing all data files.
            Files in all subdirectories are searched, hierarchically.
        :param fmt: (optional) string with file suffix for data files.
            If None, all files are tried, so files with mixed formats can be used as input.
        :param participant: string defining where to find participant ID in a file,
            = column name, 'file', or 'sheet' if excel-type file that has 'sheet's
        :param path_groups: (optional) list with group-dimension labels
            for group categories to be specified by substrings in file paths,
            used only IF NOT specified in a column in the data file.
        :param group_join_str: (optional) string between group dimension and category in file path,
            e.g., '_' in '... / Age_old / ...'
        :param ema_vars: *** only for version warning, no longer used
        :param grouping: *** only for version warning, no longer used
        :param kwargs: (optional) any additional arguments for pandas file_reader
            e.g., rename_cols={...},  converters={...}.
        :return: a single cls object

        NOTE: Situation categories and Attribute grades and group categories must agree with
            the categories previously defined in emf.
            If needed, use keyword argument
            converters={column_head: convert_fcn, ...} to pandas reader function
            with converter function(s) to make saved data fields agree with pre-defined categories.
            Use keyword argument
            rename_cols={old_head: new_head, ...} to change file column headers to desired names.
        """
        def clean_up(s_ema):
            """Remove unused group and participant columns, re-index EMA records
            :param s_ema: a pd.DataFrame for ONE participant, incl group and participant id columns
                with a single RangeIndex for EMA record number
            :return: copy of s_ema, with redundant info removed
            """
            index_cols = list(emf.group_head()) + [participant]
            drop_cols = [c for c in index_cols if c in s_ema.columns]  # avoid KeyError in drop()
            s_ema = s_ema.drop(columns=drop_cols)
            s_ema.index = pd.RangeIndex(range(s_ema.shape[0]))
            # because the original index was artificially created by concat
            return s_ema

        # ---------------------------------------------------------------
        if ema_vars is not None:  # backwards incompatibility
            logger.warning('EmaCalc v. > 0.9.0: argument ema_vars not used to select EMA variables. '
                           + 'Using file table header instead. \n'
                           + 'Change column names by "rename_cols" argument, if needed.')
        if grouping is not None:  # backwards incompatibility
            logger.warning('EmaCalc v. > 0.9.6: group categories are defined in EmaFrame.setup().'
                           +'\nDefine only "path_groups" here, for group dim.s specified by path string.')
        if fmt is not None and fmt[0] != '.':
            fmt = '.' + fmt
        path = Path(path)
        if path_groups is None:
            path_groups = []
        path_groups_corr = [emf.match_group_factor(g) for g in path_groups]  # correct spelling if needed
        if any(g_new != g_old for (g_new, g_old) in zip(path_groups_corr, path_groups)):
            logger.warning(f'*** path_groups {path_groups} changed to {path_groups_corr}')
            path_groups = path_groups_corr
        # **** up to here -> classmethod initialize
        # **** following: -> add method, to allow collecting data from different file formats ?

        # v 1.0.0: collect a list of ema chunks, then concat and separate by group and participant:
        all_ema = []  # container for all input EMA tables
        path_groups = {gf: emf.group_dtypes[gf].categories
                       for gf in emf.group_dtypes if gf in path_groups}
        # = dict with (gf, g_cats) for all gf that MAY be derived from file path.
        for (path_group_id, g_path) in _gen_group_file_paths(path, fmt, path_groups, group_join_str):
            # path_group_id = dict with element (group_key, group_cat) specified as g_path sub-strings
            logger.info(f'Path group {path_group_id}: Reading {g_path}')
            try:
                ema_file = ema_gen(g_path,
                                   participant=participant,
                                   **kwargs)
                for ema in ema_file:
                    # ema is a pd.DataFrame with a COPY of (possibly converted) data from file,
                    # for ONE or SEVERAL participants
                    # with one column name == participant.
                    for (g_factor, g_cat) in path_group_id.items():
                        if g_factor not in ema.columns:
                            ema[g_factor] = g_cat  # set group category derived from path sub-string
                    if emf.n_phases == 1:  # phase-code might be unspecified in file
                        # if file rows have phase as empty string, Pandas reads it as NaN!
                        if emf.phase_key not in ema.columns:
                            ema[emf.phase_key] = emf.situation_dtypes[emf.phase_key].categories[0]
                    ema = emf.filter(ema, participant)
                    # = pd.DataFrame with all required columns, and nothing else!
                    logger.info(f'EMA chunk with {ema.shape[0]} records. '
                                + ('Some missing data. Valid data count =\n'
                                   + _table_valid(ema) if np.any(ema.isna()) else ''))
                    if not ema.empty:
                        all_ema.append(ema)
            except FileReadError as e:
                logger.warning(e)  # and just try next file
        if len(all_ema) == 0:
            raise FileReadError('No EMA data found')
        else:
            all_ema = pd.concat(all_ema, axis=0, ignore_index=True)
        # store all data in structured dict instead: **** or just leave it as a single chunk ? ***
        if len(emf.group_dtypes) == 0:
            groups = {(): {s: clean_up(s_ema)
                           for (s, s_ema) in all_ema.groupby(participant)}
                      }
        else:
            groups = {g: {s: clean_up(s_ema)
                          for (s, s_ema) in g_ema.groupby(participant)}
                      for (g, g_ema) in all_ema.groupby(list(emf.group_dtypes.keys()),
                                                        observed=True)}
        return cls(emf, groups)

    # def add method, to include data from new files with different layout ???

    def save(self, path, fmt='.csv', allow_over_write=False,
             participant='file',
             join_groups=False,
             group_join_str='_',
             **kwargs):
        """Save all EMA data from self.groups, either
        as a single file with EMA records for all participants in all groups,
        OR in a directory tree for groups, with one file for each group,
        OR with one separate file for each participant.
        :param path: Path or string defining the top directory where files are saved
        :param allow_over_write: (optional) boolean switch
        :param fmt: (optional) file-name extension string specifying file format
        :param join_groups: (optional) boolean switch: True -> ONE file for all groups
        :param participant: (optional) string defining where to store participant ID,
            = column name, -> all participants in a group saved in ONE file
            or 'file' -> one file for each participant, with participant ID as file name
        :param group_join_str: (optional) string between group dimension and category in file path
        :param kwargs: (optional) arguments to Table.save() or selected pandas.to_xxx()
        :return: None
        """
        def drop_empty_phase(df):
            # if Phase column contains only empty strings, drop it, do NOT save it,
            # because Pandas might read it as NaN, not as empty string
            phase_key = self.emf.phase_key
            if self.emf.n_phases == 1 and all(df[phase_key] == ''):
                df = df.drop(columns=[phase_key], inplace=False)
            return df

        # --------------------------------------------------------------
        if fmt[0] != '.':
            fmt = '.' + fmt
        path = Path(path)
        if participant == 'file':
            if join_groups:
                join_groups = False
                logger.warning('Must have join_groups = False to save participants in separate files')
        try:
            if join_groups:  # AND participants
                groups = self.join_df(participant=participant)
                groups = drop_empty_phase(groups)
                f_name = group_join_str.join(emf.group_head())
                if len(f_name) == 0:
                    f_name = 'participants'
                else:
                    f_name += '_participants'
                f_path = (path / f_name).with_suffix(fmt)
                f_path.parent.mkdir(parents=True, exist_ok=True)
                Table(groups).save(f_path, allow_over_write, **kwargs)
            else:
                for (g, group_data) in self.groups.items():
                    g_dir = group_dir_str(self.emf.group_head(), g, sep=group_join_str)
                    # = group sub-path string, empty if single un-named group
                    g_path = path / g_dir
                    if participant == 'file':
                        g_path.mkdir(parents=True, exist_ok=True)
                        for (s_id, s_df) in group_data.items():
                            s_df = drop_empty_phase(s_df)
                            p = (g_path / str(s_id)).with_suffix(fmt)  # one file per participant
                            Table(s_df).save(p, allow_over_write, **kwargs)
                    else:
                        g_table = pd.concat(group_data, axis=0,
                                            ignore_index=False,
                                            sort=False,
                                            names=[participant]
                                            )
                        g_table = drop_empty_phase(g_table)
                        f_path = g_path.with_suffix(fmt)  # last dir level becomes the file
                        g_path.parent.mkdir(parents=True, exist_ok=True)
                        Table(g_table).save(f_path, allow_over_write, **kwargs)
        except FileWriteError as e:
            raise RuntimeError(f'Could not save {self.__class__.__name__} in {repr(fmt)} format. '
                               + f'Error: {e}')

    def ensure_complete(self):
        """Check that we have at least one participant in every group category,
        with at least one ema record for each participant (already checked in load method).
        :return: None

        Result:
        self.groups may be reduced:
        participants with no records are deleted,
        groups with no participants are deleted
        logger warnings for missing data.
        """
        for (g, g_participants) in self.groups.items():
            incomplete_participants = set(s for (s, s_ema) in g_participants.items()
                                      if s_ema.empty)
            for s in incomplete_participants:
                logger.warning(f'No EMA data for participant {repr(s)} in group {repr(g)}. Deleted!')
                del g_participants[s]
        incomplete_groups = set(g for (g, g_participants) in self.groups.items()
                                if len(g_participants) == 0)
        for g in incomplete_groups:
            logger.warning(f'No participants in group {repr(g)}. Deleted!')
            del self.groups[g]
        if len(self.groups) == 0:
            raise RuntimeError('No EMA data in any group.')
        for attr in self.emf.attribute_dtypes.keys():
            a_count = self.attribute_grade_count(attr)
            # = pd.DataFrame with all groups, all participants
            _check_ratings(attr, a_count)

    def join_df(self, participant='Participant'):  # **** default 'Participant' where ?
        """Join all EMA data into ONE single pd.DataFrame instance
        for all groups and all participants
        :param participant: (optional) name of column with participant ID
        :return: a single pd.DataFrame instance  **** NOT Table ?
        """
        g_dict = {g_key: pd.concat({s: s_data
                                    for (s, s_data) in g_data.items()},
                                   axis=0,
                                   sort=False,
                                   names=[participant])
                  for (g_key, g_data) in self.groups.items()}
        # if len(g_dict) == 1 and len(self.emf.group_head()) == 0:  # only ONE UN-NAMED group
        #     (g_cat, df) = g_dict.popitem()
        # else:
        #     df = pd.concat(g_dict, axis=0, names=self.emf.group_head(), sort=False)
        df = self._join_group_dict(g_dict)
        return Table(df)

    def _join_group_dict(self, g_dict):
        """Help method to concat pd.DataFrame or pd.Series instances across groups,
        with special treatment in case of single un-named group.
        Needed only internally.
        :param g_dict: dict with elements (g_key, g_data), where
            g_data is a DataFrame or pd.Series object
        :return: a single pd.DataFrame or pd.Series instance
        """
        if len(g_dict) == 1 and len(self.emf.group_head()) == 0:  # only ONE UN-NAMED group
            (g_cat, df) = g_dict.popitem()
        else:
            df = pd.concat(g_dict, axis=0, names=self.emf.group_head(), sort=False)
        return df

    def attribute_grade_count(self, a, groupby=None):
        """Collect table of ordinal grades for ONE attribute,
        for each (group, participant), optionally subdivided by situation
        :param a: ONE selected attribute key
        :param groupby: (optional) single situation dimension or list of such dimensions
            for which separate attribute-counts are calculated.
            Counts are summed across any OTHER situation dimensions.
        :return: a pd.DataFrame object with all grade counts,
            with one row for each (group, participant, *groupby) case
            and one column for each grade category
        2023-04-11, bugfix
        """
        def s_count(s_data, a, groupby):
            """Calculate participant value_count
            :param s_data: a participant DataFrame
            :param a: attribute key
            :param groupby: sequence of situation dimension, possibly empty
            :return: DataFrame instance with desired value counts for attribute a
            """
            if len(groupby) == 0:
                return s_data[a].value_counts(sort=False)
            else:
                return s_data.groupby(groupby, observed=True)[a].value_counts(sort=False)  # observed=True default
        # ------------------------------------------------------------

        a = self.emf.match_attribute_key(a)
        if groupby is None:
            groupby = []
        elif isinstance(groupby, str):
            groupby = [groupby]
        groupby = [self.emf.match_situation_key(gb) for gb in groupby]
        # groupby = [gb for gb in groupby if gb in self.emf.situation_dtypes.keys()]
        g_dict = {g_key: pd.concat({s: s_count(s_data, a, groupby)
                                    for (s, s_data) in g_data.items()},
                                   axis=0,
                                   sort=False,
                                   names=['Participant'])  # *** -> cls property ?
                  for (g_key, g_data) in self.groups.items()}
        df = self._join_group_dict(g_dict)
        return Table(df.unstack(a))

    def attribute_grade_mean(self, a=None, groupby=None, fill_missing=False):
        """Average raw attribute grades, encoded numerically as (1, ..., n_grades)
        :param a: (optional) attribute label or sequence of such labels,
            if None, include all attributes
        :param groupby: (optional) single situation dimension or iterable of such keys
            for which separate attribute-means are calculated.
            Results are aggregated across any OTHER situation dimensions.
        :param fill_missing: (optional) boolean -> include NaN for missing result row
        :return: a pd.DataFrame instance with all mean Attribute grades,
            with rows Multi-indexed for Group(s), Participant, and selected Situation dimensions.
            with one column for selected attribute(s).
        """
        def recode_attr(df, a):
            """Recode ordinal attribute grades linearly to numerical (1,...,n_grades)
            :param df: a pd.DataFrame instance
            :param a: list of attribute column names in df
            :return: None; df recoded in place
            """
            # *** allow external user-defined recoding function ?
            for a_i in a:
                c = df[a_i].array.codes.copy().astype(float)
                c[c < 0] = np.nan
                df[a_i] = c + 1

        def s_mean(s_data, a, groupby):
            """Calculate participant value_count
            :param s_data: a participant DataFrame
            :param a: attribute key or list of such keys
            :param groupby: list of situation dimension, possibly empty
            :return: DataFrame instance with desired value counts for attribute a
            """
            s_data = s_data.copy()  # avoid modifying original
            recode_attr(s_data, a)
            if len(groupby) == 0:
                return s_data[a].mean(numeric_only=True)
            else:
                s_m = s_data.groupby(groupby, observed=True)[a].mean(numeric_only=True)
                if fill_missing:    # include missing row(s) filled with NaN
                    if isinstance(s_m.index, pd.CategoricalIndex):
                        if s_m.shape[0] < len(s_m.index.categories):    # missing row(s) for some category
                            s_m = s_m.reindex(pd.CategoricalIndex(s_m.index.categories),
                                              fill_value=np.nan)
                    if isinstance(s_m.index, pd.MultiIndex):
                         if s_m.shape[0] < np.prod(s_m.index.levshape):  # missing row(s) for some category
                            s_m = s_m.reindex(pd.MultiIndex.from_product(list(s_m.index.levels)),
                                              fill_value=np.nan)
                return s_m
                # observed=True future default
        # ------------------------------------------------------------
        # ******* checking for spelling error in a and groupby *******
        if a is None:
            a = list(self.emf.attribute_dtypes.keys())
        elif isinstance(a, str):
            a = [a]
        # a = [a_i for a_i in a if a_i in self.emf.attribute_dtypes.keys()]
        a = [self.emf.match_attribute_key(a_i) for a_i in a]
        if groupby is None:
            groupby = []
        elif isinstance(groupby, str):
            groupby = [groupby]
        # groupby = [gb for gb in groupby if gb in self.emf.situation_dtypes.keys()]
        groupby = [self.emf.match_situation_key(gb) for gb in groupby]
        g_dict = {g_key: pd.concat({s: s_mean(s_data, a, groupby)
                                    for (s, s_data) in g_data.items()},
                                   axis=0,
                                   sort=False,
                                   names=['Participant'])  # *** -> cls property ?
                  for (g_key, g_data) in self.groups.items()}
        df = self._join_group_dict(g_dict)
        return Table(df)

    def nap_table(self, sit, nap_cat=None, a=None, groupby=None, p=0.95):
        """Calculate proportion of Non-overlapping Pairs = NAP result
        in ONE situation dimension with EXACTLY TWO categories, X and Y,
        = estimate of P(attribute grade in X < attribute grade in Y),
        given observed ordinal i.i.d. grade samples for attribute in situation_dtypes X and Y.
        :param sit: ONE situation dimension with TWO categories to be compared
        :param nap_cat: (optional) sequence of TWO categories (X, Y) in situation dimension sit.
            If None, sit MUST be categorical with exactly TWO categories.
        :param a: (optional) attribute name or iterable of attribute names
        :param groupby: (optional) single situation key or iterable of such keys
            for which separate NAP results are calculated.
            Results are aggregated across any OTHER situation dimensions.
        :param p: (optional) scalar confidence level for NAP result
        :return: a pd.DataFrame instance with all NAP results,
            with rows Multi-indexed for Group(s), Participant, grouping Situation-dimension(s),
            columns Multi-indexed with three NAP results for each Attribute:
            (lower conf-interval limit, point estimate, upper conf-interval limit)
        """
        if a is None:
            a = list(self.emf.attribute_dtypes.keys())
        elif isinstance(a, str):  # single attribute
            a = [a]
        # ******* check for spelling error in nap_cat, a, and groupby ? *******
        # a = [a_i for a_i in a
        #      if a_i in self.emf.attribute_dtypes.keys()]
        a = [self.emf.match_attribute_key(a_i) for a_i in a]
        if groupby is None:
            groupby = []
        elif isinstance(groupby, str):
            groupby = [groupby]
        # groupby = [gb for gb in groupby if gb in self.emf.situation_dtypes.keys()]
        groupby = [self.emf.match_situation_key(gb) for gb in groupby]
        df = self.join_df()
        g_cols = list(self.emf.group_dtypes.keys())
        if len(g_cols) == 1 and len(g_cols[0]) == 0:
            g_cols = []
        groupby = g_cols + ['Participant'] + groupby
        sit = self.emf.match_situation_key(sit)
        if nap_cat is not None:
            nap_cat = [_match_string_label(nc, self.emf.situation_dtypes[sit].categories,
                                           sit + ' nap_cat')
                       for nc in nap_cat]
        return Table(nap_pandas(df, col=sit, nap_cat=nap_cat,
                                group_cols=groupby, grade_cols=a, p=p))


# -------------------------------------------- module help functions

def _match_string_label(k, k_list, k_msg):
    """Ensure one of allowed alternatives
    :param k: key string to be checked
    :param k_list: iterable of different allowed alternatives
    :param k_msg: string label for error msg
    :return: matched_k = best-matching element in k_list
        otherwise EMAinputError raised
    """
    k_matches = get_close_matches(k, k_list)
    if len(k_matches) == 0:
        raise EmaInputError('Unknown ' + k_msg + ': ' + repr(k))
    if k_matches[0] != k:
        if len(k_matches) == 1:  # Unique but approximate match
            logger.warning('Misspelled ' + k_msg + ': ' + repr(k) + '? '
                           + f'Using {repr(k_matches[0])}')
        else:  # non-unique approximate match
            logger.warning('Ambiguous ' + k_msg + ': ' + repr(k) + '. '
                           + f'Using the first of {k_matches}')
    return k_matches[0]  # use best match anyway


def _check_required_columns(req_cols, file_columns):
    """Check necessary column heads are unambiguously present in input data frame.
    :param req_cols: list with required column head
    :param file_columns: list of column heads in input EMA data file
    :return: None
        Raise error if not EXACTLY matching
    """
    for rc in req_cols:
        err_msg = f'Required column {repr(rc)} missing in input EMA data.'
        rc_match = get_close_matches(rc, file_columns)
        if len(rc_match) == 0:
            raise EmaInputError(err_msg)
        if rc_match[0] != rc:
            if len(rc_match) == 1:
                raise EmaInputError(err_msg +
                                    f' Consider rename_cols {rc_match[0]}?')
            else:
                raise EmaInputError(err_msg +
                                    f' Did you mean one of {rc_match}?')



def group_dir_str(g_head, g, sep='_'):
    """Convert group id to a directory path string
    :param g_head: tuple of strings with group "dimensions"
    :param g: tuple of labels with corresponding group categories
    :param sep: string joining group dimension and category
    :return: string to be used as directory path
    """
    s = '/'.join((str(h_i) + sep + str(g_i)
                     for (h_i, g_i) in zip(g_head, g)))
    if s == sep:  # only a single group with empty head and category
        return ''
    else:
        return s


def _gen_group_file_paths(path, fmt, group_factors, sep='_'):
    """Generator of group categories and corresponding file Paths, recursively, for all groups
    :param path: Path instance defining top directory to be searched
    :param fmt: file suffix of desired files, INCL leading '.'
    :param group_factors: dict with tuples (g_factor, list of categories)
    :param sep: (optional) separator string between group dimension and category in file path
    :return: generator of tuples (group_key, file_path), where
        group_key is a dict with elements (g_key, g_cat), for all g_key in group_factors,
        file_path is a Path object to a file that may hold EMA data for the group,
        Only paths with matching group sub-strings AND desired file format are included.
    """
    if fmt is None:
        path_gen = path.glob('**/*.*')  # try all files in all subdirectories
    else:
        path_gen = path.glob('**/*' + fmt)  # try only requested file format
    for p in path_gen:
        group_key = _match_group_factors(p, group_factors, sep)
        # = empty dict if group_factors is empty dict -> OK file
        # = None if group_factors is non-empty, but NOT ALL matched in p
        if group_key is not None:
            yield group_key, p


def _match_group_factors(p, group_factors, sep='_'):
    """
    :param p: path to be checked
    :param group_factors: dict with elements (g_key, g_cats),
        where g_cats is a list of allowed categories fpr group dimension g_key
    :param sep: (optional) separator string between group dimension and category in file path
    :return: g_cats = dict with elements (g_key, g_cat), for all g_key in group_factors,
        IFF all matching patterns, e.g., 'Age_old' for g_key='Age', g_cat = 'old'
        were found in p.
        Otherwise, None, if not all group_factors were matched.
    """
    def find_in_string(s, k, cats):
        for c in cats:
            if 0 <= s.find(str(k) + sep + str(c)):
                return c
        return None

    # -------------------------------------------------
    g_keys = dict()
    for (g_key, g_cats) in group_factors.items():
        g_cat = find_in_string(str(p), g_key, g_cats)
        if g_cat is None:
            return None
        else:
            g_keys[g_key] = g_cat
    return g_keys


def _table_valid(ema: pd.DataFrame):
    """Count valid data elements for all columns
    :param ema: Pandas.DataFrame instance with input EMA data
    :return: table string for logger output
    """
    return pd.DataFrame([ema.count()]).to_string(index=False)


def _check_ratings(a, a_count):
    """Warning about zero rating counts in some categories
    :param a: attribute key
    :param a_count: pd.DataFrame with count distribution for this attribute
        one row for each (group, participant), summed across Situations
    :return: None
    """
    max_zero = 0.5  # proportion of all participants
    n_rows = a_count.shape[0]
    zero_participants = np.sum(a_count.to_numpy() == 0, axis=0)
    if np.any(zero_participants == n_rows):
        logger.warning(f'Attribute {a}: Some grades unused by ALL participants! '
                       + 'Consider merging grades?\n\t'
                       + f'{a} grades=\n'
                       + a_count.to_string())
    elif np.any(zero_participants > max_zero * n_rows):
        logger.warning(f'Attribute {a}: Some grades unused by some participants! '
                       + 'Consider merging grades?')


# -------------------------------------------- TEST:
if __name__ == '__main__':
    import ema_logging

    # ------------------------ Set up working directory and result logging:
    work_path = Path.home() / 'Documents' / 'EMA_sim'  # or whatever...
    data_path = work_path / 'data'  # to use simulation data generated by run_sim.py
    # result_path = work_path / 'result'  # or whatever

    # model_file = 'test_ema_model.pkl'  # name of saved model file (if saved)

    ema_logging.setup()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # ------ 1: Define Experimental Framework: Situations, Attributes, and Grades

    # NOTE: This example uses data generated by template script run_sim.py
    # Edit as needed for any other EMA data source

    sim_situations = {# 'phase': ('',),  # only ONE Test phase with empty label
                     'HA': ('A', 'B'),  # Two Hearing-aid programs
                     'CoSS': [f'C{i}' for i in range(1, 8)],    # Seven CoSS categories
                     }  # nominal variables, same for all (Sub-)Populations
    # NOTE: First situation dimension is always phase, even if only ONE category
    # User may set arbitrary phase_key label
    # Dimension 'phase' may be omitted, if only one category

    emf = EmaFrame.setup(situations=sim_situations,
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
                         groups={'Age': ('young', 'old'),
                                 # 'Gender': ('M', 'F'),
                                 },
                         population_weights={('old',): 2.,
                                             # ('old', 'F'): 2.,
                                             }
                         )

    print('emf=\n', emf)
    print(f'emf.n_phases= {emf.n_phases}')
    print(f'emf.situation_shape= {emf.situation_shape}')
    print(f'emf.rating_shape= {emf.rating_shape}')

    ds = EmaDataSet.load(emf, data_path, fmt='csv',
                         participant='file',
                         path_groups=['Age'],  #, 'Gender'],
                         dtype={'CoSS': 'string'})
    print('ds=\n', ds)

    test = ds.attribute_grade_count(a='Speech', groupby=('HA', 'CoSS'))
    test.to_string(work_path / 'test_attribute_count.txt')
    print('rating_count=\n', test)

    test = ds.attribute_grade_mean(groupby=('HA', 'CoSS'))
    test.to_string(work_path / 'test_attribute_mean.txt')
    print('mean_rating=\n', test)

    nap = ds.nap_table(sit='HA', groupby=('CoSS',))
    nap.to_string(work_path / 'test_nap_table.txt', float_format='%.3f')
    print('NAP(HA B > A)=\n', nap)

    # -------------------- test EmaDataSet.save
    test_path = work_path / 'test_save'
    ds.save(test_path, fmt='csv', participant='file', join_groups=False, group_join_str='_')
    print(f'Data set saved in {test_path}')

    # -------------------------------------TEST zero group dimensions
    emf = EmaFrame.setup(situations=sim_situations,
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
                         # groups={'Age': ('young', 'old'),
                         #         # 'Gender': ('M', 'F'),
                         #         }
                         )

    ds = EmaDataSet.load(emf, data_path, fmt='csv',
                         participant='file',
                         # path_groups=['Age', 'Gender'],
                         dtype={'CoSS': 'string'})
    print('ds= ', ds)

    test_path = work_path / 'test_save_nogroup'
    ds.save(test_path, fmt='csv', participant='TP', join_groups=True, group_join_str='_')
    print(f'Data set saved in {test_path}')

    nap = ds.nap_table(sit='HA')  # across all CoSS categories
    nap.to_string(test_path / 'test_nap_table.txt', float_format='%.3f')
    print('NAP(HA B > A)=\n', nap)


    # -------------------------------------TEST ONE group with ONE category
    emf = EmaFrame.setup(situations=sim_situations,
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
                         groups={'Age': ['young'],  # *** ONE group, named
                                 # 'Gender': ('M', 'F'),
                                 }
                         )

    ds = EmaDataSet.load(emf, data_path, fmt='csv',
                         participant='file',
                         path_groups=['Age'],
                         dtype={'CoSS': 'string'})
    print('ds= ', ds)
    test_path = work_path / 'test_save_onegroup'
    ds.save(test_path, fmt='csv', participant='TP', join_groups=True, group_join_str='_')
    print(f'Data set saved in {test_path}')

    # -------------------------------------TEST ONE group with NO situation keys
    print('\n*** Test one group with no situation keys')
    emf = EmaFrame.setup(#  situations=sim_situations,
                         #  phase_key='Phase',
                         attributes={'Speech': ['Very Hard',
                                                'Hard',
                                                'Easy',
                                                'Very Easy',
                                                'Perfect'],
                                     'Comfort': ['Bad',
                                                 'Not Good',
                                                 'Not Bad',
                                                 'Good']},
                         groups={'Age': ['young'],  # *** ONE group, named
                                 # 'Gender': ('M', 'F'),
                                 }
                         )

    ds = EmaDataSet.load(emf, data_path, fmt='csv',
                         participant='file',
                         path_groups=['Age'],
                         dtype={'CoSS': 'string'})
    print('ds= ', ds)
    test_path = work_path / 'test_save_no_Sit'
    ds.save(test_path, fmt='csv', participant='TP', join_groups=True, group_join_str='_')
    print(f'Data set saved in {test_path}')

    # -------------------------------------- TEST Empty attribute_grades
    print('\n*** Test one group, empty Attributes')
    emf = EmaFrame.setup(situations=sim_situations,
                         phase_key='Phase',
                         groups={'Age': ['young'],  # *** ONE group, named
                                 # 'Gender': ('M', 'F'),
                                 }
                         )
    ds = EmaDataSet.load(emf, data_path, fmt='csv',
                         participant='file',
                         path_groups=['Age'])
    print('ds= ', ds)
    test_path = work_path / 'test_save_no_Attr'
    ds.save(test_path, fmt='csv', participant='TP', join_groups=True, group_join_str='_')
    print(f'Data set saved in {test_path}')
