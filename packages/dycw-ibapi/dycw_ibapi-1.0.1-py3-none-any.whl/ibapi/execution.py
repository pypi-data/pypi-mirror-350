"""Copyright (C) 2023 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

from __future__ import annotations

from ibapi.const import UNSET_DECIMAL
from ibapi.object_implem import Object
from ibapi.utils import decimalMaxString, floatMaxString, intMaxString


class Execution(Object):
    def __init__(self) -> None:
        self.execId = ""
        self.time = ""
        self.acctNumber = ""
        self.exchange = ""
        self.side = ""
        self.shares = UNSET_DECIMAL
        self.price = 0.0
        self.permId = 0
        self.clientId = 0
        self.orderId = 0
        self.liquidation = 0
        self.cumQty = UNSET_DECIMAL
        self.avgPrice = 0.0
        self.orderRef = ""
        self.evRule = ""
        self.evMultiplier = 0.0
        self.modelCode = ""
        self.lastLiquidity = 0
        self.pendingPriceRevision = False

    def __str__(self) -> str:
        return (
            f"ExecId: {self.execId}, Time: {self.time}, Account: {self.acctNumber}, Exchange: {self.exchange}, Side: {self.side}, Shares: {decimalMaxString(self.shares)}, Price: {floatMaxString(self.price)}, PermId: {intMaxString(self.permId)}, "
            f"ClientId: {intMaxString(self.clientId)}, OrderId: {intMaxString(self.orderId)}, Liquidation: {intMaxString(self.liquidation)}, CumQty: {decimalMaxString(self.cumQty)}, AvgPrice: {floatMaxString(self.avgPrice)}, OrderRef: {self.orderRef}, EvRule: {self.evRule}, "
            f"EvMultiplier: {floatMaxString(self.evMultiplier)}, ModelCode: {self.modelCode}, LastLiquidity: {intMaxString(self.lastLiquidity)}, PendingPriceRevision: {self.pendingPriceRevision}"
        )


class ExecutionFilter(Object):
    # Filter fields
    def __init__(self) -> None:
        self.clientId = 0
        self.acctCode = ""
        self.time = ""
        self.symbol = ""
        self.secType = ""
        self.exchange = ""
        self.side = ""
