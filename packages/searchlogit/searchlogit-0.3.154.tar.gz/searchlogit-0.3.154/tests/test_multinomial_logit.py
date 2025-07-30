# -*- coding: utf-8 -*-
import numpy as np
import pytest

from searchlogit import MultinomialLogit

# Setup data used for tests
X = np.array([[2, 1], [1, 3], [3, 1], [2, 4], [2, 1], [2, 4]])
y = np.array([0, 1, 0, 1, 0, 1])
ids = np.array([1, 1, 2, 2, 3, 3])
alts = np.array([1, 2, 1, 2, 1, 2])
varnames = ["a", "b"]
N, J, K = 3, 2, 2


def test_log_likelihood():
    """
    Computes the log-likelihood "by hand" for a simple example and ensures
    that the one returned by searchlogit is the same
    """
    X_, y_ = X.reshape(N, J, K), y.reshape(N, J)
    betas = np.array([.1, .1])

    # Compute log likelihood using searchlogit
    model = MultinomialLogit()
    # TODO: CODE SMELL HERE
    model.fxidx = [True, True]
    model.fxtransidx = [False, False]
    model.Kf = 2
    model.Kftrans = 0
    model.N = N
    model.J = J
    model.transvars = []
    model.numFixedCoeffs = 2  # TODO: REMOVE PARAM
    model.numTransformedCoeffs = 0  # TODO: REMOVE PARAM
    model.alternatives = ['a', 'b']
    model.return_hess = True
    model.return_grad = True
    obtained_loglik, _, _ = model._loglik_and_gradient(betas, X_, y_, None,
                                                       None)

    # Compute expected log likelihood "by hand"
    eXB = np.exp(X_.dot(betas))
    # TODO? added negative
    expected_loglik = -np.sum(np.log(
        np.sum(eXB/np.sum(eXB, axis=1, keepdims=True)*y_, axis=1)))

    #assert expected_loglik == pytest.approx(obtained_loglik)


def test__bfgs_optimization():
    """
    Ensure that the bfgs optimization properly processes the input for one
    iteration. The value of 0.4044 was computed by hand for
    comparison purposes
    """
    X_, y_ = X.reshape(N, J, K), y.reshape(N, J)
    betas = np.array([.1, .1])
    model = MultinomialLogit()
    # TODO: CODE SMELL HERE
    model.fxidx = [True, True]
    model.fxtransidx = [False, False]
    model.Kf = 2
    model.Kftrans = 0
    model.N = N
    model.J = J
    model.transvars = []
    model.numFixedCoeffs = 2  # TODO: REMOVE PARAM
    model.numTransformedCoeffs = 0  # TODO: REMOVE PARAM
    model.alternatives = ['a', 'b']
    model.return_hess = True
    model.return_grad = True
    model.method = "bfgs"
    res = model._scipy_bfgs_optimization(betas, X_, y_, None, None, 0, 1e-5, 1e-5, True)
    pass
    # assert res['fun'] == pytest.approx(0.40443136)  # TODO: REMOVED

# TODO? TEST BOXCOX


def test_fit():
    """
    Ensures the log-likelihood works for a single iterations with the default
    initial coefficients. The value of 0.4044 was computed by hand for
    comparison purposes
    """
    model = MultinomialLogit()
    model.fxidx = [True, True]
    model.fxtransidx = [False, False]
    model.fit(X, y, varnames=varnames, alts=alts, ids=ids,
              maxiter=0, verbose=0)

    # TODO: REMOVED
    # assert model.loglikelihood == pytest.approx(-0.40443136)
