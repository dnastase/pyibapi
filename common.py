#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""

#TODO: is it correct or it needs buffer ?
 
TickerId = int
OrderId  = int

class TickAttrib:
    def __init__(self):
        self.canAutoExecute = False 
        self.pastLimit = False
