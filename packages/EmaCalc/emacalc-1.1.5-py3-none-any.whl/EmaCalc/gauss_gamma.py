"""This module implements a multivariate Gaussian distribution of a random vector
with INDEPENDENT ELEMENTS, i.e., diagonal covariance matrix,
and extends the scipy.stats implementations by including Bayesian learning.

*** Classes:
GaussianRV: a trainable Gaussian distribution of a random vector with independent elements,
    defined by a Gaussian mean array, and gamma-distributed precision parameters

GaussianGivenPrecisionRV: class for the random mean vector of a GaussianRV object
PrecisionRV: class for the random precision vector of a GaussianRV object

StudentRV: a multivariate Student-t distribution for a vector with independent elements,
    used for predictive distributions derived from a GaussianRV instance.

*** Version History:
* Version 1.1.3:
2025-03-27, using EmaObject superclass for pretty repr

* Version 1.0.0:
2023-05-02, allow PrecisionRV.a as 1D array, for potential future extension,
            to allow users to set smaller prior inter-individual threshold variance

* Version 0.7.1:
2022-01-19, StudentRV has own property rng, to allow external seed control,
            GaussianRV.predictive, and GaussianGivenPrecision.predictive ordinary methods
            GaussianRV.predictive, and GaussianGivenPrecision.predictive take input rng

* Version 0.7:
2022-01-02, ensure scalar precision shape parameter for EMA usage,
    deactivate GaussianRV.var, cleanup PrecisionRV.mean_inv
    checked connection with predictive StudentRV

* Version 0.6:
2021-12-03, new GaussianRV.initialize method, explicit assignment of precision params

* EmaCalc version 0.5:
2021-10-22, copied PairedCompCalc -> EmaCalc, unchanged
2021-10-22, modified for use in EmaCalc

* Older applications:
2018-08-10, used in general Bayesian mixture models, and package PairedCompCalc
"""
# **** allow array as PrecisionRV.a parameter ? *******

import numpy as np
import logging
from scipy.special import gammaln, psi

from EmaCalc.ema_repr import EmaObject

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # *** TEST


