from dimod import BinaryQuadraticModel, SPIN, BINARY
from itertools import combinations


def k_hot(bqm_vars: list, k=1., scale=1., method='standard', lamb=1.):
    """
    Generator for k-hot constraints from list of BQM variables.
    :param bqm_vars: list of BQM variables.
    :param k: number of variables to select.
    :param scale: (optional) scale of the k-hot constraint, default = 1.
    :param method: which generator to use for constraint, default = 'standard'.
    :param lamb: size of domain wall (for domain wall encoding only).
    :return: dimod BinaryQuadraticModel implementing k-hot constraint on bqm_vars.
    """

    methods = {'standard'}
    try:
        assert k < len(bqm_vars)
    except AssertionError:
        raise ValueError("k ({}) must be less than the number of variables given ({}).".format(k, len(bqm_vars)))
    try:
        assert k == int(k) or k == 1/2.
    except AssertionError:
        raise ValueError("k should be either an integer or 1/2.")

    try:
        assert method in methods
    except AssertionError:
        raise NotImplementedError("Method {} not implemented. Use one of {}".format(method, methods))

    if method == 'standard':
        return standard_k_hot(bqm_vars, k, scale)
    elif method == 'domain_wall':
        return domain_wall_k_hot(bqm_vars, k, scale, lamb)


def standard_k_hot(bqm_vars: list, k, scale):
    """
    Standard BQM generator for k-hot constraints.
    :param bqm_vars: list of BQM variables.
    :param k: number of variables to select.
    :param scale: (optional) scale of the k-hot constraint, default = 1.
    :return: dimod BinaryQuadraticModel implementing k-hot constraint on bqm_vars.
    """

    k_hot_bqm = BinaryQuadraticModel({}, {}, k**2, BINARY)

    for var1, var2 in combinations(bqm_vars, 2):
        k_hot_bqm.add_interaction(var1, var2, 2)

    for bqm_var in bqm_vars:
        k_hot_bqm.add_variable(bqm_var, 1-2*k)

    k_hot_bqm.scale(scale)
    return k_hot_bqm


def domain_wall_k_hot(bqm_vars: list, k, scale, lamb):
    """
    Domain wall encoding for k-hot constraints (k copies of the domain wall encoding for one-hot constraints).
    :param bqm_vars: list of BQM variables.
    :param k: number of variables to select.
    :param scale: (optional) scale of the k-hot constraint, default = 1.
    :param lamb: size of domain wall (for domain wall encoding only).
    :return: dimod BinaryQuadraticModel implementing k-hot constraint on bqm_vars.
    """
    raise NotImplementedError("Domain wall encoding for k-hot constraints not implemented yet.")
