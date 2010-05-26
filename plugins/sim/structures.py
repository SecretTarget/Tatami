# -*- coding: utf-8 -*-

# -- structures.py
# Defines the different structures

from final_types import FinalType, FieldType


structICC = [
    ("ID number", FieldType.Final, 10, "Card identification number", FinalType.HexString)
]


structSIM = [
    ("ICC Identification", FieldType.TransparentEF, [0x2f, 0xe2], structICC),
#    ("DF Télécom", FieldType.DF, [0x7f, 0x10], structDFTel),
#   ("DF GSM", FieldType.DF, [0x7f, 0x20], structDFGSM)
]
