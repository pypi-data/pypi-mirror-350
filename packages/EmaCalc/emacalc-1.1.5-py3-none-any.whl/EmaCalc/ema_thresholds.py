"""This module defines help classes to calculate response thresholds
from given model parameters.

*** Classes:
ThresholdsFree: allowing all response thresholds freely adaptable, new version.
ThresholdsMidFixed: forcing one mid-range threshold -> zero, other thresholds free

*** Version history:
* Version 1.0.1:
2023-06-05, Fix to prevent numerical overflow / underflow in extreme cases,
            and general code cleanup.
            New module functions mapped_tau(w), d_mapped_tau(w), mapped_tau_inv(tau),
            and related changes to Thresholdxxx methods.


* Version 0.9.5: NEW module, with functions moved from ema_base
"""
import numpy as np
from scipy.special import logit, expit, softmax
import logging

logger = logging.getLogger(__name__)

W_EPSILON = np.sqrt(np.finfo(float).eps)
# = additive constant in mapped_tau(w) to prevent too small response interval widths.
# NOTE: ema_latent uses interval (tau_low - theta, tau_high - theta) for probability calculation,
# so we must ensure that this interval is non-zero also for very big theta like 1 / W_EPSILON
# Thus, (1 / W_EPSILON + W_EPSILON) - 1 / W_EPSILON must be > 0,
# and (1 + W_EPSILON**2) - 1 > 0.


# -------------------------------------------------------------
class ThresholdsFree:
    """All internal thresholds freely variable, as specified by model parameter vector eta,
    with number of parameters == number of internal thresholds == M - 1, where
    M = number of response categories
    """
    @staticmethod
    def n_param(n_categories):
        return n_categories - 1

    @staticmethod
    def tau(eta):
        """Mapping given log-category-width parameters to response thresholds.
        :param eta: = array with
            eta[..., m] = ...-th sample of parameter defining
                non-normalized width of m-th interval in mapped domain [0, 1].
            eta.shape[-1] == self.n_param(M), with M == number of response categories.
            eta[..., M] assumed fixed == 0, NOT included in input argument
        :return: tau = threshold array, incl. all elements in [-inf, +inf]
            (tau[..., m], tau[..., m+1]) = (LOWER, UPPER) limits for m-th ordinal response interval
            tau[..., 0] ==  - np.inf
            tau[..., -1] == + np.inf
            tau.ndim == eta.ndim; tau.shape[-1] == eta.shape[-1] + 2
        """
        z_shape = (*eta.shape[:-1], 1)
        zeta = np.concatenate((eta, np.zeros(z_shape)), axis=-1)
        return mapped_tau(softmax(zeta, axis=-1))

    @staticmethod
    def d_tau(eta):
        """Jacobian of thresholds with respect to eta
        :param eta: = 1D or 2D array with
            eta[..., m] = ...-th sample of parameter defining
                 non-normalized width of m-th interval in mapped domain [0, 1].
            eta.shape[-1] == M - 1, where M == number of response intervals.
            eta[..., M] assumed fixed == 0, NOT given as input
        :return: 2D or 3D array d_tau, with
            d_tau[..., m, i] = d tau[..., m] / d eta[..., i]; m = 0,..., M; i = 0, ..., M-1
                 where (tau[s, m], tau[s, m+1] = (LOWER, UPPER) limits of m-th response interval
            d_tau[..., 0, :] = d_tau[..., -1, :] = 0., for extreme limits at +-inf
            d_tau.ndim == eta.ndim + 1; d_tau.shape[-2:] == (M+1, M-1)
        """
        z_shape = (*eta.shape[:-1], 1)
        zeta = np.concatenate((eta, np.zeros(z_shape)), axis=-1)
        w = softmax(zeta, axis=-1)
        return jac_mapped_tau(w) @ _jac_softmax(w)[..., :-1]