# -------------------------------------------
class GaussianRV(EmaObject):
    """Gaussian distribution of a random 1D (row) array
    with independent elements.
    The probability density function is
    p(x | mu, Lambda) propto prod_d Lambda_d^0.5 exp(- 0.5 (x_d - mu_d)^2 Lambda_d ), where
    mu = (..., mu_d, ...) is the mean array, and
    Lambda=(..., Lambda_d, ...) is the vector of precision values,
        = inverse variance
        = inverse diagonal of covariance matrix.

    To allow Bayesian learning, mu and Lambda are random variables, with
    p(mu, Lambda) = p(mu | Lambda) p(Lambda), where
    p(mu | Lambda) is implemented by a GaussianGivenPrecisionRV instance, and
    p(Lambda) is implemented by a PrecisionRV instance.
    """
    log_2_pi = np.log(2 * np.pi)  # class constant for mean_logpdf calc

    def __init__(self, mean, prec):
        """
        :param mean: GaussianGivenPrecisionRV instance
        :param prec: PrecisionRV instance
        """
        self.mean = mean
        self.prec = prec

    @classmethod
    def initialize(cls,
                   loc,
                   prec_a, prec_b,
                   learned_weight=0.001):
        """Create cls instance with default structure
        :param loc: 1D array-like location vector = mean of mean attribute
        :param prec_a: scalar or 1D array-like precision gamma shape parameter
        :param prec_b: 1D array-like precision gamma inverse-scale parameter
            len(prec_b) == len(loc)
        :param learned_weight: (optional) scalar effective number of observations
            learned_weight = 0. gives a non-informative improper prior density
        """
        prec = PrecisionRV(a=prec_a, b=prec_b)
        mean = GaussianGivenPrecisionRV(loc, learned_weight, prec)
        return cls(mean, prec)

    # def __repr__(self):
    #     property_sep = ',\n\t'
    #     return (self.__class__.__name__ + '(\n\t'
    #             + property_sep.join(f'{k}={repr(v)}'
    #                                 for (k, v) in vars(self).items())
    #             + ')')

    @property
    def loc(self):
        return self.mean.loc

    @property
    def size(self):
        return len(self.loc)

    def mean_logpdf(self, x):
        """E{ ln pdf( x | self ) }, expectation across all parameters of self
        :param x: 1-dim OR M-dim array or array-like list of sample vectors assumed drawn from self
            x[..., :] = ...-th sample row vector
        :return: scalar or array LL, with
            LL[...] = E{ ln pdf( x[..., :] | self ) }
            LL.shape == x.shape[:-1]

        Arne Leijon, 2018-07-08, seems OK,
        slightly less than self.predictive.logpdf, as expected by Jensen's inequality
        """
        x = np.asarray(x)
        if self.mean.learned_weight <= 0.:
            return np.full(x.shape[:-1], -np.inf)
        z2 = np.dot((x - self.loc)**2, self.prec.mean)
        # = Mahanalobis distance, z2.shape == x.shape[:-1]
        return (- z2 - self.size / self.mean.learned_weight
                + np.sum(self.prec.mean_log) - self.size * self.log_2_pi  # np.log(2 * np.pi)
                ) / 2

    def grad_mean_logpdf(self, x):
        """First derivative of self.mean_logpdf(x) w.r.t x
        :param x: 1-dim OR M-dim array or array-like list of sample vectors assumed drawn from self
            x[..., :] = ...-th sample row vector
        :return: array dLL, with
            dLL[..., i] = d E{ ln pdf( x[..., :] | self ) } / d x[..., i]
            dLL.shape == x.shape
        """
        d = np.asarray(x) - self.loc
        return - d * self.prec.mean

    def relative_entropy(self, othr):
        """Kullback-Leibler divergence between self and othr
        :param othr: single instance of same class as self
        :return: scalar KLdiv(q || p) = E_q{ln q(x) / p(x)},
            where q = self and p = othr
        """
        return (self.mean.relative_entropy(othr.mean) +
                self.prec.relative_entropy(othr.prec))

    def predictive(self, rng=None):
        """Predictive distribution of random vector, integrated over parameters.
        :param rng: (optional) random.Generator object
        :return: rv = single StudentRV instance with independent elements

        Scalar Student pdf(x) propto (1 + (1/df) (x-m)^2 / scale^2 )^(- (df + 1) / 2)
        where scale = sqrt{ (1+beta) self.prec.inv_scale / (beta self.prec.shape)
        and Student df = 2* self.prec.shape
        See Leijon EmaCalc report Appendix, or Leijon JASA PairedComp paper appendix
        """
        beta = self.mean.learned_weight
        return StudentRV(loc=self.loc,
                         scale=np.sqrt(self.prec.b * (1. + beta) / (beta * self.prec.a)),
                         df=2 * self.prec.a,
                         rng=rng)

    def adapt(self, x, x_2, w, prior):  # *** special for EmaCalc, not general ***
        """Update distribution parameters using observed data and prior.
        :param x: 2D array with samples assumed drawn from self.
        :param x_2: 2D array with squared sample elements.
        :param w: 1D array with weights of observed samples
        :param prior: prior conjugate distribution, same class as self
        :return: - KLdiv{self || prior)

        Result: updated internal parameters of self
        Method: Leijon EmaCalc report Appendix: sec:GaussGammaUpdate
        """
        self.mean.adapt(x, w, prior=prior.mean)
        self.prec.adapt(x_2, w, prior=prior.prec,
                        new_mean_2=(self.mean.learned_weight * self.mean.loc**2 -
                                    prior.mean.learned_weight * prior.mean.loc**2))
        ll = - self.relative_entropy(prior)
        if self.mean.learned_weight > 0.5:
            logger.debug(f'comp -KLdiv= {ll:.3f}')
            logger.debug(f'comp.mean.learned_weight = {self.mean.learned_weight:.2f}')
            logger.debug('comp.prec.a = ' + np.array_str(np.asarray(self.prec.a),
                                                         precision=2))
            logger.debug('comp.prec.b = ' + np.array_str(self.prec.b,
                                                         precision=2))
            logger.debug('comp.std = ' + np.array_str(np.sqrt(self.prec.mean_inv()),
                                                      precision=2))
        return ll


