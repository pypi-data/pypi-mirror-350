"""Copyright (C) 2019 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

from __future__ import annotations


class Object:
    def __str__(self) -> str:
        return "Object"

    def __repr__(self) -> str:
        return str(id(self)) + ": " + self.__str__()
