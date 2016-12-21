#!/usr/bin/env python3

"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


from utils import Object

 
class SoftDollarTier(Object):
    def __init__(self, name = "", val = "", displayName = ""):
        self.name = name
        self.val = val
        self.displayName = displayName

    def __str__(self):
        return "%s=%s,%s" % (self.name, self.val, self.displayName)
