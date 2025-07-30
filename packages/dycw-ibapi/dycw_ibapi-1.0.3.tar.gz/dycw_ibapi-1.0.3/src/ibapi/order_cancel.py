"""Copyright (C) 2024 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

from ibapi.const import UNSET_INTEGER
from ibapi.object_implem import Object
from ibapi.utils import intMaxString


class OrderCancel(Object):
    def __init__(self) -> None:
        self.manualOrderCancelTime = ""
        self.extOperator = ""
        self.externalUserId = ""
        self.manualOrderIndicator = UNSET_INTEGER

    def __str__(self) -> str:
        return f"manualOrderCancelTime: {self.manualOrderCancelTime}, extOperator: {self.extOperator}, externalUserId: {self.externalUserId}, manualOrderIndicator: {intMaxString(self.manualOrderIndicator)}"
