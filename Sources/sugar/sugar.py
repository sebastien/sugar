#!/usr/bin/env python
# Encoding: ISO-8859-1
# vim: ts=4 textwidth=79
# -----------------------------------------------------------------------------
# Project           :   Sugar                         <http://www.ivy.fr/sugar>
# Author            :   Sebastien Pierre                     <sebastien@ivy.fr>
# License           :   Lesser GNU Public License
# -----------------------------------------------------------------------------
# Creation date     :   10-Aug-2005
# Last mod.         :   16-Jan-2007
# -----------------------------------------------------------------------------

import os, sys, shutil
import grammar

from lambdafactory.reporter import DefaultReporter
from lambdafactory import javascript, c

__version__ = "0.6.4"

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

def sourceFileToJavaScript( path ):
	parser           = grammar.Parser()
	reporter         = DefaultReporter
	writer   = javascript.Writer(reporter=reporter)
	resolver = javascript.Resolver(reporter=reporter)
	source, module = parser.parse(source)
	resolver.flow(module)
	return writer.write(module), reporter

def sourceToJavaScript( name, text ):
	parser   = grammar.Parser()
	reporter = DefaultReporter
	writer   = javascript.Writer(reporter=reporter)
	resolver = javascript.Resolver(reporter=reporter)
	source, module = parser.parseModule(name, text)
	resolver.flow(module)
	return writer.write(module), reporter

def translate(moduleName, source, target="js"):
	"""Translates the given module source to the given target language."""
	# Otherwise, we are in interpreter mode
	parser           = grammar.Parser()
	writer, resolver = None, None
	reporter         = DefaultReporter
	if target == "js" :
		writer   = javascript.Writer(reporter=reporter)
		resolver = javascript.Resolver(reporter=reporter)
	else:
		print "Please specify a language."
		return -1
	source, module = parser.parseModule(moduleName, source)
	resolver.flow(module)
	return writer.write(module) + "\n"
	
def run( args, output=sys.stdout ):
	"""The run method can be used to execute a SweetC command from another
	Python script without having to spawn a shell."""
	"""Runs SDoc as a command line tool"""
	if type(args) not in (type([]), type(())): args = [args]
	from optparse import OptionParser
	# We create the parse and register the options
	oparser = OptionParser(prog="sugar", description=DESCRIPTION,
	usage=USAGE, version="Sugar " + __version__)
	oparser.add_option("-l", "--lang", action="store", dest="lang",
		help=OPT_LANG)
	oparser.add_option("-o", "--output", action="store", dest="output",
		help=OPT_OUTPUT)
	oparser.add_option("-v", "--verbose", action="store_true", dest="verbose",
		help=OPT_VERBOSE)
	oparser.add_option("-m", "--module", action="store_true", dest="module",
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
	reporter         = DefaultReporter
	if options.lang == "js" or not options.lang:
		writer   = javascript.Writer(reporter=reporter)
		resolver = javascript.Resolver(reporter=reporter)
	else:
		print "Please specify a language."
		return -1
	# We process the source files
	for source in args:
		source, module = parser.parse(source)
		resolver.flow(module)
		output.write( writer.writeModule(module, options.module) + "\n")

# ------------------------------------------------------------------------------
#
# Main
#
# ------------------------------------------------------------------------------

if __name__ == "__main__":
	run(sys.argv[1:])

# EOF
