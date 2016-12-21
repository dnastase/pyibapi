#!/usr/bin/env python3

"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""

from common import Object

class TagValue(Object):
    def __init__(self, tag=None, value=None):
        self.tag = tag
        self.value = value

    def __str__(self):
        return "%s=%s;" % (self.tag, self.value)

 
