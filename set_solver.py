# -*- coding: utf-8 -*-
"""
    set_solver.py
    ~~~~~~~~~~~~~

    Functions for setting up and solving a game of Set
"""

import random


def get_card_collection(dimensions, feature_size, cards):
    """
    Define `dimensions` and `feature_size` parameters of the card space
    `dimensions` indicates the 'width' of cards (how many features)
    `feature_size` indicates the 'depth' of cards (# distinct feature values)
    provide a list of size `cards` from the possible cards
    """
    vocab = list(combinations(dimensions, feature_size, choose=False))
    assert len(vocab) > cards, "Can't return more cards than combinations"
    random.shuffle(vocab)
    return vocab[:cards]


def combinations(dimensions, feature_size, choose=True):
    """
    Provide combinations of width `dimensions` and depth `feature_size`
    If `choose` is True, combinations do not repeat values across dimensions
    Otherwise provide all possible combinations
    """
    result = []

    def _loop(base, layer):
        if len(base) == dimensions:
            result.append(base)
            return

        if choose and base:
            start = base[-1] + 1
        else:
            start = 0

        for i in range(start, feature_size, 1):
            _loop(base + [i], layer + 1)
    _loop([], 0)
    return result


def is_set(potential_set):
    """
    Apply the rules of the game of set:
    feature values in a given dimension of a proposed set
    must all match or all vary (ie, cardinality either 1 or size of input set)
    """

    for dim, _ in enumerate(potential_set[0]):
        s = set([x[dim] for x in potential_set])
        if len(s) not in {1, len(potential_set)}:
            return False
    return True


def solution_generator(deck, dimensions, feature_size, match_size):
    """
    Generator for groups of size `match_size` drawn from `deck`
    all satisfying the rules of Set
    """
    assert all([d in combinations(
        dimensions, feature_size, choose=False)
        for d in deck])
    assert match_size > 0 and match_size < len(deck)

    card_combinations_by_index = combinations(
        match_size, len(deck))
    for combo in card_combinations_by_index:
        cards = [deck[int(i)] for i in combo]
        if is_set(cards):
            yield cards
