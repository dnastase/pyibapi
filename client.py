#!/usr/bin/env python3

"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


"""
#TODO: not really sure what this class is conceptually. Figure out !
"""


from message import OUT
import comm
from comm import make_field
from utils import crt_fn_name
from logger import LOGGER


class Client(object):
 
    # TWS New Bulletins constants
    NEWS_MSG              = 1    # standard IB news bulleting message
    EXCHANGE_AVAIL_MSG    = 2    # control message specifing that an exchange is available for trading
    EXCHANGE_UNAVAIL_MSG  = 3    # control message specifing that an exchange is unavailable for trading


    def __init__(self, socket_conn):
        self.socket = socket_conn

    #int serverVersion();
    #std::string TwsConnectionTime();

    def send_msg(self, msg):
        full_msg = comm.make_msg(msg)
        LOGGER.debug("%s %s %s", crt_fn_name(1), "sending", full_msg)
        comm.send_msg(self.socket, full_msg)


    def startApi(self):
        VERSION = 2
        clientId = 0
        optCapab = ""

        msg = make_field(OUT.START_API) \
           + make_field(VERSION)    \
           + make_field(clientId)   \
           + make_field(optCapab)

        self.send_msg(msg)
     
    #void reqMktData(TickerId id, const Contract& contract,
    #        const std::string& genericTicks, bool snapshot, const TagValueListSPtr& mktDataOptions);
    #void cancelMktData(TickerId id);
    #void placeOrder(OrderId id, const Contract& contract, const Order& order);
    #void cancelOrder(OrderId id) ;

    def reqOpenOrders(self):
        VERSION = 1

        msg = make_field(OUT.REQ_OPEN_ORDERS) \
            + make_field(VERSION)

        self.send_msg(msg)
     
    #void reqAccountUpdates(bool subscribe, const std::string& acctCode);
    #void reqExecutions(int reqId, const ExecutionFilter& filter);
    #void reqIds(int numIds);
    #void reqContractDetails(int reqId, const Contract& contract);
    #void reqMktDepth(TickerId tickerId, const Contract& contract, int numRows, const TagValueListSPtr& mktDepthOptions);
    #void cancelMktDepth(TickerId tickerId);
    #void reqNewsBulletins(bool allMsgs);
    #void cancelNewsBulletins();
    #void setServerLogLevel(int level);
    #void reqAutoOpenOrders(bool bAutoBind);

    def reqAllOpenOrders(self):
        VERSION = 1

        msg = make_field(OUT.REQ_ALL_OPEN_ORDERS) \
            + make_field(VERSION)

        self.send_msg(msg)
     

    def reqManagedAccts():
        VERSION = 1

        msg = make_field(OUT.REQ_MANAGED_ACCTS) \
           + make_field(VERSION)

        return make_msg(msg)
     
    #void requestFA(faDataType pFaDataType);
    #void replaceFA(faDataType pFaDataType, const std::string& cxml);
    #void reqHistoricalData( TickerId id, const Contract& contract,
    #        const std::string& endDateTime, const std::string& durationStr,
    #        const std::string&  barSizeSetting, const std::string& whatToShow,
    #        int useRTH, int formatDate, const TagValueListSPtr& chartOptions);
    #void exerciseOptions(TickerId tickerId, const Contract& contract,
    #        int exerciseAction, int exerciseQuantity,
    #        const std::string& account, int override);
    #void cancelHistoricalData(TickerId tickerId );
    #void reqRealTimeBars(TickerId id, const Contract& contract, int barSize,
    #        const std::string& whatToShow, bool useRTH, const TagValueListSPtr& realTimeBarsOptions);
    #void cancelRealTimeBars(TickerId tickerId );
    #void cancelScannerSubscription(int tickerId);
    #void reqScannerParameters();
    #void reqScannerSubscription(int tickerId, const ScannerSubscription& subscription, const TagValueListSPtr& scannerSubscriptionOptions);

    def reqCurrentTime(self):
        VERSION = 1

        msg = make_field(OUT.REQ_CURRENT_TIME) \
           + make_field(VERSION)

        self.send_msg(msg)
     
    #void reqFundamentalData(TickerId reqId, const Contract&, const std::string& reportType);
    #void cancelFundamentalData(TickerId reqId);
    #void calculateImpliedVolatility(TickerId reqId, const Contract& contract, double optionPrice, double underPrice);
    #void calculateOptionPrice(TickerId reqId, const Contract& contract, double volatility, double underPrice);
    #void cancelCalculateImpliedVolatility(TickerId reqId);
    #void cancelCalculateOptionPrice(TickerId reqId);
    #void reqGlobalCancel();
    #void reqMarketDataType(int marketDataType);
    #void reqPositions();
    #void cancelPositions();
    #void reqAccountSummary( int reqId, const std::string& groupName, const std::string& tags);

    def reqAccountSummary(self, reqId: int, groupName: str, tags: str) -> bytes:
        VERSION = 1

        msg = make_field(OUT.REQ_ACCOUNT_SUMMARY) \
           + make_field(VERSION)   \
           + make_field(reqId)     \
           + make_field(groupName) \
           + make_field(tags)

        self.send_msg(msg)
     
    #void cancelAccountSummary( int reqId);
    #void verifyRequest( const std::string& apiName, const std::string& apiVersion);
    #void verifyMessage( const std::string& apiData);
    #void verifyAndAuthRequest( const std::string& apiName, const std::string& apiVersion, const std::string& opaqueIsvKey);
    #void verifyAndAuthMessage( const std::string& apiData, const std::string& xyzResponse);
    #void queryDisplayGroups( int reqId);
    #void subscribeToGroupEvents( int reqId, int groupId);
    #void updateDisplayGroup( int reqId, const std::string& contractInfo);
    #void unsubscribeFromGroupEvents( int reqId);
    #void reqPositionsMulti( int reqId, const std::string& account, const std::string& modelCode);
    #void cancelPositionsMulti( int reqId);
    #void reqAccountUpdatessMulti( int reqId, const std::string& account, const std::string& modelCode, bool ledgerAndNLV);
    #void cancelAccountUpdatesMulti( int reqId);
    #void reqSecDefOptParams(int reqId, const std::string& underlyingSymbol, const std::string& futFopExchange, const std::string& underlyingSecType, int underlyingConId);
    #void reqSoftDollarTiers(int reqId);
    #void reqFamilyCodes();
    #void reqMatchingSymbols(int reqId, const std::string& pattern);

