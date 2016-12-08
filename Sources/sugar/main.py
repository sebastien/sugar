#!/usr/bin/env python
# # New implementation for the Sugar Command line
#
from lambdafactory.main import Command as BaseCommand
import sugar.grammar as grammar
import os, sys, tempfile

class Command(BaseCommand):

	def setupEnvironment( self ):
		python_plugin       = self.environment.loadLanguage("python")
		javascript_plugin   = self.environment.loadLanguage("javascript")
		actionscript_plugin = self.environment.loadLanguage("actionscript")
		pnuts_plugin        = self.environment.loadLanguage("pnuts")
		python_plugin.addRecognizedExtension("spy")
		javascript_plugin.addRecognizedExtension("sjs")
		actionscript_plugin.addRecognizedExtension("sas")
		pnuts_plugin.addRecognizedExtension("spnuts")
		pnuts_plugin.addRecognizedExtension("spnut")
		# WTF ?? I don't get this code
		python_plugin.reader = grammar.Parser
		python_reader = python_plugin.reader()
		python_reader.environment = self.environment
		# FIXME: This is temporary, until we use the proper reader interface
		if hasattr(self.environment, "getProgram"):
			python_reader._program = self.environment.getProgram()
		# FIXME: This should be done by the Parser itself
		self.environment.addParser(python_reader, "sg spy sjs sjava spnuts sas".split())

	def run( self, *args ):
		self.cleanup()
		BaseCommand.run(self, *args)
		self.cleanup()
		# We need to cleanup the cache left by dparser, which creates a core dump on
		# 64bit architectures

	def cleanup( self ):
		base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
		for name in ["_parser_mach_gen.g.d_parser.dat", "d_parser_mach_gen.g.md5"]:
			p = os.path.join(base_dir, name)
			if os.path.exists(p):
				os.unlink(p)

def sourceFileToJavaScript( path, moduleName=None, options="" ):
	command = Command()
	opts = ["-cljavascript"]
	opts.extend(options.split())
	if moduleName:
		opts.append("-m" + moduleName)
	if type(path) in (list,tuple):
		for p in path:
			opts.append(p)
	else:
		opts.append(path)
	return command.runAsString(opts)

def sourceToJavaScript( text, moduleName=None, options="" ):
	command = Command()
	opts = ["-cljavascript"]
	opts.extend(options.split())
	if moduleName:
		opts.append("-m" + moduleName)
	opts.append("-ssg")
	opts.append(text)
	return command.runAsString(opts)

def run(arguments):
	command = Command("sugar")
	if not arguments: arguments = ["--help"]
	command.run(arguments)
	return command.environment.program


def parseFile( path, moduleName=None, options="" ):
	command = Command()
	opts = ["-cljavascript"]
	opts.extend(options.split())
	if moduleName:
		opts.append("-m" + moduleName)
	if type(path) in (list,tuple):
		for p in path:
			opts.append(p)
	else:
		opts.append(path)
	command.runAsString(opts)
	return command.environment.program

if __name__ == "__main__":
	if False:
		# This is the main function for profiling
		# We've renamed our original main() above to real_main()
		import cProfile, pstats
		prof  = cProfile.Profile()
		prof  = prof.runctx("run(sys.argv[1:])", globals(), locals())
		stats = pstats.Stats(prof)
		stats.sort_stats("time")  # Or cumulative
		stats.print_stats(80)  # 80 = how many to print
		# The rest is optional.
		# stats.print_callees()
		# stats.print_callers()
	else:
		run(sys.argv[1:])
# EOF
