#!/usr/bin/env python3

"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


import comm

 
class OrderCondition:
    Price = 1
    Time = 3
    Margin = 4
    Execution = 5
    Volume = 6
    PercentChange = 7

    def __init__(self):
        self.condType = None
        self.isConjunctionConnection = False

    def readExternal(self, fields):
        connector = decode(str, fields)
        self.isConjunctionConnection = connector == "a"

    #TODO: complete !!
    #void writeExternal(std::ostream &out) const;
    #std::string toString();



class ExecutionCondition(OrderCondition):
    def __init__(self):
        OrderCondition.__init__(self)
        self.secType = ""
        self.exchange = ""
        self.symbol = ""

    def readExternal(self, fields):
        OrderCondition.readExternal(self, fields)
        self.secType = decode(str, fields)
        self.exchange = decode(str, fields)
        self.symbol = decode(str, fields)

    #std::string toString();
    #void writeExternal(std::ostream &out) const;


class OperatorCondition(OrderCondition):
    def __init__(self):
        OrderCondition.__init__(self)
        self.isMore = False

    #std::string valueToString() const = 0;
    #void valueFromString(const std::string &v) = 0;
    def readExternal(self, fields):
        OrderCondition.readExternal(self, fields)
        self.isMore = decode(bool, fields)
    #std::string toString();
    #void writeExternal(std::ostream &out) const;



class MarginCondition(OperatorCondition):
    def __init__(self):
        OperatorCondition.__init__(self)
        self.percent = 0

    #static const OrderConditionType conditionType = OrderConditionType::Margin;
    #std::string valueToString() const;
    #void valueFromString(const std::string &v);
    #std::string toString();


class ContractCondition(OperatorCondition):
    def __init__(self):
        OperatorCondition.__init__(self)
        self.conId = 0
        self.exchange = ""

    #std::string toString();
    def readExternal(self, fields):
        OperatorCondition.readExternal(self, fields)
        self.conId = decode(int, fields)
        self.exchange = decode(str, fields)
    #void writeExternal(std::ostream &out) const;


class TimeCondition(OperatorCondition):
    def __init__(self):
        OperatorCondition.__init__(self)
        self.time = ""

    #std::string valueToString() const;
    #void valueFromString(const std::string &v);
    #static const OrderConditionType conditionType = OrderConditionType::Time;
    #std::string toString();

                              
class PriceCondition(ContractCondition):
    def __init__(self):
        ContractCondition.__init__(self)
        self.price = 0.
        self.triggerMethod = 0

   #std::string valueToString() const;
   #void valueFromString(const std::string &v);

   #static const OrderConditionType conditionType = OrderConditionType::Price;
   #enum Method {
   #       Default = 0,
   #       DoubleBidAsk = 1,
   #       Last = 2,
   #       DoubleLast = 3,
   #       BidAsk = 4,
   #       LastBidAsk = 7,
   #       MidPoint = 8
   #};
   #std::string toString();
    def readExternal(self, fields):
        ContractCondition.readExternal(self, fields)
        self.triggerMethod = decode(int, fields)
   #void writeExternal(std::ostream & out) const;
   #
   #Method triggerMethod();


class PercentChangeCondition(ContractCondition):
    def __init__(self):
        ContractCondition.__init__(self)
        self.changePercent = None

    #virtual std::string valueToString() const;
    #virtual void valueFromString(const std::string &v);
    #static const OrderConditionType conditionType = OrderConditionType::PercentChange;


def Create(condType):
    cond = None

    if Execution == condType:
        cond = ExecutionCondition()
    elif Margin == condType:
        cond = MarginCondition()
    elif PercentChange == condType:
        cond = PercentChangeCondition()
    elif Price == condType:
        cond = PriceCondition()
    elif Time == condType:
        cond = TimeCondition()
    elif Volume == condType:
        cond = VolumeCondition()

    if cond is not None:
        cond.condType = condType

    return cond
  
