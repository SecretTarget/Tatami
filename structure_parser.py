# -*- coding: utf-8 -*-

# -- card_parser.py
# Defines the parsing functions

#from symbols import *
#from structures import *
#from interpreters import *
import plugin
from card_interface import *

from smartcard.util import toHexString
from smartcard.ATR import ATR

import exceptions


MAX_RECORDS = 10
debugMode = False


class FieldType:
	DF = 0
	EF = 1
	Bitmap = 2
	Final = 3
	Counter = 4
	

def interpretFinalField(value, type, name):
        interpretation = plugin.getInterpretersTable()[type](value)
	plugin.getInterpretersTable()["any"](name, interpretation, type, value)
	return interpretation


class IncorrectStructure(exceptions.Exception):
	def __init__(self):
		return
		
	def __str__(self):
		print ": ","Tried to parse a binary string with an incorrect structure"


def parseCardStruct(connection, structure, data=[], sizeParsed=[]):
	table = {}
	keys = []
	total = 0
	while (structure != []):
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
					for number in range(MAX_RECORDS):
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
	card["ATR"] = plugin.parseATR(ATR(getATR(connection)))
	card["Content"] = parseCardStruct(connection, plugin.getRootStructure())
	card["Keys"] = ["ATR", "Content"]
	return card