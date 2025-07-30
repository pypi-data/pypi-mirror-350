"""This module implements Dirichlet-distributed random vectors,
similar to scipy.stats.dirichlet.

A Dirichlet-distributed vector is a random vector of fractions,
with sum == 1., and all elements in [0., 1.].

The Dirichlet-distributed vector may be used as a probability-mass parameter
for a corresponding Multinomial-distributed count array of integer elements,
or for the component weights in a Mixture Model.

*** Main Classes:
DirichletVector: model for Dirichlet-distributed probability-mass vector,
    with all elements in [0., 1.], and sum of all elements == 1.
    The distribution is specified by an array of concentration parameters.
    The concentration parameters can be adapted to observed data.

*** Module functions:
log_multi_beta = log normalization factor for Dirichlet distribution
d_log_multi_beta = gradient of log_multi_beta

*** Version History:
* Version 0.9.3:
2022-08-23, simplify old code, to allow only 1-dim random Dirichlet vector in EmaCalc version

* Earlier versions:
2019-12-22, first multidimensional version, including Multinomial
"""
import numpy as np
from scipy.special import gammaln, psi

import logging

# ------------------------------------------------------------------------
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # test

JEFFREYS_CONC = 0.5


# --------------------------------------------------------------------------------
class DirichletVector:
    """Representing a multivariate Dirichlet-distributed vector.

    If U is a Dirichlet Random Vector, with elements U_i,
    the probability density function of U is determined by
    a vector of Concentration Parameters alpha, as
    p_U(u) = (1 / B(alpha) ) * prod_i u_i**(alpha_i - 1),
    B(alpha) = ( prod_i Gamma( alpha_i) ) / Gamma( sum_i alpha_i ),
    within the support domain
    0 < u_i < 1, all i, and sum_i( u_i ) == 1

    The normalization factor B(alpha) is implemented by module function
    log_multi_beta.
    """
    def __init__(self, alpha, rng=None):
        """
        :param alpha: 1-dim array-like sequence of concentration parameters
        :param rng: (optional) numpy.random.Generator object
        """
        self.alpha = np.array(alpha, dtype=float)
        if rng is None:
            self.rng = np.random.default_rng()
        else:
            self.rng = rng

    def __repr__(self):
        skip = '\n\t'
        return (self.__class__.__name__ + '(' + skip +
                (',' + skip).join(f'{key}={repr(v)}'
                                  for (key, v) in vars(self).items()) +
                skip + ')')

    # @classmethod
    # def initialize(cls, x, **kwargs):  # ********
    #     """Crude initial setting of concentration parameters
    #     :param x: array-like 1D list with non-normalized row vector(s)
    #         that might be generated from a cls instance,
    #         OR from a multinomial distribution with a cls instance as probability
    #         x[..., :] = ...-th row vector
    #     :param kwargs: (optional) any other key-word arguments for __init__
    #     :return: a new cls instance
    #     """
    #     a = np.array(x) + JEFFREYS_CONC
    #     # including Jeffreys concentration as pseudo-count
    #     a /= np.sum(a, axis=-1, keepdims=True)
    #     a *= JEFFREYS_CONC * a.shape[-1]
    #     # = normalized with average conc = JEFFREYS_CONC
    #     return cls(a, **kwargs)

    @property
    def shape(self):
        return self.alpha.shape

    @property
    def size(self):
        return self.alpha.size

    @property
    def ndim(self):  # == 1
        """Dimensionality of self"""
        return self.alpha.ndim

    @property
    def mean(self):
        return self.alpha / np.sum(self.alpha)

    @property
    def var(self):
        """Dirichlet variance Ref Bishop Eq B.18
        :return: v = array with
            v[...] = variance of ...-th element in random array
            v.shape == self.shape
        """
        a = self.alpha
        a0 = np.sum(a)  # across all elements regardless of shape
        return a * (a0 - a) / (a0**2 * (a0 + 1))

    @property
    def cov(self):
        """Ref Leijon PattRecKomp, Ch. 8
        Bishop Eq B.19 only for off-diag elements
        :return: c = 2D square covariance matrix for self, i.e.
            c[j, k] = covariance between (j,k)-th elements of self
            c.shape == (self.size, self.size)
        """
        return _cov_dirichlet(self.alpha)

    @property
    def mean_log(self):
        """E{ log U } where U is DirichletVector self
        :return: ml = vector with
            ml[k] = E{ log self[k] }
            ml.shape == self.shape
        """
        return psi(self.alpha) - psi(np.sum(self.alpha))

    # @property
    # def mean_root(self):  # *** not needed for EmaCalc
    #     """E{ sqrt(U) } element-wise, where U is DirichletVector self
    #     :return: ml = array with
    #         r[k] = E{ sqrt(self[k]) }
    #         r.shape == self.shape
    #     """
    #     a0 = np.sum(self.alpha)
    #     ln_r = (gammaln(a0) - gammaln(a0 + 0.5)
    #             + gammaln(self.alpha + 0.5) - gammaln(self.alpha))
    #     return np.exp(ln_r)

    # def mean_square_hellinger(self, othr):  # *** not needed in EmaCalc
    #     """Expected square Hellinger distance between self and othr,
    #     assuming independence
    #     :param othr: object with same class and shape as self
    #     :return: scalar h2 = E{H^2(self, othr)} = 1 - sum_k E{sqrt( u_k v_k ) }
    #         where u = (..., u_k, ...) = self, and v = (..., v_k, ...) = othr
    #     """
    #     return 1. - np.dot(self.mean_root, othr.mean_root)

    def relative_entropy(self, othr):
        """Relative Entropy = Kullback-Leibler divergence
        between two DirichletVector instances.
        :param othr: DirichletVector instance with same shape as self
        :return: KLdiv = scalar
            KLdiv = E{ log p_self(U) / p_othr(U) } evaluated for U = self
        """
        if self.shape == othr.shape:
            return (gammaln(np.sum(self.alpha)) - gammaln(np.sum(othr.alpha))
                    + np.sum(gammaln(othr.alpha) - gammaln(self.alpha))
                    + np.dot((self.alpha - othr.alpha).reshape(-1),
                             self.mean_log.reshape(-1))
                    )
        else:
            logger.warning('relative_entropy: Shape mismatch')
            return np.inf

    def logpdf(self, x):  # *** not needed for EmaCalc
        """log probability density of input sample vector(s).
        :param x: array-like (sequence of) vectors
            that might be samples drawn from self
        :return: lp = scalar or array with one value for each input sample array
            lp.shape == x.shape[:-1]
        """
        x = np.asarray(x)
        if x.ndim < 1:
            raise RuntimeError('Dimension mismatch')
        if x.shape[-1:] != self.shape:
            raise RuntimeError('Shape mismatch')
        # x and self.alpha are broadcast-compatible
        sum_axes = tuple(range(-1, 0))
        ok = np.logical_and(np.all(0. <= x, axis=-1),
                            np.isclose(1., np.sum(x, axis=-1)))
        if not np.all(ok):
            logger.warning('Some input is not in Dirichlet support -> logpdf = -inf')
        lp = (np.sum((self.alpha - 1.) * np.log(x), axis=sum_axes)
              - log_multi_beta(self.alpha))
        if np.isscalar(lp):
            if not ok:
                lp = -np.inf
        else:
            lp[np.logical_not(ok)] = -np.inf
        return lp

    def rvs(self, size=None):  # *** not needed for EmaCalc
        """Random sample array(s) drawn from self.
        :param size: (optional) scalar integer or tuple of ints with desired number of samples
        :return: u = array of random-generated probability-profile vectors
            Using numpy.random.Generation conventions:
            if size is None:
                u.shape == self.shape
            else:
                u.shape == (*size, *self.shape)
        """
        u = self.rng.dirichlet(alpha=self.alpha, size=size)
        if size is None:
            return u.reshape(self.shape)
        elif np.iterable(size):
            return u.reshape((*size, *self.shape))
        else:
            return u.reshape((size, *self.shape))


