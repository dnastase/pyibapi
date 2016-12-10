#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


"""
This is the interface that will need to be overloaded by the customer so
that his/her code can receive info from the TWS/IBGW.
"""


from common import * 
from utils import *
from logger import LOGGER


(BID_SIZE, BID, ASK, ASK_SIZE, LAST, LAST_SIZE,
                HIGH, LOW, VOLUME, CLOSE,
                BID_OPTION_COMPUTATION,
                ASK_OPTION_COMPUTATION,
                LAST_OPTION_COMPUTATION,
                MODEL_OPTION,
                OPEN,
                LOW_13_WEEK,
                HIGH_13_WEEK,
                LOW_26_WEEK,
                HIGH_26_WEEK,
                LOW_52_WEEK,
                HIGH_52_WEEK,
                AVG_VOLUME,
                OPEN_INTEREST,
                OPTION_HISTORICAL_VOL,
                OPTION_IMPLIED_VOL,
                OPTION_BID_EXCH,
                OPTION_ASK_EXCH,
                OPTION_CALL_OPEN_INTEREST,
                OPTION_PUT_OPEN_INTEREST,
                OPTION_CALL_VOLUME,
                OPTION_PUT_VOLUME,
                INDEX_FUTURE_PREMIUM,
                BID_EXCH,
                ASK_EXCH,
                AUCTION_VOLUME,
                AUCTION_PRICE,
                AUCTION_IMBALANCE,
                MARK_PRICE,
                BID_EFP_COMPUTATION,
                ASK_EFP_COMPUTATION,
                LAST_EFP_COMPUTATION,
                OPEN_EFP_COMPUTATION,
                HIGH_EFP_COMPUTATION,
                LOW_EFP_COMPUTATION,
                CLOSE_EFP_COMPUTATION,
                LAST_TIMESTAMP,
                SHORTABLE,
                FUNDAMENTAL_RATIOS,
                RT_VOLUME,
                HALTED,
                BID_YIELD,
                ASK_YIELD,
                LAST_YIELD,
                CUST_OPTION_COMPUTATION,
                TRADE_COUNT,
                TRADE_RATE,
                VOLUME_RATE,
                LAST_RTH_TRADE,
                RT_HISTORICAL_VOL,
                IB_DIVIDENDS,
                BOND_FACTOR_MULTIPLIER,
                REGULATORY_IMBALANCE,
                NEWS_TICK,
                SHORT_TERM_VOLUME_3_MIN,
                SHORT_TERM_VOLUME_5_MIN,
                SHORT_TERM_VOLUME_10_MIN,
                DELAYED_BID,
                DELAYED_ASK,
                DELAYED_LAST,
                DELAYED_BID_SIZE,
                DELAYED_ASK_SIZE,
                DELAYED_LAST_SIZE,
                DELAYED_HIGH,
                DELAYED_LOW,
                DELAYED_VOLUME,
                DELAYED_CLOSE,
                DELAYED_OPEN,
                RT_TRD_VOLUME,
                CREDITMAN_MARK_PRICE,
                CREDITMAN_SLOW_MARK_PRICE,
                NOT_SET) = range(81)
TickType = int

class Wrapper:
#    def tickPrice( TickerId tickerId, TickType field, double price, const TickAttrib& attrib):
#    pass
    def tickSize(self, tickerId: TickerId, field: TickType, size: int):
        LOGGER.debug("%s %s", crt_fn_name(), vars())
#    def tickOptionComputation( TickerId tickerId, TickType tickType, double impliedVol, double delta,
#       double optPrice, double pvDividend, double gamma, double vega, double theta, double undPrice):
#    pass
#    def tickGeneric(TickerId tickerId, TickType tickType, double value):
#    pass
#    def tickString(TickerId tickerId, TickType tickType, const std::string& value):
#    pass
#    def tickEFP(TickerId tickerId, TickType tickType, double basisPoints, const std::string& formattedBasisPoints,
#       double totalDividends, int holdDays, const std::string& futureLastTradeDate, double dividendImpact, double dividendsToLastTradeDate):
#    pass
#    def orderStatus( OrderId orderId, const std::string& status, double filled,
#       double remaining, double avgFillPrice, int permId, int parentId,
#       double lastFillPrice, int clientId, const std::string& whyHeld):
#    pass
    def openOrder(self, orderId: OrderId, contract, order, orderState):
        LOGGER.debug("%s %s", crt_fn_name(), vars())
        LOGGER.debug("Order: %s %s %d %f %s", contract.symbol, order.action, order.totalQuantity, order.lmtPrice, order.permId)

    def openOrderEnd(self):
        LOGGER.debug("%s %s", crt_fn_name(), vars())
        
