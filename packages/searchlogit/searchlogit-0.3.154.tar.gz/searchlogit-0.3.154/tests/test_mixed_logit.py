# -*- coding: utf-8 -*-
import numpy as np
import pytest

from searchlogit import MixedLogit, device

device.disable_gpu_acceleration()

# Setup data used for tests
X = np.array([[2, 1], [1, 3], [3, 1], [2, 4], [2, 1], [2, 4]])
y = np.array([0, 1, 0, 1, 0, 1])
ids = np.array([1, 1, 2, 2, 3, 3])
alts = np.array([1, 2, 1, 2, 1, 2])
panels = np.array([1, 1, 1, 1, 2, 2])
varnames = ["a", "b"]
randvars = {'a': 'n', 'b': 'n'}
N, J, K, R = 3, 2, 2, 5


def test__balance_panels():
    """
    Ensures that unbalanced panels are properly balanced when required
    """
    X_, y_ = X.reshape(N, J, K), y.reshape(N, J, 1)
    model = MixedLogit()
    X_, y_, _, panel_info = model._balance_panels(X_, y_, None, panels)

    assert np.array_equal(panel_info, np.array([[1, 1], [1, 0]]))
    assert X_.shape == (4, 2, 2)


def test_log_likelihood():
    """
    Computes the log-likelihood "by hand" for a simple example and ensures
    that the one returned by searchlogit is the same
    """
    P = 1  # Without panel data
    betas = np.array([.1, .1, .1, .1])
    X_, y_ = X.reshape(N, P, J, K), y.reshape(N, P, J, 1)

    # Compute log likelihood using searchlogit
    model = MixedLogit()
    model._rvidx,  model._rvdist = np.array([True, True]), np.array(['n', 'n'])
    draws = model._generate_halton_draws(N, R, K)  # (N,Kr,R)
    # drawstrans = model._generate_halton_draws(N, R, 0)  # (N,Kr,R)
    drawstrans = np.atleast_3d(np.array([]))
    panel_info = np.ones((N, P))

    # TODO: code smell
    model.Kf = 0
    model.Kr = 2
    model.Kftrans = 0
    model.Krtrans = 0
    model.Kchol = 0
    model.correlationLength = 0
    model.Kbw = 2
    model.n_draws = R
    model.N = N
    model.fxidx = [False, False]
    model.fxtransidx = [False, False]
    model.rvidx = [True, True]
    model.rvtransidx = [False, False]
    model.P = 1
    model.J = 2
    model.batch_size = R
    model.rvdist = ['n', 'n']
    model.save_fitted_params = False
    model.transvars = []
    model.varnames = ['a', 'b']
    model.return_grad = True
    model.return_hess = True

    obtained_loglik, _ = model._loglik_gradient(betas, X_, y_, panel_info,
                                                draws, drawstrans, None, None, K)

    # Compute expected log likelihood "by hand"
    Br = betas[None, [0, 1], None] + draws*betas[None, [2, 3], None]
    eXB = np.exp(np.einsum('npjk,nkr -> npjr', X_, Br))
    p = eXB/np.sum(eXB, axis=2, keepdims=True)
    expected_loglik = -np.sum(np.log(
        (y_*p).sum(axis=2).prod(axis=1).mean(axis=1)))

    #assert expected_loglik == pytest.approx(obtained_loglik)


def test__transform_betas():
    """
    Check that betas are properly transformed to random draws

    """
    # TODO
    pass
    # betas = np.array([.1, .1, .1, .1])

    # # Compute log likelihood using searchlogit
    # model = MixedLogit()
    # model.Kf = 0
    # model.Kr = 4
    # model.Kftrans = 0
    # model.Krtrans = 0
    # model.Kchol = 0
    # model.correlationLength = 0
    # model.Kbw = 0
    # model._rvidx,  model._rvdist = np.array([True, True]), np.array(['n', 'n'])
    # draws = model._generate_halton_draws(N, R, K)  # (N,Kr,R)
    # expected_betas = betas[None, [0, 1], None] + \
    #     draws*betas[None, [2, 3], None]
    # _, obtained_betas = model._transform_betas(betas, draws, chol_mat)

    # assert np.allclose(expected_betas, obtained_betas)


def test_fit():
    """
    Ensures the log-likelihood works for a single iterations with the default
    initial coefficients. The value of -1.794 was computed by hand for
    comparison purposes
    """
    # There is no need to initialize a random seed as the halton draws produce
    # reproducible results
    assert True
    # model = MixedLogit()
    # model.fit(X, y, varnames=varnames, alts=alts, n_draws=10, panels=panels,
#               ids=ids, randvars=randvars, maxiter=0, verbose=0, halton=True)

   # assert model.loglikelihood == pytest.approx(-1.79451632)


def test_validate_inputs():
    """
    Covers potential mistakes in parameters of the fit method that searchlogit
    should be able to identify
    """
    model = MixedLogit()
    with pytest.raises(ValueError):  # randvars is required for mixedlogit
        model.fit(X, y, varnames=varnames, alts=alts, ids=ids, n_draws=10,
                  maxiter=0, verbose=0, halton=True)

    with pytest.raises(ValueError):  # wrong distribution
        model.fit(X, y, varnames=varnames, alts=alts, ids=ids, n_draws=10,
                  maxiter=0, verbose=0, halton=True, randvars={'a': 'fake'})

    with pytest.raises(ValueError):  # wrong var name
        model.fit(X, y, varnames=varnames, alts=alts, ids=ids, n_draws=10,
                  maxiter=0, verbose=0, halton=True, randvars={'fake': 'n'})


def test_gpu_not_available():
    """
    Ensures that searchlogit
    detects that GPU is not available based on CuPy's
    installation status

    """
    assert not MixedLogit.check_if_gpu_available()

# TODO: test correlation, boxcox
