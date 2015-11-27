# -*- coding: utf-8 -*-
"""
    test_set_solver.py
    ~~~~~~~~~~~~~~~~~~

    Tests for set solver module
"""

import itertools
import pytest
from math import factorial
import set_solver


def n_choose_r(n, r):
    return factorial(n) / factorial(r) / factorial(n - r)


def _as_hashable(set_):
    list_ = list(set_)
    list_.sort()
    return str(list_)


@pytest.mark.unit
def test_choose_combinations():
    for i, j in zip(range(3, 5), range(8, 14, 2)):
        combos = set_solver.combinations(i, j)
        alternative_combos = map(list, itertools.combinations(range(j), i))
        combo_set = set(map(_as_hashable, combos))
        # does this match the combinatoric expectation?
        assert len(combos) == n_choose_r(j, i)
        # are all entries unique?
        assert len(combos) == len(combo_set)
        # does this match the response from python core?
        assert combo_set == set(
            map(_as_hashable, alternative_combos)
        )
        assert all([c in alternative_combos for c in combos])


@pytest.mark.unit
def test_full_combinations():
    for i, j in zip(range(3, 5), range(8, 14, 2)):
        combos = set_solver.combinations(i, j, choose=False)
        # is result proper size to include all values for all positions?
        assert len(combos) == j ** i
        # is result free of duplicates?
        assert len(combos) == len(set(map(str, combos)))


@pytest.mark.unit
def test_get_card_collection():
    assert len(set_solver.get_card_collection(3, 3, 12)) == 12
    with pytest.raises(AssertionError):
        set_solver.get_card_collection(3, 3, 120)


@pytest.mark.unit
def test_solver_input_validation(deck3x4):
    with pytest.raises(AssertionError):
        set_solver.solution_generator(deck3x4, 4, 5, 6).next()

    with pytest.raises(AssertionError):
        set_solver.solution_generator(deck3x4, 3, 4, 0).next()

    with pytest.raises(AssertionError):
        set_solver.solution_generator(deck3x4, 3, 4, 20).next()


@pytest.mark.integration
def test_sizes(deck3x4, deck4x5):
    match_size = 4
    size_4_sets = list(set_solver.solution_generator(
        deck3x4, dimensions=3, feature_size=4, match_size=match_size))

    assert size_4_sets == [
        [[3, 1, 1], [2, 0, 3], [0, 2, 0], [1, 3, 2]],
        [[3, 1, 1], [0, 1, 0], [2, 1, 2], [1, 1, 3]]
    ]
    for entry, cardinalities in zip(
        size_4_sets,
        [[match_size, match_size, match_size], [match_size, 1, match_size]]
    ):
        for dim in range(3):
            assert len(set([card[dim] for card in entry])) \
                == cardinalities[dim]

    match_size = 5
    dimensions = 4
    size_5_sets = list(set_solver.solution_generator(
        deck4x5, dimensions=dimensions, feature_size=5, match_size=match_size))
    assert size_5_sets == [
        [[3, 2, 1, 2], [0, 0, 3, 3], [2, 3, 2, 1], [4, 1, 4, 0], [1, 4, 0, 4]]
    ]

    for entry, cardinalities in zip(size_5_sets, [[match_size] * dimensions]):
        for dim in range(4):
            assert len(set([card[dim] for card in entry])) \
                == cardinalities[dim]

    assert all(map(set_solver.is_set, size_4_sets + size_5_sets))

    assert not list(set_solver.solution_generator(
        deck3x4, dimensions=3, feature_size=4, match_size=5))
