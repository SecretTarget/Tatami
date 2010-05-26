# -*- coding: utf-8 -*-

import structures

from final_types import FinalType

    
   
def interpretUnknown(value):
    return interpretHexString(value)
    
    
def interpretHexString(value):
    txt = ""
    for c in value:
        txt += "%02x " % c
    return txt


interpretingFunctions = {
    FinalType.HexString: interpretHexString,

    FinalType.Unknown: interpretUnknown,
}