# --------------------------------------------------- general module functions
def log_multi_beta(a, axis=-1):
    """Log multivariate beta function
    = log normalization factor for Dirichlet distribution
    :param a: array-like concentration parameter ROW vector
        or array-like sequence of such row vectors
    :param axis: (optional) int or tuple of ints for axis to be reduced
    :return: log_multi_beta =  log-normalization value(s)
        log_multi_beta.shape == a.shape[:-1]
    """
    return (np.sum(gammaln(a), axis=axis, keepdims=False)
            - gammaln(np.sum(a, axis=axis, keepdims=False)))


# def d_log_multi_beta(a, axis=-1):
#     """Gradient of log_multi_beta
#     :param a: array-like sequence of concentration parameter vectors
#     :param axis: (optional) int or tuple of ints for axis to be summed
#     :return: d_log_multi_beta[..., k] = d log_multi_beta(a) / d a[..., k]
#         log_multi_beta.shape == a.shape
#     """
#     return psi(a) - psi(np.sum(a, axis=axis, keepdims=True))


# --------------------------------------------------- local module helper stuff
def _cov_dirichlet(a):
    """DirichletVector covariance, given concentration.
    Called recursively in case of multi-dimensional concentration array
    :param a: multi-dim array of concentration ROW vectors
    :return: c = array of square covariance matrices,
        one for each row vector in a.
        c.shape == (a.size, a.size)
    """
    # if a.ndim == 1:
    asum = np.sum(a)
    c = - a[:, np.newaxis] * a  # off-diagonal
    cd = a * (asum - a)  # diagonal
    cd_ind = np.diag_indices_from(c)
    c[cd_ind] = cd
    return c / (asum**2 * (asum + 1))
    # else:
    #     return np.array([_cov_dirichlet(a_i) for a_i in a])


