#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


"""
Just a thin wrapper around a socket.
It allows us to keep some other info w/ it.
"""

import sys
import socket
import comm
from logger import LOGGER


class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None


    def connect(self):
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))
        self.socket.settimeout(1)


    def disconnect(self):
        LOGGER.debug("disconnecting")
        self.socket.close()
        self.socket = None
        LOGGER.debug("disconnected")


    def is_connected(self):
        #TODO: also handle when socket gets interrupted/error
        return self.socket is not None

    def recv_msg(self):
        try:
            buf = comm.recv_msg(self.socket)
        except:
            LOGGER.debug("exception from recv_msg %s", sys.exc_info())
            buf = b""
        else:
            pass

        return buf            
        
