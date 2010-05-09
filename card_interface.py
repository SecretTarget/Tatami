# -*- coding: utf-8 -*-

# card.py: interactions avec la carte

from smartcard.util import toHexString
from smartcard.ATR import ATR

# FIXME, ca devrait etre une var globale pour tous les py
debugMode = False

def selectFile(connection, address):
        """selectionne un fichier"""
        cla = 0x94
        ins = 0xa4
        param1, param2 = 0x08, 0x00
        addressLen = len(address)
        apdu = [cla, ins, param1, param2, addressLen] + address
        response, sw1, sw2 = connection.transmit(apdu)
        if debugMode: printExchange(apdu, response, sw1, sw2)
        return response, sw1, sw2

def readRecord(connection, number, length=29):
        """Lit un enregistrement dans un fichier selectionné."""
        cla = 0x94
        ins = 0xb2
        mode = 0x04
#        length = 29
        apdu = [cla, ins, number, mode, length]
        response, sw1, sw2 = connection.transmit(apdu)
        if debugMode: printExchangeWithBinary(apdu, response, sw1, sw2)
        return response, sw1, sw2

def readRecordBinaryResponse(connection, number):
        response, sw1, sw2 = readRecord(connection, number)
        return toBinaryString(response)

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
