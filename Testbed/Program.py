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
import argparse
import datetime
import collections


import wrapper
from client import Client
from utils import iswrapper

#types
from common import *
from order_condition import *
from contract import *
from order import *
from order_state import *
from execution import ExecutionFilter
from scanner import ScannerSubscription
from ticktype import *

from logger import LOGGER

from ContractSamples import ContractSamples 
from OrderSamples import OrderSamples 


#TODO: finish adding the snippet markets for the wrapper methods !

#! [socket_declare]
#! [socket_init]
# The Client class takes care of everything that's done individually in the 
# API-s: 
# - creating the Socket, Reader and Decoder
# - initializing the socket
# 
#! [socket_init]
#! [socket_declare]

#! [ewrapperimpl]
class TestApp(Client, wrapper.Wrapper):
#! [ewrapperimpl]
    def __init__(self):
        Client.__init__(self, self)
        self.nextValidOrderId = None
        self.permId2ord = {}
        # we will count how many answers we get for each request
        self.reqId2nOps = {}


    def requesting(self, reqIds):
        if type(reqIds) is not list:
            reqIds = [reqIds, ]

        for reqId in reqIds:
            if reqId in self.reqId2nOps:
                raise ValueError("reqId already used %d" % reqId)
            self.reqId2nOps[reqId] = 0


    def gotAnswer(self, reqId):
        if reqId not in self.reqId2nOps:
            LOGGER.debug("AppError: unknown reqId %d" % reqId)
        else:
            self.reqId2nOps[reqId] += 1


    def printReqAnsSituation(self):
        print("RequestId", "#Operations")
        for (reqId, nOps) in self.reqId2nOps.items():
            print(reqId, nOps)


    @iswrapper
    #! [nextvalidid]
    def nextValidId(self, orderId:int):
        super().nextValidId(orderId)

        LOGGER.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
    #! [nextvalidid]

        #we can start now
        self.marketDataType()
        self.tickDataOperations_req()


    def placeOneOrder(self):
        con = Contract()
        con.symbol = "AMD"
        con.secType = "STK"
        con.currency = "USD"
        con.exchange = "SMART"
        order = Order()
        order.action = "BUY"
        order.orderType = "LMT"
        order.tif = "GTC"
        order.totalQuantity = 3
        order.lmtPrice = 1.23
        self.placeOrder(self.nextOrderId(), con, order)


    def cancelOneOrder(self):
        pass
 

    def nextOrderId(self):
        id = self.nextValidOrderId
        self.nextValidOrderId += 1
        return id


    @iswrapper
    #! [error]
    def error(self, id, errorCode:int, errorString:str):
        super().error(id, errorCode, errorString)
    #! [error]


    @iswrapper
    def winError(self, text:str, lastError:int):
        super().winError(text, lastError)
 

    @iswrapper
    def openOrder(self, orderId:OrderId, contract:Contract, order:Order, 
                  orderState:OrderState):
        super().openOrder(orderId, contract, order, orderState)

        order.contract = contract
        self.permId2ord[order.permId] = order


    @iswrapper
    def openOrderEnd(self, *args):
        super().openOrderEnd(*args)

        LOGGER.debug("Received %d openOrders", len(self.permId2ord))


    @iswrapper
    def orderStatus(self, orderId:OrderId , status:str, filled:float,
                    remaining:float, avgFillPrice:float, permId:int, 
                    parentId:int, lastFillPrice:float, clientId:int, 
                    whyHeld:str):
        super().orderStatus(orderId, status, filled, remaining,
            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld)



    def marketDataType(self):
        #! [reqmarketdatatype]
        # Switch to live (1) frozen (2) delayed (3) or delayed frozen (4)
        self.reqMarketDataType(2)
        #! [reqmarketdatatype]


    def tickDataOperations_req(self):
        # Requesting real time market data 

        #! [reqmktdata]
        self.reqMktData(1101, ContractSamples.USStockAtSmart(), "", False, None)
        self.reqMktData(1001, ContractSamples.StockComboContract(), "", False, None)
        #! [reqmktdata]
        self.requesting(1101)
        self.requesting(1001)

        #! [reqmktdata_snapshot]
        self.reqMktData(1003, ContractSamples.FutureComboContract(), "", True, None)
        #! [reqmktdata_snapshot]
        self.requesting(1003)

        #! [reqmktdata_genticks]
        # Requesting RTVolume (Time & Sales), shortable and Fundamental Ratios generic ticks
        self.reqMktData(1004, ContractSamples.USStock(), "233,236,258", False, None)
        #! [reqmktdata_genticks]
        self.requesting(1004)

        #! [reqmktdata_contractnews]