# ----------------------------------------------------------------------
class GaussianGivenPrecisionRV(EmaObject):
    """Conditional Gaussian distribution of the mean of a Gaussian random vector,
    given the precision array.
    The probability density function is
    p(mu | Lambda) propto prod_d (beta Lambda_d)^0.5 exp(- 0.5 (mu_d - m_d)^2 beta Lambda_d
    where
    mu is a row vector, sample of random vector self
    m is the location of self,
    beta is the scalar learned_weight property
    Lambda is the precision vector.
    """
    def __init__(self, loc, learned_weight, prec):
        """
        Conditional Gaussian vector, given precision matrix
        :param loc: location vector
        :param learned_weight: scalar effective number of learning data
        :param prec: single PrecisionRV instance
        """
        assert np.isscalar(learned_weight), 'learned_weight must be scalar'
        self.loc = np.asarray(loc)
        self.learned_weight = learned_weight
        self.prec = prec

    def __repr__(self):
        return (self.__class__.__name__ + '(' +
                f'loc= {repr(self.loc)}, ' +
                f'learned_weight= {repr(self.learned_weight)}, ' +
                'prec= prec)')

    def adapt(self, x, w, prior):
        """Update distribution parameters using observed data and prior.
        :param x: 2D array or array-like list of sample vectors assumed drawn from self
        :param w: 1D array of weights
            len(w) == x.shape[0]
        :param prior: prior conjugate distribution, same class as self
        :return: None
        Result: updated internal parameters of self
        """
        m = self.loc  # for debug only
        self.learned_weight = prior.learned_weight + np.sum(w)
        sx = prior.learned_weight * prior.loc + np.dot(w, x)
        self.loc = sx / self.learned_weight
        d = self.loc - m  # update change in location
        if self.learned_weight > 0.5:
            logger.debug('comp loc change: '
                         + np.array_str(d, precision=3))

    def relative_entropy(self, othr):
        """Kullback-Leibler divergence between self and othr
        :param othr: single instance of same class as self
        :return: scalar KLdiv[q || p] = E_q{ln q(x) / p(x)},
            where q = self and p = othr
        """
        d = len(self.loc)
        md = self.loc - othr.loc
        beta_pq_ratio = othr.learned_weight / self.learned_weight
        return (othr.learned_weight * np.dot(md**2, self.prec.mean)
                + d * (beta_pq_ratio - np.log(beta_pq_ratio) - 1.)
                ) / 2

    def predictive(self, rng=None):
        """Predictive distribution of self, integrated over self.prec
        p(mu) = integral p(mu | prec) p(prec) d_prec, where
        p(prec) is represented by the PrecisionRV instance self.prec
        :param rng: (optional) random.Generator object
        :return: rv = single StudentRV instance

        Method: see JASA PairedComp paper Appendix
        see also Leijon EmaCalc doc report,
        re-checked 2022-01-01
        """
        beta = self.learned_weight
        return StudentRV(loc=self.loc,
                         scale=np.sqrt(self.prec.b / (self.prec.a * beta)),
                         df=2 * self.prec.a,
                         rng=rng)