# -------------------------------------------------------------
class ThresholdsMidFixed:
    """One mid-range threshold fixed == 0.,
    other thresholds mapped from parameter array eta,
    with number of parameters == M - 2, where
    M = number of response categories
    """
    @staticmethod
    def n_param(n_categories):
        return n_categories - 2

    @staticmethod
    def tau(eta):
        """Mapping given log-category-width parameters to response thresholds.
        :param eta: = array with
            eta[..., m - 1] = ...-th sample of parameter defining
                non-normalized width of m-th interval in mapped domain [0, 1].
            eta.shape[-1] == self.n_param(M), with M == number of response categories.
        :return: tau = 1D or 2D array, incl. all elements in [-inf, +inf]
            (tau[..., m], tau[..., m+1]) = (LOWER, UPPER) limits for m-th ordinal response interval
            tau[..., 0] ==  - np.inf
            tau[..., -1] == + np.inf
            tau.ndim == eta.ndim; tau.shape[-1] == eta.shape[-1] + 2
        """
        pad = np.zeros((*eta.shape[:-1], 1))
        zeta = np.concatenate((pad, eta, pad),
                              axis=-1)
        n_half = zeta.shape[-1] // 2
        w = np.concatenate((softmax(zeta[..., :n_half], axis=-1),
                            softmax(zeta[..., n_half:], axis=-1)), axis=-1)
        return mapped_tau(w)

    @staticmethod
    def d_tau(eta):
        """Jacobian of tau(eta) w.r.t. eta
        :param eta: = 1D or 2D array with
            eta[..., m - 1] = ...-th sample of parameter defining
                non-normalized width of m-th interval in mapped domain [0, 1].
            eta.shape[-1] == self.n_param(M), with M == number of response categories.
        :return: 2D or 3D array d_tau, with
            d_tau[..., m, i] = d tau[..., m] / d eta[..., i]; m = 0,..., M; i = 0, ..., M-1
                 where (tau[s, m], tau[s, m+1] = (LOWER, UPPER) limits of m-th response interval
            d_tau[..., 0, :] = d_tau[..., -1, :] = 0., for extreme limits at +-inf
            d_tau.ndim == eta.ndim + 1; d_tau.shape[-2:] == (M+1, M-2)
        """
        pad = np.zeros((*eta.shape[:-1], 1))
        zeta = np.concatenate((pad, eta, pad),
                              axis=-1)
        n_half = zeta.shape[-1] // 2
        w1 = softmax(zeta[..., :n_half], axis=-1)    # normalized lower half
        w2 = softmax(zeta[..., n_half:], axis=-1)    # normalized upper half
        dw_dzeta = np.zeros((*zeta.shape, zeta.shape[-1]))
        dw_dzeta[..., :n_half, :n_half] = _jac_softmax(w1)
        dw_dzeta[..., n_half:, n_half:] = _jac_softmax(w2)
        # dw_deta = dw_dzeta[..., 1:-1]  # EXCL fixed pad elements
        dtau_dw = jac_mapped_tau(np.concatenate((w1, w2), axis=-1))
        return dtau_dw @ dw_dzeta[..., 1:-1]


# ----------------------------- general module functions

# NOTE: logit, expit are NOT symmetric around mid-point for extreme arguments
# logit(expit(37.)) = 37.; logit(expit(38.)) = +inf; logit(expit(-38.)) = -38.
# logit(expit(-709.)) = -709.; logit(expit(-710.)) = -inf
# *** Now should be sufficiently protected by W_EPSILON in mapped_tau() function

def mapped_tau(w):
    """Response thresholds from given un-normalized interval widths
    :param w: array of row vector(s) with POSITIVE width parameters
        normalized with sum == 1. for ThresholdsFree, or 2. for ThresholdsMidFixed
        w.shape[-1] == number of ordinal response levels.
    :return: tau = corresponding threshold values, INCL. extreme -inf, ..., +inf
        tau.shape[-1] == w.shape[-1] + 1
    """
    w = w + W_EPSILON   # ensure no interval width gets truncated -> 0.
    cum_w = np.cumsum(w, axis=-1)
    z_shape = (*cum_w.shape[:-1], 1)
    cum_w = np.concatenate((np.zeros(z_shape), cum_w),
                           axis=-1)  # include cum_w[..., 0] = 0.
    # cw = cum_w[..., 1:-1]  # EXCL extreme == zero
    # sw = cum_w[..., -1:]
    # tau = logit(cw / sw) = np.log(cw) - np.log(sw - cw) EXCL extreme limits at -inf, +inf
    # + W_EPSILON HERE, TOO ?
    # ***** Check: close tau values + 1000 might get truncated to ZERO interval width
    tau = logit(cum_w / cum_w[..., -1:])  # INCL extreme at -inf, +inf
    # *** interval of (tau - theta) might get -> 0 ?
    d = np.diff(tau - 10000., axis=-1)
    d_warn = d == 0.
    if np.any(d_warn):
        logger.warning(f'mapped_tau: num. underflow: diff(tau) = \n' +
                       np.array_str(d[d_warn]) +
                       f'\nw =\n' + np.array_str(w[d_warn]))
        if tau.ndim > 1:
            d_warn = np.any(d_warn, axis=-1)
            logger.warning(f'mapped_tau: tau = \n'+
                           np.array_str(tau[d_warn]))
    return tau


