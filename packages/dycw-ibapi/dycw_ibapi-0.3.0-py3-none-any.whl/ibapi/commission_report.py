"""Copyright (C) 2019 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

from __future__ import annotations

from ibapi.object_implem import Object
from ibapi.utils import floatMaxString, intMaxString


class CommissionReport(Object):
    def __init__(self) -> None:
        self.execId = ""
        self.commission = 0.0
        self.currency = ""
        self.realizedPNL = 0.0
        self.yield_ = 0.0
        self.yieldRedemptionDate = 0  # YYYYMMDD format

    def __str__(self) -> str:
        return f"ExecId: {self.execId}, Commission: {floatMaxString(self.commission)}, Currency: {self.currency}, RealizedPnL: {floatMaxString(self.realizedPNL)}, Yield: {floatMaxString(self.yield_)}, YieldRedemptionDate: {intMaxString(self.yieldRedemptionDate)}"
