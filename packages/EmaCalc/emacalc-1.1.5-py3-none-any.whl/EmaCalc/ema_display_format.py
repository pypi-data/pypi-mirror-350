"""This module includes functions to format output displays of
EmaModel results, in graphic and textual form.

Plot properties may be controlled by
1: specifying matplotlib style sheet(s) by keyword argument mpl_style
2: setting specific matplotlib parameters at runtime by keyword argument mpl_params
3: setting specific parameters in FMT, e.g., 'colors' and 'markers'

*** Version History:
* Version 1.1.3.:
2025-03-21, using ema_repr.EmaObject as superclass

* Version 1.1.0:
2024-01-30, removed explicit plot format settings where possible; using matplotlib.rcParams instead
2024-01-30, new FMT parameters 'threshold_color', 'threshold_linewidth'

* Version 0.9.6:
2023-04-16, some plot parameters -> FMT for user control
2023-04-12, new simplified tab_percentles, tab_credible_diff
2023-03-31, new help function make_product_name *** NO LONGER NEEDED

* Version 0.9.5:
2023-03-07, fig_category_barplot allow both observed and model-predicted quantile data

* Version 0.9.4:
2023-01-22, Bug fix in output file name creation, to avoid problem under Windows.
            Added 'interaction_sep' and 'condition_sep' in FMT dict, for user control.
            Added try...catch for any errors in ResultPlot.save() and ResultTable.save()

* Version 0.9.3:
2022-07-27, allow setting matplotlib style sheet(s) and individual matplotlib params
2022-07-12, Special DiffTable class to suppress numerical index in save.
2022-07-12, Simplified header in tab_credible_diff.

* Version 0.9.2:
2022-06-17, fig_percentiles: allow caller to set y_min, y_max
2022-06-04, suppress integer index column in Table.save. New support function harmonize_ylim
2022-06-03, tab_credible_diff with clarified header

* Version 0.9.1:
2022-04-10, fig_percentiles using DataFrame table as input
2022-03-30, make all tables as pandas DataFrame objects

* Version 0.8:
2022-02-15, minor cleanup of tab_percentile: allow cdf=None, header percentile format .1f

* Version 0.7.1:
2022-01-21, minor fix in tab_cred_diff to avoid credibility == 100.0%
2022-01-08, set_tight_layout for all ResultPlot objects
2022-01-13, changed EmaDisplaySet.show format argument: show_intervals -> grade_thresholds

* Version 0.7:
2021-12-19, function nap_table to format NAP results

2021-11-07, copied and modified PairedCompCalc -> EmaCalc
"""
import numpy as np
from itertools import cycle, islice
import matplotlib.pyplot as plt
import logging
import pandas as pd

from .ema_repr import EmaObject
from .ema_file import Table

logger = logging.getLogger(__name__)


FMT = {'colors': 'rbgk',    # to distinguish results in plots, cyclic use
       'markers': 'oxs*_',  # corresponding markers, cyclic use
       'threshold_linewidth': None, # default in set_format_param, using rcParams
       'threshold_color': None,     # default in set_format_param, using rcParams
       'x_space': 0.3,      # clean space between x_tick categories
       'interaction_sep': '\u00D7',  # mult.sign. separating situation labels in result file names
       'condition_sep': '_',    # separating attribute and its conditioning situation(s) in file names
       'diff_marker': '-diff',  # marker after diff-axis categories in file names
       'max_plot_cases': 50,    # max cases in percentile plots
       'max_case_heads': 1,     # limit in plot legends
       'and_head': ('', ''),    # two-level heading for diff-table first column
       'and_label': 'and',      # logical and in diff-table first column
       }

# NOTE: FMT['colors'] and FMT['markers'] override matplotlib.rcParams.axes.prop_cycle,
#   because prop_cycle allows only equal lengths of 'colors' and 'markers'.
#   The FMT['colors'] and FMT['markers'] are used cyclically,
#   so the default sequences with unequal lengths will combine
#   into a sequence with many combinations, before repeating itself.