# def _neg_logprob_conc(a, x, w, conc_prior):  # ****** local or static class method
#     """Objective function to optimize Dirichlet concentration parameters
#     using observed multinomial data
#     :param a: 1D array with tentative concentration parameters
#     :param x: 2D array with observed count profiles, externally shaped as
#         x[n, k] = k-th element of n-th observed count profile
#         x.shape[-1:] == a.shape
#     :param w: 1D array with weight factors in (0, 1.)
#         len(w) == x.shape[0] == (N,)
#     :param conc_prior: a ConcVector instance
#     :return: nlp = scalar = - w-weighted average of ln p(x_n | a),
#         un-normalized because x remains fixed during learning.
#     """
#     # a[k] = k-th element of a, for x[n, k]
#     # log_multi_beta(a).shape == ()
#     # log_multi_beta(a + x).shape == (len(x),)
#     lp = (np.dot(w, log_multi_beta(a) - log_multi_beta(a + x))
#           # - prior_logprob_conc(a))
#           - conc_prior.logprob(a))
#     # lp = scalar
#     return lp
#
#
# def _d_neg_logprob_conc(a, x, w, conc_prior):
#     """Gradient of _neg_logprob_conc w.r.t given vector of concentration parameters.
#     :param a: 1D array with tentative concentration parameters
#     :param x: 2D array with observed count profiles, externally shaped as
#         x[n, k] = k-th element of n-th observed count profile
#         x.shape[-1:] == a.shape
#     :param w: 1D array with weight factors in (0, 1.)
#         len(w) == x.shape[0] == (N,)
#     :param conc_prior: a ConcVector instance
#     :return: d_nlp = 1D array with
#         d_nlp[k] = d _neg_logprob_conc(a, x, w) / d_a[k]
#         d_nlp.shape == a.shape
#     """
#     # d_log_multi_beta(a).shape == a.shape
#     # d_log_multi_beta(a + x).shape == x.shape
#     dlp = (np.dot(w, d_log_multi_beta(a) - d_log_multi_beta(a + x))
#            - conc_prior.d_logprob(a))
#            # - d_prior_logprob_conc(a))
#     # dlp.shape == a.shape
#     return dlp


