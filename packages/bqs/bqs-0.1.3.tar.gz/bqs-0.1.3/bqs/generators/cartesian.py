from itertools import product
from dimod import BinaryQuadraticModel, BINARY


def step_through(iterable_1, iterable_2, values: dict, how_to_address=None):
    """
    Some optimization problems involve Cartesian product between variables. In these cases it is necessary to apply
    terms between successive 'steps' of these vector spaces. A classic example is TSP: distance is defined between
    binary variables from one step in the tour to the next. This helper function takes iterables and steps through the
    Cartesian product space to add the appropriate terms to the QUBO.
    :param iterable_1: first iterable
    :param iterable_2: second iterable
    :param values: values of pairs of iterables
    :param how_to_address: how to construct BQM variable from iterables (default is a string of the form iter1_iter2).
    :return: BQM of Cartesian product between variable groups populated by values dict.
    """
    if not how_to_address:
        how_to_address = lambda a, b: '{}_{}'.format(a, b)

    bqm = BinaryQuadraticModel({}, {}, 0., BINARY)
    iter2_product = list(product(iterable_2, iterable_2))
    for iter1 in range(len(iterable_1)-1):
        for iter2_first, iter2_second in iter2_product:

            v1 = how_to_address(iter2_first, iterable_1[iter1])
            v2 = how_to_address(iter2_second, iterable_1[iter1 + 1])
            bqm.add_interaction(v1, v2, values[iter2_first][iter2_second])

    return bqm
