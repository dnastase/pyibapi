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


class Object(object):

    def __str__(self):
        return "Object"

    def __repr__(self):
        return self.__str__()


class BadMessage(Exception):
    def __init__(self, text):
        self.text = text


class Enum:
    def __init__(self, *args):
        self.idx2name = {}
        for (idx, name) in enumerate(args):
            setattr(self, name, idx)
            self.idx2name[idx] = name

    def to_str(self, idx):
        return self.idx2name.get(idx, "NOTFOUND")


def test_enum():
    e = Enum("ZERO", "ONE", "TWO")
    print(e.ZERO)
    print(e.to_str(e.ZERO))


def crt_fn_name(parent_idx = 0):
    #depth is 1 bc this is already a fn, so we need the caller
    return sys._getframe(1 + parent_idx).f_code.co_name


def setattr_log(self, var_name, var_value):
    #import code; code.interact(local=locals())
    LOGGER.debug("%s %s %s=|%s|", self.__class__, id(self), var_name, var_value)
    super(self.__class__, self).__setattr__(var_name, var_value)


SHOW_UNSET = True
def decode(the_type, fields, show_unset = False):
    try:
        s = next(fields)
    except StopIteration:
        raise BadMessage()  

    LOGGER.debug("decode %s %s", the_type, s)

    if the_type is str:
        if type(s) is str:
            return s
        elif type(s) is bytes:
            return s.decode()
        else:
            raise TypeError("unsupported type " + type(s))
    
    orig_type = the_type
    if the_type is bool:
        the_type = int
        
    if show_unset:
        if s is None or len(s) == 0:
            n = None
        else:
            n = the_type(s)
    else:
        n = the_type(s or 0)

    if orig_type is bool:
        n = False if n == 0 else True

    return n

 
def test_setattr_log():
    class A:
        def __init__(self):
            self.n = 5

    A.__setattr__ = setattr_log
    a = A()
    print(a.n)
    a.n = 6
    print(a.n)


def test_polymorphism():
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
    #test_poly()
    test_enum()
 