#    def winError( const std::string& str, int lastError):
#    pass
#    def connectionClosed():
#    pass
    def updateAccountValue(self, key: str, val: str , currency: str, accountName: str):
        LOGGER.debug("%s %s", crt_fn_name(), vars())

#    def updatePortfolio( const Contract& contract, double position,
#      double marketPrice, double marketValue, double averageCost,
#      double unrealizedPNL, double realizedPNL, const std::string& accountName):
#    pass
#    def updateAccountTime(const std::string& timeStamp):
#    pass
#    def accountDownloadEnd(const std::string& accountName):
#    pass
    def nextValidId(self, orderId:int):
        LOGGER.debug("%s %s", crt_fn_name(), vars())
#    def contractDetails( int reqId, const ContractDetails& contractDetails):
#    pass
#    def bondContractDetails( int reqId, const ContractDetails& contractDetails):
#    pass
#    def contractDetailsEnd( int reqId):
#    pass
#    def execDetails( int reqId, const Contract& contract, const Execution& execution) =0;
#    def execDetailsEnd( int reqId) =0;
    def error(self, id, errorCode, errorString):
        LOGGER.debug("%s %s", crt_fn_name(), vars())
        
#    def updateMktDepth(TickerId id, int position, int operation, int side,
#      double price, int size):
#    pass
#    def updateMktDepthL2(TickerId id, int position, std::string marketMaker, int operation,
#      int side, double price, int size):
#    pass
#    def updateNewsBulletin(int msgId, int msgType, const std::string& newsMessage, const std::string& originExch):
#    pass
    def managedAccounts(self, accountsList:str):
        LOGGER.debug("%s %s", crt_fn_name(), vars())
#    def receiveFA(faDataType pFaDataType, const std::string& cxml):
#    pass
#    def historicalData(TickerId reqId, const std::string& date, double open, double high, 
#       double low, double close, int volume, int barCount, double WAP, int hasGaps):
#    pass
#    def scannerParameters(const std::string& xml):
#    pass
#    def scannerData(int reqId, int rank, const ContractDetails& contractDetails,
#       const std::string& distance, const std::string& benchmark, const std::string& projection,
#       const std::string& legsStr):
#    pass
#    def scannerDataEnd(int reqId):
#    pass
#    def realtimeBar(TickerId reqId, long time, double open, double high, double low, double close,
#       long volume, double wap, int count):
#    pass
    def currentTime(self, time:int):
        LOGGER.debug("%s %s", crt_fn_name(), vars())
#    def fundamentalData(TickerId reqId, const std::string& data):
#    pass
#    def deltaNeutralValidation(int reqId, const UnderComp& underComp):
#    pass
#    def tickSnapshotEnd( int reqId):
#    pass
#    def marketDataType( TickerId reqId, int marketDataType):
#    pass
#    def commissionReport( const CommissionReport& commissionReport):
#    pass
#    def position( const std::string& account, const Contract& contract, double position, double avgCost):
#    pass
#    def positionEnd():
#    pass
    def accountSummary(self, reqId:int, account:str, tag:str, value:str, curency:str):
        LOGGER.debug("%s %s", crt_fn_name(), vars())
#    def accountSummaryEnd( int reqId):
#    pass
#    def verifyMessageAPI( const std::string& apiData):
#    pass
#    def verifyCompleted( bool isSuccessful, const std::string& errorText):
#    pass
#    def displayGroupList( int reqId, const std::string& groups):
#    pass
#    def displayGroupUpdated( int reqId, const std::string& contractInfo):
#    pass
#    def verifyAndAuthMessageAPI( const std::string& apiData, const std::string& xyzChallange):
#    pass
#    def verifyAndAuthCompleted( bool isSuccessful, const std::string& errorText):
#    pass
#    def connectAck():
#    pass
#    def positionMulti( int reqId, const std::string& account,const std::string& modelCode, const Contract& contract, double pos, double avgCost):
#    pass
#    def positionMultiEnd( int reqId):
#    pass
#    def accountUpdateMulti( int reqId, const std::string& account, const std::string& modelCode, const std::string& key, const std::string& value, const std::string& currency):
#    pass
#    def accountUpdateMultiEnd( int reqId):
#    pass
#    def securityDefinitionOptionalParameter(int reqId, const std::string& exchange, int underlyingConId, const std::string& tradingClass, const std::string& multiplier, std::set<std::string> expirations, std::set<double> strikes):
#    pass
#    def securityDefinitionOptionalParameterEnd(int reqId):
#    pass
#    def softDollarTiers(int reqId, const std::vector<SoftDollarTier> &tiers):
#    pass
#    def familyCodes(const std::vector<FamilyCode> &familyCodes):
#    pass
#    def symbolSamples(int reqId, const std::vector<ContractDescription> &contractDescriptions):
#    pass
#

