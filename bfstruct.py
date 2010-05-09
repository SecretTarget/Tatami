#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -- bfstruct.py
# Bruteforces through the file structure

from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.util import toHexString

from card_parser import *
from card import *
from dump import prettyPrint

import sys
import card

#debugMode = False
recursiveMode = False


def printAddress(address, space):
    length = len(address)
    print space, "[0x%02x%02x]" % (address[length-2], address[length-1])

def printRecord(response, nb):
    print "====  ", nb, "  ===="
    print "\t", toBinaryString(response), "\n"


def dumpStruct(connection, startAddress = [], space = "", firstByteMin = 0,
               firstByteMax = 0xff, secondByteMin = 0, secondByteMax = 0xff):

	for firstByte in range(firstByteMin, firstByteMax+1):
	#        print space + ("0x%02x" % firstByte) + " 0xxx"
		for secondByte in range(secondByteMin, secondByteMax+1):
			address = startAddress + [firstByte, secondByte]
			response, sw1, sw2 = selectFile(connection, address)

			if not statusIsOK(sw1, sw2):
				continue
			# Le select est bon, on regarde les enregistrements.
			printAddress(address, space)

			for recordNumber in range(255):
				response, sw1, sw2 = readRecord(connection, recordNumber+1)
				print "\t",
				if statusIsOK(sw1, sw2):
					printRecord(response, recordNumber+1)
				else:
					if statusSecurityNotOK(sw1, sw2):
						print "Security status not satisfied\n"
					elif statusCommandNotAllowed(sw1, sw2): # ie. c'est un DF
						print "This is a DF\n"
						if recursiveMode:
							dumpStruct(connection, startAddress+address, space+"   ")
					elif statusRecordNotFound(sw1, sw2):
						# Record not found, it was the last one
						print "Total: %u record(s)\n" % (recordNumber)
					elif statusBadLength(sw1, sw2):
						# mauvaise longueur, on peut recuperer le coup.
						len = sw2
						response, sw1, sw2 = readRecord(connection, recordNumber+1, sw2)
						if statusIsOK(sw1, sw2):
							printRecord(response, recordNumber+1)
							print "\t(longueur %d)\n" % len
					else:
						print "Unknown error: %02x %02x\n" % (sw1, sw2)
					break

            # FIXME: il vient d'ou ce sw ?
            # if sw1 == 0x67: #We are not in a DF
            #    print "boum"
            #    return


def launchBF():
    for reader in readers():
        try:
            connection = reader.createConnection()
            connection.connect()
        except  (NoCardException, CardConnectionException):
            print reader, '--> no card inserted'
            break

	atr = parseATR(connection)
	prettyPrint(atr)
        print "\n"
#        dumpStruct(connection)

	dumpStruct(connection, [], "", 0x00, 0x3f, 0x00, 0x80)
#        dumpStruct(connection, [0x00, 0x00], "", 0x00, 0x00, 0x00, 0x70)
#        dumpStruct(connection, [0x10, 0x00], "", 0x10, 0x11, 0x00, 0x70)
#        dumpStruct(connection, [0x20, 0x00], "", 0x20, 0x21, 0x00, 0x70)
#        dumpStruct(connection, [0x30, 0x00], "", 0x30, 0x31, 0x00, 0x70)


if __name__ == '__main__':
    for param in sys.argv:
        if param == "-d":
            card.debugMode = True
        elif param == "-r":
            recursiveMode = True
    launchBF()
