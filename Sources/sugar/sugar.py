#!/usr/bin/env python
# Encoding: ISO-8859-1
# vim: ts=4 textwidth=79
# -----------------------------------------------------------------------------
# Project           :   Sugar                         <http://www.ivy.fr/sugar>
# Author            :   Sebastien Pierre                     <sebastien@ivy.fr>
# License           :   Lesser GNU Public License
# -----------------------------------------------------------------------------
# Creation date     :   10-Aug-2005
# Last mod.         :   22-May-2007
# -----------------------------------------------------------------------------

import os, sys, shutil, traceback, StringIO
import grammar

from lambdafactory.reporter import DefaultReporter
from lambdafactory import javascript, c, modelwriter

__version__ = "0.7.4"

OPT_LANG       = "Specifies the target language (js, c, py)"
OPT_OUTPUT     = "Name of the output file containing the processed source files"
OPT_VERBOSE    = "Verbose parsing output (useful for debugging)"
OPT_API        = "Generates SDoc API documentation (give the apifilename)"
OPT_TEST       = "Tells wether the source code is valid or not"
OPT_VERSION    = "Ensures that Sugar is at least of the given version"
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

def apidoc( modules, output="api.html" ):
	import sdoc.main
	documenter = sdoc.main.LambdaFactoryDocumenter()
	# And now document the module
	target_html = None
	for module in modules:
		documenter.documentModule(module, module.getName())
	# We eventually return the HTML file
	title = "API documentation (SDoc)"
	html  = documenter.toHTML(title=title)
	if type(output) in (str, unicode):
		open(output, "w").write(html)
	else:
		output.write(html)
	return html

def parseVersion(text):
	val = 0
	res = text.split(".")
	if len(res) >= 1: val += int(res[0]) * 1000000
	if len(res) >= 2: val += int(res[1]) * 1000
	if len(res) >= 3: val += int(res[2])
	return val

def ensureVersion( require ):
	return parseVersion(__version__) >= parseVersion(require)

def runAsString( args ):
	"""Runs Sugar, but instead of printing the result to the given
	output, it returns a Python string with the result. It is very useful
	when embedding sugar."""
	output = StringIO.StringIO()
	run(args, output)
	return "" + output.getvalue()

def run( args, output=sys.stdout ):
	"""The run method can be used to execute a SweetC command from another
	Python script without having to spawn a shell."""
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
	oparser.add_option("-a", "--api", action="store", dest="api",
		help=OPT_API)
	oparser.add_option("-t", "--test", action="store_true", dest="test", 
		help=OPT_TEST)
	oparser.add_option("-V", None, action="store", dest="version", 
		help=OPT_VERSION)
	# We parse the options and arguments
	options, args = oparser.parse_args(args=args)
	# If no argument is given, we simply print the description
	if len(args) == 0:
		oparser.print_help()
		return
	if options.version and not ensureVersion(options.version):
		print "Current version is %s, but required version is %s" % (__version__, options.version)
		return -1
	# Otherwise, we are in interpreter mode
	parser           = grammar.Parser(verbose=options.verbose)
	writer, resolver = None, None
	reporter         = DefaultReporter
	if options.lang in ("js","javascript") or not options.lang:
		writer   = javascript.Writer(reporter=reporter)
		resolver = javascript.Resolver(reporter=reporter)
	elif options.lang == "c":
		writer   = c.Writer(reporter=reporter)
		resolver = c.Resolver(reporter=reporter)
	elif options.lang in ("s", "sg", "sugar"):
		writer   = modelwriter.Writer(reporter=reporter)
		resolver = c.Resolver(reporter=reporter)
	else:
		print "Please specify a valid language (js or c)"
		return -1
	# We process the source files
	# TODO: Refactor this
	# 1 -- Parse the modules, stop on syntax errors
	# 2 -- Flow the modules
	# 3 -- Program prcocessing passes (typing, resolution, etc)
	# 4 -- Generate the output files
	modules = []
	for source_path in args:
		try:
		#if True:
			source, module = parser.parse(source_path)
			modules.append(module)
			# FIXME: This should be split off
			resolver.flow(parser.program())
			if options.test:				
				writer.writeModule(module, options.module)
				print "%-40s [%s]" % (source_path,  'OK')
			elif module.isAbstract():
				writer.writeModule(module, options.module)
			else:
				output.write( writer.writeModule(module, options.module) + "\n")
		#if False:
		except Exception, e:
			if options.test:
				print "%-40s [%s]" % (source_path,  'FAILED')
			else:
				error_msg = StringIO.StringIO()
				traceback.print_exc(file=error_msg)
				error_msg = error_msg.getvalue()
				print error_msg
	if options.api:
		apidoc(modules, options.api)

# ------------------------------------------------------------------------------
#
# Main
#
# ------------------------------------------------------------------------------

if __name__ == "__main__":
	run(sys.argv[1:])

# EOF
