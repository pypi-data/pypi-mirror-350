"""This module estimates the effect measure Non-overlap of All Pairs (NAP),
to be used as a non-Bayesian measure of difference between Attribute Ratings.

The NAP measure is a non-parametric estimate of the probability that
Attribute Rating X < Y, given observed ordinal i.i.d. rating samples
x_n drawn from random variable X, and y_n drawn from Y,
X and Y represent two separate Situations.
The NAP measure is closely related to the Mann-Whitney statistic for ordinal data.

This module calculates point estimates and approximate confidence intervals for the NAP measure.

The confidence intervals are symmetric in probability.
For example, with a confidence level p=0.95,
the upper and lower tail probabilities are both = 0.025.
However, the central NAP point estimate is usually
NOT at the midpoint of the confidence interval.

There are many ways to calculate an approximate confidence interval for NAP.
Feng et al (2017) studied 29 different methods.
This module uses the "MW-N" variant, defined on page 2607 in their paper,
which showed good performance.
This variant was originally proposed by Newcombe (2009).

*** References:
R. I. Parker and K. Vannest.
An improved effect size for single-case research: Nonoverlap of all pairs.
Behavior Therapy, 40(4):357–367, 2009. doi: 10.1016/j.beth.2008.10.006

D. Feng, G. Cortese, and R. Baumgartner.
A comparison of confidence/credible interval methods for the area under the ROC curve
for continuous diagnostic tests with small sample size.
Statistical Methods in Medical Research, 26(6):2603–2621, 2017.
doi: 10.1177/0962280215602040

R. G. Newcombe.
Confidence intervals for an effect size measure based on the Mann–Whitney statistic.
Part 2: Asymptotic methods and evaluation.
Statistics in Medicine, 25:559–573, 2006. doi: 10.1002/sim.2324


*** Main module functions:
nap_pandas --- calculates point estimate and symmetric confidence intervals
    for Ordinal Grades stored as columns in a pandas DataFrame instance,
    grouped by values in other categorical columns, if desired.

nap_count --- calculates point estimate and symmetric confidence intervals
    for Ordinal Grades stored as arrays of grade Counts at each ordinal level.

nap_ci_low --- approximate lower limit of confidence interval
nap_ci_high --- approximate upper limit of confidence interval
    Can be used for either one-tailed or two-tailed confidence interval.

*** Version history:
* Version 1.1.3:
2025-03-28, fix to avoid FutureWarning for Pandas 2.1. Removed earlier fix for Pandas <= 1.5

* Version 0.9.4:
2022-11-06: Temp fix in nap_pandas for Pandas v 1.5.2 FutureWarning

* Version 0.9:
2022-03-24, calculate NAP from data stored in a pandas DataFrame

* Version 0.7:
2021-12-16, first functional version incl. confidence interval
2022-01-03, minor fix to give clearer warning message in case of nan result
"""
# *** publish this as package NAPcalc on PyPi separate from EmaCalc ? ********
import warnings  # *** needed? use logging?

import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.optimize import brentq
import logging

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # *** TEST
# ham.logger.setLevel(logging.DEBUG)  # *** TEST


# ------------------------------------------------ Module exceptions
class NapError(RuntimeError):
    """Any type of exception while calculating NAP
    """


