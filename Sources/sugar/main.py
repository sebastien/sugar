#!/usr/bin/env python
# # New implementation for the Sugar Command line
# 
from lambdafactory.main import Command as BaseCommand
import grammar

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
		python_reader._program = self.environment.getProgram()
		# FIXME: This should be done by the Parser itself
		self.environment.addParser(python_reader, "sg spy sjs sjava spnuts sas".split())

def sourceFileToJavaScript( path, moduleName=None, options="" ):
	command = Command()
	opts = ["-cljavascript"]
	opts.extend(options.split())
	if moduleName:
		opts.append("-m" + moduleName)
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

if __name__ == "__main__":
	import sys
	run(sys.argv[1:])