# ---------------------------------------------------------------------------
class PrecisionRV:
    """Distribution of the precision vector Lambda of a Gaussian vector
    The probability density function is
    p(Lambda) = prod_d C_d Lambda_d^(a_d - 1) exp(- b_d Lambda_d), i.e., a gamma density,
        where
        a = scalar (or 1D array) shape parameters
        b = 1D array of inverse-scale parameters
        Lambda.shape == b.shape
        a and b must have broadcast-compatible shapes
        C_d = b_d^a / Gamma(a) is the normalization factor
    """
    def __init__(self, a=0., b=1.):
        """
        :param a: scalar or 1D array-like shape parameter(s)
        :param b: 1D array-like with inverse scale parameter(s)
        """
        # assert np.isscalar(a), 'shape parameter should be scalar for EMA usage'
        try:
            a = np.array(a)
            b = np.array(b)
            test = a / b
        except ValueError as e:
            raise RuntimeError('a and b parameters must be broadcast-compatible and > 0. ' + str(e))
        self.a = a
        self.b = b

    def __repr__(self):
        return self.__class__.__name__ + f'(a= {repr(self.a)}, b= {repr(self.b)})'

    @property
    def size(self):
        return self.mean.size

    @property
    def scale(self):
        return 1./self.b

    @property
    def inv_scale(self):
        return self.b

    @property
    def mean(self):
        """E{self}"""
        return self.a / self.b

    def mean_inv(self):  # *** not needed for EMA ?
        """E{ inv(self) }, where
        inv(self) has an inverse-gamma distribution
        """
        if self.a.ndim > 0:
            m = self.b / np.maximum(self.a - 1, np.finfo(float).eps)
            m[self.a <= 1.] = np.nan
            return m
        elif self.a <= 1.:
            return np.full_like(self.b, np.nan)
        else:
            return self.b / (self.a - 1)

    def mode_inv(self):
        """mode{ inv(self) }, where
        inv(self) has an inverse-gamma distribution
        """
        return self.b / (self.a + 1.)

    @property
    def mean_log(self):
        """E{ ln self } element-wise"""
        return psi(self.a) - np.log(self.b)

    def logpdf(self, x):  # ******* not needed for Ema ?  ********
        """ln pdf(x | self)
        :param x: array or array-like list of 2D arrays
        :return: lp = scalar or array, with
            lp[...] = ln pdf(x[..., :] | self)
            lp.shape == x.shape[:-1]
        """
        bx = self.b * np.asarray(x)
        return np.sum((self.a - 1.) * np.log(bx) - bx
                      + np.log(self.b) - gammaln(self.a),
                      axis=-1)

    def adapt(self, x2, w, prior, new_mean_2):
        """Update distribution parameters using observed data and prior.
        :param x2: 2D array or array-like list of squared samples
            for vectors assumed drawn from distribution with precision == self.
        :param w: 1D array with sample weights
        :param prior: prior conjugate distribution, same class as self
        :param new_mean_2: weighted difference (nu * new_loc^2 - nu' * prior_loc^2)
            where nu is the new sum-weight and nu' is the prior sum-weight
        :return: None

        Result: updated internal parameters of self
        Method: Leijon EmaCalc report: sec:GaussGammaUpdate
        """
        self.a = prior.a + np.sum(w) / 2
        # eq:GammaUpdateA
        self.b = prior.b + (np.dot(w, x2) - new_mean_2) / 2
        # eq:GammaUpdateB

    def relative_entropy(q, p):
        """Kullback-Leibler divergence between PrecisionRV q and p,
        :param p: another instance of same class as self = q
        :return: scalar KLdiv( q || p ) = E{ ln q(x)/p(x) }_q

        Arne Leijon, 2018-07-07 copied from gamma.py 2015-10-16
        """
        pb_div_qb = p.b / q.b
        return np.sum(gammaln(p.a) - gammaln(q.a)
                      - p.a * np.log(pb_div_qb)
                      + (q.a - p.a) * psi(q.a)
                      - q.a * (1. - pb_div_qb)
                      )


class StudentRV:
    """Frozen Student distribution of 1D random vector with INDEPENDENT elements
    generalizing scipy.stats.t for vector-valued random variable
    """
    def __init__(self, df, loc=np.array(0.), scale=np.array(1.),
                 rng=None):
        """Create a StudentRV instance
        :param df: scalar or 1D array-like, degrees of freedom
        :param loc: 1D array or array-like list of location elements
        :param scale: scalar or 1D array or array-like list of scale parameter(s)
            df, loc, and scale must have broadcast-compatible shapes
        :param rng: (optional) random.Generator object
        """
        self.df = np.asarray(df)
        self.loc = np.asarray(loc)
        self.scale = np.asarray(scale)
        if rng is None:
            self.rng = np.random.default_rng()
        else:
            self.rng = rng

    def __repr__(self):
        return (self.__class__.__name__
                + f'(df= {repr(self.df)}, '
                + f'loc= {repr(self.loc)}, '
                + f'scale= {repr(self.scale)})')

    @property
    def size(self):
        return self.loc.size  # len(self.loc)

    @property
    def mean(self):
        if self.df.ndim > 0:
            m = self.loc + 0.  # copy
            m[self.df <= 1.] = np.nan
            return m
        elif self.df > 1.:
            return self.loc
        else:
        # if self.df > 1:
        #     return self.loc
        # else:
            return np.full_like(self.loc, np.nan)

    @property
    def var(self):
        """Variance array"""
        if self.df.ndim > 0:
            v = self.scale ** 2 * self.df / np.maximum(self.df - 2., np.finfo(float).eps)
            v[self.df <= 2.] = np.inf
            v[self.df <= 1.] = np.nan
            return v
        elif self.df > 2:  # scalar df
            return self.scale ** 2 * self.df / (self.df - 2.)
        elif self.df > 1:
            return np.full_like(self.loc, np.inf)
        else:
            return np.full_like(self.loc, np.nan)

    def logpdf(self, x):
        """ln pdf(x | self)
        :param x: array or array-like list of sample vectors
            must be broadcast-compatible with self.loc
        :return: lp = scalar or array of logpdf values
            lp[...] = ln pdf[x[..., :] | self)
            lp.shape == x.shape[:-1]
        Arne Leijon, 2018-07-08, **** checked by comparison to scipy.stats.t
        """
        d = (x - self.loc) / self.scale
        return np.sum(- np.log1p(d**2 / self.df) * (self.df + 1) / 2
                      - np.log(self.scale)
                      + gammaln((self.df + 1) / 2) - gammaln(self.df / 2)
                      - 0.5 * np.log(np.pi * self.df),
                      axis=-1)

    def rvs(self, size=None):
        """Random vectors drawn from self.
        :param size: scalar or tuple with number of sample vectors
        :return: x = array of samples
            x.shape == (*size, self.size)
        """
        if size is None:
            s = self.size
        elif np.isscalar(size):
            s = (size, self.size)
        else:
            s = (*size, self.size)
        # z_sc = scipy_t.rvs(df=self.df, size=s)
        z = self.rng.standard_t(df=self.df, size=s)
        # = standardized samples
        return self.loc + self.scale * z


