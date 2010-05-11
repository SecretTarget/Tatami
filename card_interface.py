# -*- coding: utf-8 -*-

# card.py: interactions avec la carte

from smartcard.util import toHexString
from smartcard.ATR import ATR
from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.pcsc.PCSCExceptions import EstablishContextException

import display

# FIXME, ca devrait etre une var globale pour tous les py
verboseMode = False


def getReadersList():
	try:
		return readers()
	except (EstablishContextException):
		return []
		
		
def connectToCard(card):
	try:
		card.connection = card.createConnection()
		card.connection.connect()
		return True
	except  (NoCardException, CardConnectionException):
		return False
		
		
def connectCard(reader):
	try:
		connection = reader.createConnection()
		connection.connect()
		return connection
	except  (NoCardException, CardConnectionException):
		return False
		
def getCard():
	reader = selectReader()
	if not reader:
		return False
	card = connectCard(reader)
	if card == False:
		print reader, "--> no card inserted"
		return False
	return card
		
def selectReader():
	reader = False
	list = getReadersList()
	if len(list) == 0:
		print "No reader has been found."
	elif len(list) == 1:
		reader = list[0]
	else:
		i = 1
		for reader in list:
			print "%u: %s" % (i, reader)
			i+=1
		choice = raw_input("\nWhich reader do you want to use ? ")
		try:
			reader = list[int(choice)-1]
		except:
			print "Please type a correct number"
	return reader


def selectFile(connection, address):
        """selectionne un fichier"""
        cla = 0x94
        ins = 0xa4
        param1, param2 = 0x08, 0x00
        addressLen = len(address)
        apdu = [cla, ins, param1, param2, addressLen] + address
        response, sw1, sw2 = connection.transmit(apdu)
        if verboseMode: display.printExchange(apdu, response, sw1, sw2)
        return response, sw1, sw2

def readRecord(connection, number, length=29):
        """Lit un enregistrement dans un fichier selectionné."""
        cla = 0x94
        ins = 0xb2
        mode = 0x04
        apdu = [cla, ins, number, mode, length]
        response, sw1, sw2 = connection.transmit(apdu)
        if verboseMode: display.printExchangeWithBinary(apdu, response, sw1, sw2)
        return response, sw1, sw2

def readRecordBinaryResponse(connection, number):
        response, sw1, sw2 = readRecord(connection, number)
        return display.toBinaryString(response)

def getATR(connection):
        return connection.getATR()


def statusIsOK(sw1, sw2):
        """retourne True ssi le statut est OK."""
        return (sw1 == 0x90 and sw2 == 0)

def statusSecurityNotOK(sw1, sw2):
        """retourne True ssi le 'security status' est pas satifsait."""
        return (sw1 == 0x69 and sw2 == 0x82)

def statusRecordNotFound(sw1, sw2):
        """retourne True ssi l'enregistrement n'existe pas."""
        return (sw1==0x6a and sw2==0x83)

def statusCommandNotAllowed(sw1, sw2):
        """retourne True ssi la commande est interdite."""
        return (sw1==0x69 and sw2==0x86)

def statusBadLength(sw1, sw2):
        """retourne True ssi on a demandé une mauvaise longueur."""
        return sw1 == 0x6c
