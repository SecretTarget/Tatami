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
cla = 0


def getReadersList():
    try:
        return readers()
    except (EstablishContextException):
        return []
        
        
def sendAPDU(connection, apdu):
    response, sw1, sw2 = connection.transmit(apdu)
    if verboseMode: display.printExchange(apdu, response, sw1, sw2)
    return response, sw1, sw2
        
        
def warmResetNeeded(connection):
    global cla
    testAPDU = [cla,0,0,0]
    response, sw1, sw2 = sendAPDU(connection, testAPDU)
    if sw1 == 0x6e:
        return True
    return False    
        
        
def establishConnection(connection):
    # disposition = 1 = SCARD_RESET_CARD (warm reset)
    connection.connect(disposition=1)
    if warmResetNeeded(connection):
        connection.disconnect()
        connection.connect()
        if verboseMode: display.printExchange("reset", getATR(connection), 0x90, 0)
        
        
def connectToCard(card):
    try:
        card.connection = card.createConnection()
        #card.connection.connect()
        establishConnection(connection)
        return True
    except  (NoCardException, CardConnectionException):
        return False
        
        
def connectCard(reader):
    try:
        connection = reader.createConnection()
        #connection.connect()
        establishConnection(connection)
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


def findTransparentEFSize(connection, infoSize):
    global cla
    apdu = [cla, 0xc0, 0, 0, infoSize]
    response, sw1, sw2 = sendAPDU(connection, apdu)
    return response[3]


def selectFileByName(connection, name):
    hexName = []
    for c in name:
        hexName.append(ord(c))
    return selectFile(connection, hexName, 0x04)


def selectFile(connection, address, param1 = 0x08, param2 = 0x00):
    """selectionne un fichier"""
    global cla
    ins = 0xa4
   # param1, param2 = 0x08, 0x00
    addressLen = len(address)
    apdu = [cla, ins, param1, param2, addressLen] + address
    response, sw1, sw2 = sendAPDU(connection, apdu)
    return response, sw1, sw2
    
    
def readBinaryData(connection, size):
    global cla
    apdu = [cla, 0xb0, 0, 0, size]
    return sendAPDU(connection, apdu)
    

def readRecord(connection, number, length=29, mode = 0x04):
    """Lit un enregistrement dans un fichier selectionné."""
    global cla
    ins = 0xb2
    #mode = 0x04
    #mode = 0x3c
    apdu = [cla, ins, number, mode, length]
    response, sw1, sw2 = sendAPDU(connection, apdu)
    if statusBadLength(sw1, sw2):
        apdu[4] = sw2
        response, sw1, sw2 = sendAPDU(connection, apdu)
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
    
def statusFileNotFound(sw1, sw2):
    """retourne True ssi les un fichier n'a pas été trouvé."""
    return (sw1==0x6a and sw2==0x82)
    
def statusWrongParameters(sw1, sw2):
    """retourne True ssi les paramètres ne sont pas corrects."""
    return (sw1==0x6a and sw2==0x86)

def statusBadLength(sw1, sw2):
    """retourne True ssi on a demandé une mauvaise longueur de record."""
    return sw1 == 0x6c
