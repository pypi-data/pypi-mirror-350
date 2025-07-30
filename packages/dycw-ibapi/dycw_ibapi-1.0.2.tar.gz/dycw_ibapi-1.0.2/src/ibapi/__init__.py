"""Copyright (C) 2023 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

""" Package implementing the Python API for the TWS/IB Gateway """


VERSION = {"major": 10, "minor": 30, "micro": 1}


def get_version_string():
    return "{major}.{minor}.{micro}".format(**VERSION)


__version__ = get_version_string()
__qrt_version__ = "1.0.2"
