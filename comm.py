#!/usr/bin/env python3


"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


"""
This module has tools for implementing the IB low level messaging.
"""


import struct
from logger import LOGGER


def make_msg(text) -> bytes:
    """ adds the length prefix """
    #msg = array.array('B', 
    msg = struct.pack("!I%ds" % len(text), len(text), str.encode(text))
    return msg


def make_field(val) -> bytes:
    """ adds the NULL string terminator """
    field = str(val) + '\0'
    return field


def read_msg(buf: bytes) -> tuple:
    """ first the size prefix and then the corresponding msg payload """
    size = struct.unpack("!I", buf[0:4])[0]
    text = struct.unpack("!%ds" % size, buf[4:4+size])[0]

    return (size, text, buf[4+size:])
     

def read_fields(buf: bytes) -> tuple:
    """ msg payload is made of fields terminated/separated by NULL chars """
    fields = buf.split(b"\0")

    return fields[0:-1]   #last one is empty; this may slow dow things though, TODO


def send_msg(the_socket, msg):
    the_socket.send(msg)


def recv_msg(the_socket):
    cont = True
    allbuf = b""

    while cont:
        buf = the_socket.recv(4096)
        allbuf += buf
        LOGGER.debug("len %d raw:%s|", len(buf), buf)

        if len(buf) < 4096:
            cont = False

    return allbuf  
  