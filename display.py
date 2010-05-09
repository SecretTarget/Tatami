# -*- coding: utf-8 -*-

def toBinaryString(tab):
        """retourne la chaine de la representation binaire de tab"""
        s = ''
        blen = len(tab) * 8
        for b in range(0,blen):
                s = s + "%d" % (((tab[b/8] >> ((7-b)%8))) & 1)
        return s

# FIXME: nom pourri
def printExchange(query, response, sw1, sw2):
        """Affiche un échange query-response."""
        print ">> ", toHexString(query)
        print "<< ", toHexString(response), " / ", "%x %x" % (sw1, sw2)

def printExchangeWithBinary(query, response, sw1, sw2):
        """Affiche un échange query-response, avec en plus la reponse en binaire."""
        printExchange(query, response, sw1, sw2)
        print "\t ==  ", toBinaryString(response)

def prettyPrint(data, tabs=""):
        if type(data) == type(dict()):
                for key in data["Keys"]:
                        print
                        if (type(key) == type("")):
                                print tabs, ("%-27s" % key),
                                prettyPrint(data[key], tabs+"   ")
                        else:
                                print tabs, "====  ", key, "  ====",
                                prettyPrint(data[key], tabs)
        else:
                print ": "+data,
				