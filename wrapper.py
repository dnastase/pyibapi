#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


"""
This is the interface that will need to be overloaded by the customer so
that his/her code can receive info from the TWS/IBGW.

NOTE: the methods use type annotations to describe the types of the arguments.
This is used by the Decoder to dynamically and automatically decode the
received message into the given Wrapper method. This method can only be 
used for the most simple messages, but it's still huge helper.
Also this method currently automatically decode a 'version' field in the
message. However having a 'version' field is a legacy thing, newer
message use the 'unified version': the agreed up min version of both
server and client.

"""


from common import * 
from utils import *
from logger import LOGGER
from contract import Contract
from contract import ContractDetails
from contract import UnderComp
from order import Order
from order_state import OrderState
from execution import Execution
from ticktype import TickType
from commission_report import CommissionReport


class TickAttrib:
    def __init__(self):
        self.canAutoExecute = False
        self.pastLimit = False

 

class Wrapper:
    def logAnswer(self, fnName, fnParams):
        LOGGER.debug("ANSWER %s %s", fnName, fnParams)


    def tickPrice(self, tickerId:TickerId , tickType:TickType, price:float, 
                  attrib):
        self.logAnswer(crt_fn_name(), vars()) 


    def tickSize(self, tickerId:TickerId, tickType:TickType, size:int):
        self.logAnswer(crt_fn_name(), vars()) 


    def tickOptionComputation(self, tickerId:TickerId, tickType:TickType ,
            impliedVol:float, delta:float, optPrice:float, pvDividend:float, 
            gamma:float, vega:float, theta:float, undPrice:float):
        """This function is called when the market in an option or its
        underlier moves. TWS's option model volatilities, prices, and
        deltas, along with the present value of dividends expected on that
        options underlier are received."""

        self.logAnswer(crt_fn_name(), vars()) 


    def tickGeneric(self, tickerId:TickerId, tickType:TickType, value:float):
        self.logAnswer(crt_fn_name(), vars()) 


    def tickString(self, tickerId:TickerId, tickType:TickType, value:str):
        self.logAnswer(crt_fn_name(), vars()) 


    def tickEFP(self, tickerId:TickerId, tickType:TickType, basisPoints:float, 
                formattedBasisPoints:str, totalDividends:float, 
                holdDays:int, futureLastTradeDate:str, dividendImpact:float, 
                dividendsToLastTradeDate:float):
        self.logAnswer(crt_fn_name(), vars()) 


    def orderStatus(self, orderId:OrderId , status:str, filled:float,
                    remaining:float, avgFillPrice:float, permId:int, 
                    parentId:int, lastFillPrice:float, clientId:int, 
                    whyHeld:str):
        self.logAnswer(crt_fn_name(), vars()) 


    def openOrder(self, orderId:OrderId, contract:Contract, order:Order, 
                  orderState:OrderState):
        self.logAnswer(crt_fn_name(), vars()) 
        LOGGER.debug("Order: %s %s %d %f %s", contract.symbol, order.action, order.totalQuantity, order.lmtPrice, order.permId)


    def openOrderEnd(self):
        self.logAnswer(crt_fn_name(), vars()) 
        

    def winError(self, text:str, lastError:int):
        self.logAnswer(crt_fn_name(), vars()) 

    def connectAck(self):
        self.logAnswer(crt_fn_name(), vars()) 


    def connectionClosed(self):
        """This function is called when TWS closes the sockets
        connection with the ActiveX control, or when TWS is shut down."""

        self.logAnswer(crt_fn_name(), vars()) 


    def updateAccountValue(self, key:str, val:str, currency:str, 
                            accountName:str):
        """ This function is called only when ReqAccountUpdates on
        EClientSocket object has been called. """

        self.logAnswer(crt_fn_name(), vars()) 


    def updatePortfolio(self, contract:Contract, position:float,
                        marketPrice:float, marketValue:float, 
                        averageCost:float, unrealizedPNL:float, 
                        realizedPNL:float, accountName:str):
        """This function is called only when reqAccountUpdates on
        EClientSocket object has been called."""

        self.logAnswer(crt_fn_name(), vars()) 


    def updateAccountTime(self, timeStamp:str):
        self.logAnswer(crt_fn_name(), vars()) 


    def accountDownloadEnd(self, accountName:str):
        """This is called after a batch updateAccountValue() and
        updatePortfolio() is sent."""

        self.logAnswer(crt_fn_name(), vars()) 


    def nextValidId(self, orderId:int):
        self.logAnswer(crt_fn_name(), vars()) 


    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        """This function is called only when reqContractDetails function
        on the EClientSocket object has been called."""

        self.logAnswer(crt_fn_name(), vars()) 


    def bondContractDetails(self, reqId:int, contractDetails:ContractDetails):
        """This function is called only when reqContractDetails function
            on the EClientSocket object has been called for bonds."""

        self.logAnswer(crt_fn_name(), vars()) 


    def contractDetailsEnd(self, reqId:int):
        """This function is called once all contract details for a given
        request are received. This helps to define the end of an option
        chain."""

        self.logAnswer(crt_fn_name(), vars()) 


    def execDetails(self, reqId:int, contract:Contract, execution:Execution):
        """This event is fired when the reqExecutions() functions is
        invoked, or when an order is filled.  """

        self.logAnswer(crt_fn_name(), vars()) 


    def execDetailsEnd(self, reqId:int):
        """This function is called once all executions have been sent to
        a client in response to reqExecutions()."""

        self.logAnswer(crt_fn_name(), vars()) 


    def error(self, id, errorCode:int, errorString:str):
        """This event is called when there is an error with the
        communication or when TWS wants to send a message to the client."""

        self.logAnswer(crt_fn_name(), vars()) 
        

    def updateMktDepth(self, id:TickerId , position:int, operation:int,
                        side:int, price:float, size:int):
        self.logAnswer(crt_fn_name(), vars()) 


    def updateMktDepthL2(self, id:TickerId , position:int, marketMaker:str,
                          operation:int, side:int, price:float, size:int):
        self.logAnswer(crt_fn_name(), vars()) 


    def updateNewsBulletin(self, msgId:int, msgType:int, newsMessage:str, 
                           originExch:str):
        self.logAnswer(crt_fn_name(), vars()) 


    def managedAccounts(self, accountsList:str):
        self.logAnswer(crt_fn_name(), vars()) 


    def receiveFA(self, pFaDataType:faDataType , cxml:str):
        self.logAnswer(crt_fn_name(), vars()) 


    def historicalData(self, reqId:TickerId , date:str, open:float, high:float, 
                       low:float, close:float, volume:int, barCount:int, 
                        WAP:float, hasGaps:int):
        self.logAnswer(crt_fn_name(), vars()) 


    def scannerParameters(self, xml:str):
        self.logAnswer(crt_fn_name(), vars()) 


    def scannerData(self, reqId:int, rank:int, contractDetails:ContractDetails,
                     distance:str, benchmark:str, projection:str, legsStr:str):
        self.logAnswer(crt_fn_name(), vars()) 


    def scannerDataEnd(self, reqId:int):
        self.logAnswer(crt_fn_name(), vars()) 


    def realtimeBar(self, reqId:TickerId , time:int, open:float, high:float, 
                    low:float, close:float, volume:int, wap:float, 
                    count: int):
        self.logAnswer(crt_fn_name(), vars()) 


    def currentTime(self, time:int):
        self.logAnswer(crt_fn_name(), vars()) 


    def fundamentalData(self, reqId:TickerId , data:str):
        """This function is called to receive Reuters global fundamental
        market data. There must be a subscription to Reuters Fundamental set 
        up in Account Management before you can receive this data."""

        self.logAnswer(crt_fn_name(), vars()) 


    def deltaNeutralValidation(self, reqId:int, underComp:UnderComp):
        """Upon accepting a Delta-Neutral RFQ(request for quote), the
        server sends a deltaNeutralValidation() message with the UnderComp
        structure. If the delta and price fields are empty in the original
        request, the confirmation will contain the current values from the
        server. These values are locked when the RFQ is processed and remain
        locked until the RFQ is canceled."""

        self.logAnswer(crt_fn_name(), vars()) 


    def tickSnapshotEnd(self, reqId:int):
        """This is called after a batch updateAccountValue() and
        updatePortfolio() is sent."""

        self.logAnswer(crt_fn_name(), vars()) 


    def marketDataType(self, reqId:TickerId , marketDataType:int):
        """TWS sends a marketDataType(type) callback to the API, where
        type is set to Frozen or RealTime, to announce that market data has been
        switched between frozen and real-time. This notification occurs only
        when market data switches between real-time and frozen. The
        marketDataType( ) callback accepts a reqId parameter and is sent per
        every subscription because different contracts can generally trade on a
        different schedule."""

        self.logAnswer(crt_fn_name(), vars()) 

    def commissionReport(self, commissionReport:CommissionReport):
        """The commissionReport() callback is triggered as follows:
        - immediately after a trade execution
        - by calling reqExecutions()."""

        self.logAnswer(crt_fn_name(), vars()) 


    def position(self, account:str, contract:Contract, position:float, 
                 avgCost:float):
        """This event returns real-time positions for all accounts in
        response to the reqPositions() method."""

        self.logAnswer(crt_fn_name(), vars()) 


    def positionEnd(self):
        """This is called once all position data for a given request are
        received and functions as an end marker for the position() data. """

        self.logAnswer(crt_fn_name(), vars()) 


    def accountSummary(self, reqId:int, account:str, tag:str, value:str, 
                       curency:str):
        """Returns the data from the TWS Account Window Summary tab in
        response to reqAccountSummary()."""

        self.logAnswer(crt_fn_name(), vars()) 


    def accountSummaryEnd(self, reqId:int):
        """This method is called once all account summary data for a
        given request are received."""

        self.logAnswer(crt_fn_name(), vars()) 


    def verifyMessageAPI(self, apiData:str):

        self.logAnswer(crt_fn_name(), vars()) 


    def verifyCompleted(self, isSuccessful:bool, errorText:str):

        self.logAnswer(crt_fn_name(), vars()) 


    def verifyAndAuthMessageAPI(self, apiData:str, xyzChallange:str):

        self.logAnswer(crt_fn_name(), vars()) 


    def verifyAndAuthCompleted(isSuccessful:bool, errorText:str):

        self.logAnswer(crt_fn_name(), vars()) 

 
    def displayGroupList(self, reqId:int, groups:str):
        """This callback is a one-time response to queryDisplayGroups().

        reqId - The requestId specified in queryDisplayGroups().
        groups - A list of integers representing visible group ID separated by
            the | character, and sorted by most used group first. This list will
             not change during TWS session (in other words, user cannot add a 
            new group; sorting can change though)."""

        self.logAnswer(crt_fn_name(), vars()) 


    def displayGroupUpdated(self, reqId:int, contractInfo:str):
        """This is sent by TWS to the API client once after receiving
        the subscription request subscribeToGroupEvents(), and will be sent
        again if the selected contract in the subscribed display group has
        changed.

        requestId - The requestId specified in subscribeToGroupEvents().
        contractInfo - The encoded value that uniquely represents the contract 
            in IB. Possible values include:
            none = empty selection
            contractID@exchange = any non-combination contract. 
                Examples: 8314@SMART for IBM SMART; 8314@ARCA for IBM @ARCA.
            combo = if any combo is selected.  """

        self.logAnswer(crt_fn_name(), vars()) 


    def positionMulti(self, reqId:int, account:str, modelCode:str,
                      contract:Contract, pos:float, avgCost:float):
        """same as position() except it can be for a certain
        account/model"""

        self.logAnswer(crt_fn_name(), vars()) 


    def positionMultiEnd(self, reqId:int):
        """same as positionEnd() except it can be for a certain
        account/model"""

        self.logAnswer(crt_fn_name(), vars()) 


    def accountUpdateMulti(self, reqId:int, account:str, modelCode:str,
                            key:str, value:str, currency:str):
        """same as updateAccountValue() except it can be for a certain
        account/model"""

        self.logAnswer(crt_fn_name(), vars()) 


    def accountUpdateMultiEnd(self, reqId:int):
        """same as accountDownloadEnd() except it can be for a certain
        account/model"""

        self.logAnswer(crt_fn_name(), vars()) 


    SetOfString = set
    SetOfFloat = set
    def securityDefinitionOptionalParameter(self, reqId:int, exchange:str,
        underlyingConId:int, tradingClass:str, multiplier:str, 
        expirations:SetOfString, strikes:SetOfFloat):
        """ gets called w/ the future and option contracts for an underlying"""

        self.logAnswer(crt_fn_name(), vars()) 


    def securityDefinitionOptionalParameterEnd(self, reqId:int):
        self.logAnswer(crt_fn_name(), vars()) 


    def softDollarTiers(self, reqId:int, tiers:list):
        self.logAnswer(crt_fn_name(), vars()) 


    ListOfFamilyCode = list
    def familyCodes(self, familyCodes:ListOfFamilyCode):
        self.logAnswer(crt_fn_name(), vars()) 


    ListOfContractDescription = list
    def symbolSamples(self, reqId:int, contractDescriptions:ListOfContractDescription):
        self.logAnswer(crt_fn_name(), vars()) 



