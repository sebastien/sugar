# New implementation for the Sugar Command line
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
			python_plugin.addRecognizedExtension("spy")
			javascript_plugin.addRecognizedExtension("sjs")
			actionscript_plugin.addRecognizedExtension("sas")
			python_plugin.reader = grammar.Parser
			python_reader = python_plugin.reader()
			# FIXME: This is temporary, until we use the proper reader interface
			python_reader._program = self.environment.getProgram()
			# FIXME: This should be done by the Parser itself
			self.environment.addParser(python_reader, "sg spy sjs sjava spnuts sas".split())

def sourceFileToJavaScript( path ):
	command = Command()
	return command.runAsString(["-cljavascript", path]), command.environment.report

def sourceToJavaScript( text ):
	command = Command()
	return command.runAsString(["-cljavascript", "-ssg", text]), command.environment.report

if __name__ == "__main__":
	import sys
	command = Command("sugar")
	command.run(sys.argv[1:])
	