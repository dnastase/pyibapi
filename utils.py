#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


"""
Collection of misc tools
"""


import sys
from logger import LOGGER


def crt_fn_name(parent_idx = 0):
    #depth is 1 bc this is already a fn, so we need the caller
    return sys._getframe(1 + parent_idx).f_code.co_name


def setattr_log(self, var_name, var_value):
    #import code; code.interact(local=locals())
    LOGGER.debug("%s %s %s %s", self.__class__, id(self), var_name, var_value)
    super(self.__class__, self).__setattr__(var_name, var_value)


def test_setattr_log():
    class A:
        def __init__(self):
            self.n = 5

    A.__setattr__ = setattr_log
    a = A()
    print(a.n)
    a.n = 6
    print(a.n)


def test_poly():
    class A:
        def __init__(self):
            self.n = 5
        def m(self):
            self.n += 1
    class B(A):
        def m(self):
            self.n += 2

    o = B()
    import code; code.interact(local=locals())


if __name__ == "__main__":
    #test_setattr_log()
    test_poly()
 