def set_format_param(mpl_style=None, mpl_params=None, **kwargs):
    """Set / modify format parameters.
    Called before any displays are generated.
    :param mpl_style: (optional) matplotlib style sheet, or list of style sheets
    :param mpl_params: (optional) dict with matplotlib (k, v) rcParam settings
    :param kwargs: dict with any formatting variables to be stored in FMT
    :return: None
    """
    if mpl_style is not None:
        plt.style.use(mpl_style)
    if mpl_params is not None:
        plt.rcParams.update(mpl_params)
    FMT['threshold_linewidth'] = 0.2 * plt.rcParams['lines.linewidth']  # default
    FMT['threshold_color'] = plt.rcParams['axes.edgecolor']  # default
    other_fmt = dict()
    for (k, v) in kwargs.items():  # user settings
        k = k.lower()
        if k in FMT:
            FMT[k] = v
        else:
            other_fmt[k] = v
    if len(other_fmt) > 0:
        logger.warning(f'Parameters {other_fmt} unknown, not used.')


# ---------------------------- Basic Result Classes

class ResultPlot(EmaObject):
    """Container for a single graph instance
    """
    def __init__(self, ax, name):
        """
        :param ax: matplotlib Axes instance containing the graph
        :param name: string identifying the plot; used as file name
        """
        self.ax = ax
        self.name = name

    @property
    def fig(self):
        return self.ax.figure

    def save(self, path,
             figure_format,
             **kwargs):
        """Save figure to given path
        :param path: Path to directory for saving self
        :param figure_format: figure-format string code -> file-name suffix
        :param kwargs (optional) any additional kwargs, *** NOT USED ***
        :return: None
        """
        # *** select subset of kwargs allowed by savefig() ?
        # NO, depends on Matplotlib backend!
        f = (path / self.name).with_suffix('.' + figure_format)
        try:
            self.fig.savefig(f)
        except Exception as e:  # any error, just warn and continue
            logger.warning(f'Could not save plot to {f}. Error: {e}')


class ResultTable(Table):
    """A pd.DataFrame table subclass, with a name and special save method
    """
    def __init__(self, df, name):
        """
        :param df: a Table(pd.DataFrame) instance
        :param name: file name for saving the table
        """
        super().__init__(df)
        self.name = name

    def save(self, path,
             table_format='txt',
             **kwargs):
        """Save table to file.
        :param path: Path to directory for saving self.
            suffix is determined by FMT['table_format'] anyway
        :param table_format: table-format string code -> file-name suffix
        :param kwargs: (optional) any additional arguments to pandas writer function
        :return: None
        """
        f = (path / self.name).with_suffix('.' + table_format)
        try:
            super().save(f, **kwargs)
        except Exception as e:  # any error, just warn and continue
            logger.warning(f'Could not save result table. Error: {e}')


class DiffTable(ResultTable):
    """Special subclass suppressing index in save method
    """
    def save(self, path,
             **kwargs):
        """Save table to file.
        :param path: Path to directory for saving self.
            suffix is determined by FMT['table_format'] anyway
        :param table_format: table-format string code -> file-name suffix
        :param kwargs: (optional) any additional arguments to pandas writer function
        :return: None
        """
        if 'index' not in kwargs:
            kwargs['index'] = False  # override Pandas default = True
        super().save(path, **kwargs)


# ---------------------------------------- Formatting functions:

