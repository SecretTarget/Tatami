# -*- coding: utf-8 -*-

import interpreters
import structures

currentStructure = ()

def parseATR(atrStruct):
	"""Parse une partie de l'ATR et affiche quelques paramètres intéressants."""
	global currentStructure
	atr = {}
	keys = []
	historicalBytes = atrStruct.getHistoricalBytes()
	card_number = historicalBytes[11] + (historicalBytes[10] << 8) \
		+ (historicalBytes[9] << 16) + (historicalBytes[8] << 24)
	atr["Card number"] = str(card_number)
	chipType = historicalBytes[2]
	atr["Chip type"] = "%02x" % chipType
	applicationType = historicalBytes[3]
	atr["Application type"] =  "%02x" % (applicationType)
	applicationSubtype = historicalBytes[4]
	atr["Application subtype"] =  "%02x" % (applicationSubtype)
	issuer = historicalBytes[5]
	atr["Issuer"] =  "%02x" % (issuer)
	rom = historicalBytes[6]
	atr["ROM"] =  "%02x" % (rom)
	eeprom = historicalBytes[7]
	atr["EEPROM"] =  "%02x" % (eeprom)
	
	currentStructure = structures.cardTypes[atr["Chip type"] + atr["Application type"] + atr["Application subtype"]]
	atr["Card type"] = currentStructure[0]
	
	atr["Keys"] = ["Card number", "Chip type", "Application type", "Application subtype", "Issuer", "ROM", "EEPROM", "Card type"]
	return atr
	#print "Chip: 0x%02x," % chipType,
	#print "Application Type: 0x%02x," % applicationType,
	#print "Application Subtype: 0x%02x" % applicationSubtype
	#print "Card number:", card_number
	#         print "issuer 0x%02x" % issuer,
	#         print "rom 0x%02x" % rom,
	#         print "eeprom 0x%02x" % eeprom

	
def getRootStructure():
	return currentStructure[1]

def getGlobalFields():
	return interpreters.globalFields
	
def getInterpretersTable():
	return interpreters.interpretingFunctions