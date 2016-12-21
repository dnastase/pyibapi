#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""

import sys 
import socket 
import struct
import array
import datetime
import inspect
import time
import argparse

from common import * 
import decoder
import wrapper
from ticktype import TickType, TickTypeEnum
from comm import *
from message import IN, OUT
from client import Client
from logger import LOGGER
from connection import Connection
from reader import Reader
from queue import Queue
from utils import *
from execution import ExecutionFilter
from scanner import ScannerSubscription
from order_condition import *

#import pdb; pdb.set_trace()
#import code; code.interact(local=locals())



class TestApp(Client, wrapper.Wrapper):
    def __init__(self):
        Client.__init__(self, self)
        self.nextValidOrderId = None


    def nextValidId(self, orderId:int):
        LOGGER.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId


    def nextOrderId(self):
        id = self.nextValidOrderId
        self.nextValidOrderId += 1
        return id


    def error(self, *args):
        super().error(*args)
        print(crt_fn_name(), vars())


    def winError(self, *args):
        super().error(*args)
        print(crt_fn_name(), vars())
 

    def openOrder(self, *args):
        super().openOrder(*args)
        print(crt_fn_name(), vars())


    def openOrderEnd(self, *args):
        super().openOrderEnd(*args)
        print(crt_fn_name(), vars(), file=sys.stderr)
        #LOGGER.debug("openOrderEnd - quitting")
        #self.conn.disconnect()


    def tickPrice(self, tickerId: TickerId , tickType: TickType, price: float, attrib):
        super().tickPrice(tickerId, tickType, price, attrib)
        print(crt_fn_name(), tickerId, TickTypeEnum.to_str(tickType), price, attrib, file=sys.stderr)


    def tickSize(self, tickerId: TickerId, tickType: TickType, size: int):
        super().tickSize(tickerId, tickType, size)
        print(crt_fn_name(), tickerId, TickTypeEnum.to_str(tickType), size, file=sys.stderr)


    def scannerParameters(self, xml:str):
        open('scanner.xml', 'w').write(xml)



def main():

    cmdLineParser = argparse.ArgumentParser("api tests")
    #cmdLineParser.add_option("-c", action="store_true", dest="use_cache", default = False, help = "use the cache")
    #cmdLineParser.add_option("-f", action="store", type="string", dest="file", default="", help="the input file")
    cmdLineParser.add_argument("-p", "--port", action="store", type=int, 
        dest="port", default = 4005, help="The TCP port to use")
    args = cmdLineParser.parse_args()
    print("Using args", args)
    LOGGER.debug("Using args %s", args)
    #print(args)
                                                                                                                                           
    LOGGER.debug("now is %s", datetime.datetime.now())
    import logging
    #LOGGER.setLevel(logging.ERROR)

    #enable logging when member vars are assigned
    import utils 
    from order import Order
    Order.__setattr__ = utils.setattr_log
    from contract import Contract,UnderComp
    Contract.__setattr__ = utils.setattr_log 
    UnderComp.__setattr__ = utils.setattr_log 
    from tag_value import TagValue
    TagValue.__setattr__ = utils.setattr_log
    TimeCondition.__setattr__ = utils.setattr_log 
    ExecutionCondition.__setattr__ = utils.setattr_log  
    MarginCondition.__setattr__ = utils.setattr_log  
    PriceCondition.__setattr__ = utils.setattr_log 
    PercentChangeCondition.__setattr__ = utils.setattr_log 
    VolumeCondition.__setattr__ = utils.setattr_log 

    #from inspect import signature as sig
    #import code; code.interact(local=dict(globals(), **locals()))
    #sys.exit(1)

    the_client = TestApp()
    the_client.connect("127.0.0.1", args.port, 0)

    the_client.reqCurrentTime()
    the_client.reqManagedAccts()
    the_client.reqAccountSummary(reqId = 2, groupName = "All", 
                                 tags = "NetLiquidation")

    the_client.reqAllOpenOrders()

    contract = Contract()
    contract.symbol = "AMD"
    contract.secType = "STK"   
    contract.currency = "USD"  
    contract.exchange = "SMART"
    #the_client.reqMarketDataType(1)
    #the_client.reqMktData(1001, contract, "", snapshot=True)
    #the_client.cancelMktData(1001)
    #the_client.reqExecutions(2001, ExecutionFilter())
    #the_client.reqContractDetails(3001, contract)
    #the_client.reqPositions()
    #the_client.reqIds(2)

    #the_client.reqMktDepth(4001, contract, 5, "")
    #the_client.cancelMktDepth(4001)

    #the_client.reqNewsBulletins(allMsgs=True)
    #the_client.cancelNewsBulletins()

    #the_client.requestFA(faDataTypeEnum.GROUPS)

    #the_client.reqHistoricalData(5001, contract, "20161215 16:00:00", "2 D",
    #                             "1 hour", "TRADES", 0, 1, []) 
    #the_client.cancelHistoricalData(5001)
                                 
    #the_client.reqFundamentalData(6001, contract, "ReportSnapshot")
    #the_client.cancelFundamentalData(6001)

    #the_client.queryDisplayGroups(7001)
    #the_client.subscribeToGroupEvents(7002, 1)
    #the_client.unsubscribeFromGroupEvents(7002)

    #the_client.reqScannerParameters()
    ss = ScannerSubscription()
    ss.instrument = "STK"
    ss.locationCode = "STK.US"
    ss.scanCode = "TOP_PERC_LOSE"
    #the_client.reqScannerSubscription(8001, ss, [])
    #the_client.cancelScannerSubscription(8001)

    #the_client.reqRealTimeBars(9001, contract, 5, "TRADES", 0, [])
    #the_client.cancelRealTimeBars(9001) 

    #the_client.reqSecDefOptParams(10001, "AMD", "", "STK", 4391)

    #the_client.reqSoftDollarTiers(11001)

    #the_client.reqFamilyCodes()

    #the_client.reqMatchingSymbols(12001, "AMD")

    contract = Contract()
    contract.symbol = "AMD"
    contract.secType = "OPT"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.lastTradeDateOrContractMonth = "20170120"
    contract.strike = 10
    contract.right = "C"
    contract.multiplier = "100"
    #Often, contracts will also require a trading class to rule out ambiguities
    contract.tradingClass = "AMD"
    #the_client.calculateImpliedVolatility(13001, contract, 1.3, 10.85)
    #the_client.calculateOptionPrice(13002, contract, 0.65, 10.85)

    the_client.run()


if __name__ == "__main__":
    main()

#TODO: create test that dynamically iterates all the methods of client.py and 
# finds the corresponding test and runs it; this will ensure that added
# methods w/out associated test will not be silently "passed"

#TODO: see that we receive fields like 1.7976931348623157E30 DBL_MAX !!