def fig_percentiles(df,
                    y_label='',
                    file_label='',
                    cat_limits=None,
                    y_min=None,
                    y_max=None,
                    **kwargs):
    """create a figure with percentile results
    as defined in a given pd.DataFrame instance
    :param df: pd.DataFrame instance with primary percentile data, with
        one row for each case category, as defined in df.index.values elements,
        one column for each percentile value.
    :param y_label: (optional) string for y-axis label
    :param file_label: (optional) string as first part of file name
    :param cat_limits: 1D array with response-interval limits (medians)
    :param y_min: (optional) enforced lower limit of vertical axis
    :param y_max: (optional) enforced upper limit of vertical axis
    :param kwargs: (optional) dict with any additional keyword arguments for plot commands. *** NOT NEEDED ? ****
    :return: ResultPlot instance with plot axis with all results

    NOTE: plot will use df.index.level[0] categories as x-axis labels,
    and index.level[1:] as plot labels in the legend
    """
    # ----------------------------------- set up plot design:
    if df is None:
        return None
    if df.index.nlevels == 1:
        x_label = df.index.name
        x_tick_labels = list(df.index.values)
        case_head = ()
        case_list = [()]
    elif df.index.nlevels == 2:
        x_label = df.index.names[0]
        x_tick_labels = list(dict.fromkeys([c[0] for c in df.index.values]))
        case_head = df.index.names[1]
        case_list = list(dict.fromkeys([c[1] for c in df.index.values]))
    else:
        x_label = df.index.names[0]
        x_tick_labels = list(dict.fromkeys([c[0] for c in df.index.values]))
        case_head = tuple(df.index.names[1:])
        case_list = list(dict.fromkeys([c[1:] for c in df.index.values]))
        # in order as appearing in df
    if df.shape[0] > FMT['max_plot_cases']:
        logger.warning(f'Too many {x_label}, {case_head} cases to plot. '
                       + f'Set max_plot_cases >= {df.shape[0]} if really needed.')
        return None
    n_cases = len(case_list)
    dx = (1. - FMT['x_space']) / n_cases
    # = x step between range plots for separate cases
    x_offset = {c: (i - (n_cases - 1) / 2) * dx
                for (i, c) in enumerate(case_list)}
    case_color = {c: col for (c, col) in zip(case_list, cycle(FMT['colors']))}
    case_marker = {c: mark for (c, mark) in zip(case_list, cycle(FMT['markers']))}
    # ------------------------------------------------------------------------
    def plot_one(ax, row_index, y):
        """
        :param ax: axis for plot
        :param row_index: index label(s) for ONE row in df
        :param y: 1D array with corresponding y = values in ONE row
            y[p] = p-th percentile value
        :return: None
        """
        if df.index.nlevels == 1:
            x_tick = row_ind
            x_case = ()
        elif df.index.nlevels == 2:
            x_tick = row_ind[0]
            x_case = row_ind[1]
        else:
            x_tick = row_ind[0]
            x_case = row_ind[1:]
        x = x_tick_labels.index(x_tick) + x_offset[x_case]
        x = x * np.ones_like(y)
        c = case_color[x_case]
        m = case_marker[x_case]
        if len(y) == 1:  # only single marker
            line = ax.plot(x, y,
                           linestyle='', color=c,
                           marker=m, markeredgecolor=c, markerfacecolor='w',
                           **kwargs)  # ******** ?
        elif len(y) == 2:  # vertical range, no markers
            line = ax.plot(x, y,
                           # linestyle='solid',  # *** use Matplotlib rcParams ?
                           color=c,
                           marker=m, markeredgecolor=c, markerfacecolor='w',
                           **kwargs)
        else:  # vertical range, and markers for intermediate percentiles
            y = sorted(list(y))
            ax.plot([x[0], x[-1]], [y[0], y[-1]],
                    # linestyle='solid',
                    color=c,
                    **kwargs)
            line = ax.plot(x[1:-1], y[1:-1],
                           # linestyle='solid',
                           color=c,  # to get line+marker into label
                           marker=m, markeredgecolor=c, markerfacecolor='w',
                           **kwargs)
        if x_tick == x_tick_labels[0]:
            if type(case_head) is tuple and len(case_head) > FMT['max_case_heads']:
                line[0].set_label(str(x_case))
            else:
                line[0].set_label(str(case_head) + '=' + str(x_case))

    # ------------------------------------------------------------------
    fig, ax = plt.subplots()
    for (row_ind, y) in df.iterrows():
        plot_one(ax, row_ind, y)

    (x_min, x_max) = ax.get_xlim()
    x_min = min(x_min, -FMT['x_space'])
    x_max = max(x_max, len(x_tick_labels) - 1 + FMT['x_space'])
    ax.set_xlim(x_min, x_max)
    if cat_limits is not None:
        _plot_response_intervals(ax, cat_limits)
    ax.set_xticks(np.arange(len(x_tick_labels)))
    xticks = [str(c) for c in x_tick_labels]
    ax.set_xticklabels(xticks,
                       **_x_tick_style(xticks))
    (y0, y1) = ax.get_ylim()
    if y_min is not None:
        y0 = y_min
    if y_max is not None:
        y1 = y_max
    ax.set_ylim(y0, y1)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    if len(case_list) > 1:
        ax.legend()  # (loc='best') ***************
    if len(file_label) > 0:
        file_label += FMT['condition_sep']
    f_name = file_label + FMT['interaction_sep'].join(df.index.names)
    # fig.set_tight_layout(tight=True)  # **** let rcParams control this  ****
    return ResultPlot(ax, name=f_name)