#TODO: put back ! 
        self.reqMktData(1005, ContractSamples.USStock(), "mdoff,292:BZ", False, None)
        self.reqMktData(1006, ContractSamples.USStock(), "mdoff,292:BT", False, None)
        self.reqMktData(1007, ContractSamples.USStock(), "mdoff,292:FLY", False, None)
        self.reqMktData(1008, ContractSamples.USStock(), "mdoff,292:MT", False, None)
        #! [reqmktdata_contractnews]
        #! [reqmktdata_broadtapenews]
        self.reqMktData(1009, ContractSamples.BTbroadtapeNewsFeed(), "mdoff,292", False, None)
        self.reqMktData(1010, ContractSamples.BZbroadtapeNewsFeed(), "mdoff,292", False, None)
        self.reqMktData(1011, ContractSamples.FLYbroadtapeNewsFeed(), "mdoff,292", False, None)
        self.reqMktData(1012, ContractSamples.MTbroadtapeNewsFeed(), "mdoff,292", False, None)
        #! [reqmktdata_broadtapenews]

        #! [reqoptiondatagenticks]
        # Requesting data for an option contract will return the greek values
        self.reqMktData(1002, ContractSamples.OptionWithLocalSymbol(), "", False, None)
        #! [reqoptiondatagenticks]
        self.requesting(1002)

        #time.sleep(10000)


    def tickDataOperations_cancel(self):
        # Canceling the market data subscription 
        #! [cancelmktdata]
        self.cancelMktData(1101)
        self.cancelMktData(1001)
        self.cancelMktData(1002)
        self.cancelMktData(1003)
        #! [cancelmktdata]
        self.requesting(-1101)
        self.requesting(-1001)
        self.requesting(-1002)
        self.requesting(-1003)
 
    @iswrapper
    #! [tickprice]
    def tickPrice(self, reqId: TickerId , tickType: TickType, price: float,
                  attrib:TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)

        self.gotAnswer(reqId)
    #! [tickprice]

        if self.reqId2nOps.get(1101, 0) == 2:
            self.tickDataOperations_cancel()
            self.marketDepthOperations_req()


    @iswrapper
    #! [ticksize]
    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        super().tickSize(reqId, tickType, size)
    #! [ticksize]
        #self.gotAnswer(reqId)


    @iswrapper
    #! [tickgeneric]
    def tickGeneric(self, reqId:TickerId, tickType:TickType, value:float):
        super().tickGeneric(reqId, tickType, value)
    #! [tickgeneric]
        #self.gotAnswer(reqId)


    @iswrapper
    #! [tickstring]
    def tickString(self, reqId:TickerId, tickType:TickType, value:str):
        super().tickString(reqId, tickType, value)
    #! [tickstring]
        #self.gotAnswer(reqId)
  

    @iswrapper
    #! [ticksnapshotend]
    def tickSnapshotEnd(self, reqId:int):
        super().tickSnapshotEnd(reqId)
    #! [ticksnapshotend]
        #self.gotAnswer(reqId)


    def marketDepthOperations_req(self):
        # Requesting the Deep Book 
        #! [reqmarketdepth]
        self.reqMktDepth(2101, ContractSamples.USStock(), 5, None)
        self.reqMktDepth(2001, ContractSamples.EurGbpFx(), 5, None)
        #! [reqmarketdepth]
        self.requesting(2101)
        self.requesting(2001)


    @iswrapper
    def updateMktDepth(self, reqId:TickerId , position:int, operation:int,
                        side:int, price:float, size:int): 
        super().updateMktDepth(id, position, operation, side, price, size)

        self.gotAnswer(reqId)

        if self.reqId2nOps.get(2101, 0) == 1:
            self.marketDepthOperations_cancel() 
            self.realTimeBars_req()
 

    def marketDepthOperations_cancel(self):
        # Canceling the Deep Book request
        #! [cancelmktdepth]
        self.cancelMktDepth(2101)
        self.cancelMktDepth(2001)
        #! [cancelmktdepth]


    def realTimeBars_req(self):
        # Requesting real time bars 
        #! [reqrealtimebars]
        self.reqRealTimeBars(3101, ContractSamples.USStockAtSmart(), 5, "MIDPOINT", True, None)
        self.reqRealTimeBars(3001, ContractSamples.EurGbpFx(), 5, "MIDPOINT", True, None)
        #! [reqrealtimebars]
        self.requesting(3001)
        self.requesting(3101)


    @iswrapper
    def realtimeBar(self, reqId:TickerId , time:int, open:float, high:float, 
                    low:float, close:float, volume:int, wap:float, 
                    count: int):
        super().realtimeBar(reqId, time, open, high, low, close, volume, wap, count)

        self.gotAnswer(reqId)

        if self.reqId2nOps.get(3101, 0) == 1:
            self.realTimeBars_cancel()
            self.historicalDataRequests_req()

 
    def realTimeBars_cancel(self):
        # Canceling real time bars 
        #! [cancelrealtimebars]
        self.cancelRealTimeBars(3101)
        self.cancelRealTimeBars(3001)
        #! [cancelrealtimebars]


    def historicalDataRequests_req(self):
        # Requesting historical data 
        #! [reqhistoricaldata]
        queryTime = (datetime.datetime.today() -
                    datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
        #String queryTime = DateTime.Now.AddMonths(-6).ToString("yyyyMMdd HH:mm:ss")
        self.reqHistoricalData(4101, ContractSamples.USStockAtSmart(), queryTime, 
                               "1 M", "1 day", "MIDPOINT", 1, 1, None)
        self.reqHistoricalData(4001, ContractSamples.EurGbpFx(), queryTime, 
                               "1 M", "1 day", "MIDPOINT", 1, 1, None)
        self.reqHistoricalData(4002, ContractSamples.EuropeanStock(), queryTime,
                                "10 D", "1 min", "TRADES", 1, 1, None)
        #! [reqhistoricaldata]

        self.requesting(4101)
        self.requesting(4001)
        self.requesting(4002)


    def historicalDataRequests_cancel(self):
        # Canceling historical data requests 
        self.cancelHistoricalData(4101)
        self.cancelHistoricalData(4001)
        self.cancelHistoricalData(4002)


    @iswrapper
    def historicalData(self, reqId:TickerId , date:str, open:float, high:float, 
                       low:float, close:float, volume:int, barCount:int, 
                        WAP:float, hasGaps:int):
        super().historicalData(reqId, date, open, high, low, close, volume,
                               barCount, WAP, hasGaps)

        self.gotAnswer(reqId)

        if self.reqId2nOps.get(4101, 0) > 1:
            self.historicalDataRequests_cancel()
            self.optionsOperations_req()
 

    def optionsOperations_req(self):
        #! [reqsecdefoptparams]
        self.reqSecDefOptParams(0, "IBM", "", "STK", 8314)
        #! [reqsecdefoptparams]

        # Calculating implied volatility 
        #! [calculateimpliedvolatility]
        self.calculateImpliedVolatility(5001, ContractSamples.OptionAtBOX(), 5, 85, None)
        #! [calculateimpliedvolatility]

        # Calculating option's price 
        #! [calculateoptionprice]
        self.calculateOptionPrice(5002, ContractSamples.OptionAtBOX(), 0.22, 85, None)
        #! [calculateoptionprice]

        # Exercising options 
        #! [exercise_options]
        self.exerciseOptions(5003, ContractSamples.OptionWithTradingClass(), 1, 1, None, 1)
        #! [exercise_options]

        self.requesting(5001)
        self.requesting(5002)
        self.requesting(5003)


    def optionsOperations_cancel(self):
        # Canceling implied volatility 
        self.cancelCalculateImpliedVolatility(5001)
        # Canceling option's price calculation 
        self.cancelCalculateOptionPrice(5002)


    @iswrapper
    def securityDefinitionOptionParameter(self, reqId:int, exchange:str,
                        underlyingConId:int, tradingClass:str, multiplier:str, 
                        expirations:SetOfString, strikes:SetOfFloat):
        super().securityDefinitionOptionParameter(reqId, exchange,
            underlyingConId, tradingClass, multiplier, expirations, strikes)

        self.gotAnswer(reqId)        


    @iswrapper
    def securityDefinitionOptionParameterEnd(self, reqId:int):
        super().securityDefinitionOptionParameterEnd(reqId)

        self.gotAnswer(reqId)        


    @iswrapper
    def tickOptionComputation(self, reqId:TickerId, tickType:TickType ,
            impliedVol:float, delta:float, optPrice:float, pvDividend:float, 
            gamma:float, vega:float, theta:float, undPrice:float):  
        super().tickOptionComputation(reqId, tickType, impliedVol, delta,
                            optPrice, pvDividend, gamma, vega, theta, undPrice)

        self.gotAnswer(reqId)        

        if self.reqId2nOps.get(5003, 0) > 0:
            self.optionsOperations_cancel()
            self.contractOperations()


    def contractOperations(self):
        self.reqContractDetails(209, ContractSamples.EurGbpFx())
        #! [reqcontractdetails]
        self.reqContractDetails(210, ContractSamples.OptionForQuery())
        #! [reqcontractdetails]

        #! [reqMatchingSymbols]
        self.reqMatchingSymbols(211, "IB")
        #! [reqMatchingSymbols]

        self.requesting(209)
        self.requesting(210) 
        self.requesting(211) 


    def contractNewsFeed(self):
        #! [reqcontractdetailsnews]
        self.reqContractDetails(211, ContractSamples.NewsFeedForQuery())
        #! [reqcontractdetailsnews]

        self.requesting(211) 


    @iswrapper
    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        super(reqId, ContractDetails)

        self.gotAnswer(reqId)


    @iswrapper
    def bondContractDetails(self, reqId:int, contractDetails:ContractDetails):
        super(reqId, ContractDetails)

        self.gotAnswer(reqId)


    @iswrapper
    def contractDetailsEnd(self, reqId:int):
        super(reqId)

        self.gotAnswer(reqId)

        if self.reqId2nOps.get(210,0) > 0:
            self.marketScanners_req()


    def marketScanners_req(self):
        # Requesting all available parameters which can be used to build a scanner request
        #! [reqscannerparameters]
        self.reqScannerParameters()
        #! [reqscannerparameters]

        # Triggering a scanner subscription 
        #! [reqscannersubscription]
        self.reqScannerSubscription(7001,
            ScannerSubscriptionSamples.HighOptVolumePCRatioUSIndexes(), None)
        #! [reqscannersubscription]

        self.requesting(7001)


    def marketScanners_cancel(self):
        # Canceling the scanner subscription 
        #! [cancelscannersubscription]
        self.cancelScannerSubscription(7001)
        #! [cancelscannersubscription]


    @iswrapper
    def scannerParameters(self, xml:str):
        super().scannerParameters(xml)
        open('scanner.xml', 'w').write(xml)
        

    @iswrapper
    def scannerData(self, reqId:int, rank:int, contractDetails:ContractDetails,
                     distance:str, benchmark:str, projection:str, legsStr:str):
        super().scannerData(reqId, rank, contractDetails, distance, benchmark,
                            projection, legStr)

        self.gotAnswer(reqId)


    @iswrapper
    def scannerDataEnd(self, reqId:int):
        super().scannerDataEnd(reqId)

        self.gotAnswer(reqId)

        if self.reqId2nOps.get(7001,0) > 0:
            self.marketScanners_cancel()
            self.reutersFundamentals_req()
       
 
    def reutersFundamentals_req(self):
        # Requesting Fundamentals 
        #! [reqfundamentaldata]
        self.reqFundamentalData(8001, ContractSamples.USStock(),
                                  "ReportsFinSummary", None)
        #! [reqfundamentaldata]

        self.requesting(8001)


    def reutersFundamentals_cancel(self):
        # Canceling fundamentals request ***/
        #! [cancelfundamentaldata]
        self.cancelFundamentalData(8001)
        #! [cancelfundamentaldata]

    @iswrapper
    def fundamentalData(self, reqId:TickerId , data:str):
        super().fundamentalData(reqId, data)

        if self.reqId2nOps.get(8001,0) > 0:
            self.reutersFundamentals_cancel()
            self.bulletins_req()


    def bulletins_req(self):
        # Requesting Interactive Broker's news bulletins */
        #! [reqnewsbulletins]
        self.reqNewsBulletins(True)
        #! [reqnewsbulletins]


    def bulletins_cancel(self):
        # Requesting Interactive Broker's news bulletins */
        # Canceling IB's news bulletins ***/
        #! [cancelnewsbulletins]
        self.cancelNewsBulletin()
        #! [cancelnewsbulletins]


    @iswrapper
    def updateNewsBulletin(self, msgId:int, msgType:int, newsMessage:str, 
                           originExch:str):
        super().updateNewsBulletin(msgId, msgType, newsMessage, originExch)

        self.bulletins_cancel()
        self.accountOperations_req()
        

    def accountOperations_req(self):
        # Requesting managed accounts***/
        #! [reqmanagedaccts]
        self.reqManagedAccts()
        #! [reqmanagedaccts]
        # Requesting accounts' summary ***/

        #! [reqaaccountsummary]
        self.reqAccountSummary(9001, "All", AccountSummaryTags.GetAllTags())
        #! [reqaaccountsummary]

        #! [reqaaccountsummaryledger]
        self.reqAccountSummary(9002, "All", "$LEDGER")
        #! [reqaaccountsummaryledger]

        #! [reqaaccountsummaryledgercurrency]
        self.reqAccountSummary(9003, "All", "$LEDGER:EUR")
        #! [reqaaccountsummaryledgercurrency]

        #! [reqaaccountsummaryledgerall]
        self.reqAccountSummary(9004, "All", "$LEDGER:ALL")
        #! [reqaaccountsummaryledgerall]

        # Subscribing to an account's information. Only one at a time! 
        #! [reqaaccountupdates]
        self.reqAccountUpdates(True, "U150462")
        #! [reqaaccountupdates]

        #! [reqaaccountupdatesmulti]
        self.reqAccountUpdatesMulti(9005, "U150462", "EUstocks", True)
        #! [reqaaccountupdatesmulti]

        # Requesting all accounts' positions.
        #! [reqpositions]
        self.reqPositions()
        #! [reqpositions]

        #! [reqpositionsmulti]
        self.reqPositionsMulti(9006, "DU74649", "EUstocks")
        #! [reqpositionsmulti]

        #! [reqFamilyCodes]
        self.reqFamilyCodes()
        #! [reqFamilyCodes]

        self.requesting(9001, 9002, 9003, 9004, 9005, 9006)


    def accountOperations_cancel(self):
        #! [cancelaaccountsummary]
        self.cancelAccountSummary(9001)
        self.cancelAccountSummary(9002)
        self.cancelAccountSummary(9003)
        self.cancelAccountSummary(9004)
        #! [cancelaaccountsummary]

        #! [cancelaaccountupdates]
        self.reqAccountUpdates(false, "U150462")
        #! [cancelaaccountupdates]
 
        #! [cancelpositions]
        self.cancelPositions()
        #! [cancelpositions]


    @iswrapper
    def accountSummary(self, reqId:int, account:str, tag:str, value:str, 
                       currency:str):
        super().accountSummary(reqId, account, tag, value, currency)

        self.gotAnswer(reqId)


    @iswrapper
    def updateAccountValue(self, key:str, val:str, currency:str, 
                            accountName:str):
        super().updateAccountValue(key, val, currency, accountName)


    @iswrapper
    def updatePortfolio(self, contract:Contract, position:float,
                        marketPrice:float, marketValue:float, 
                        averageCost:float, unrealizedPNL:float, 
                        realizedPNL:float, accountName:str):
        super().updatePortfolio(contract, position, marketPrice, marketValue,
                        averageCost, unrealizedPNL, realizedPNL, accountName)


    @iswrapper
    def updateAccountTime(self, timeStamp:str):
        super().updateAccountTime(timeStamp)


    @iswrapper
    def accountDownloadEnd(self, accountName:str):
        super().accountDownloadEnd(accountName)


    @iswrapper
    def position(self, account:str, contract:Contract, position:float, 
                 avgCost:float):
        super().position(account, contract, position, avgCost)


    @iswrapper
    def positionEnd(self):
        super().positionEnd()

 
    def positionMulti(self, reqId:int, account:str, modelCode:str,
                      contract:Contract, pos:float, avgCost:float):
        super().positionMulti(reqId, account, modelCode, contract, pos, avgCost)

        self.gotAnswer(reqId)

    def positionMultiEnd(self, reqId:int):
        super().positionMultiEnd(reqId)

        self.gotAnswer(reqId)

        if self.reqId2nOps.get(9006,0) > 0:
            self.accountOperations_cancel()

    
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
    #import code code.interact(local=dict(globals(), **locals()))
    #sys.exit(1)

    app = TestApp()
    app.connect("127.0.0.1", args.port, 0)

    app.reqCurrentTime()
    app.reqManagedAccts()
    app.reqAccountSummary(reqId = 2, groupName = "All", 
                                 tags = "NetLiquidation")

    #app.reqAllOpenOrders()

    contract = Contract()
    contract.symbol = "AMD"
    contract.secType = "STK"   
    contract.currency = "USD"  
    contract.exchange = "SMART"
    #app.reqMarketDataType(1)
    #app.reqMktData(1001, contract, "", snapshot=True)
    #app.cancelMktData(1001)
    #app.reqExecutions(2001, ExecutionFilter())
    #app.reqContractDetails(3001, contract)
    #app.reqPositions()
    #app.reqIds(2)

    #app.reqMktDepth(4001, contract, 5, "")
    #app.cancelMktDepth(4001)

    #app.reqNewsBulletins(allMsgs=True)
    #app.cancelNewsBulletins()

    #app.requestFA(faDataTypeEnum.GROUPS)

    #app.reqHistoricalData(5001, contract, "20161215 16:00:00", "2 D",
    #                             "1 hour", "TRADES", 0, 1, []) 
    #app.cancelHistoricalData(5001)
                                 
    #app.reqFundamentalData(6001, contract, "ReportSnapshot")
    #app.cancelFundamentalData(6001)

    #app.queryDisplayGroups(7001)
    #app.subscribeToGroupEvents(7002, 1)
    #app.unsubscribeFromGroupEvents(7002)

    #app.reqScannerParameters()
    ss = ScannerSubscription()
    ss.instrument = "STK"
    ss.locationCode = "STK.US"
    ss.scanCode = "TOP_PERC_LOSE"
    #app.reqScannerSubscription(8001, ss, [])
    #app.cancelScannerSubscription(8001)

    #app.reqRealTimeBars(9001, contract, 5, "TRADES", 0, [])
    #app.cancelRealTimeBars(9001) 

    #app.reqSecDefOptParams(10001, "AMD", "", "STK", 4391)

    #app.reqSoftDollarTiers(11001)

    #app.reqFamilyCodes()

    #app.reqMatchingSymbols(12001, "AMD")

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
    #app.calculateImpliedVolatility(13001, contract, 1.3, 10.85)
    #app.calculateOptionPrice(13002, contract, 0.65, 10.85)

    app.run()


if __name__ == "__main__":
    main()
   