def nap_pandas(df, col, nap_cat=None,
               group_cols=None, grade_cols=None, p=0.95):
    """Calculate proportion of Non-overlapping Pairs = NAP result
    = estimate of P(X < Y), given observed ordinal i.i.d. rating samples
    x_n drawn from random variable X, and y_n drawn from Y.
    :param df: a Pandas.DataFrame object containing input data
    :param col: name of ONE column with categories for which NAP is to be calculated
    :param nap_cat: (optional) sequence of TWO categories (X, Y) in col.
        If None, df[col].dtype MUST be Categorical with exactly TWO categories.
    :param group_cols: (optional) sequence with name(s) of columns,
        for which results will be grouped.
    :param grade_cols: (optional) sequence with name(s) of columns with ordinal grades
        for which the NAP effect measure is calculated.
        If None, use ALL ordinal data columns in df
    :param p: (optional) confidence level for probability-symmetric confidence interval,
        i.e., upper == lower tail probability == (1-p) / 2.
    :return: a pandas DataFrame with all results stored in
        rows MultiIndex-ed by elements of group_cols, and
        columns MultiIndex-ed as (g_i, low), (g_i, nap), (g_i, high), where
            g_i is a grade label in grade_cols, and
            low is the lower conf.interval limit
            nap is the NAP point estimate,
            high is the upper conf.interval limit
        All calculated values show NAP for Second re. First category in col.
        Result table is sorted by categories in group_cols.
    """
    def calc_nap(group_name, group_df):
        """Calculate NAP results for given (sub-grouped) DataFrame
        :param group_name: single column or tuple of column names to mark in result
        :param group_df: a pd.DataFrame object
        :return: a dict with all NAP results as (key, value) pairs
        """
        # ***** check NaN grade columns ********
        # if len(group_cols) == 1:  # *** temp fix for Pandas <= 1.5.2
        #     # not needed in future Pandas version !
        #     group_name = [group_name]  # because pd.groupby made it scalar in v. <= 1.5.2
        res = {g_col: g_cat
               for (g_col, g_cat) in zip(group_cols, group_name)}
        for a in grade_cols:
            x = group_df[group_df[col] == nap_cat[0]][a]
            y = group_df[group_df[col] == nap_cat[1]][a]
            x = x[x.notna()]
            y = y[y.notna()]
            n_x = len(x)
            n_y = len(y)
            if n_x == 0 or n_y == 0:
                res.update({(a, '[<'): np.nan,
                            (a, 'NAP'): np.nan,
                            (a, '<]'): np.nan})
            else:
                n_y_gt_x = sum(sum(y.gt(x_i) for x_i in x))  # x, y both pd.Series objects
                n_y_eq_x = sum(sum(y.eq(x_i) for x_i in x))
                nap_point = (n_y_gt_x + n_y_eq_x / 2) / (n_x * n_y)
                z_tail = - norm.ppf((1. - p) / 2)
                res.update({(a, '[<'): nap_ci_low(nap_point, n_x, n_y, z_tail),
                            (a, 'NAP'): nap_point,
                            (a, '<]'): nap_ci_high(nap_point, n_x, n_y, z_tail)})
                # added three new columns for this attribute
        return res
        # ---------------------------------------------------------------------
    if nap_cat is None:
        if df[col].dtype.name == 'category' and len(df[col].dtype.categories) == 2:
            nap_cat = df[col].dtype.categories
        else:
            raise NapError(f'Cannot calculate NAP for column {col}. Must have exactly TWO categories')
    elif len(nap_cat) != 2:
        raise NapError(f'Cannot calculate NAP for nap_cat={nap_cat}. Must have exactly TWO categories')
    if grade_cols is None:
        grade_cols = [c for c in df.columns
                      if df[c].dtype == 'category'
                      and df[c].dtype.ordered]
    if len(grade_cols) == 0:
        raise NapError(f'No ordinal category columns found in given DataFrame.')
    if group_cols is None:
        group_cols = ()
        res = pd.DataFrame.from_records([calc_nap((), df)])
        # = DataFrame with ONE row of NAP results, no grouping
    # elif len(group_cols) == 1:  # temp fix to avoid FutureWarning in Pandas <= 1.5.2
    #     # *** not needed when future df.groupby returns tuple (group_name,)
    #     res = pd.DataFrame.from_records([calc_nap(*df_g)
    #                                      for df_g in df.groupby(group_cols)])  # [0])])
    #     # = DataFrame with one row for each groupby category
    #     res.set_index(group_cols, inplace=True)
    else:
        res = pd.DataFrame.from_records([calc_nap(*df_g)
                                         for df_g in df.groupby(group_cols,
                                                                observed=True)])  # avoid FutureWarning v 2.1
        # = DataFrame with one row for each groupby category
        res.set_index(group_cols, inplace=True)
    col_ind = pd.MultiIndex.from_tuples(res.columns)
    return res.reindex(columns=col_ind)


# -----------------------------------------------------------------
def nap_count(x, y, p=0.95):  # *** not used in EmaCalc ***
    """Calculate proportion of Non-overlapping Pairs = NAP result,
    = estimate of P(X > Y), given observed ordinal i.i.d. rating samples
    x_n drawn from random variable X, and y_n drawn from Y,
    where X and Y represent two separate Situations.
    :param x: array of grade COUNTS for samples of ordinal random variable X
        x[i, ...] = number of observed samples of i-th ordinal grade
    :param y: array of COUNTS for ordinal random variable Y, similar
        y.shape == x.shape
    :param p: (optional) scalar confidence level
    :return: nap = array with
        nap[0, ...] = lower limit of symmetric confidence interval
        nap[1, ...] = point estimate of P(X > Y)
        nap[2, ...] = upper limit of symmetric confidence interval
        nap.shape[1:] == x.shape[1:] == y.shape[1:]
    """
    result_shape = x.shape[1:]
    cum_y = np.cumsum(y, axis=0)
    # cum_y[i] = n Y <= i
    n_y = cum_y[-1]
    n_x = np.sum(x, axis=0)
    n_x_gt_y = np.sum(x[1:, ...] * cum_y[:-1, ...], axis=0)
    # = sum_i number of pairs where X == i AND Y < i
    n_x_eq_y = np.sum(x * y, axis=0)
    # = n pairs where X == Y
    n_pairs = n_x * n_y
    if np.any(n_pairs == 0):
        logger.warning('NO rating pairs -> undefined NAP value in some case(s).')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')  # suppress standard warning for div by zero
        nap_point = (n_x_gt_y + 0.5 * n_x_eq_y) / n_pairs
    z_tail = norm.isf((1. - p) / 2)  # upper tail quantile
    ci_low = np.array([nap_ci_low(p, nx, ny, z_tail)
                       for (p, nx, ny) in zip(nap_point.reshape((-1,)),
                                              n_x.reshape((-1,)),
                                              n_y.reshape((-1,)))])
    ci_high = np.array([nap_ci_high(p, nx, ny, z_tail)
                       for (p, nx, ny) in zip(nap_point.reshape((-1,)),
                                              n_x.reshape((-1,)),
                                              n_y.reshape((-1,)))])
    return np.array([ci_low.reshape(result_shape),
                     nap_point,
                     ci_high.reshape(result_shape)])


