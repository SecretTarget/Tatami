# -*- coding: utf-8 -*-

import structures

from final_types import FinalType
from codes import MCCs, MNCs

# TODO : rendre les interpréteurs SAFE    

mcc = 0

   
def interpretUnknown(value):
    return interpretHexString(value)
    
    
def interpretHexString(value):
    txt = ""
    for c in value:
        txt += "%02x " % c
    return txt
    
    
def interpretRevHexString(value):
    txt = ""
    for c in value:
        txt += "%1u%1u" % (c%16, c>>4)
    return txt


def interpretInteger(value):
    n = 0
    for c in value:
        n = n*256 + c
    return str(n)
    
    
def interpretMCC(value):
    global mcc
    code = (value[0]>>4)
    code = 10*code + value[1]%16
    code = 10*code + (value[1]>>4)
    mcc = code
    return matchWithIntCode(MCCs, code)
    
    
def interpretMNC(value):
    global mcc
    code = str(mcc)+'-'+interpretRevHexString(value)
    return matchWithIntCode(MNCs, code)


interpretingFunctions = {
    FinalType.RevHexString: interpretRevHexString,
    FinalType.HexString: interpretHexString,
    FinalType.Integer: interpretInteger,
    FinalType.MCC: interpretMCC,
    FinalType.MNC: interpretMNC,

    FinalType.Unknown: interpretUnknown,
}


def matchWithIntCode(codes, code):
    """Renvoie la valeur associée à un code.
    `codes' est un dictionnaire, les clés sont les codes entiers,
    `value' est une clé potentielle en binaire."""
    if code in codes:
        res = codes[code]
    else:
        res = "Inconnu"
    return res