def _plot_response_intervals(ax, c_lim):
    """plot horizontal lines to indicate response thresholds
    :param ax: axis object
    :param c_lim: 1D array with scalar interval limits
    :return: None
    """
    (x_min, x_max) = ax.get_xlim()
    return ax.hlines(c_lim, x_min, x_max,
                     colors=FMT['threshold_color'],
                     linewidths=FMT['threshold_linewidth'],
                     )


def fig_category_barplot(df,
                         x_label,
                         y_label,
                         df_q=None,
                         file_label='',
                         y_min=None,  # *** not needed, always = 0
                         y_max=None,  # *** not needed, adaptive
                         mpl_params=None,  # *** not needed? called only from ema_display ***
                         **kwargs  # *** NOT needed
                         ):
    """Bar plot of DataFrame values,
    to be displayed with one sequence of vertical bars along x-axis for each row,
    with one bar for each column,
    suitable, e.g., for plotting attribute_grade_counts
    :param df: a DataFrame instance,
        one row for each selected situation category, one column for each grade
    :param df_q: (optional) DataFrame instance with quantiles
        similar to df, but expanded with one row for each (situation category, quantile)
    :param x_label: x-axis label string
    :param y_label: y-axis label string
    :param file_label: plot name for saving file
    :param y_min: (optional) enforced lower limit of vertical axis *** NOT USED
    :param y_max: (optional) enforced upper limit of vertical axis *** NOT USED
    :param mpl_param: (optional) dict with matplotlib rcParam settings
    :param kwargs: (optional) dict with keyword arguments for plot commands *** NOT NEEDED ? ****
    :return: a ResultPlot instance
    """
    fig, ax = plt.subplots()
    assert df.ndim > 1, 'Input must be DataFrame'
    (n_cases, n_x) = df.shape
    x = np.arange(n_x)
    bar_space = 0.02  # space to allow all bar edges to be visible
    w = 0.8 / n_cases - bar_space
    if len(df.index.names) > 1:
        case_head = tuple(df.index.names)
    else:
        case_head = df.index.name
    x_dev = (w + bar_space) * (np.arange(n_cases) - (n_cases - 1) / 2)
    for (d, c, case) in zip(x_dev,
                            cycle(FMT['colors']),
                            df.index.values):
        y = df.loc[case].to_numpy()
        # *** check case_head vs FMT['max_case_head'] ***
        if type(case_head) is tuple and len(case_head) > FMT['max_case_heads']:
            case_legend = str(case)
        else:
            case_legend = str(case_head) + '= ' + str(case)
        ax.bar(x + d, height=y,
               width=w, edgecolor=c, facecolor='w',  # ************
               label=case_legend)
    if df_q is not None:  # *** model-predicted count range:
        for (d, c, case) in zip(x_dev,
                                cycle(FMT['colors']),
                                df.index.values):
            y = df_q.loc[case].to_numpy()
            ax.plot(np.tile(x + d, (len(y),1)), y,
                    # '-',   # rcParams default
                    color=c,
                    linewidth=1.5 * plt.rcParams['lines.linewidth'],
                    )
    ax.set_xticks(np.arange(n_x))
    xticks = [str(c) for c in df.columns.values]
    ax.set_xticklabels(xticks,
                       **_x_tick_style(xticks))
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if n_cases > 1:
        ax.legend()  # (loc='best')
        f_name = file_label + FMT['condition_sep'] + FMT['interaction_sep'].join(df.index.names)
    else:
        f_name = file_label
    # fig.set_tight_layout(tight=True)
    return ResultPlot(ax, name=f_name)


# ----------------------------------------- table displays:

def tab_percentiles(q_ds, file_label=''):
    """Re-format a pd.DataFrame with percentile results.
    :param q_ds: a pd.Series instance with quantiles as last index axis,
        and cases in other index axes.
    :param file_label: (optional) string as first part of file name
    :return: a ResultTable(pd.DataFrame) instance,
        with one column for each percentile,
        and one row for each combination product of cases considered.
    """
    tab_perc = q_ds.unstack()
    case_head = tab_perc.index.names
    tab_perc.columns = [f'{q:.1%}' for q in tab_perc.columns]
    if len(file_label) > 0:
        file_label += FMT['condition_sep']
    f_name = file_label + FMT['interaction_sep'].join(case_head)
    return ResultTable(tab_perc, name=f_name)


