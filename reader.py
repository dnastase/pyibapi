#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


"""
The Reader runs in a separate threads and is responsible for receiving the
incoming messages.
It will receive them and put them in a Queue.
"""


from threading import Thread
import comm
from logger import LOGGER


class Reader(Thread):
    def __init__(self, conn, msg_queue):
        super().__init__()
        self.conn = conn
        self.msg_queue = msg_queue


    def run(self):
        while self.conn.is_connected():
        
            buf = self.conn.recv_msg()
            LOGGER.debug("reader loop, recvd size: %d buf %s", len(buf), buf)
           
            while len(buf) > 0:
                (size, msg, buf) = comm.read_msg(buf)
                #LOGGER.debug("resp %s", buf.decode('ascii'))
                LOGGER.debug("size:%d msg:|%s| buf:%s|", size, buf, "|")
                self.msg_queue.put(msg)

        LOGGER.debug("Reader thread finished")

