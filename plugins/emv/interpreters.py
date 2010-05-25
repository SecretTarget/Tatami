# -*- coding: utf-8 -*-

import structures


def interpretInteger(value):
    n = 0
    for c in value:
        n = n*256 + c
    return str(n)


def interpretString(value):
    txt = ""
    for c in value:
        txt += chr(c)
    return txt
    
    
def interpretHexString(value):
    txt = ""
    for c in value:
        txt += "%02x " % c
    return txt


interpretingFunctions = {
    0x4f:   ("Application ID", interpretHexString),
    0x50:   ("Application name", interpretString),
    0x61:   ("EMV Application information", -1),
    0x70:   ("Application information", -1),
    0x84:   ("DF name", interpretString),
    0x87:   ("Application priority", interpretInteger)
}