def jac_mapped_tau(w):
    """Jacobian of mapped_tau(w) with respect to w
    :param w: 1D or 2D array with POSITIVE width parameters >= ETA_W_EPSILON
    :return: 2D or 3D array d_tau, with
        d_tau[..., m, i] = d tau[..., m] / d w[..., i],
            for m = 0,..., M + 1; i = 0, ..., M - 1
            where (tau[s, m], tau[s, m+1]) = (LOWER, UPPER) limits of m-th response interval
        d_tau[..., 0, :] = d_tau[..., -1, :] == 0., for extreme limits at +-inf
        d_tau.shape == (N, M+1, M); N = n_samples; M = n response categories
    """
    w = w + W_EPSILON
    nw = w.shape[-1]
    cum_w = np.cumsum(w, axis=-1)
    cw = cum_w[..., :-1, np.newaxis]  # only inner limits
    sw = cum_w[..., -1:, np.newaxis]
    # dcw_dw[..., m, i] = dcw[..., m, 0] / dw[..., i]  = 1. if i <= m else 0.
    dcw_dw = np.tril(np.ones((nw - 1, nw), dtype=int))  # dtype = Boolean ?
    # tau[..., m+1] = ln cw[..., m, 0]  - ln (sw[..., 0, 0] - cw[..., m, 0])
    dtau_dw = dcw_dw / cw - (1 - dcw_dw) / (sw - cw)
    pad = np.zeros((*dtau_dw.shape[:-2], 1, dtau_dw.shape[-1]))
    return np.concatenate((pad,
                           dtau_dw,
                           pad), axis=-2)


def mapped_tau_inv(tau):
    """Approximate inverse of mapped_tau(w)[..., 1:-1]
    :param tau: 1D or 2D array with response thresholds, EXCEPT extremes at +-inf,
        i.e., all tau elements in (-inf, +inf),
        tau[..., m] = UPPER limit for m-th interval,
            = LOWER limit for the (m+1)-th interval
        tau.shape[-1] == number of response intervals - 1
    :return: w: 1D or 2D array, such that
        mapped_tau(w) approx == tau (except for added W_EPSILON)
    """
    y = expit(tau)
    cat_shape = (*y.shape[:-1], 1)
    y = np.concatenate((np.zeros(cat_shape),
                        y,
                        np.ones(cat_shape)), axis=-1)
    # = including extreme limits at 0 and 1
    return np.diff(y, axis=-1)


# ----------------------------- local module help functions

# ----------- Original up to version 0.9.1 -> numeric overflow in some extreme cases
# w = mapped_width(eta) = np.exp(eta)
#
# ---------- *** piecewise (inverted linear, linear ) variant, tested for v. 0.9.4, also no good

# ----------- Version 0.9.4 - 1.0.0:
# def mapped_width(eta):
#     return np.exp(eta) + ETA_W_EPSILON
# *** solved numeric problem with large negative eta,
# *** BUT still could give numeric overflow in some cases with very large positive eta

# Version 1.0.1 now using original exp mapping,
# with normalized widths w = softmax(eta),
# and eps protection only in mapped_tau(w), AFTER width normalization.


def _jac_softmax(w):
    """Jacobian of w = softmax(eta, axis=-1) w.r.t eta,
    calculated as a function of w,
    because w must be already calculated by caller anyway
    :param w: = array of ROW vectors with normalized width values = softmax(eta, axis=-1)
    :return: array dw, with
        dw[..., i, m] = d softmax(eta, axis=-1)[..., i] / d eta[..., m]
        dw.shape == (*w.shape, w.shape[-1]) == (*eta.shape, eta.shape[-1])
    """
    n = w.shape[-1]
    dw = - w[..., :, None] * w[..., None, :]    # dw[..., i, m] = w[..., i] * w[..., m]
    dw[..., range(n), range(n)] += w            # dw[..., i, i] += w[..., i]
    return dw


