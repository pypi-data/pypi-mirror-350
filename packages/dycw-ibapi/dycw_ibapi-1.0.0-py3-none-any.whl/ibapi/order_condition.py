"""Copyright (C) 2019 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

from __future__ import annotations

from ibapi import comm
from ibapi.const import UNSET_DOUBLE
from ibapi.enum_implem import Enum
from ibapi.object_implem import Object
from ibapi.utils import decode

# TODO: add support for Rebate, P/L, ShortableShares conditions


class OrderCondition(Object):
    Price = 1
    Time = 3
    Margin = 4
    Execution = 5
    Volume = 6
    PercentChange = 7

    def __init__(self, condType) -> None:
        self.condType = condType
        self.isConjunctionConnection = True

    def type(self):
        return self.condType

    def And(self):
        self.isConjunctionConnection = True
        return self

    def Or(self):
        self.isConjunctionConnection = False
        return self

    def decode(self, fields) -> None:
        connector = decode(str, fields)
        self.isConjunctionConnection = connector == "a"

    def make_fields(self):
        return [comm.make_field("a" if self.isConjunctionConnection else "o")]

    def __str__(self) -> str:
        return "<AND>" if self.isConjunctionConnection else "<OR>"


class ExecutionCondition(OrderCondition):
    def __init__(self, secType=None, exch=None, symbol=None) -> None:
        OrderCondition.__init__(self, OrderCondition.Execution)
        self.secType = secType
        self.exchange = exch
        self.symbol = symbol

    def decode(self, fields) -> None:
        OrderCondition.decode(self, fields)
        self.secType = decode(str, fields)
        self.exchange = decode(str, fields)
        self.symbol = decode(str, fields)

    def make_fields(self):
        return [
            *OrderCondition.make_fields(self),
            comm.make_field(self.secType),
            comm.make_field(self.exchange),
            comm.make_field(self.symbol),
        ]

    def __str__(self) -> str:
        return (
            "trade occurs for "
            + self.symbol
            + " symbol on "
            + self.exchange
            + " exchange for "
            + self.secType
            + " security type"
        )


class OperatorCondition(OrderCondition):
    def __init__(self, condType=None, isMore=None) -> None:
        OrderCondition.__init__(self, condType)
        self.isMore = isMore

    def valueToString(self) -> str:
        msg = "abstractmethod!"
        raise NotImplementedError(msg)

    def setValueFromString(self, text: str) -> None:
        msg = "abstractmethod!"
        raise NotImplementedError(msg)

    def decode(self, fields) -> None:
        OrderCondition.decode(self, fields)
        self.isMore = decode(bool, fields)
        text = decode(str, fields)
        self.setValueFromString(text)

    def make_fields(self):
        return [
            *OrderCondition.make_fields(self),
            comm.make_field(self.isMore),
            comm.make_field(self.valueToString()),
        ]

    def __str__(self) -> str:
        sb = ">= " if self.isMore else "<= "
        return f" {sb} {self.valueToString()}"


class MarginCondition(OperatorCondition):
    def __init__(self, isMore=None, percent=None) -> None:
        OperatorCondition.__init__(self, OrderCondition.Margin, isMore)
        self.percent = percent

    def decode(self, fields) -> None:
        OperatorCondition.decode(self, fields)

    def make_fields(self):
        return OperatorCondition.make_fields(self)

    def valueToString(self) -> str:
        return str(self.percent)

    def setValueFromString(self, text: str) -> None:
        self.percent = float(text)

    def __str__(self) -> str:
        return f"the margin cushion percent {OperatorCondition.__str__(self)} "


class ContractCondition(OperatorCondition):
    def __init__(self, condType=None, conId=None, exch=None, isMore=None) -> None:
        OperatorCondition.__init__(self, condType, isMore)
        self.conId = conId
        self.exchange = exch

    def decode(self, fields) -> None:
        OperatorCondition.decode(self, fields)
        self.conId = decode(int, fields)
        self.exchange = decode(str, fields)

    def make_fields(self):
        return [
            *OperatorCondition.make_fields(self),
            comm.make_field(self.conId),
            comm.make_field(self.exchange),
        ]

    def valueToString(self) -> str:
        # TODO
        pass

    def setValueFromString(self, text: str) -> None:
        # TODO
        pass

    def __str__(self) -> str:
        return f"{self.conId} on {self.exchange} is {OperatorCondition.__str__(self)} "


class TimeCondition(OperatorCondition):
    def __init__(self, isMore=None, time=None) -> None:
        OperatorCondition.__init__(self, OrderCondition.Time, isMore)
        self.time = time

    def decode(self, fields) -> None:
        OperatorCondition.decode(self, fields)

    def make_fields(self):
        return OperatorCondition.make_fields(self)

    def valueToString(self) -> str:
        return self.time

    def setValueFromString(self, text: str) -> None:
        self.time = text

    def __str__(self) -> str:
        return f"time is {OperatorCondition.__str__(self)} "


class PriceCondition(ContractCondition):
    TriggerMethodEnum = Enum(
        "Default",  # = 0,
        "DoubleBidAsk",  # = 1,
        "Last",  # = 2,
        "DoubleLast",  # = 3,
        "BidAsk",  # = 4,
        "N/A1",
        "N/A2",
        "LastBidAsk",  # = 7,
        "MidPoint",
    )  # = 8

    def __init__(
        self, triggerMethod=None, conId=None, exch=None, isMore=None, price=None
    ) -> None:
        ContractCondition.__init__(self, OrderCondition.Price, conId, exch, isMore)
        self.price = price
        self.triggerMethod = triggerMethod

    def decode(self, fields) -> None:
        ContractCondition.decode(self, fields)
        self.triggerMethod = decode(int, fields)

    def make_fields(self):
        return [
            *ContractCondition.make_fields(self),
            comm.make_field(self.triggerMethod),
        ]

    def valueToString(self) -> str:
        return str(self.price)

    def setValueFromString(self, text: str) -> None:
        self.price = float(text)

    @property
    def __str__(self) -> str:
        return f"{PriceCondition.TriggerMethodEnum.toStr(self.triggerMethod)} price of {ContractCondition.__str__(self)} "


class PercentChangeCondition(ContractCondition):
    def __init__(
        self, conId=None, exch=None, isMore=None, changePercent=UNSET_DOUBLE
    ) -> None:
        ContractCondition.__init__(
            self, OrderCondition.PercentChange, conId, exch, isMore
        )
        self.changePercent = changePercent

    def decode(self, fields) -> None:
        ContractCondition.decode(self, fields)

    def make_fields(self):
        return ContractCondition.make_fields(self)

    def valueToString(self) -> str:
        return str(self.changePercent)

    def setValueFromString(self, text: str) -> None:
        self.changePercent = float(text)

    def __str__(self) -> str:
        return f"percent change of {ContractCondition.__str__(self)} "


class VolumeCondition(ContractCondition):
    def __init__(self, conId=None, exch=None, isMore=None, volume=None) -> None:
        ContractCondition.__init__(self, OrderCondition.Volume, conId, exch, isMore)
        self.volume = volume

    def decode(self, fields) -> None:
        ContractCondition.decode(self, fields)

    def make_fields(self):
        return ContractCondition.make_fields(self)

    def valueToString(self) -> str:
        return str(self.volume)

    def setValueFromString(self, text: str) -> None:
        self.volume = int(text)

    def __str__(self) -> str:
        return f"volume of {ContractCondition.__str__(self)} "


def Create(condType):
    cond = None

    if OrderCondition.Execution == condType:
        cond = ExecutionCondition()
    elif OrderCondition.Margin == condType:
        cond = MarginCondition()
    elif OrderCondition.PercentChange == condType:
        cond = PercentChangeCondition()
    elif OrderCondition.Price == condType:
        cond = PriceCondition()
    elif OrderCondition.Time == condType:
        cond = TimeCondition()
    elif OrderCondition.Volume == condType:
        cond = VolumeCondition()

    return cond
