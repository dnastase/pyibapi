#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""
 


import logging
import time

time.strftime("pyibapi.%Y%m%d_%H%M%S.log")

recfmt = '\n(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'

timefmt = '%y%m%d_%H:%M:%S'

#TODO: the choice if to rewrite log should possibly come from cmd line switch
#logging.basicConfig( level=logging.DEBUG, 
#                    format=recfmt, datefmt=timefmt)
logging.basicConfig(filename=time.strftime("pyibapi.%y%m%d_%H%M%S.log") , 
                    filemode="w",
                    level=logging.DEBUG, 
                    format=recfmt, datefmt=timefmt)
LOGGER = logging.getLogger("pyibapi")

#TODO:logging module is SLOW !

