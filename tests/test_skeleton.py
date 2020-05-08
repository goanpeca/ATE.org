# -*- coding: utf-8 -*-

import pytest
from ATE.skeleton import fib

__author__ = "Tom Hören"
__copyright__ = "Tom Hören"
__license__ = "gpl2"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
