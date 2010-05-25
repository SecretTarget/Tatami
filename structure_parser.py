# -*- coding: utf-8 -*-

# -- card_parser.py
# Defines the parsing functions


import plugin
from card_interface import *

from smartcard.util import toHexString
from smartcard.ATR import ATR

import exceptions


MAX_RECORDS = 10


class FieldType:
    DF = 0
    EF = 1
    Bitmap = 2
    Final = 3
    Counter = 4
    DFName = 5


def interpretFinalField(value, type, name):
    interpretation = plugin.getInterpretersTable()[type](value)
    if "ANY" in plugin.getInterpretersTable():
        plugin.getInterpretersTable()["ANY"](name, interpretation, type, value)
    return interpretation


class IncorrectStructure(exceptions.Exception):
    def __init__(self):
        return

    def __str__(self):
        print ": ","Tried to parse a binary string with an incorrect structure"



def parseTLV(data):
    typeTable = plugin.getInterpretersTable()
    table = {}
    keys = []
    while len(data) > 0:
        type = data[0]
        if not type in typeTable:
            break
        length = data[1]
        value = data[2:2+length]
        data = data[2+length:]
        info = typeTable[type]
        name = info[0]
        interpreter = info[1]
        keys.append(name)
        if interpreter == -1:
            table[name] = parseTLV(value)
        else:
            table[name] = interpreter(value)
    table["Keys"] = keys
    return table



def parseCardStruct(connection, structure, data=[], sizeParsed=[]):
    table = {}
    keys = []
    total = 0
    while (structure != []):
    
    
        # TODO : maj total
        if structure == -1: #TLV !
            for number in range(1, MAX_RECORDS):
                data, sw1, sw2 = readRecord(connection, number)
                if len(data)>0:
                    table[number] = parseTLV(data)
                    keys.append(number)
            table["Keys"] = keys
            return table                



        else:
            field = structure[0]
            name = field[0]
            if type(name) == type([]):
                hiddenFields = True
            else:
                hiddenFields = False
            structure = structure[1:]
            if field[1] == FieldType.Bitmap:
                length = field[2]
                bitmap = data[0:length]
                #print bitmap
                data = data[length:]
                total += length
                counter = 0
                subfields = []
                for subfield in field[3]:
                    try:
                        if bitmap[len(bitmap)-counter-1] == '1':
                            subfields.append(subfield)
                    except IndexError:
                        raise IncorrectStructure
                    counter += 1
                structure = subfields + structure
            else:
                if field[1] == FieldType.DF:
                    entry = parseCardStruct(connection, field[3], data+field[2])
                elif field[1] == FieldType.DFName:
                    # TODO : Check error
                    selectFileByName(connection, field[2])
                    entry = parseCardStruct(connection, field[3],[])
                elif field[1] == FieldType.EF:
                    (response, sw1, sw2) = selectFile(connection, data+field[2])
                    if not statusIsOK(sw1, sw2):
                        entry = "Could not select the file in order to fetch the data"
                    else:
                        if hiddenFields:
                            size = []
                            entry = []
                            for i in range(len(name)):
                                entry.append({})
                        else:
                            entry = {}
                        subkeys = []
                        for number in range(1, MAX_RECORDS):
                            bindata = readRecordBinaryResponse(connection, number)
                            if bindata != "":
                                if hiddenFields:
                                    counter = 0
                                    for struct in field[3]:
                                        entry[counter][number] = parseCardStruct(connection, struct, bindata, size)
                                        bindata = bindata[size[0]:]
                                        counter += 1
                                else:
                                    entry[number] = parseCardStruct(connection, field[3], bindata)
                                subkeys.append(number)

                        if hiddenFields:
                            for i in range(len(name)):
                                entry[i]["Keys"] = subkeys
                        else:
                            entry["Keys"] = subkeys
                elif field[1] == FieldType.Counter:
                    length = field[2]
                    counter = int(data[0:length], 2)
                    data = data[length:]
                    total += length
                    entry = {}
                    subkeys = []
                    for number in range(counter):
                        size = []
                        entry[number] = parseCardStruct(connection, field[3], data, size)
                        subkeys.append(number)
                        data = data[size[0]:]
                    entry["Keys"] = subkeys
                elif field[1] == FieldType.Final:
                    length = field[2]
                    if length != 0:
                        value = data[0:length]
                        data = data[length:]
                        total += length
                    else:
                        value = data
                        data = []
                        total += len(value)
                    interpretation = interpretFinalField(value, field[4], name)
                    entry = ("%-35s" % interpretation)+" ---   "+value+" ("+field[3]+")"

                if hiddenFields:
                    counter = 0
                    for subname in name:
                        table[subname] = entry[counter]
                        keys.append(subname)
                        counter += 1
                else:
                    table[name] = entry
                    keys.append(name)

    sizeParsed.append(total)
    table["Keys"] = keys
    return table



def parseCard(connection):
    card = {}
    if "ATR" in plugin.getInterpretersTable():
        card["ATR"] = plugin.getInterpretersTable()["ATR"](ATR(getATR(connection)))
    else:
        card["ATR"] = toHexString(getATR(connection))
    card["Content"] = parseCardStruct(connection, plugin.getRootStructure())
    card["Keys"] = ["ATR", "Content"]
    return card
