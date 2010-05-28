# -*- coding: utf-8 -*-

# -- structures.py
# Defines the different structures

from final_types import FinalType, FieldType


structICC = [
    ("ID number", FieldType.Final, 10, "Card identification number", FinalType.RevHexString)
]


structLP = [
    ("Language code", FieldType.FinalRepeated, 1, "", FinalType.Integer)
]


structIMSI = [
    ("IMSI length", FieldType.Final, 1, "", FinalType.Integer),
    ("MCC", FieldType.Final, 2, "Mobile Country Code", FinalType.IMSIMCC),
    ("MNC", FieldType.Final, 1, "Mobile Network Code", FinalType.MNC),
    ("HLR number", FieldType.Final, 1, "Home Location Register number", FinalType.RevHexString),
    ("MSIN", FieldType.Final, 4, "Mobile Subscriber Identification Number", FinalType.RevHexString),
]


structKc = [
    ("Key", FieldType.Final, 8, "Ciphering key Kc", FinalType.HexString),
    ("Sequence number", FieldType.Final, 1, "Ciphering key sequence number", FinalType.Integer)
]


structPLMN = [
    ("MCC", FieldType.Final, 2, "Mobile Country Code", FinalType.PLMNMCC),
    ("MNC", FieldType.Final, 1, "Mobile Network Code", FinalType.MNC),
]

# Public Land Mobile Network
structPLMNsel = [
    ("Prefered PLMN (Public Land Mobile Network) list", FieldType.StructRepeated, 3, structPLMN)
]


structGSM = [
    ("Language preference", FieldType.TransparentEF, [0x6f, 0x05], structLP),
    ("IMSI", FieldType.TransparentEF, [0x6f, 0x07], structIMSI),
    ("Kc", FieldType.TransparentEF, [0x6f, 0x20], structKc),
    ("PLMN selector", FieldType.TransparentEF, [0x6f, 0x30], structPLMNsel),
]


structSIM = [
    ("ICC identification", FieldType.TransparentEF, [0x2f, 0xe2], structICC),
#    ("DF Télécom", FieldType.DF, [0x7f, 0x10], structDFTel),
   ("DF GSM", FieldType.DF, [0x7f, 0x20], structGSM)
]
