# -*- coding: utf-8 -*-

# -- structures.py
# Defines the different structures

from final_types import FinalType, FieldType


structICC = [
    ("ID number", FieldType.Final, 10, "Card identification number", FinalType.RevHexString)
]


structLP = [
    ("Language code", FieldType.Repeated, 1, "", FinalType.Integer)
]


structIMSI = [
    ("IMSI length", FieldType.Final, 1, "", FinalType.Integer),
    ("MCC", FieldType.Final, 2, "Mobile Country Code", FinalType.MCC),
    ("MNC", FieldType.Final, 1, "Mobile Network Code", FinalType.MNC),
    ("HLR number", FieldType.Final, 1, "Home Location Register number", FinalType.RevHexString),
    ("MSIN", FieldType.Final, 4, "Mobile Subscriber Identification Number", FinalType.RevHexString),
]


structGSM = [
    ("Language preference", FieldType.TransparentEF, [0x6f, 0x05], structLP),
    ("IMSI", FieldType.TransparentEF, [0x6f, 0x07], structIMSI),
]


structSIM = [
    ("ICC identification", FieldType.TransparentEF, [0x2f, 0xe2], structICC),
#    ("DF Télécom", FieldType.DF, [0x7f, 0x10], structDFTel),
   ("DF GSM", FieldType.DF, [0x7f, 0x20], structGSM)
]
