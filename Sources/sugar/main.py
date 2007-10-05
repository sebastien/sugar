#!/usr/bin/env python
# # New implementation for the Sugar Command line
# 
from lambdafactory.main import Command as BaseCommand
from lambdafactory.resolver import AbstractResolver
import grammar

class Command(BaseCommand):

	def setupEnvironment( self ):
			self.environment.resolver = AbstractResolver()
			python_plugin       = self.environment.loadLanguage("python")
			javascript_plugin   = self.environment.loadLanguage("javascript")
			actionscript_plugin = self.environment.loadLanguage("actionscript")
			pnuts_plugin        = self.environment.loadLanguage("pnuts")
			python_plugin.addRecognizedExtension("spy")
			javascript_plugin.addRecognizedExtension("sjs")
			actionscript_plugin.addRecognizedExtension("sas")
			pnuts_plugin.addRecognizedExtension("spnuts")
			pnuts_plugin.addRecognizedExtension("spnut")
			python_plugin.reader = grammar.Parser
			python_reader = python_plugin.reader()
			python_reader.environment = self.environment
			# FIXME: This is temporary, until we use the proper reader interface
			python_reader._program = self.environment.getProgram()
			# FIXME: This should be done by the Parser itself
			self.environment.addParser(python_reader, "sg spy sjs sjava spnuts sas".split())

def sourceFileToJavaScript( path, moduleName=None ):
	command = Command()
	if moduleName:
		return command.runAsString(["-cljavascript", "-m" + moduleName, path])
	else:
		return command.runAsString(["-cljavascript", path])

def sourceToJavaScript( text, moduleName=None ):
	command = Command()
	if moduleName:
		return command.runAsString(["-cljavascript", "-m" + moduleName, "-ssg", text])
	else:
		return command.runAsString(["-cljavascript", "-ssg", text])

if __name__ == "__main__":
	import sys
	command = Command("sugar")
	command.run(sys.argv[1:])
	
