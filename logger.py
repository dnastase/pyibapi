#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""
 


import logging


recfmt = '\n(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(message)s'

timefmt = '%y%m%d_%H:%M:%S'

logging.basicConfig(level=logging.DEBUG, format=recfmt, datefmt=timefmt)
LOGGER = logging.getLogger("pyibapi")

#TODO:logging module is SLOW !

