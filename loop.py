#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -- dump.py
# Main file, the dumper

from card_parser import parseNavigo
#from parser import *

from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.pcsc.PCSCExceptions import EstablishContextException
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

from time import sleep
from os import sep

import sys
import card
import Tkinter
import os
import datetime
import exceptions

class ReloadDump(exceptions.Exception):
	def __init__(self):
		return
		
	def __str__(self):
		print ": ","There was an error during the dumping process"


dumped = [] # les cartes deja vues

def prettyPrint(data, file, tabs=""):
        """Ecriture d'un dump sous forme lisible dans le fichier `file' (handle)."""
	if type(data) == type(dict()):
		for key in data["Keys"]:
			file.write("\n")
			if (type(key) == type("")):
				file.write(tabs)
				file.write(("%-27s" % key))
				prettyPrint(data[key], file, tabs+"   ")
			else:
				file.write(tabs)
				file.write("====  ")
				file.write(str(key))
				file.write("  ====")
				prettyPrint(data[key], file, tabs)
	else:
		file.write(": "+str(data))


def getReadersList():
	try:
		return readers()
	except (EstablishContextException):
		return []


def dumpNavigo(card):
        """Initie une connection à la carte, dumpe, se déconnecte
        et fait un beep."""
	try:
		card.connection = card.createConnection()
		card.connection.connect()
	except  (NoCardException, CardConnectionException):
		return {}

	Tkinter.Tk().bell()
	try:
		navigo = parseNavigo(card.connection)
	except CardConnectionException:
		return {}

	card.connection.disconnect()
	Tkinter.Tk().bell()
	return navigo


class observer(CardObserver):
        """`directory' est le repertoire où on stocke les dumps."""
	def __init__(self, directory):
		self.directory = directory

	def update(self, observable, (addedcards, removedcards)):
                """Quand on detecte un carte, on dumpe puis on l'ecrit dans
                le fichier `directory'/xx - ATR.txt"""
		try:
			for card in addedcards:
				Tkinter.Tk().bell()
				if not card.atr in dumped:
					navigo = dumpNavigo(card)
					if navigo != {}:
						dumped.append(card.atr)
						filename = "%s%s%02u - %s.txt" % \
												(self.directory, os.sep, len(dumped),
												 toHexString(card.atr))
						print filename,
						file = open(filename, 'w')
						prettyPrint(navigo, file)
						file.close()
						print ": OK."
					else:
						raise ReloadDump
		except ReloadDump:
			dump()
		except:
			return
						

def dump():
        """Choisit un lecteur, accroche l'observeur. On rentre dans un boucle infinie
        qui réagit aux ajouts de cartes."""
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

	now = datetime.datetime.today()
	directory = "%04u-%02u-%02u_%02uh%02um%02us" % \
            (now.year, now.month, now.day, now.hour, now.minute, now.second)
	os.makedirs(directory)
	cardmonitor = CardMonitor()
	cardobserver = observer(directory)
	cardmonitor.addObserver(cardobserver)

	while True:
		try:
			sleep(60)
		except:
			break

	cardmonitor.deleteObserver(cardobserver)


if __name__ == '__main__':
	if len(sys.argv) > 1:
		card.debugMode = True

	dump()
