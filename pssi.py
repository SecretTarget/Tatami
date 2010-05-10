#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -- pssi.py
# Main file

import sys
import getopt
import card_interface


def usage():
	print "usage"
	sys.exit(2)


def main():
	options = "hv"
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], options)
	except getopt.GetoptError, err:
		print str(err)
		usage()

	for o, a in opts:
		if o == "-v":
			card_interface.verboseMode = True
		elif o == "-h":
			usage()
		else:
			assert False, "unhandled option"
	
	if len(args) < 1:
		usage()
		
	sys.path.append(args[0])
	import dumper
	dumper.dump()


if __name__ == '__main__':
	main()	
