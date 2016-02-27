import numpy

from difflib import SequenceMatcher


def similarity(a, b):
    """
    Determines the similarity of two strings.

    :param a: first string
    :param b: second string
    :return: float value in the range from 0 to 1
             0.0 means no similarity
             1.0 means the strings are equal
    """
    return SequenceMatcher(None, a, b).ratio()


def median(lst):
    """
    not necessarily an int!

    :param lst: List of numeric values
    """
    return numpy.median(numpy.array(lst))
