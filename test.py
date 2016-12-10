#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""

import sys 
import socket 
import struct
import array
import datetime
import inspect

import decoder
import wrapper
from comm import *
from message import IN, OUT
from client import Client
from logger import LOGGER
from connection import Connection
from reader import Reader
from queue import Queue

#import pdb; pdb.set_trace()
#import code; code.interact(local=locals())



class MyWrapper(wrapper.Wrapper):
    def __init__(self, conn):
        self.conn = conn


    def openOrderEnd(self):
        LOGGER.debug("openOrderEnd - quitting")
        self.conn.disconnect()


def main():
    LOGGER.debug("now is %s", datetime.datetime.now())
    import logging
    LOGGER.setLevel(logging.ERROR)

    #enable logging when member vars are assigned
    import utils 
    from order import Order
    Order.__setattr__ = utils.setattr_log
    from contract import Contract,UnderComp
    Contract.__setattr__ = utils.setattr_log 
    UnderComp.__setattr__ = utils.setattr_log 
    from tag_value import TagValue
    TagValue.__setattr__ = utils.setattr_log 

    #from inspect import signature as sig
    #import code; code.interact(local=dict(globals(), **locals()))
    #sys.exit(1)


    global the_conn
    #s = socket.socket()
    #s.connect(("127.0.0.1", 4001))
    the_conn = Connection("127.0.0.1", 4001)
    the_conn.connect()
    
    v100prefix = "API\0"
    v100version = "v100..109"
    msg = make_msg(v100version)
    LOGGER.debug("msg %s", msg)
    msg2 = str.encode(v100prefix, 'ascii') + msg
    LOGGER.debug("msg2 %s", msg2)

    send_msg(the_conn.socket, msg2)
    buf = recv_msg(the_conn.socket)
    (size, text, rest) = read_msg(buf)
    LOGGER.debug("resp %s", buf.decode())
    LOGGER.debug("size %d text %s rest:%s|", size, text, rest)
    fields = read_fields(text)
    LOGGER.debug("fields %s", fields)
    (server_version, date_time) = fields
 
    the_wrapper = MyWrapper(the_conn)
    the_decoder = decoder.Decoder(the_wrapper, int(server_version))
    the_client = Client(the_conn.socket)
    the_msg_queue = Queue()
    the_reader = Reader(the_conn, the_msg_queue)
    the_reader.start()
    the_client.startApi()
    the_client.reqCurrentTime()
    the_client.reqAccountSummary(reqId = 2, groupName = "All", tags = "NetLiquidation")
    the_client.reqAllOpenOrders()
    
    #while the_conn.is_connected():
    #
    #    buf = recv_msg(the_conn.socket)
    #    LOGGER.debug("main loop, recvd buf %s", buf)
    #   
    #    while len(buf) > 0:
    #        (size, text, buf) = read_msg(buf)
    #        LOGGER.debug("resp", buf.decode())
    #        LOGGER.debug("size", size, "text", text, ". buf", buf, "|")
    #        fields = read_fields(text)
    #        LOGGER.debug("fields", fields)
    #        the_decoder.interpret(fields)

    while the_conn.is_connected() or not the_msg_queue.empty():
        try:
            text = the_msg_queue.get(block=True, timeout=0.2)
        except:
            LOGGER.debug("exception from queue.get")
        else:
            fields = read_fields(text)
            LOGGER.debug("fields %s", fields)
            the_decoder.interpret(fields)
        LOGGER.debug("conn:%d queue.sz:%d", the_conn.is_connected(), the_msg_queue.qsize())
        

if __name__ == "__main__":
    main()

