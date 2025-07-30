"""This module defines functions that read / write EMA data and analysis result tables,
from/to a table file of any kind that package Pandas can handle.

A single data file for READING may include EMA records from ONE or SEVERAL respondents,
in ONE or SEVERAL respondent groups.
The participant id may be stored in a designated column of the table,
otherwise the file name can be used as participant id,
or (in Excel-type file) the participant may be identified by the sheet name.
The table may include grouping categories, and other data not used for EMA analysis.

Regardless of the file storage format, even if an input file represents only ONE participant,
the EMA data is always delivered by a generator function
ema_gen, which is an iterable over pandas DataFrame instances.

Some pandas file readers can also do some
data conversions and/or type checking.
Column names may be modified before the data are delivered to caller.

For writing EMA data or any other table to a file,
cast the DataFrame instance to subclass Table,
and use Table(df).save(...) method.

*** Version History:
* Version 1.0.2:
2023-07-04, Table.save() with no enforced sheet_name, still allowed in file_kwargs

* Version 1.0.0:
2023-04-20, simplified ema_gen(..): yield whole table as a single pd.DataFrame,
            All data checking, and separation by group(s) and participant, is done externally.

* Version 0.9.3:
2022-07-22, changed 'subject' -> 'participant'
2022-07-15, minor bugfix in ema_gen.separate

* Version 0.9:
2022-03-21, use pd.DataFrame as interface to all file formats

* Version 0.8.3 and earlier: Handled only xlsx files.
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


# ------------------------------------------------ File exceptions
class FileReadError(RuntimeError):
    """Any type of exception while attempting to read EMA data from a file
    """


class FileWriteError(RuntimeError):
    """Any type of exception while attempting to write a pd.DataFrame table to a file
    """


# --------------------------------------------------
class Table(pd.DataFrame):
    """Subclass adding a general save method,
    automatically switching to desired file format.
    """
    def save(self, file_path,
             allow_over_write=True,
             write_fcn=None,
             **file_kwargs):
        """Save self to a table-style file.
        :param file_path: Path instance defining file location and full name incl. suffix.
        :param allow_over_write: (optional) boolean, if False, find new unused path stem.
        :param write_fcn: (optional) user-supplied function with signature
            write_fcn(table, path, **kwargs).
            If None, default pd.DataFrame method is used, determined by file_path.suffix
        :param file_kwargs: (optional) any additional arguments for the
            write function for the specific file format.
        :return: None
        """
        if not allow_over_write:
            file_path = safe_file_path(file_path)
        suffix = file_path.suffix
        try:
            # ******** file_path.parent.mkdir here? NO, done by container class
            if write_fcn is None:
                if suffix in ['.xlsx', '.xls', '.odf', '.ods', '.odt']:
                    # self.to_excel(file_path, sheet_name=file_path.stem, **file_kwargs) # use default
                    self.to_excel(file_path, **file_kwargs)
                elif suffix in ['.csv']:
                    self.to_csv(file_path, **file_kwargs)
                elif suffix in ['.txt']:
                    self.to_string(file_path, **file_kwargs)
                elif suffix in ['.tex']:
                    # with warnings.catch_warnings():
                    #     # suppress Pandas FutureWarning about to_latex method
                    #     warnings.simplefilter('ignore')
                    #     self.to_latex(file_path, **file_kwargs)
                    self.to_latex(file_path, **file_kwargs)
                else:
                    raise FileWriteError(f'No DataFrame write method for file type {suffix}')
            else:
                write_fcn(self, file_path, **file_kwargs)
        except Exception as e:
            raise FileWriteError(f'Could not write to {file_path}. Error: {e}')


# ----------------------------------------- General File Reader:
def ema_gen(file_path,
            participant=None,
            rename_cols=None,
            read_fcn=None,
            **file_kwargs
            ):
    """Reader of data stored in a table-style file that can be read by Pandas.read_xxx()
    or user-supplied function with similar signature.
    Each file row is assumed to include fields for one EMA record, but may also include other data fields.
    :param file_path: Path to existing file for reading
    :param participant: (optional) 'sheet' or 'file' or column header for participant identification label
        None -> 'sheet', if Excel-type file, otherwise -> 'file'
    :param rename_cols: (optional) dict with elements (old_name: new_name) for table column(s)
    :param read_fcn: (optional) basic read function, e.g., pd.read_excel,
        or any user-supplied function with similar signature.
        If None, a default pandas function is determined by file_path.suffix.
    :param file_kwargs: any additional arguments for the
        read function for the specific file format
    :return: generator object yielding pd.DataFrame instance(s),
        with one row for each EMA record,
        and one column specifying participant id,
        possibly copied from file name or sheet name if requested.
    """
    if read_fcn is None:
        read_fcn = _default_reader(file_path)
    logger.debug(f'Reading from {file_path} with {read_fcn}')
    if participant == 'sheet':
        if read_fcn is pd.read_excel:
            if 'sheet_name' not in file_kwargs.keys():
                file_kwargs['sheet_name'] = None
                # because pd.read_excel uses sheet_name=0 by default
        else:
            logger.warning(f'File type {file_path.suffix} has no "sheet"s. Using participant="file".')
            participant = 'file'
    try:
        df = read_fcn(file_path,
                      **file_kwargs)
    except Exception as e:
        raise FileReadError(f'{read_fcn.__name__}({file_path}) error: {e}')
    if type(df) is pd.DataFrame:
        if rename_cols is not None:
            df.rename(columns=rename_cols, inplace=True)
        if participant is None or participant == 'file':
            df['file'] = file_path.stem
            yield df
        elif participant in df.columns:
            yield df
        else:
            logger.debug(f'No column participant={participant} in this file')
    else:  # we have a dict of sheet DataFrames
        for (sheet_name, df_s) in df.items():
            if rename_cols is not None:
                df_s.rename(columns=rename_cols, inplace=True)
            if participant is None or participant == 'sheet':
                df_s['sheet'] = sheet_name
                yield df_s
            elif participant == 'file':
                df_s[participant] = file_path.stem
                yield df_s
            elif participant in df_s.columns:
                yield df_s
            else:
                logger.debug(f'Missing column participant={participant} in sheet {sheet_name} of this file')


# ------------------------------------------ help functions:
def safe_file_path(p):
    """Ensure previously non-existing file path, to avoid over-writing,
    by adding a sequence number to the path stem
    :param p: file path
    :return: p_safe = similar file path with modified name
    """
    f_stem = p.stem
    f_suffix = p.suffix
    i = 0
    while p.exists():
        i += 1
        p = p.with_name(f_stem + f'-{i}' + f_suffix)
    return p


def _default_reader(file_path):
    """Find a function that can read the given file path
    :param file_path: a Path instance
    :return: a pandas reader function, e.g., pd.read_excel
    """
    suffix = file_path.suffix
    if suffix in ['.xlsx', '.xls', '.odf', '.ods', '.odt']:
        return pd.read_excel
    elif suffix in ['.csv', '.txt']:
        return pd.read_csv
    elif suffix in ['.sav', '.zsav']:
        return pd.read_spss
    elif suffix in ['.dta']:
        return pd.read_stata
    else:
        raise FileReadError(f'Cannot (yet) read file format {suffix}')


# ----------------------------------------- TEST:
if __name__ == '__main__':
    from pathlib import Path
    import ema_logging

    work_path = Path.home() / 'Documents' / 'EMA_sim'  # or whatever...
    data_path = work_path / 'data_xlsx' / 'Age_old'  # to use simulation data generated by run_sim.py
    # data_path = work_path / 'data' / 'Age_old'  # to use simulation data generated by run_sim.py

    ema_logging.setup()  # to save the log file

    ema_file = ema_gen(data_path / 'Pop0_S1.xlsx',
                       participant='sheet',
                       dtype={'CoSS': pd.StringDtype()}  # ******** needed ?
                       )
    # for (s, ema) in ema_file:
    for ema in ema_file:
        print(ema.head(100))
        print('dtypes=\n', ema.dtypes)
        count = ema.value_counts(subset=['HA', 'CoSS'], sort=False)
        # ind = pd.MultiIndex.from_frame(ema[['HA', 'CoSS']])
        # c1 = count.reindex(index=ind, fill_value=0)
        print(count)

    path = data_path / 'test_write' / 'test_participant.csv'
    path.parent.mkdir(parents=True, exist_ok=True)
    # ********* check CoSS data type ? should be string ****'
    Table(ema).save(path)
