#!/usr/bin/env python3

"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""

"""
The Decoder knows how to transform a message's payload into higher level 
IB message (eg: order info, mkt data, etc).
It will call the corresponding method from the Wrapper so that customer's code
(eg: class derived from Wrapper) can make further use of the data.
"""


import inspect

from message import IN, OUT
from wrapper import Wrapper
from order import Order
from contract import Contract
from contract import UnderComp
import order_condition
from order_state import OrderState 
from logger import LOGGER



#MIN_SERVER_VER_REAL_TIME_BARS       = 34;
#MIN_SERVER_VER_SCALE_ORDERS         = 35;
#MIN_SERVER_VER_SNAPSHOT_MKT_DATA    = 35;
#MIN_SERVER_VER_SSHORT_COMBO_LEGS    = 35;
#MIN_SERVER_VER_WHAT_IF_ORDERS       = 36;
#MIN_SERVER_VER_CONTRACT_CONID       = 37;
MIN_SERVER_VER_PTA_ORDERS             = 39;
MIN_SERVER_VER_FUNDAMENTAL_DATA       = 40;
MIN_SERVER_VER_UNDER_COMP             = 40;
MIN_SERVER_VER_CONTRACT_DATA_CHAIN    = 40;
MIN_SERVER_VER_SCALE_ORDERS2          = 40;
MIN_SERVER_VER_ALGO_ORDERS            = 41;
MIN_SERVER_VER_EXECUTION_DATA_CHAIN   = 42;
MIN_SERVER_VER_NOT_HELD               = 44;
MIN_SERVER_VER_SEC_ID_TYPE            = 45;
MIN_SERVER_VER_PLACE_ORDER_CONID      = 46;
MIN_SERVER_VER_REQ_MKT_DATA_CONID     = 47;
MIN_SERVER_VER_REQ_CALC_IMPLIED_VOLAT = 49;
MIN_SERVER_VER_REQ_CALC_OPTION_PRICE  = 50;
MIN_SERVER_VER_CANCEL_CALC_IMPLIED_VOLAT = 50;
MIN_SERVER_VER_CANCEL_CALC_OPTION_PRICE  = 50;
MIN_SERVER_VER_SSHORTX_OLD            = 51;
MIN_SERVER_VER_SSHORTX                = 52;
MIN_SERVER_VER_REQ_GLOBAL_CANCEL      = 53;
MIN_SERVER_VER_HEDGE_ORDERS			= 54;
MIN_SERVER_VER_REQ_MARKET_DATA_TYPE	= 55;
MIN_SERVER_VER_OPT_OUT_SMART_ROUTING  = 56;
MIN_SERVER_VER_SMART_COMBO_ROUTING_PARAMS = 57;
MIN_SERVER_VER_DELTA_NEUTRAL_CONID    = 58;
MIN_SERVER_VER_SCALE_ORDERS3          = 60;
MIN_SERVER_VER_ORDER_COMBO_LEGS_PRICE = 61;
MIN_SERVER_VER_TRAILING_PERCENT       = 62;
MIN_SERVER_VER_DELTA_NEUTRAL_OPEN_CLOSE = 66;
MIN_SERVER_VER_POSITIONS              = 67;
MIN_SERVER_VER_ACCOUNT_SUMMARY        = 67;
MIN_SERVER_VER_TRADING_CLASS          = 68;
MIN_SERVER_VER_SCALE_TABLE            = 69;
MIN_SERVER_VER_LINKING                = 70;
MIN_SERVER_VER_ALGO_ID                = 71;
MIN_SERVER_VER_OPTIONAL_CAPABILITIES  = 72;
MIN_SERVER_VER_ORDER_SOLICITED        = 73;
MIN_SERVER_VER_LINKING_AUTH           = 74;
MIN_SERVER_VER_PRIMARYEXCH            = 75;
MIN_SERVER_VER_RANDOMIZE_SIZE_AND_PRICE = 76;
MIN_SERVER_VER_FRACTIONAL_POSITIONS = 101;
MIN_SERVER_VER_PEGGED_TO_BENCHMARK = 102;
MIN_SERVER_VER_MODELS_SUPPORT         = 103;
MIN_SERVER_VER_SEC_DEF_OPT_PARAMS_REQ = 104;
MIN_SERVER_VER_EXT_OPERATOR	        = 105;
MIN_SERVER_VER_SOFT_DOLLAR_TIER		= 106;
MIN_SERVER_VER_REQ_FAMILY_CODES		= 107;
MIN_SERVER_VER_REQ_MATCHING_SYMBOLS	= 108;
MIN_SERVER_VER_PAST_LIMIT		= 109;