# --------------------------------------------------------------- TEST:
if __name__ == '__main__':

    from scipy.optimize import approx_fprime, check_grad
    from EmaCalc import ema_logging
    ema_logging.setup()

    len_conc = 4  # length of concentration vector(s)

    # --------------------------------------------
    print('*** Testing log_multi_beta behavior')
    nx = 5
    nu_prime = 0.5

    def log_l(a, nx, nu):
        """log prob multinomial as function of uniform conc and uniform obs
        :param a: tentative scalar conc value
        :param nx: scalar size of vector
        :param nu: scalar tentative prior param
        :return: log p(a | nx, nu) non-normalized
        """
        a_vec = np.ones(nx)
        a_vec[0] = a
        return (log_multi_beta(a_vec + nu)
                - log_multi_beta(a_vec))
    # --------------------------------------------------

    a = np.linspace(0.1, 5., 50)
    lp_a = np.array([log_l(a_i, nx, nu_prime) for a_i in a])
    print('   a= ', np.array2string(a, precision=3))
    print('lp_a= ', np.array2string(lp_a, precision=3))

    # --------------------------------------------
    # print('*** Testing gradient of log_multi_beta')
    #
    # # ----------------------------------------
    # def test_ln_B(a):
    #     return log_multi_beta(a)
    #
    # def test_d_ln_B(a):
    #     return d_log_multi_beta(a)
    # # -----------------------------------------
    #
    # test_conc = np.arange(len_conc) + 1.
    # print(f'test_conc = {test_conc}')
    # print(f'test_ln_B(test_conc) = {test_ln_B(test_conc)}')
    # print(f'test_ln_B([test_conc]) = {test_ln_B([test_conc])}')
    # print('test_d_ln_B =', test_d_ln_B(test_conc))
    #
    # err = check_grad(test_ln_B, test_d_ln_B, test_conc)
    # print('approx_grad = ', approx_fprime(test_conc,
    #                                       test_ln_B,
    #                                       epsilon=1e-6))
    # print('check_grad err = ', err)

    # --------------------------------------------
    print('\n*** Testing DirichletVector')
    from scipy.stats import dirichlet as scipy_dir

    test_conc = np.array([1., 2., 3., 4.] )
    # test_conc = np.ones(5)

    drv = DirichletVector(test_conc)
    print(f'drv = {drv}')
    print(f'drv.alpha = {drv.alpha}')
    print(f'drv.mean = {drv.mean}')
    if drv.ndim == 1:
        print(f'scipy_dir.mean = {scipy_dir(alpha=test_conc).mean()}')
    print(f'mean(drv.rvs(size=1000) = {np.mean(drv.rvs(size=1000), axis=0)}')

    # print(f'\ndrv.mean_root = {drv.mean_root}')
    # print(f'sqrt(drv.mean) = {np.sqrt(drv.mean)}')
    # print(f'mean(sqrt((drv.rvs(size=1000)) = {np.mean(np.sqrt(drv.rvs(size=1000)), axis=0)}')
    #
    # h2 = drv.mean_square_hellinger(drv)
    # print(f'\ndrv.mean_square_hellinger(drv) = {h2}')
    # r_u = np.sqrt(drv.rvs(size=1000))
    # r_v = np.sqrt(drv.rvs(size=1000))
    # print(f'mean_sample(1 - dot(sqrt(v),sqrt(v))) = {1. - np.mean(np.sum(r_u * r_v, axis=-1))}')
    # print(f'angle Hellinger= {np.arccos(1 - h2) * 180 / np.pi:.1f} degrees')

    print(f'\ndrv.var = {drv.var}')
    if drv.ndim == 1:
        print(f'scipy_dir.var = {scipy_dir(alpha=test_conc).var()}')

    print(f'var(drv.rvs(size=1000) = {np.var(drv.rvs(size=1000), axis=0)}')
    print(f'drv.cov = {drv.cov}')
    print(f'drv.mean_log = {drv.mean_log}')

    print(f'mean(log(drv.rvs(size=1000)) = {np.mean(np.log(drv.rvs(size=1000)), axis=0)}')
    x = drv.rvs()
    print(f'x = drv.rvs() = {x}')
    print(f'drv.logpdf(x) = {drv.logpdf(x)}')
    if drv.ndim == 1:
        print(f'scipy_dir.logpdf(x) = {scipy_dir.logpdf(x, alpha=test_conc)}')
    x = drv.rvs(size=1)
    print(f'x=drv.rvs(size=1) = {x}')
    print(f'drv.logpdf(x) = {drv.logpdf(x)}')
    # print(f'scipy_dir.logpdf(x) = {scipy_dir.logpdf(x, alpha=test_conc)}')  # not allowed
    x = drv.rvs(size=(2, 3))
    print(f'x = drv.rvs(size=(2, 3) = {x}')
    print(f'sum(x) = {np.sum(x, axis=-1)}')
    print(f'drv.logpdf(x) = {drv.logpdf(x)}')
    # print(f'scipy_dir.logpdf(x) = {scipy_dir.logpdf(x, alpha=test_conc)}')  # not allowed
    x[0, 0, 0] += 0.001  # test outside DirichletVector support
    print(f'sum(x) = {np.sum(x, axis=-1)}')
    print(f'drv.logpdf(x) = {drv.logpdf(x)}')