# ------------------------------------------------- TEST:
if __name__ == '__main__':
    from scipy.optimize import approx_fprime, check_grad

    n_categories = 4  # 2, 3, 5
    # *** extreme values:
    eta_extreme = -100000.  # -1000.

    print('\n*** Testing mapped_width = softmax ***')
    eta = np.array([-5., 0., 5, 10.])
    eta = np.zeros(n_categories)
    eta[1] = eta_extreme
    # eta = - eta_extreme * np.ones(n_categories)
    # all these cases work OK now

    w = softmax(eta)
    print(f'softmax({eta}, axis=-1) = ', w)
    print(f'dsoftmax_deta({eta}) = \n', _jac_softmax(w))
    print(f'd sum_softmax({eta} = \n', np.sum(_jac_softmax(w), axis=0))
    for i in range(len(eta)):
        def fun(eta):
            return softmax(eta)[i]
        def jac(eta):
            w = softmax(eta)
            return _jac_softmax(w)[i]
        print('approx gradient = ', approx_fprime(eta, fun, epsilon=1e-6))
        print('exact  gradient = ', jac(eta))
        err = check_grad(fun, jac, eta, epsilon=1e-6)
        print('check_grad err = ', err)

    print('\n*** Testing mapped_tau ***')
    w = 1. + np.arange(n_categories)
    # w /= np.sum(w)  # normalized
    tau = mapped_tau(w)
    print(f'mapped_tau({w} = ', tau)
    tau_inv = mapped_tau_inv(tau[1:-1])
    print(f'mapped_tau_inv({tau[1:-1]} = ', tau_inv)
    print('Max(mapped_tau_inv - normalized(w)) = ', max(tau_inv - w / np.sum(w)))

    for i in range(1, len(tau)-1):
        def fun(w):
            return mapped_tau(w)[i]
        def jac(w):
            return jac_mapped_tau(w)[i]

        print('approx gradient = ', approx_fprime(w, fun, epsilon=1e-6))
        print('exact  gradient = ', jac(w))
        err = check_grad(fun, jac, w, epsilon=1e-6)
        print('check_grad err = ', err)

    n_samples = 1
    print(f'\nn_categories = {n_categories}')

    for thr in [ThresholdsFree, ThresholdsMidFixed]: # , Thresholds
        eta = np.zeros(thr.n_param(n_categories))

        # eta -= eta_extreme
        if len(eta) > 0:
            eta[0] = eta_extreme
            eta[-1] = - eta_extreme

        print(f'\n*** Testing {thr.__name__}.tau ***')

        tau = thr.tau(eta)
        print(f'eta = ', eta)
        # w = mapped_width(eta)
        # print(f'mapped_width({eta} = ', w)
        print(f'tau({eta}) = ', tau)
        print(f'diff(tau) = ', np.diff(tau, axis=-1))
        # print(f'tau_inv(tau[..., 1:-1] = ', thr.tau_inv(tau[..., 1:-1]))
        # print(f'tau(tau_inv(tau[..., 1:-1]) = ', thr.tau(thr.tau_inv(tau[..., 1:-1])))
        print(f'd_tau({eta}) = ', thr.d_tau(eta))

        def fun(eta):
            eta = np.tile(eta, (n_samples, 1))
            return thr.tau(eta)[0, limit]

        def jac(eta):
            eta = np.tile(eta, (n_samples, 1))
            return thr.d_tau(eta)[0, limit]

        if eta.ndim > 1:
            eta_test = eta[0]  # must be 1D vector for gradient test
        else:
            eta_test = eta

        for limit in range(1, n_categories):
            print(f'\n*** Testing Jacobian {thr.__name__}.d_tau[..., {limit}, :] ***')

            print(f'tau({eta_test}) = {thr.tau(eta_test)}')

            print('approx gradient = ', approx_fprime(eta_test, fun, epsilon=1e-6))
            print('exact  gradient = ', jac(eta_test))
            err = check_grad(fun, jac, eta_test, epsilon=1e-6)
            print('check_grad err = ', err)