# ------------------------------------------------- TEST
if __name__ == '__main__':
    from scipy.stats import norm
    from scipy.stats import gamma
    from scipy.stats import t as scipy_t  # ******** skip ?
    import copy

    # --------------------------- Test PrecisionRV
    b = np.array([1., 2., 3.])
    nx = 50

    for a in [0.5, 10., [3., 2., 1.]]:
        g = PrecisionRV(a=a, b=b)
        print(f'\n*** Testing {g}:')
        # x = np.array([gamma(a=a, scale=1/b_i).rvs(size=nx)
        #               for b_i in b]).T
        x = gamma(a=a, scale=1/b).rvs(size=(nx, len(b)))
        print(f'mean= {g.mean}')
        print(f'mean_inv= {g.mean_inv()}')
        print(f'mode_inv= {g.mode_inv()}')
        print(f'gamma samples x[:10]= {x[:10]}')
        print(f'mean(x)= {np.mean(x, axis=0)}')
        print(f'PrecisionRV.logpdf(x)= {g.logpdf(x)}')
        # g_ll = np.array([np.sum([gamma(a=a, scale=1/b_i).logpdf(x_si)
        #                          for (b_i, x_si) in zip(b, x_s)])
        #                  for x_s in x])
        g_ll = np.sum(gamma(a=a, scale=1/b).logpdf(x),
                      axis=-1)
        print(f'scipy gamma.logpdf(x)= {g_ll}')

    # --------------------------- Test StudentRV
    df = 10.
    m = [1., 2., 3.]
    s = [3., 2., 1.]
    for df in [0.5, 1.5, 10., [2., 3., 4.]]:
        st = StudentRV(df=df, loc=m, scale=s)
        print(f'\n*** Testing {st}')
        print(f'mean= {st.mean}')
        print(f'var= {st.var}')
        # scipy_x = np.array([scipy_t.rvs(df=df, loc=m_i, scale=s_i, size=nx)
        #                     for (m_i, s_i) in zip(m, s)]).T
        scipy_x = scipy_t.rvs(df=df, loc=m, scale=s, size=(nx, len(m)))
        print(f'scipy_t samples x[:10]= {scipy_x[:10]}')
        print(f'mean(x)= {np.mean(scipy_x, axis=0)}')

        print(f'StudentRV.rvs() = {st.rvs()}')
        x = st.rvs(size=[nx])
        print(f'StudentRV.rvs(size=[nx]) = x[:10] = {x[:10]}')
        print(f'mean(x)= {np.mean(x, axis=0)}')
        print(f'StudentRV.logpdf(x)= {st.logpdf(x)}')
        # st_ll = np.array([np.sum([scipy_t(df=df, loc=m_i, scale=s_i).logpdf(x_si)
        #                          for (m_i, s_i, x_si) in zip(m, s, x_s)])
        #                  for x_s in x])
        st_ll = np.sum(scipy_t(df=df, loc=m, scale=s).logpdf(x),
                       axis=-1)
        print(f'scipy_t.logpdf(x)= {st_ll}')

    # --------------------------- Test GaussianRV
    scale = np.array([1., 2., 3.])
    prec_a = 1.1
    prec_b = prec_a * scale**2
    g = GaussianRV.initialize(loc=[0., 1., 2.],
                              prec_a=prec_a, prec_b=prec_b,
                              learned_weight=2.01)
    print(f'\n*** Testing {g}')
    print(f'\n* g.predictive = {g.predictive()}')
    print(f'g.predictive.var = \n{g.predictive().var}')
    print(f'g.prec.mean= \n{g.prec.mean}')
    print(f'g.prec.mean_inv= \n{g.prec.mean_inv()}')

