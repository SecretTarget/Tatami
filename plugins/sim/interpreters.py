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
        if c == 0xff:
            break
        txt += "%02x" % c
    if len(txt) == 0:
        return "No information"
    return txt
    
    
def interpretRevHexString(value):
    txt = ""
    for c in value:
        if c == 0xff:
                break
        txt += "%1x%1x" % (c%16, c>>4)
    if len(txt) == 0:
        return "No information"
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


def interpretDisplayCondition(value):
    bit = value[0] % 2
    base = "display of registered PLMN "
    if bit == 1:
        return base + "REQUIRED"
    return base + "NOT REQUIRED"
    
def interpretString(value):
    txt = ""
    for c in value:
        if c == 0xff:
            break
        txt += chr(c)
    return txt
    
    
def interpretBinaryString(value):
    txt = ''
    blen = len(value) * 8
    for b in range(0,blen):
        txt = txt + "%d" % (((value[b/8] >> ((7-b)%8))) & 1)
    return txt




locationUpdateStatuses = {
    0:  "updated",
    1:  "not updated",
    2:  "PLMN not allowed",
    3:  "Location Area not allowed",
    7:  "reserved"
}

def interpretLocationUpdateStatus(value):
    code = value[0]%8
    return matchWithIntCode(locationUpdateStatuses, code)
    
    
    
operationModes = {
    0x00:   "Normal operation",
    0x80:   "Type approval operations",
    0x01:   "Normal operation + specific facilities",
    0x81:   "Type approval operations + specific facilities",
    0x02:   "Maintenance (off line)",
    0x04:   "Cell test operation"
}    
    
def interpretOperationMode(value):
    return matchWithIntCode(operationModes, value[0])
 
    
    
phaseValues = {
    0x00:   "Phase 1",
    0x02:   "Phase 2",
}    
    
def interpretPhase(value):
    return matchWithIntCode(phaseValues, value[0])
        

def interpretNumRevHexString(value):
    txt = interpretRevHexString(value)
    number = ""
    for c in txt:
        if '0' <= c <= '9':
            number += c
        elif c == 'A':
            number += '*'
        elif c == 'B':
            number += '#'
        elif c == 'C':
            number += '-'
        elif c == 'D':
            number += '?'
        else:
            break
    return number
    

def interpretTonNpi(value):
    val = value[0]
    npi = val % 16
    ton = (val>>4) % 8
    return "Number Plan Identifier: %u, Type Of Number: %u" % (npi, ton)


SMSStatuses = {
    0: "Free space",
    1: "Message received and read",
    3: "MEssage received but not read yet",
    5: "Message sent",
    7: "Message to be sent"    
}

def interpretSMSStatus(value):
    code = value[0] % 8
    return matchWithIntCode(SMSStatuses, code)


interpretingFunctions = {
    FinalType.RevHexString: interpretRevHexString,
    FinalType.HexString: interpretHexString,
    FinalType.Integer: interpretInteger,
    FinalType.IMSIMCC: interpretIMSIMCC,
    FinalType.PLMNMCC: interpretPLMNMCC,
    FinalType.MNC: interpretMNC,
    FinalType.DisplayCondition: interpretDisplayCondition,
    FinalType.String: interpretString,
    FinalType.BinaryString: interpretBinaryString,
    FinalType.LocationUpdateStatus: interpretLocationUpdateStatus,
    FinalType.OperationMode: interpretOperationMode,
    FinalType.Phase: interpretPhase,
    FinalType.NumRevHexString: interpretNumRevHexString,
    FinalType.TonNpi: interpretTonNpi,
    FinalType.SMSStatus: interpretSMSStatus,
    
    FinalType.Unknown: interpretUnknown,
}


def matchWithIntCode(codes, code):
    """Renvoie la valeur associée à un code.
    `codes' est un dictionnaire, les clés sont les codes entiers,
    `value' est une clé potentielle en binaire."""
    if code in codes:
        res = codes[code]
    else:
        res = "Inconnu --> %s" % (code)
    return res

