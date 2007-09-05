#!/usr/bin/env python
# Encoding: ISO-8859-1
# vim: ts=4 textwidth=79
# ----------------------------------------------------------------------------
# Project           :   Sugar                        <http://www.ivy.fr/sugar>
# Author            :   Sebastien Pierre                    <sebastien@ivy.fr>
# License           :   Lesser GNU Public License
# ----------------------------------------------------------------------------
# Creation date     :   10-Aug-2005
# Last mod.         :   31-Aug-2007
# ----------------------------------------------------------------------------

import os, sys, shutil, traceback, tempfile, StringIO
import grammar

from lambdafactory.reporter import DefaultReporter
from lambdafactory import javascript, java, c, pnuts, actionscript, python, modelwriter, typer
from lambdafactory import passes, environment

__version__ = "0.8.2"

OPT_LANG       = "Specifies the target language (js, java, pnuts, actionscript)"
OPT_OUTPUT     = "Specifies the output where the files will be generated (stdout, file or folder)"
OPT_VERBOSE    = "Verbose parsing output (useful for debugging)"
OPT_API        = "Generates SDoc API documentation (give the apifilename)"
OPT_TEST       = "Tells wether the source code is valid or not"
OPT_DEFINE     = "Defines a specific target (for @specific)"
OPT_RUN        = "Directly runs the script (default)"
OPT_COMPILE    = "Compiles the given code to the output (current) directory"
OPT_RUNTIME    = "Outputs the runtime as well when compiled"
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
	if type(args) != list: args = list(args)
	from optparse import OptionParser
	# We create the parse and register the options
	oparser = OptionParser(prog="sugar", description=DESCRIPTION,
	usage=USAGE, version="Sugar " + __version__)
	oparser.add_option("-r", "--run",  action="store_true", dest="run",
		help=OPT_RUN)
	oparser.add_option("-c", "--compile", action="store_true", dest="compile",
		help=OPT_COMPILE)
	oparser.add_option("-R", "--runtime", action="store_true", dest="runtime",
		help=OPT_RUNTIME)
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
	oparser.add_option("-D", "--define", action="append", dest="targets", 
		help=OPT_DEFINE)
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
	parser           = grammar.Parser(verbose=False)
	if options.targets:
		for target in options.targets:
			parser.options.addTarget(target)
	writer, resolver = None, None
	reporter         = DefaultReporter
	if not options.lang and args:
		if args[0].endswith("js"): options.lang = "js"
		elif args[0].endswith("java"): options.lang = "java"
		elif args[0].endswith("pnuts"): options.lang = "pnuts"
		elif args[0].endswith("c"): options.lang = "c"
		elif args[0].endswith("as"): options.lang = "as"
		elif args[0].endswith("py"): options.lang = "python"
	if options.lang in ("js","javascript") or not options.lang:
		writer   = javascript.Writer(reporter=reporter)
		resolver = javascript.Resolver(reporter=reporter)
		parser.options.addTarget("JavaScript")
		options.lang = "javascript"
	elif options.lang == "c":
		writer   = c.Writer(reporter=reporter)
		resolver = c.Resolver(reporter=reporter)
		parser.options.addTarget("C")
		assert not options.run
		options.lang = "c"
	elif options.lang == "java":
		writer   = java.Writer(reporter=reporter)
		resolver = java.Resolver(reporter=reporter)
		parser.options.addTarget("Java")
		assert not options.run
		options.lang = "java"
	elif options.lang == "pnuts":
		writer   = pnuts.Writer(reporter=reporter)
		resolver = pnuts.Resolver(reporter=reporter)
		parser.options.addTarget("Pnuts")
		options.lang = "pnuts"
	elif options.lang in ("as", "actionscript"):
		writer   = actionscript.Writer(reporter=reporter)
		resolver = actionscript.Resolver(reporter=reporter)
		parser.options.addTarget("ActionScript")
		options.lang = "actionscript"
	elif options.lang in ("py", "python"):
		writer   = python.Writer(reporter=reporter)
		resolver = python.Resolver(reporter=reporter)
		parser.options.addTarget("Python")
		options.lang = "python"
	elif options.lang in ("s", "sg", "sugar"):
		writer   = modelwriter.Writer(reporter=reporter)
		resolver = c.Resolver(reporter=reporter)
		options.lang = "sugar"
		assert not options.run
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
	if options.test:
		options.run = options.compile = False
	if not options.run and not options.compile:
		options.run = True
	if options.run:
		output = StringIO.StringIO()
		output.write(writer.getRuntimeSource())
	# We parse the interfaces
	interfaces_dir = os.path.join(os.path.dirname(os.path.abspath(modelwriter.__file__)), "runtimes", "interfaces")
	for interface in os.listdir(interfaces_dir):
		interface_path = os.path.join(interfaces_dir, interface)
		if not interface_path.endswith(".sg") or not os.path.isfile(interface_path):
			continue
		if options.verbose:
			print "Loading interface", interface_path
		parser.parse(interface_path)
	# We parse the source files
	if options.run:
		sources_to_parse  = [args[0]]
		runtime_arguments = args[1:]
	else:
		sources_to_parse  = args
		runtime_arguments = []
	for source_path in sources_to_parse:
		if options.verbose:
			print "Parsing", source_path
		try:
		#if True:
			source, module = parser.parse(source_path)
			modules.append(module)
		#if False:
		except Exception, e:
			if options.test:
				print "%-40s [%s]" % (source_path,  'FAILED')
			#else:
			if not options.test or options.verbose :
				error_msg = StringIO.StringIO()
				traceback.print_exc(file=error_msg)
				error_msg = error_msg.getvalue()
				print error_msg.rstrip("\n")
				status = 255
	# WIP:IMPORT_START
	#import lambdafactory.languages.python.importer as pyimporter
	#env = environment.Environment(parser.program())
	#env.addImporter(pyimporter.Importer(env))
	#env.addParser(parser, "sg spy sjs sjava spnuts".split())
	#env.writer = writer ; env.resolver = resolver ; env.reporter = env.writer.report
	#env.addPass(passes.ImportationPass())
	#context = passes.PassContext(env)
	#context.run()
	# WIP:IMPORT_END
	#passes.ImportationPass().run(context)
	# We flow everything
	resolver.flow(parser.program())
	# We type everything
	typer.type(parser.program())
	# Then we execute the operations
	if options.api:
		apidoc(modules, options.api)
	if options.compile or options.run:
		# FIXME: Should ask the program for a proper module ordering so that
		# dependency conflicts are avoided
		mode = "w"
		splitter = None
		# We write the runtime if it is specified
		if options.runtime:
			source = writer.getRuntimeSource()
			if options.output is None:
				output.write( source )
			elif os.path.isdir(options.output):
				if splitter is None:
					splitter = modelwriter.FileSplitter(options.output)
				splitter.fromString(source)
			else:
				f = file(options.output, mode) ; mode = "a"
				f.write(source)
				f.close()
		# Then we write the modules
		for module in modules:
			if options.output is None:
				output.write( writer.write(module) + "\n")
			elif os.path.isdir(options.output):
				if splitter is None:
					splitter = modelwriter.FileSplitter(options.output)
				splitter.fromString(writer.write(module))
			else:
				f = file(options.output, mode) ; mode = "a"
				f.write(writer.write(module))
				f.close()
	status = 0
	if options.run:
		f, path = tempfile.mkstemp(prefix="Sugar")
		code = output.getvalue()
		os.write(f,code )
		# TODO: Run the program main
		os.close(f)
		args_str = " ".join(runtime_arguments)
		# FIXME: LambdaFactory should support compilers and runners
		if options.lang in ("js","javascript") or not options.lang:
			interpreter = os.getenv("SUGAR_JS") or "rhino"
			command = "%s '%s' %s" % (interpreter, path, args_str)
		elif options.lang == "pnuts":
			interpreter = os.getenv("SUGAR_PNUTS") or "pnuts"
			command = "%s '%s' %s" % (interpreter, path, args_str)
		elif options.lang == "python":
			interpreter = os.getenv("SUGAR_PYTHON") or "python"
			command = "%s '%s' %s" % (interpreter, path, args_str)
		else:
			print "No runtime available for language:", options.lang
		status = (os.system(command) / 256) or status
		os.unlink(path)
	return status

# ------------------------------------------------------------------------------
#
# Main
#
# ------------------------------------------------------------------------------

if __name__ == "__main__":
	sys.exit(run(sys.argv[1:]))

# EOF
