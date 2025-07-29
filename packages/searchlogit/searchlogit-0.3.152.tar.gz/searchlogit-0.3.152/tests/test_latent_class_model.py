import numpy as np

# import pytest
from searchlogit import LatentClassModel, device

device.disable_gpu_acceleration()

# Setup data used for tests
X = np.array([[2, 1], [1, 3], [3, 1], [2, 4], [2, 1], [2, 4]])
y = np.array([0, 1, 0, 1, 0, 1])
# ids = np.array([1, 1, 2, 2, 3, 3])
# alts = np.array([1, 2, 1, 2, 1, 2])
# panels = np.array([1, 1, 1, 1, 2, 2])
# varnames = ["a", "b"]
# randvars = {'a': 'n', 'b': 'n'}
# N, J, K, R = 3, 2, 2, 5


def test_fit():
    pass

def test_log_likelihood():
    pass

def test_fit():
    pass

def test_validate_inputs():
    pass

def test_gpu_not_available():
    pass
