# -*- coding: utf-8 -*-

import structures
from final_types import FinalType


def hexAsInt(c):
    return (c>>4)*10 + (c%16)


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
    
    
def interpretAID(value):
    structures.aidList.append(value)
    return interpretUnknown(value)


def interpretDate(value):
    return "%02u / %02u / %02u" % (hexAsInt(value[2]), hexAsInt(value[1]), hexAsInt(value[0]))
    
    
def interpretAmount(value):
    amount = 0
    for i in range(5):
        c = hexAsInt(value[i])
        amount = amount*100 + c
    cents = hexAsInt(value[5])
    return "%u.%02u" % (amount, cents)
    
    
def interpretUnknown(value):
    txt = ""
    for c in value:
        txt += "%02x " % c
    return txt


interpretingFunctions = {
    0x4f:   ("Application ID", interpretAID),
    0x50:   ("Application name", interpretString),
    0x61:   ("EMV Application information", -1),
    0x70:   ("Application information", -1),
    0x84:   ("DF name", interpretString),
    0x87:   ("Application priority", interpretInteger),
    
    FinalType.Date: interpretDate,
    FinalType.Amount: interpretAmount,
    FinalType.Integer: interpretInteger,

    FinalType.Unknown: interpretUnknown,
}
