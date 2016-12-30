#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


import sys
sys.path.append("../../../source/pythonclient")
#TODO: rm this
sys.path.append("../pythonclient")


from object_implem import Object
from tag_value import TagValue
from order import Order


class AvailableAlgoParams(Object):
    #! [arrivalpx_params]
    @staticmethod
    def FillArrivalPriceParams(baseOrder:Order, maxPctVol:float, 
                    riskAversion:str, startTime:str, endTime:str, 
                    forceCompletion:bool, allowPastTime:bool):
        baseOrder.algoStrategy = "ArrivalPx"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("maxPctVol", maxPctVol))
        baseOrder.algoParams.append(TagValue("riskAversion", riskAversion))
        baseOrder.algoParams.append(TagValue("startTime", startTime))
        baseOrder.algoParams.append(TagValue("endTime", endTime))
        baseOrder.algoParams.append(TagValue("forceCompletion",
                                             int(forceCompletion)))
        baseOrder.algoParams.append(TagValue("allowPastEndTime",
                                             int(allowPastTime)))
    #! [arrivalpx_params]

    #! [darkice_params]
    @staticmethod
    def FillDarkIceParams(baseOrder:Order, displaySize:int, startTime:str,
                          endTime:str, allowPastEndTime:bool):
        baseOrder.algoStrategy = "DarkIce"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("displaySize", displaySize))
        baseOrder.algoParams.append(TagValue("startTime", startTime))
        baseOrder.algoParams.append(TagValue("endTime", endTime))
        baseOrder.algoParams.append(TagValue("allowPastEndTime",
                                             int(allowPastEndTime)))
    #! [darkice_params]

    #! [pctvol_params]
    @staticmethod
    def FillPctVolParams(baseOrder:Order, pctVol:float, startTime:str,
                        endTime:str, noTakeLiq:bool):
        baseOrder.algoStrategy = "PctVol"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("pctVol", pctVol))
        baseOrder.algoParams.append(TagValue("startTime", startTime))
        baseOrder.algoParams.append(TagValue("endTime", endTime))
        baseOrder.algoParams.append(TagValue("noTakeLiq", int(noTakeLiq)))
    #! [pctvol_params]

    #! [twap_params]
    @staticmethod
    def FillTwapParams(baseOrder:Order, strategyType:str, startTime:str,
                        endTime:str, allowPastEndTime:bool):
        baseOrder.algoStrategy = "Twap"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("strategyType", strategyType))
        baseOrder.algoParams.append(TagValue("startTime", startTime))
        baseOrder.algoParams.append(TagValue("endTime", endTime))
        baseOrder.algoParams.append(TagValue("allowPastEndTime",
                                             int(allowPastEndTime)))
    #! [twap_params]

    #! [vwap_params]
    @staticmethod
    def FillVwapParams(baseOrder:Order, maxPctVol:float, startTime:str,
                        endTime:str, allowPastEndTime:bool, noTakeLiq:bool):
        baseOrder.algoStrategy = "Vwap"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("maxPctVol", maxPctVol))
        baseOrder.algoParams.append(TagValue("startTime", startTime))
        baseOrder.algoParams.append(TagValue("endTime", endTime))
        baseOrder.algoParams.append(TagValue("allowPastEndTime",
                                             int(allowPastEndTime)))
        baseOrder.algoParams.append(TagValue("noTakeLiq", int(noTakeLiq)))
    #! [vwap_params]

    #! [ad_params]
    @staticmethod
    def FillAccumulateDistributeParams(baseOrder:Order, componentSize:int, 
            timeBetweenOrders:int, randomizeTime20:bool, randomizeSize55:bool,
            giveUp:int, catchUp:bool, waitForFill:bool, startTime:str, 
            endTime:str):
        baseOrder.algoStrategy = "AD"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("componentSize", componentSize))
        baseOrder.algoParams.append(TagValue("timeBetweenOrders", timeBetweenOrders))
        baseOrder.algoParams.append(TagValue("randomizeTime20",
                                             int(randomizeTime20)))
        baseOrder.algoParams.append(TagValue("randomizeSize55",
                                             int(randomizeSize55)))
        baseOrder.algoParams.append(TagValue("giveUp", giveUp))
        baseOrder.algoParams.append(TagValue("catchUp", int(catchUp)))
        baseOrder.algoParams.append(TagValue("waitForFill", int(waitForFill)))
        baseOrder.algoParams.append(TagValue("startTime", startTime))
        baseOrder.algoParams.append(TagValue("endTime", endTime))
    #! [ad_params]

    #! [balanceimpactrisk_params]
    @staticmethod
    def FillBalanceImpactRiskParams(baseOrder:Order, maxPctVol:float, 
                                    riskAversion:str, forceCompletion:bool):
        baseOrder.algoStrategy = "BalanceImpactRisk"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("maxPctVol", maxPctVol))
        baseOrder.algoParams.append(TagValue("riskAversion", riskAversion))
        baseOrder.algoParams.append(TagValue("forceCompletion",
                                                int(forceCompletion)))
    #! [balanceimpactrisk_params]

    #! [minimpact_params]
    @staticmethod
    def FillMinImpactParams(baseOrder:Order, maxPctVol:float):
        baseOrder.algoStrategy = "MinImpact"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("maxPctVol", maxPctVol))
    #! [minimpact_params]

    #! [adaptive_params]
    @staticmethod
    def FillAdaptiveParams(baseOrder:Order, priority:str):
        baseOrder.algoStrategy = "Adaptive"
        baseOrder.algoParams = []
        baseOrder.algoParams.append(TagValue("adaptivePriority", priority))
    #! [adaptive_params]


def Test():
    av = AvailableAlgoParams()
 
if "__main__" == __name__:
    Test()
        
