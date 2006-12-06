#!/usr/bin/env python
# Encoding: ISO-8859-1
# vim: ts=4 textwidth=79
# -----------------------------------------------------------------------------
# Project           :   Sugar                         <http://www.ivy.fr/sugar>
# Author            :   Sebastien Pierre                     <sebastien@ivy.fr>
# License           :   Lesser GNU Public License
# -----------------------------------------------------------------------------
# Creation date     :   10-Aug-2005
# Last mod.         :   01-Dec-2006
# -----------------------------------------------------------------------------


import os, sys, shutil
import grammar

__version__ = "0.5.0"

OPT_LANG       = "Specifies the target language (js, c, py)"
OPT_OUTPUT     = "Name of the output file containing the processed source files"
OPT_VERBOSE    = "Verbose parsing output (useful for debugging)"
DESCRIPTION    = """\
Sugar is a meta-language that can be easily converted to other languages such
as C, JavaScript or Python. Programs written in sugar are entirely accessible
as an OO model, which can be manipulated and modified programmatically.

Sugar syntax was designed to be easy to read, expressive, and encourages best
practives. It is very much inspired from Python and Eiffel.

See <http://www.ivy.fr/sugar> for more information."""
USAGE          = "%prog [options] SOURCE..."

# ------------------------------------------------------------------------------
#
# Run method
#
# ------------------------------------------------------------------------------

def run( args ):
	"""The run method can be used to execute a SweetC command from another
	Python script without having to spawn a shell."""
	"""Runs SDoc as a command line tool"""
	if type(args) not in (type([]), type(())): args = [args]
	from optparse import OptionParser
	# We create the parse and register the options
	oparser = OptionParser(prog="sdoc", description=DESCRIPTION,
	usage=USAGE, version="SDoc " + __version__)
	oparser.add_option("-l", "--lang", action="store", dest="lang",
		help=OPT_LANG)
	oparser.add_option("-o", "--output", action="store", dest="output",
		help=OPT_OUTPUT)
	oparser.add_option("-v", "--verbose", action="store_true", dest="verbose",
		help=OPT_VERBOSE)
	# We parse the options and arguments
	options, args = oparser.parse_args(args=args)
	# If no argument is given, we simply print the description
	if len(args) == 0:
		oparser.print_help()
		return
	# Otherwise, we are in interpreter mode
	parser           = grammar.Parser(verbose=options.verbose)
	writer, resolver = None, None
	if options.lang == "js" or not options.lang:
		from lambdafactory.javascript import Writer, Resolver
		writer   = Writer()
		resolver = Resolver()
	else:
		print "Please specify a language."
		return -1
	# We process the source files
	for source in args:
		source, module = parser.parse(source)
		resolver.flow(module)
		print writer.write(module)

# ------------------------------------------------------------------------------
#
# Main
#
# ------------------------------------------------------------------------------

if __name__ == "__main__":
	run(sys.argv[1:])

# EOF
