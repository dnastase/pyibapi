#!/usr/bin/env python3

"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""

from common import UNSET_INTEGER, UNSET_DOUBLE


class OrderState:

    def __init__(self):
      self.status= ""
      self.initMargin= ""
      self.maintMargin= ""
      self.equityWithLoan= ""

      self.commission = UNSET_DOUBLE      # type: float
      self.minCommission = UNSET_DOUBLE   # type: float
      self.maxCommission = UNSET_DOUBLE   # type: float
      self.commissionCurrency = ""
      self.warningText = ""

