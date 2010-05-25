# -*- coding: utf-8 -*-

import structures

from final_types import FinalType
from countries import countryCodes
from currencies import currencyCodes


def hexAsInt(c):
    return (c>>4)*10 + (c%16)


def hexListAsInt(list):
    res = 0
    for c in list:
        n = hexAsInt(c)
        res = res*100 + n
    return res


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
    amount = hexListAsInt(value[0:5])
    cents = hexAsInt(value[5])
    return "%u.%02u" % (amount, cents)
    
    
def interpretCountry(value):
    code = hexListAsInt(value)
    return countryCodes[code]
    
    
def interpretCurrency(value):
    code = hexListAsInt(value)
    return currencyCodes[code]
    
   
def interpretUnknown(value):
    return interpretHexString(value)
    
    
def interpretHexString(value):
    txt = ""
    for c in value:
        txt += "%02x " % c
    return txt


interpretingFunctions = {
    0x4f:   ("Application ID", interpretAID),
    0x50:   ("Application name", interpretString),
    0x57:   ("Track 2 data", interpretHexString),
    0x5a:   ("Card number", interpretHexString),
    0x61:   ("EMV Application information", -1),
    0x70:   ("Application information", -1),
    0x84:   ("DF name", interpretString),
    0x87:   ("Application priority", interpretInteger),
    0x8c:   ("CDOL 1", interpretHexString),
    0x8d:   ("CDOL 2", interpretHexString),
    0x8e:   ("Cardholder verification list", interpretHexString),
    0x8f:   ("Certificate authority PKI", interpretInteger),
    0x90:   ("Issuer certificate", interpretHexString),
    0x92:   ("Issuer remainder", interpretInteger),
    0x93:   ("Signed static application data", interpretHexString),
    
    0x5f20: ("Cardholder", interpretString),
    0x5f24: ("Validity end", interpretDate),
    0x5f25: ("Validity beginning", interpretDate),
    0x5f28: ("Country", interpretCountry),
    0x5f34: ("PAN sequence number", interpretInteger),
    
    0x9f07:   ("Application usage control", interpretHexString),
    0x9f08:   ("Application version number", interpretInteger),
    0x9f0d:   ("Issuer default action code", interpretHexString),
    0x9f0e:   ("Issuer default denial code", interpretHexString),
    0x9f0f:   ("Issuer default online code", interpretHexString),
    0x9f1f:   ("Track 1 discretionary data", interpretString),
    0x9f32:   ("Issuer exponent", interpretInteger),
    0x9f46:   ("Card certificate", interpretHexString),
    0x9f47:   ("Card exponent", interpretInteger),
    0x9f48:   ("Card remainder", interpretInteger),
    0x9f4a:   ("Static data authentication tag list", interpretInteger),
    
    FinalType.Date: interpretDate,
    FinalType.Amount: interpretAmount,
    FinalType.Integer: interpretInteger,
    FinalType.Country: interpretCountry,
    FinalType.Currency: interpretCurrency,

    FinalType.Unknown: interpretUnknown,
}
