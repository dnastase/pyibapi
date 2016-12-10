#!/usr/bin/env python3

"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


"""
	SAME_POS    = open/close leg value is same as combo
	OPEN_POS    = open
	CLOSE_POS   = close
	UNKNOWN_POS = unknown
"""
(SAME_POS, OPEN_POS, CLOSE_POS, UNKNOWN_POS) = range(4)

class ComboLeg:
    def __init__():
        self.conId = 0  # type: int
        self.ratio = 0  # type: int
        self.action = ""      # BUY/SELL/SSHORT 
        self.exchange = ""
        self.openClose = 0   # type: int; LegOpenClose enum values 
         # for stock legs when doing short sale
        self.shortSaleSlot = 0
        self.designatedLocation = ""
        self.exemptCode = -1

#        //operator ==()
#		return (conId == other.conId &&
#			ratio == other.ratio &&
#			openClose == other.openClose &&
#			shortSaleSlot == other.shortSaleSlot &&
#			exemptCode == other.exemptCode &&
#			action == other.action &&
#			exchange == other.exchange &&
#			designatedLocation == other.designatedLocation);


class UnderComp:
    def __init__(self):
        self.conId = 0   # type: int
        self.delta = 0.  # type: float
        self.price = 0.  # type: float


class Contract:
    def __init__(self):
        self.conId = 0
        self.symbol = ""
        self.secType = ""
        self.lastTradeDateOrContractMonth = ""
        self.strike = 0
        self.right = ""
        self.multiplier = ""
        self.exchange = ""
        self.primaryExchange = "" # pick an actual (ie non-aggregate) exchange that the contract trades on.  DO NOT SET TO SMART.
        self.currency = ""
        self.localSymbol = ""
        self.tradingClass = ""
        self.includeExpired = False
        self.secIdType = ""	  # CUSIP;SEDOL;ISIN;RIC
        self.secId = ""

        #combos
        self.comboLegsDescrip = ""  # type: str; received in open order 14 and up for all combos
        self.comboLegs = None     # type: vector<ComboLeg>
        self.underComp = None


class ContractDetails:
    def __init__(self):
        self.summary = Contract()        
        self.marketName = ""
        self.minTick = 0.
        self.orderTypes = ""
        self.validExchanges = ""
        self.priceMagnifier = 0
        self.underConId = 0
        self.longName = ""
        self.contractMonth = ""
        self.industry = ""
        self.category = ""
        self.subcategory = ""
        self.timeZoneId = ""
        self.tradingHours = ""
        self.liquidHours = ""
        self.evRule = ""
        self.evMultiplier = 0
        self.secIdList = None
        # BOND values
        self.cusip = ""
        self.ratings = ""
        self.descAppend = ""
        self.bondType = ""
        self.couponType = "" 
        self.callable = False
        self.putable = False
        self.coupon = 0
        self.convertible = False
        self.maturity = ""
        self.issueDate = ""
        self.nextOptionDate = ""
        self.nextOptionType = ""
        self.nextOptionPartial = False
        self.notes = "" 


class ContractDescription:
    def __init__(self):
        self.contract = Contract()
        self.derivativeSecTypes = None   # type: vector<std::string>


#inline void
#Contract::CloneComboLegs(ComboLegListSPtr& dst, const ComboLegListSPtr& src)
#{
#	if (!src.get())
#		return;
#
#	dst->reserve(src->size());
#
#	ComboLegList::const_iterator iter = src->begin();
#	const ComboLegList::const_iterator iterEnd = src->end();
#
#	for (; iter != iterEnd; ++iter) {
#		const ComboLeg* leg = iter->get();
#		if (!leg)
#			continue;
#		dst->push_back(ComboLegSPtr(new ComboLeg(*leg)));
#	}
#}
#

