#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -- dump.py
# Main file, the dumper

from structure_parser import parseNavigo
#from parser import *

from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.pcsc.PCSCExceptions import EstablishContextException

import sys
import card_interface





def getReadersList():
	try:
		return readers()
	except (EstablishContextException):
		return []
		
		
def dumpNavigo(reader):
	try:
		connection = reader.createConnection()
		connection.connect()
	except  (NoCardException, CardConnectionException):
		return {}
		
	return parseNavigo(connection)


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
			
	navigo = dumpNavigo(reader)
	if navigo == {}:
		print reader, "--> no card inserted"
		return
	prettyPrint(navigo)
	

if __name__ == '__main__':
	if len(sys.argv) > 1:
		card.debugMode = True
		
	dump()
