#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""

from utils import Object


class ScanData(Object):
    def __init__(self):
        contract = None
        rank = 0
        distance = ""
        benchmark = ""
        projection = ""
        legsStr = ""

    def __str__(self):
        return "%s,%d,%s,%s,%s,%s" % (self.contract, self.rank, self.distance,
            self.benchmark, self.projection, self.legsStr)
 
NO_ROW_NUMBER_SPECIFIED = -1

class ScannerSubscription(Object):

    def __init__(self):
        self.numberOfRows = NO_ROW_NUMBER_SPECIFIED
        self.instrument = ""
        self.locationCode = ""
        self.scanCode =  ""
        self.abovePrice = None
        self.belowPrice = None
        self.aboveVolume = None
        self.marketCapAbove = None
        self.marketCapBelow = None
        self.moodyRatingAbove =  ""
        self.moodyRatingBelow =  ""
        self.spRatingAbove =  ""
        self.spRatingBelow =  ""
        self.maturityDateAbove =  ""
        self.maturityDateBelow =  ""
        self.couponRateAbove = None
        self.couponRateBelow = None 
        self.excludeConvertible = 0
        self.averageOptionVolumeAbove = 0
        self.scannerSettingPairs =  ""
        self.stockTypeFilter =  ""
     