def nap_ci_low(a_hat, nx, ny, z_quantile):
    """Calculate lower limit of symmetric confidence interval for NAP
    :param a_hat: scalar point estimate of P(X > Y)
    :param nx: number of X observations
    :param ny: number of Y observations
    :param z_quantile: quantile at higher tail of standard-normal distribution
    :return: scalar ci_low

    Method: MW-N as described by Feng et al (2017),
        using the improved variant solving their nonlinear Eq. (3)
    """
    def fun_3(a):
        """Function to solve Feng et al Eq (3)
        for the LOWER confidence limit, where 0 <= a < a_hat
        :param a: scalar solution candidate
        :return: scalar function value
        """
        return a_hat - a - z_quantile * nap_stdev(a, nx, ny)
    # --------------------------------------------------
    if nx == 0 or ny == 0:
        return np.nan
    if np.isclose(a_hat, 0.):
        return 0.
    ci_lim, res = brentq(fun_3, 0., a_hat, full_output=True)
    if res.converged:
        return ci_lim
    else:
        logger.warning('Confidence-interval calculation did not converge')
        return np.nan


def nap_ci_high(a_hat, nx, ny, z_quantile):
    """Calculate upper limit of symmetric confidence interval for NAP
    :param a_hat: scalar point estimate of P(X > Y)
    :param nx: number of X observations
    :param ny: number of Y observations
    :param z_quantile: quantile at higher tail of standard-normal distribution
    :return: scalar ci_low

    Method: MW-N as described by Feng et al (2017),
        using the improved variant solving their nonlinear Eq. (3)
    """
    def fun_3(a):
        """Function to solve Feng et al Eq (3)
        for the UPPER confidence limit, where a_hat < a <= 1.
        :param a: scalar solution candidate
        :return: scalar function value
        """
        return a - a_hat - z_quantile * nap_stdev(a, nx, ny)
    # --------------------------------------------------
    if nx == 0 or ny == 0:
        return np.nan
    if np.isclose(a_hat, 1.):
        return 1.
    ci_lim, res = brentq(fun_3, a_hat, 1., full_output=True)
    if res.converged:
        return ci_lim
    else:
        logger.warning('Confidence-interval calculation did not converge')
        return np.nan


def nap_stdev(a, nx, ny):
    """Help function to estimate st.dev. of NAP value
    :param a: scalar candidate value for NAP
    :param nx: number of X observations
    :param ny: number of Y observations
    :return: s = sqrt(var(A)), estimated at point NAP A == a

    Method: var_H defined just before Eq (3) in Feng et al (2017)
    """
    n_star = (nx + ny) / 2 - 1
    # = symmetrized as suggested by Newcombe (2009)
    v = a * (1. - a)
    v *= 1. + n_star * ((1. - a) / (2. - a) + a / (1. + a))
    v /= nx * ny
    return np.sqrt(v)


# ------------------------------------------------- TEST:
if __name__ == '__main__':
    print('*** Testing nap_pandas ***')
    df = pd.DataFrame({'HA': list('ABABAA'),
                       }, dtype='category')  # not ordered
    df['Speech'] = pd.Series(['Bad', 'Good', 'Good', 'Good', 'Bad', 'Bad'],
                             dtype=pd.CategoricalDtype(categories=['Bad', 'Good'],
                                                       ordered=True))
    df['Comfort'] = pd.Series(['Bad', 'OK', 'Bad', 'Good', 'Good', 'OK'],
                             dtype=pd.CategoricalDtype(categories=['Bad', 'OK', 'Good'],
                                                       ordered=True))
    nap = nap_pandas(df, 'HA')
    print(nap)
    print('')
    df['Group'] = 'All'
    nap = nap_pandas(df, 'HA', group_cols=['Group'])
    print(nap)
    print('')
    nap = nap_pandas(df, 'HA', nap_cat=('B', 'A'), group_cols=['Group'])
    print(nap)
    print('')
    df.loc[0, 'Speech'] = np.nan
    nap = nap_pandas(df, 'HA', nap_cat=('B', 'A'), group_cols=['Group'])
    print(nap)
    print('')

    print('*** Testing nap_statistic ***')
    x_count = np.array([1, 2, 3, 4, 5])
    y_count = np.array([3, 3, 3, 3, 3])
    print(f'NAP result =\n\t{nap_count(x_count, y_count)}')

    print('*** Testing nap_statistic ***')
    x_count = np.array([0, 0, 0, 5])
    y_count = np.array([4, 3, 2, 0])
    print(f'NAP result =\n\t{nap_count(x_count, y_count)}')