def tab_credible_diff(diff,
                      diff_head,
                      cred_head,
                      case_head=(),
                      y_label='',
                      file_label='',
                      and_label=FMT['and_label'],
                      and_head=FMT['and_head']
                      ):
    """Create table with credible differences among results -- pandas version
    :param diff: list of tuples (((i,j), c0,...), p),
        defining jointly credible differences, indicating that
        prob{ quality of diff category i > quality of category j, given case category c
        AND all previous pairs } == p
        i, j are either a string label or a tuple of such labels
        c0,... is one or more case labels
    :param diff_head: tuple of keys for heading of diff_labels column in table
        len(diff_head) == len(i) == len(j) if tuple, or len(diff_head) == 1
    :param cred_head: string for header of Credibility column
    :param case_head: (optional) tuple of case keys, one for each case-dimension table column
        len(case_head) == len(c0,...)
    :param y_label: (optional) string with label of tabulated attribute
    :param file_label: (optional) string for first part of file name
    :param and_label: (optional) joining AND label in first column
    :param and_head: (optional) tuple with two strings for head first column
    :return: ResultTable object with header lines + one line for each credible difference
    """
    if len(diff) == 0:
        return None
    y_head_i = y_label + ' >'
    y_head_j = y_label
    # --------------------- table columns as dicts:
    col = {and_head:  [' '] + [and_label] * (len(diff) - 1)}  # first column with only AND flags
    diff_i = [(ijc[0][0] if type(ijc[0][0]) is tuple else (ijc[0][0],)) for (ijc, p) in diff]
    diff_j = [(ijc[0][1] if type(ijc[0][1]) is tuple else (ijc[0][1],)) for (ijc, p) in diff]
    diff_c = [ijc[1:] for (ijc, p) in diff]
    diff_p = [p for (ijc, p) in diff]
    # --------- column(s) for higher results:
    col |= {(y_head_i, d_head_k): [d[k] for d in diff_i]
            for (k, d_head_k) in enumerate(diff_head)}
    # --------- column(s) for lower results:
    col |= {(y_head_j, d_head_k): [d[k] for d in diff_j]
            for (k, d_head_k) in enumerate(diff_head)}  # cols for lesser results
    # --------- column(s) for optional case labels:
    if len(case_head) > 0:
        # diff_c = [case_labels[d[0][2]]
        #           for d in diff]
        col |= {('', c_head_k): [d[k] for d in diff_c]
                for (k, c_head_k) in enumerate(case_head)}
    # --------- credibility column:
    col |= {(' ', cred_head): diff_p}
    df = pd.DataFrame(col)  # do all this in samppy.credibility_pd ? ***********
    # each column name is a tuple with two elements -> MultiIndex with two levels
    # df = df.reindex(columns=pd.MultiIndex.from_tuples(df.columns))  # ****** Needed ?
    if len(file_label) > 0:
        file_label += FMT['condition_sep']
    f_name = file_label + FMT['interaction_sep'].join(diff_head) + FMT['diff_marker']
    if len(case_head) > 0:
        f_name += FMT['condition_sep'] + FMT['interaction_sep'].join(case_head)
    return DiffTable(df, name=f_name)


# -------------------------------------- display adjustment functions
def harmonize_ylim(axes_list, y_min=None, y_max=None):
    """Adjust several plots to equal vertical range
    :param axes_list: sequence of plt.Axes instances
    :param y_min: (optional) extra user-defined minimum
    :param y_max: (optional) extra user-defined maximum
    :return: None
    """
    y0 = min(*(ax.get_ylim()[0]
               for ax in axes_list))
    if y_min is not None:
        y0 = min(y0, y_min)
    y1 = max(*(ax.get_ylim()[1]
               for ax in axes_list))
    if y_max is not None:
        y1 = max(y1, y_max)
    for ax in axes_list:
        ax.set_ylim(y0, y1)


# -------------------------------------- private help functions
def _x_tick_style(labels):
    """Select xtick properties to avoid tick-label clutter
    :param labels: list of tick label strings
    :return: dict with keyword arguments for set_xticklabels
    """
    maxL = max(len(l) for l in labels)
    rotate_x_label = maxL * len(labels) > 75  # ad hoc criterion
    if rotate_x_label:
        style = dict(rotation=15, horizontalalignment='right')
    else:
        style = dict(rotation='horizontal', horizontalalignment='center')
    return style
