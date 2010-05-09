#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -- pssi.py
# Main file

#from dumper import dump
import sys

def usage():
	print "usage"
	sys.exit(2)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		usage()
	
	sys.path.append(sys.argv[1])
	import dumper
	dumper.dump()
