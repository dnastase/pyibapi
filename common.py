#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


from utils import Enum
from utils import Object


NO_VALID_ID = -1
MAX_MSG_LEN = 0xFFFFFF # 16Mb - 1byte

 
TickerId = int
OrderId  = int
TagValueList = list

faDataType = int
faDataTypeEnum = Enum("GROUPS", "PROFILES", "ALIASES")

MarketDataType = int
MarketDataTypeEnum = Enum("REALTIME", "FROZEN", "DELAYED", "DELAYED_FROZEN")


class BarData(Object):
    def __init__(self):
        date = ""
        open = 0. 
        high = 0. 
        low = 0. 
        close = 0. 
        volume = 0
        average = 0.
        hasGaps = "" 
        barCount = 0

    def __str__(self):
        return "%s:%f,%f,%f,%f,%d,%f,%d,%d" % (self.date, self.open, self.high,
            self.low, self.close, self.volume, self.average, self.hasGaps,
            self.barCount)


class TickAttrib(Object):
    def __init__(self):
        self.canAutoExecute = False 
        self.pastLimit = False

    def __str__(self):
        return "%d,%d" % (self.canAutoExecute, self.pastLimit)


class FamilyCode(Object):
    def __init__(self):
        self.accountID = ""
        self.familyCodeStr = ""

    def __str__(self):
        return "%s,%s" % (self.accountID, self.familyCodeStr)

 
