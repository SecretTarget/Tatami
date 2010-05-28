# -*- coding: utf-8 -*-

import structures

from final_types import FinalType
from codes import MCCs, MNCs

# TODO : rendre les interpréteurs SAFE    

mncBase = ""

   
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
        txt += "%1x%1x" % (c%16, c>>4)
    return txt


def interpretInteger(value):
    n = 0
    for c in value:
        n = n*256 + c
    return str(n)
    
    
def interpretIMSIMCC(value):
    global mncBase
    code = (value[0]>>4)
    code = 10*code + value[1]%16
    code = 10*code + (value[1]>>4)
    mncBase = str(code)+'-'
    # TODO : Ça se passe comment si le MNC est à 3 chiffres ?
    return matchWithIntCode(MCCs, code)
    
    
def interpretPLMNMCC(value):
    global mncBase
    code = interpretRevHexString(value)
    mncBase = code[0:3]+'-'
    if code[3] != 'f': # Le MNC est à 3 chiffres
        mncBase += code[3]
    code = int(code[0:3])
    return matchWithIntCode(MCCs, code)
    
    
def interpretMNC(value):
    global mncBase
    code = mncBase + interpretRevHexString(value)
    return matchWithIntCode(MNCs, code)


interpretingFunctions = {
    FinalType.RevHexString: interpretRevHexString,
    FinalType.HexString: interpretHexString,
    FinalType.Integer: interpretInteger,
    FinalType.IMSIMCC: interpretIMSIMCC,
    FinalType.PLMNMCC: interpretPLMNMCC,
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