# 100+ messaging */
# 100 = enhanced handshake, msg length prefixes

MIN_CLIENT_VER = 100;
MAX_CLIENT_VER = MIN_SERVER_VER_PAST_LIMIT;




SHOW_UNSET = True
def decode(the_type, fields, show_unset = False):
    s = next(fields)
    LOGGER.debug("decode %s %s", the_type, s)

    if the_type is str:
        return s
    
    orig_type = the_type
    if the_type is bool:
        the_type = int
        
    if show_unset:
        if s is None or len(s) == 0:
            n = None
        else:
            n = the_type(s)
    else:
        n = the_type(s or 0)

    if orig_type is bool:
        n = False if n == 0 else True

    return n
         

#TODO: rm meth=None
class HandleInfo:
    def __init__(self, wrap=None, proc=None):
        self.wrapperMeth = wrap
        self.wrapperParams = None
        self.processMeth = proc


class Decoder:
    def __init__(self, wrapper, serverVersion):
        self.wrapper = wrapper
        self.serverVersion = serverVersion
        self.discover_params()


    def processOpenOrder(self, fields):

        sMsgId = next(fields)
        version = decode(int, fields)

        order = Order()
        order.orderId = decode(int, fields)

        contract = Contract()

        contract.conId = decode(int, fields) # ver 17 field
        contract.symbol = decode(str, fields) 
        contract.secType = decode(str, fields) 
        contract.lastTradeDateOrContractMonth = decode(str, fields) 
        contract.strike = decode(int, fields)
        contract.right = decode(str, fields) 
        if version >= 32:
            contract.multiplier = decode(str, fields) 
        contract.exchange = decode(str, fields) 
        contract.currency = decode(str, fields) 
        contract.localSymbol = decode(str, fields)  # ver 2 field
        if version >= 32:
            contract.tradingClass = decode(str, fields) 

        # read order fields
        order.action = decode(str, fields)  

        if self.serverVersion >= MIN_SERVER_VER_FRACTIONAL_POSITIONS:
            order.totalQuantity = decode(float, fields)  
        else:
            order.totalQuantity = decode(int, fields)

        order.orderType = decode(str, fields) 
        if version < 29:
            order.lmtPrice = decode(float, fields)
        else:
            order.lmtPrice = decode(float, fields, SHOW_UNSET)
        if version < 30:
            order.auxPrice = decode(float, fields)
        else:
            order.auxPrice = decode(float, fields, SHOW_UNSET)
        order.tif = decode(str, fields)
        order.ocaGroup = decode(str, fields)
        order.account = decode(str, fields)
        order.openClose = decode(str, fields)

        order.origin = decode(int, fields)

        order.orderRef = decode(str, fields)
        order.clientId = decode(int, fields) # ver 3 field
        order.permId = decode(int, fields)   # ver 4 field

        order.outsideRth = decode(bool, fields); # ver 18 field
        order.hidden = decode(bool, fields); # ver 4 field
        order.discretionaryAmt = decode(int, fields); # ver 4 field
        order.goodAfterTime = decode(str, fields); # ver 5 field

        order.sharesAllocation = decode(str, fields); # deprecated ver 6 field

        order.faGroup = decode(str, fields); # ver 7 field
        order.faMethod = decode(str, fields); # ver 7 field
        order.faPercentage = decode(str, fields); # ver 7 field
        order.faProfile = decode(str, fields); # ver 7 field

        if self.serverVersion >= MIN_SERVER_VER_MODELS_SUPPORT:
            order.modelCode = decode(str, fields);

        order.goodTillDate = decode(str, fields); # ver 8 field

        order.rule80A = decode(str, fields); # ver 9 field
        order.percentOffset = decode(float, fields, SHOW_UNSET); # ver 9 field
        order.settlingFirm = decode(str, fields); # ver 9 field
        order.shortSaleSlot = decode(int, fields); # ver 9 field
        order.designatedLocation = decode(str, fields); # ver 9 field
        if self.serverVersion == MIN_SERVER_VER_SSHORTX_OLD:
            exemptCode = decode(int, fields);
        elif version >= 23:
            order.exemptCode = decode(int, fields);
        order.auctionStrategy = decode(int, fields); # ver 9 field
        order.startingPrice = decode(float, fields, SHOW_UNSET); # ver 9 field
        order.stockRefPrice = decode(float, fields, SHOW_UNSET); # ver 9 field
        order.delta = decode(float, fields, SHOW_UNSET); # ver 9 field
        order.stockRangeLower = decode(float, fields, SHOW_UNSET); # ver 9 field
        order.stockRangeUpper = decode(float, fields, SHOW_UNSET); # ver 9 field
        order.displaySize = decode(int, fields); # ver 9 field

        #if( version < 18) {
        #		# will never happen
        #		/* order.rthOnly = */ readBoolFromInt();
        #}

        order.blockOrder = decode(bool, fields); # ver 9 field
        order.sweepToFill = decode(bool, fields); # ver 9 field
        order.allOrNone = decode(bool, fields); # ver 9 field
        order.minQty = decode(int, fields, SHOW_UNSET); # ver 9 field
        order.ocaType = decode(int, fields); # ver 9 field
        order.eTradeOnly = decode(bool, fields); # ver 9 field
        order.firmQuoteOnly = decode(bool, fields); # ver 9 field
        order.nbboPriceCap = decode(float, fields, SHOW_UNSET); # ver 9 field

        order.parentId = decode(int, fields); # ver 10 field
        order.triggerMethod = decode(int, fields); # ver 10 field

        order.volatility = decode(float, fields, SHOW_UNSET); # ver 11 field
        order.volatilityType = decode(int, fields); # ver 11 field
        order.deltaNeutralOrderType = decode(str, fields); # ver 11 field (had a hack for ver 11)
        order.deltaNeutralAuxPrice = decode(float, fields, SHOW_UNSET); # ver 12 field

        if version >= 27 and order.deltaNeutralOrderType:
            order.deltaNeutralConId = decode(int, fields);
            order.deltaNeutralSettlingFirm = decode(str, fields);
            order.deltaNeutralClearingAccount = decode(str, fields);
            order.deltaNeutralClearingIntent = decode(str, fields);

        if version >= 31 and order.deltaNeutralOrderType:
            order.deltaNeutralOpenClose = decode(str, fields);
            order.deltaNeutralShortSale = decode(bool, fields);
            order.deltaNeutralShortSaleSlot = decode(int, fields);
            order.deltaNeutralDesignatedLocation = decode(str, fields);

        order.continuousUpdate = decode(bool, fields); # ver 11 field

        # will never happen
        #if( self.serverVersion == 26) {
        #	order.stockRangeLower = readDouble();
        #	order.stockRangeUpper = readDouble();
        #}

        order.referencePriceType = decode(int, fields); # ver 11 field

        order.trailStopPrice = decode(float, fields, SHOW_UNSET); # ver 13 field

        if version >= 30:
            order.trailingPercent = decode(float, fields, SHOW_UNSET);

        order.basisPoints = decode(float, fields, SHOW_UNSET); # ver 14 field
        order.basisPointsType = decode(int, fields, SHOW_UNSET); # ver 14 field
        contract.comboLegsDescrip = decode(str, fields); # ver 14 field

        if version >= 29:
            contract.comboLegsCount = decode(int, fields);

            if contract.comboLegsCount > 0:
                contract.comboLegs = []
                for idxLeg in range(comboLegsCount):
                    comboLeg = ComboLeg()
                    comboLeg.conId = decode(int, fields);
                    comboLeg.ratio = decode(int, fields);
                    comboLeg.action = decode(str, fields);
                    comboLeg.exchange = decode(str, fields);
                    comboLeg.openClose = decode(int, fields);
                    comboLeg.shortSaleSlot = decode(int, fields);
                    comboLeg.designatedLocation = decode(str, fields);
                    comboLeg.exemptCode = decode(int, fields);
                    contract.comboLegs.append(comboLeg);

            order.orderComboLegsCount = decode(int, fields);
            if order.orderComboLegsCount > 0:
                order.orderComboLegs = []
                for idxOrdLeg in range(orderComboLegsCount):
                    orderComboLeg = OrderComboLeg()
                    orderComboLeg.price = decode(float, fields, SHOW_UNSET);
                    order.orderComboLegs.append(orderComboLeg);

        if version >= 26:
            order.smartComboRoutingParamsCount = decode(int, fields);
            if order.smartComboRoutingParamsCount > 0:
                order.smartComboRoutingParams = []
                for idxPrm in range(smartComboRoutingParamsCount):
                    tagValue = TagValue()
                    tagValue.tag = decode(str, fields);
                    tagValue.value = decode(str, fields);
                    order.smartComboRoutingParams.append(tagValue)

        if version >= 20:
            order.scaleInitLevelSize = decode(int, fields, SHOW_UNSET);
            order.scaleSubsLevelSize = decode(int, fields, SHOW_UNSET);
        else:
            # ver 15 fields
            order.notSuppScaleNumComponents = decode(int, fields, SHOW_UNSET);
            order.scaleInitLevelSize = decode(int, fields, SHOW_UNSET); # scaleComponectSize

        order.scalePriceIncrement = decode(float, fields, SHOW_UNSET); # ver 15 field

        if version >= 28 and order.scalePriceIncrement is not None \
                and order.scalePriceIncrement > 0.0:
            order.scalePriceAdjustValue = decode(float, fields, SHOW_UNSET);
            order.scalePriceAdjustInterval = decode(int, fields, SHOW_UNSET);
            order.scaleProfitOffset = decode(float, fields, SHOW_UNSET);
            order.scaleAutoReset = decode(bool, fields);
            order.scaleInitPosition = decode(int, fields, SHOW_UNSET);
            order.scaleInitFillQty = decode(int, fields, SHOW_UNSET);
            order.scaleRandomPercent = decode(bool, fields);

        if version >= 24:
            order.hedgeType = decode(str, fields);
            if order.hedgeType:
                order.hedgeParam = decode(str, fields);

        if version >= 25:
            order.optOutSmartRouting = decode(bool, fields);

        order.clearingAccount = decode(str, fields); # ver 19 field
        order.clearingIntent = decode(str, fields); # ver 19 field

        if version >= 22:
            order.notHeld = decode(bool, fields);

        if version >= 20:
            contract.underCompPresent = decode(bool, fields);
            if contract.underCompPresent:
                contract.underComp = UnderComp()
                contract.underComp.conId = decode(int, fields);
                contract.underComp.delta = decode(float, fields);
                contract.underComp.price = decode(float, fields);

        if version >= 21:
            order.algoStrategy = decode(str, fields);
            if order.algoStrategy:
                order.algoParamsCount = decode(int, fields);
                if algoParamsCount > 0:
                    order.algoParams = []
                    for idxAlgoPrm in range(algoParamsCount):
                        tagValue = TagValue()
                        tagValue.tag = decode(str, fields);
                        tagValue.value = decode(str, fields);
                        order.algoParams.append(tagValue);

        if version >= 33:
            order.solicited = decode(bool, fields);

        orderState = OrderState()

        order.whatIf = decode(bool, fields); # ver 16 field

        orderState.status = decode(str, fields); # ver 16 field
        orderState.initMargin = decode(str, fields); # ver 16 field
        orderState.maintMargin = decode(str, fields); # ver 16 field
        orderState.equityWithLoan = decode(str, fields); # ver 16 field
        orderState.commission = decode(float, fields, SHOW_UNSET); # ver 16 field
        orderState.minCommission = decode(float, fields, SHOW_UNSET); # ver 16 field
        orderState.maxCommission = decode(float, fields, SHOW_UNSET); # ver 16 field
        orderState.commissionCurrency = decode(str, fields); # ver 16 field
        orderState.warningText = decode(str, fields); # ver 16 field

        if version >= 34:
            order.randomizeSize = decode(bool, fields);
            order.randomizePrice = decode(bool, fields);

        if self.serverVersion >= MIN_SERVER_VER_PEGGED_TO_BENCHMARK:
            if order.orderType == "PEG BENCH":
                order.referenceContractId = decode(int, fields);
                order.isPeggedChangeAmountDecrease = decode(bool, fields);
                order.peggedChangeAmount = decode(float, fields);
                order.referenceChangeAmount = decode(float, fields);
                order.referenceExchangeId = decode(str, fields);

            order.conditionsSize = decode(int, fields);
            if conditionsSize > 0:
                order.conditions = []
                for idxCond in range(conditionsSize):
                    order.conditionType = decode(int, fields);

                    #ibapi::shared_ptr<OrderCondition> item = ibapi::shared_ptr<OrderCondition>(OrderCondition::create((OrderCondition::OrderConditionType)conditionType));
                    #if (!(ptr = item->readExternal(ptr, endPtr)))
                    #        return 0;

                    condition = order_condition.Create(conditionType)
                    condition.readExternal(fields)
                    order.conditions.append(item)

                order.conditionsIgnoreRth = decode(bool, fields);
                order.conditionsCancelOrder = decode(bool, fields);

            order.adjustedOrderType = decode(str, fields);
            order.triggerPrice = decode(float, fields);
            order.trailStopPrice = decode(float, fields);
            order.lmtPriceOffset = decode(float, fields);
            order.adjustedStopPrice = decode(float, fields);
            order.adjustedStopLimitPrice = decode(float, fields);
            order.adjustedTrailingAmount = decode(float, fields);
            order.adjustableTrailingUnit = decode(int, fields);

        if self.serverVersion >= MIN_SERVER_VER_SOFT_DOLLAR_TIER:
            name = decode(str, fields);
            value = decode(str, fields);
            displayName = decode(str, fields);
            order.softDollarTier = SoftDollarTier(name, value, displayName);

        self.wrapper.openOrder(order.orderId, contract, order, orderState)


    def discover_params(self):
        meth2handleInfo = {}
        for handleInfo in self.msgId2handleInfo.values():
            meth2handleInfo[handleInfo.wrapperMeth] = handleInfo
        
        methods = inspect.getmembers(Wrapper, inspect.isfunction)
        for (name, meth) in methods:
            LOGGER.debug("meth %s", name)
            sig = inspect.signature(meth)
            handleInfo = meth2handleInfo.get(meth, None)
            if handleInfo is not None:
                handleInfo.wrapperParams = sig.parameters
        
            for (pname, param) in sig.parameters.items():
                 LOGGER.debug("\tparam %s %s %s", pname, param.name, param.annotation)


    def print_params(self):
        for (msgId, handleInfo) in self.msgId2handleInfo.items():
            if handleInfo.wrapperMeth is not None:
                LOGGER.debug("meth %s", handleInfo.wrapperMeth.__name__)
                if handleInfo.wrapperParams is not None:
                    for (pname, param) in handleInfo.wrapperParams.items():
                         LOGGER.debug("\tparam %s %s %s", pname, param.name, param.annotation)
                    

    #TODO: show error msgs !
    def interpret_with_signature(self, fields, handleInfo):
        if handleInfo.wrapperParams is None:
            LOGGER.debug("no param info")
            return
       
        nIgnoreFields = 2 #bypass msgId and versionId; faster this way
        if len(fields) - nIgnoreFields != len(handleInfo.wrapperParams) - 1:
            LOGGER.debug("diff len fields and params %d %d", len(fields), 
                         len(handleInfo.wrapperParams))
            return 

        fieldIdx = nIgnoreFields
        args = []
        for (pname, param) in handleInfo.wrapperParams.items():
            if pname != "self":
                arg = fields[fieldIdx].decode()
                LOGGER.debug("arg %s type %s", arg, param.annotation)
                if param.annotation is int:
                    arg = int(arg)
                elif param.annotation is float:
                    arg = float(arg)

                args.append(arg)
                fieldIdx += 1

        #handleInfo.wrapperMeth(self.wrapper, *args)
        method = getattr(self.wrapper.__class__, handleInfo.wrapperMeth.__name__)
        LOGGER.debug("calling %s with %s %s", method, self.wrapper, args)
        method(self.wrapper, *args)
       
    
    def interpret(self, fields):
        if len(fields) == 0:
            LOGGER.debug("no fields")
            return

        sMsgId = fields[0]
        nMsgId = int(sMsgId)

        handleInfo = self.msgId2handleInfo.get(nMsgId, None)

        if handleInfo is None:
            LOGGER.debug("no handleInfo")
            return
       
        if handleInfo.wrapperMeth is not None:
            self.interpret_with_signature(fields, handleInfo)
        elif handleInfo.processMeth is not None:
            handleInfo.processMeth(self, iter(fields))

 
    msgId2handleInfo = { 
        IN.TICK_PRICE: HandleInfo(), 
        IN.TICK_SIZE: HandleInfo(wrap=Wrapper.tickSize), 
        IN.ORDER_STATUS: HandleInfo(), 
        IN.ERR_MSG: HandleInfo(), 
        IN.OPEN_ORDER: HandleInfo(proc=processOpenOrder), 
        IN.ACCT_VALUE: HandleInfo(wrap=Wrapper.updateAccountValue), 
        IN.PORTFOLIO_VALUE: HandleInfo(), 
        IN.ACCT_UPDATE_TIME: HandleInfo(), 
        IN.NEXT_VALID_ID: HandleInfo(wrap=Wrapper.nextValidId, ), 
        IN.CONTRACT_DATA: HandleInfo(), 
        IN.EXECUTION_DATA: HandleInfo(), 
        IN.MARKET_DEPTH: HandleInfo(), 
        IN.MARKET_DEPTH_L2: HandleInfo(), 
        IN.NEWS_BULLETINS: HandleInfo(), 
        IN.MANAGED_ACCTS: HandleInfo(wrap=Wrapper.managedAccounts, ),
        IN.RECEIVE_FA: HandleInfo(), 
        IN.HISTORICAL_DATA: HandleInfo(), 
        IN.BOND_CONTRACT_DATA: HandleInfo(), 
        IN.SCANNER_PARAMETERS: HandleInfo(), 
        IN.SCANNER_DATA: HandleInfo(), 
        IN.TICK_OPTION_COMPUTATION: HandleInfo(), 
        IN.TICK_GENERIC: HandleInfo(), 
        IN.TICK_STRING: HandleInfo(), 
        IN.TICK_EFP: HandleInfo(), 
        IN.CURRENT_TIME: HandleInfo(wrap=Wrapper.currentTime, ), 
        IN.REAL_TIME_BARS: HandleInfo(), 
        IN.FUNDAMENTAL_DATA: HandleInfo(), 
        IN.CONTRACT_DATA_END: HandleInfo(), 
        IN.OPEN_ORDER_END: HandleInfo(wrap=Wrapper.openOrderEnd), 
        IN.ACCT_DOWNLOAD_END: HandleInfo(), 
        IN.EXECUTION_DATA_END: HandleInfo(), 
        IN.DELTA_NEUTRAL_VALIDATION: HandleInfo(), 
        IN.TICK_SNAPSHOT_END: HandleInfo(), 
        IN.MARKET_DATA_TYPE: HandleInfo(), 
        IN.COMMISSION_REPORT: HandleInfo(), 
        IN.POSITION_DATA: HandleInfo(), 
        IN.POSITION_END: HandleInfo(), 
        IN.ACCOUNT_SUMMARY: HandleInfo(Wrapper.accountSummary, ), 
        IN.ACCOUNT_SUMMARY_END: HandleInfo(), 
        IN.VERIFY_MESSAGE_API: HandleInfo(), 
        IN.VERIFY_COMPLETED: HandleInfo(), 
        IN.DISPLAY_GROUP_LIST: HandleInfo(), 
        IN.DISPLAY_GROUP_UPDATED: HandleInfo(), 
        IN.VERIFY_AND_AUTH_MESSAGE_API: HandleInfo(), 
        IN.VERIFY_AND_AUTH_COMPLETED: HandleInfo(), 
        IN.POSITION_MULTI: HandleInfo(), 
        IN.POSITION_MULTI_END: HandleInfo(), 
        IN.ACCOUNT_UPDATE_MULTI: HandleInfo(), 
        IN.ACCOUNT_UPDATE_MULTI_END: HandleInfo(), 
        IN.SECURITY_DEFINITION_OPTION_PARAMETER: HandleInfo(), 
        IN.SECURITY_DEFINITION_OPTION_PARAMETER_END: HandleInfo(), 
        IN.SOFT_DOLLAR_TIERS: HandleInfo(), 
        IN.FAMILY_CODES: HandleInfo(), 
        IN.SYMBOL_SAMPLES: HandleInfo(), 
   }



