#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""

from object_implem import Object 


class CommissionReport(Object):

    def __init__(self):
        self.execId = ""
        self.commission = 0. 
        self.currency = ""
        self.realizedPNL =  0.
        self.yield_ = 0.
        self.yieldRedemptionDate = 0  # YYYYMMDD format
 
