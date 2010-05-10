# -*- coding: utf-8 -*-

# -- dump.py
# The dumper

from structure_parser import parseCard


from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.pcsc.PCSCExceptions import EstablishContextException

import sys
import card_interface
import display



def getReadersList():
	try:
		return readers()
	except (EstablishContextException):
		return []
		
		
def dumpCard(reader):
	try:
		connection = reader.createConnection()
		connection.connect()
	except  (NoCardException, CardConnectionException):
		return {}
		
	return parseCard(connection)


def dump():
	list = getReadersList()
	if len(list) == 0:
		print "No reader has been found."
		return
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
			return
			
	card = dumpCard(reader)
	if card == {}:
		print reader, "--> no card inserted"
		return
	display.prettyPrint(card)
