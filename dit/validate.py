#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Centralized location to store validation functions.

"""
import numpy as np

from .math import close
from .exceptions import (
    ditException,
    InvalidNormalization,
    InvalidOutcome,
    InvalidProbability,
)

__all__ = [
    'is_pmf',
    'validate_normalization',
    'validate_outcomes',
    'validate_probabilities',
    'validate_sequence'
]

def is_pmf(pmf, ops):
    """
    Returns `True` if the pmf is valid.

    Parameters
    ----------
    pmf : array-like
        The probability mass function of the distribution.
    ops : operations
        The object which abstracts log and non-log operations.

    Returns
    -------
    v : bool
        `True` if the pmf is valid.

    Raises
    ------
    InvalidNormalization
        When the distribution is not properly normalized.
    InvalidProbability
        When a pmf value is not between 0 and 1, inclusive.

    """
    try:
        validate_normalization(pmf, ops)
    except InvalidNormalization:
        return False

    try:
        validate_probabilities(pmf, ops)
    except InvalidProbability:
        return False

    return True

def validate_normalization(pmf, ops):
    """
    Returns `True` if the distribution is properly normalized.

    Parameters
    ----------
    pmf : array-like
        The probability mass function of the distribution.
    ops : operations
        The object which abstracts log and non-log operations.

    Returns
    -------
    v : bool
        `True` if the distribution is properly normalized.

    Raises
    ------
    InvalidNormalization
        When the distribution is not properly normalized.

    """
    # log_func is the identity function for non-log distributions.
    log = ops.log
    one = ops.one

    # Make sure the distribution is normalized properly.
    total = ops.add_reduce( pmf )
    if not close(total, one):
        raise InvalidNormalization(total)

    return True

def validate_outcomes(outcomes, sample_space):
    """
    Returns `True` if every outcome is in the sample space.

    Implicitly, this also verifies that every outcome is of the same class
    and that their lengths are the same too.  It does not verify that the
    items are indexable though.

    Parameters
    ----------
    outcomes : list
        The outcomes that will be checked against the sample space.
    sample_space : iterable
        An iterable over the sample space.

    Returns
    -------
    v : bool
        `True` if the outcomes are in the sample space.

    Raises
    ------
    InvalidOutcome
        When an outcome is not in the sample space.

    """
    # Make sure the outcomes are in the outcome space.
    outcomes = set(outcomes)
    sample_space = set(sample_space)
    bad = outcomes.difference(sample_space)
    L = len(bad)
    if L == 1:
        raise InvalidOutcome(bad, single=True)
    elif L:
        raise InvalidOutcome(bad, single=False)

    return True

def validate_probabilities(pmf, ops):
    """
    Returns `True` if the pmf values are probabilities.

    Parameters
    ----------
    pmf : array-like
        The probability mass function of the distribution.
    ops : operations
        The object which abstracts log and non-log operations.

    Returns
    -------
    v : bool
        `True` if the pmf vlaies are probabilities.

    Raises
    ------
    InvalidProbability
        When a pmf value is not between 0 and 1, inclusive.

    """
    one = ops.one
    zero = ops.zero

    # Make sure the values are in the correct range.
    # Recall ops.zero = +inf for bases less than 1.
    #        ops.zero = -inf for bases greater than 1.
    too_low = pmf < min(zero, one)
    too_high = pmf > max(zero, one)
    if too_low.any() or too_high.any():
        bad = pmf[ np.logical_or(too_low, too_high) ]
        raise InvalidProbability( bad, ops=ops )

    return True

def validate_sequence(outcome):
    """
    Returns `True` if outcome is a sequence, and `False` otherwise.

    Parameters
    ----------
    outcome : outcome
        The outcome to be tested.

    Raises
    ------
    InvalidOutcome
        When the class of the outcome is not a sequence.

    """
    from collections import Sequence
    if not isinstance(outcome, Sequence):
        raise ditException('Outcome class is not a sequence.')
    else:
        return True
