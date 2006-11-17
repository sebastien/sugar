# Encoding: ISO-8859-1
# vim: ts=4 textwidth=79
# -----------------------------------------------------------------------------
# Project           :   SweetC                       <http://www.ivy.fr/sweetc>
# Author            :   Sebastien Pierre                     <sebastien@ivy.fr>
# License           :   BSD License (revised)
# -----------------------------------------------------------------------------
# Creation date     :   10-Aug-2005
# Last mod.         :   11-Nov-2006
# -----------------------------------------------------------------------------

import os, sys, tpg
from lambdafactory import modelbase as model

F = model.Factory(model)

# ------------------------------------------------------------------------------
#
# Parser
#
# ------------------------------------------------------------------------------

KEYWORDS = "return yield if else for in while".split()
def isKeyword( symbol ):
	return symbol in KEYWORDS

class Parser:
	"""The parser is a simple API that can be used as an entry point
	to manipulate SweetC source code."""

	def __init__( self, verbose = 0 ):
		"""Creates a new interpreter."""
		Grammar.verbose = verbose
		self.parser    = Grammar()
		self._warnings = []

	def parse( self, filepath ):
		"""Reads and parses the content given of the given file and returns a
		couple (original source code, AST), where AST is None if there was
		any error.
		
		Using the AST, you can directly access the program model elements bound
		to the AST declarations. For instance, to access the Module program
		element bound to the ModuleDeclaration, you have to get the ModuleDeclaration
		from the AST (using ast.child(ofType='ModuleDeclaration')), and then
		access the model element by calling modelElement().
		
		The whole program is accessible as interpreter.parser.pb.program (PB
		stands for ProgramBuilder, which is the factory object that constructs
		the program)."""
		text = open(filepath, 'r').read()
		# We trim the EOF
		text = text[:-1]
		# And ensure that there is an EOL
		if text[-1] != "\n":
			self.warn("No trailing EOL in file: " + filepath)
			text += "\n"
		# We try to parse the file
		try:
			res = self.parser.parseModule(self.pathToModuleName(filepath), text)
			# We set the module file path (for informative purpose only)
			res.setSource("file://" + os.path.abspath(filepath))
			return ( text, res )
		# And catch possible exceptions
		except tpg.SyntacticError:
			self.syntaxError(filepath)
			return ( text, None )
		except tpg.SemanticError:
			self.semanticError(filepath)
			return ( text, None )

	def pathToModuleName(self, modulePath):
		"""The given path must point to a SweetC source file. This method
		will return the fully qualified name of the module pointed by the
		given file."""
		# FIXME: For now, we have a single-level
		return os.path.splitext(os.path.basename(modulePath))[0]

	def warn( self, message ):
		"""Adds a warning to the self._warnings list."""
		self._warnings.append(message)

	def syntaxError( self, filepath ):
		"""Prints the current syntax error on stderr. This requires the parser
		to have generate at least one error. This is an internal method called
		by the parse method."""
		res  = "Syntax error in file '%s'\n" % (filepath)
		res += "at line %s\n" % (self.parser._errorLine)
		res += " \t%s\n" %  (self.parser._errorContext[0])
		res += " *\t%s\n" % (self.parser._errorContext[1])
		res += " \t%s\n" % (self.parser._errorContext[2])
		res += "with parser log:\n"
		for line in self.parser._log:
			res += "\t" + line + "\n"
		sys.stderr.write(res)

	def semanticError( self, filepath ):
		"""Prints the current semantic error on stderr. This requires the parser
		to have generate at least one error. This is an internal method called
		by the parse method."""
		res  = "Semantic error in file '%s'\n" % (filepath)
		res +=  "%s\n"  % (self.parser._error)
		res += "at line " % (self.parser._errorLine)
		res += " \t%s\n"  % (self.parser._errorContext[0])
		res += " *\t%s\n" %  (self.parser._errorContext[1])
		res += " \t%s\n"  %  (self.parser._errorContext[2])
		sys.stderr.write(res)

# ------------------------------------------------------------------------------
#
# Grammar
#
# ------------------------------------------------------------------------------

class Grammar(tpg.VerboseParser):
	r"""
		set lexer = ContextSensitiveLexer

		separator spaces		'[ \t]+';

		token EOL				'\n+';
		token ANY				'[^\n]+';

		token import			'import';
		token from				'from';
		token class				'class';
		token attribute			'attribute';
		token constructor		'constructor';
		token destructor		'destructor';
		token method			'method';
		token operation			'operation';
		token function			'function';
		token main				'main';
		token enddecl			'end';
		token lambda			'lambda';

		token const				'const';
		token for				'for';
		token in				'in';
		token step				'step';
		token if				'if';
		token else				'else';
		token elif				'elif';
		token while				'while';
		token return			'return';
		token new				'new';
		token release			'release';
		token application		'\-\>';

		token tab				'\t';
		token equals			'\=';
		token comma				',';
		token dot				'\.';
		token semicolon			';';
		token colon				'\:';
		token dquote			'"';
		token lparen			'\(';
		token rparen			'\)';
		token lbracket			'\[';
		token rbracket			'\]';
		token lbrace			'\{';
		token rbrace			'\}';
		token comment			'#.*';
		token range				'\.\.';

		token SYMBOL			'[A-Za-z0-9_]+';
		token NUMBER			'[0-9]+(\.[0-9]+)?';
		token TYPE				'(const\s+)?[A-Za-z0-9_]+(\[\]|\*)*';

		# --------------------------------------------------------------------
		#
		# Start and comments
		#
		# --------------------------------------------------------------------
		
		START/m			-> Module/m
		;

		Comment/c		->  $ text = ""
							(
								comment/line EOL
								$ text += line
							)+
							$ c = self.lf.comment(text)
		;

		# --------------------------------------------------------------------
		#
		# Module and Classes declarations
		#
		# --------------------------------------------------------------------
		
		Module/m		->	$ m = self.lf.createModule(self.moduleName)
							
							(   Comment/cm           |
							  EOL
							) *
# TODO: Support value assignation
							(   ModuleRequirements/mr   ) *
							(   Comment/cm             )*
							(   ClassDeclaration/cd     $ m.setSlot(cd.getName(), cd)    $    )*
							(   Comment
							|   FunctionDeclaration/fd  $ m.setSlot(fd.getName(), fd) $    )*
							(   Comment
							|   MainDeclaration/md      $ m.setSlot("__main__", md) $    )?
	;


		ModuleRequirements/r -> import SYMBOL/s
								$ if isKeyword(s):raise tpg.WrongToken
			      	            
			      	            $ r = [] ; symbols = [s]
								(	comma SYMBOL/s
									$ if isKeyword(s):raise tpg.WrongToken
									$ symbols.append(s)
								)*
                                	$ from_module = None
								(	from SYMBOL/from_module
									$ if isKeyword(from_module):raise tpg.WrongToken
								)?
								# FIXME: These operations do not seem really appropriate
								# Maybe there should be importModule and importSymbols operations
								EOL+
		;
		
		ClassDeclaration/c ->	class SYMBOL/name colon EOL
								$ if isKeyword(name):raise tpg.WrongToken
								$ c = self.lf.createClass(name)
								(	Comment
								|	AttributeDeclaration/ad	$ c.setSlot(ad.getReferenceName(), ad)
								)*
								(	Constructor/cd			$ c.setSlot("__init__", cd) $	)?
								(	Destructor/dd			$ c.setSlot("__destroy__", dd) $ 	)?
								(	Comment
								|	MethodDeclaration/md 	$ c.setSlot(md.getName(), md) $	)*
								(	ClassMethodDeclaration/cd	$ c.setSlot(cd.getName(), cd) $)*
								enddecl EOL+

		;

		AttributeDeclaration/a -> attribute (TYPE/t)? SYMBOL/s EOL
								$ if isKeyword(s):raise tpg.WrongToken
								$ a = self.lf._attr(s, t)
		;
		
		# --------------------------------------------------------------------
		#
		# Methods and function declarations
		#
		# --------------------------------------------------------------------

		# Returns a "Parameter" element with the code attribute filled with
		# the list of arguments
		Parameters/p		->	lparen
								$ p = []
								$ name = None
								(	TYPE/t (SYMBOL/name)?
									$ if isKeyword(t):raise tpg.WrongToken
									$ if isKeyword(name):raise tpg.WrongToken
									$ if not name:
									$   p.append(self.lf._arg(t))
									$ else:
									$   p.append(self.lf._arg(name, t))
									(	$ name = None
										comma TYPE/t (SYMBOL/name)?
										$ if isKeyword(t):raise tpg.WrongToken
										$ if isKeyword(name):raise tpg.WrongToken
										$ if not name:
										$   p.append(self.lf._arg(t))
										$ else:
										$   p.append(self.lf._arg(name, t))
									)*
								)? rparen
		;

		# Returns an array of Statements
		FunctionBody/b		->	$ b = []
								(	Statement/s (EOL|semicolon)+
									$ b.extend(s)
								)*
		;

		Constructor/c 		->	$ args = []
								constructor Parameters/p EOL
								$ args.add(p)
								$ c = self.lf.createMethod("__init__")
								Comment?
								FunctionBody/fb
								$ c.addOperations(*fb)
								enddecl EOL+
		;

		Destructor/d 		->	$ d = self.lf.createMethod("__destroy__")
								destructor EOL								
								Comment?
								FunctionBody/fb
								$ d.addOperations(*fb)
								enddecl EOL+
		;

		# If there is an error here, it is probably an omission of return value,
		# a bad method name, or bad parameter expressions --> there should be 
		# a method to do so
		MethodDeclaration/d ->	method SYMBOL/name Parameters/p colon EOL
								$ if isKeyword(name):raise tpg.WrongToken
								$ d = self.lf.createMethod(name, p)
								Comment?
								FunctionBody/fb
								$ d.addOperations(*fb)
								enddecl EOL+
		;

		ClassMethodDeclaration/d ->	operation SYMBOL/name Parameters/p colon EOL
								$ if isKeyword(name):raise tpg.WrongToken
								$ d = self.lf.createClassMethod(name, p)
								Comment?
								FunctionBody/fb
								$ d.addOperations(*fb)
								enddecl EOL+
		;


		FunctionDeclaration/d -> function SYMBOL/name Parameters/p colon EOL
								$ if isKeyword(name):raise tpg.WrongToken
								$ d = self.lf.createFunction(name, p)
								# Function documentation
								Comment?
								FunctionBody/fb
								$ d.addOperations(*fb)
								enddecl EOL+
		;

		MainDeclaration/m  ->	main colon EOL
								( Comment )?
								$ m = self.lf.createFunction("__main__",())
								FunctionBody/fb
								$ m.addOperations(*fb)
								(Comment | EOL)*
								enddecl EOL+
		;

		# --------------------------------------------------------------------
		#
		# Statements
		#
		# --------------------------------------------------------------------
		# This set of rules tries to parse a subset of the C language extended
		# with SweetC additional keywords and operators. This is where symbol
		# resolution and type checking is done.
		
		# Returns a string representing the symbol. You should call
		# self.context.resolve() later to ensure that the symbol is accessible
		Symbol/s			->	SYMBOL/sym
								$ if isKeyword(sym): raise tpg.WrongToken
								$ s = self.lf._ref(sym)
								(
									dot SYMBOL/s2
									$ if isKeyword(s2): raise tpg.WrongToken
									$ s = self.lf.resolve(s, self.lf._ref(s2))
								)*
		;
		
		Litteral/c			->	(	NUMBER/n
									$ if n.find(".") != -1: c = self.lf._number(float(n))
									$ else: c = self.lf._number(int(n))
								|	dquote
									@beginning
									(	'\\"'/v
									|	'[^"]'/v
									)*
									@end
									dquote
									$ c = self.lf._string(self.extract(beginning, end))
								)
		;

		List/l				->	lbracket
								$ l = self.lf._list()
								(
									Expression/e $ l.addValue(e)
									(
										comma
										Expression/e
										$ l.addValue(e)
									)*
								)?
								rbracket
		;

		Dict/d				->	lbrace
								$ d = self.lf._dict()
								(
									Expression/k colon Expression/v
									$ d.setValue(k, v) 
									(
										comma
										Expression/k colon Expression/v 
										$ d.setValue(k, v) 
									)*
								)?
								rbrace
		;

		Cast/c				->	lparen
								$ c = ""
								(	const
									$ c += "const "
								)?
								TYPE/t
								$ c += t
								(	'\*'
									$ c += "*"
								)*
								rparen
		;

		Closure/c			->	Parameters/p application lbrace EOL*
								$ c = self.lf.createClosure(p)
								(	Statement/s 
									$ c.addOperations(*s)
									(
										( EOL | semicolon )
										Statement/s
										$ c.addOperations(*s)
									)*
								)?
								EOL*
								rbrace
		;

		Value/v				->	$ c= None
								# I removed Cast, as I don't feeel is
								# necessary
								#(
								#	Cast/c
								#)
								#?
								(	Litteral/v
								|	List/v
								|	Dict/v
								|	Invocation/v
								|	Symbol/v
								|	Closure/v
								|	lparen Expression/v rparen 
								)
		;

		PrefixOperator/o	->	( '-'/o  | '\ +'/o | '&'/o | '\*+'/o )
		;

		ComparisonOperator/o ->	( '=='/o   | '<[=]?'/o  | '>[=]?'/o )
		;

		InfixOperator/o		->	( '&&'/o | '\|\|'/o | '<<'/o | '>>'/o 
								| '[/\*\+\-]'/o
								| ComparisonOperator/o
								)
		;

		# This was disabled, but suffix operators will be "[xx..xx]
		# SuffixOperator/o	-> ( '--'/o | '\+\+'/o )
		# ;

		# An expression can be substituted to a value, either directly
		# (which is the case for litterals), or after evaluation, which
		# is the case for the rest (operations), excepted for some languages
		# where control flow operations do not directly raise a value.
		Expression/e		->	(
									new Symbol/s lparen
									#$ e = self.pb.instanciate(self.pb.resolve(s))
									(	Expression/sube
										#$ e.add(sube)
										(	comma Expression/sube
										#	$ e.add(sube)
										)*
									)?
									rparen
								|	Value/a InfixOperator/o Value/b
									$ e = self.lf.compute(self.lf._op(o), a, b)
								|	PrefixOperator/o Value/v
									$ e = self.lf.compute(self.lf._op(o), v)
								#|	Value/v SuffixOperator/o
								#	$ e = self.lf.compute(self.lf._op(o), v)
								|	Value/v '\[' Expression/ie '\]'
									# TODO
								|	Value/start range Value/end
									$ e = self.lf.enumerate(start, end)
								# TODO: This is ugly, but it is the only way to
								# make it work. It seems like everything that
								# starts with a paren has to be recalled here.
								|	Closure/e
								|	lparen Value/start rparen range Value/end
									$ e = self.lf.enumerate(start, end)
								|	lparen Value/start rparen range lparen Value/end rparen
									$ e = self.lf.enumerate(start, end)
								|	lparen Value/e rparen 
								|	Value/e
								)
		;
		


		# Statements represent many kind of operations, so the Statement
		# grammar rule simply acts as a switch to dispatch between the
		# different possibilities.
		Statement/s			->	( Comment | EOL ) *
								(	Control/s
								|	Invocation/s
								|	Declaration/s
								|	Assignation/s
								) 
								$ if type(s) not in (tuple, list):s=[s]
		;

		Block/b				->	EOL?
									$ b = self.lf.createBlock()
									( EOL
									| Comment
									| Statement/s $ b.addOperations(*s)
									)*
								
		;

		Declaration/v		->	TYPE/t SYMBOL/s
								$ if isKeyword(t):raise tpg.WrongToken
								$ if isKeyword(s):raise tpg.WrongToken
								$ slot = self.lf._slot(s,t)
								$ v    = self.lf.allocate(slot)
								(	equals/e Expression/ex
									$ a = v
									$ b = self.pb.assign(slot, ex)
									$ v = [a, b]
								)?
		;

		# TODO: Add LValue instead of Symbol
		Assignation/v		-> Symbol/s ( '=\['/o | '=\]'/o | '='/o | '\:='/o |'-='/o | '\+='/o ) Expression/e
							   $ if o == '=':
							   $     v = self.lf.assign(s, e)
							   $ elif o == ':=':
							   $     s = self.lf._slot(s.getReferenceName())
							   $     v = [self.lf.allocate(s), self.lf.assign(s,e)]
							   $ elif o == "-=":
							   $     v = self.lf.assign(s, self.lf.compute("-", s, e))
							   $ elif o == "+=":
							   $     v = self.pb.assign(s, self.lf.compute("+", s, e))
							   $ elif o == "=[":
							   $     i = self.pb.invoke(self.pb.message(s, "prepend"))
							   $     i.add(e)	
							   $     v = self.pb.assign(s, i)
							   $ elif o == "=]":
							   $     i = self.pb.invoke(self.pb.message(s, "append"))
							   $     i.add(e)	
							   $     v = self.pb.assign(s, i)
							   $ else:
							   $     assert None, "Uknown assignation operator: " + o
		;

		Invocation/v		->	Symbol/func lparen
								$ args = []
								(	Expression/e
									$ args.append(e)
									(	comma Expression/e
										$ args.append(e)
									)*
								)?
								$ v = self.lf.invoke(func, *args)
								rparen
		;

		# --------------------------------------------------------------------
		#
		# Control
		#
		# --------------------------------------------------------------------
		# Control structures describe the program runtime behaviour
		
		Control/v			->	(	return Expression/e
									$ v = self.lf.returns(e)
								|	For/v
								|	While/v
								|	If/v
								) 
		;

		For/v				->	for SYMBOL/s in Expression/iterator
								$ if isKeyword(s):raise tpg.WrongToken
								(  step Expression/step
								   $ iterator.setStep(step)
								)?
								colon EOL
								Block/bl
								$ v = self.lf.iterate(self.lf._slot(s), iterator, bl)
								enddecl
		;

		While/v				->	while Expression/e colon EOL*
								Block/b
								$ v = self.lf.repeat(e, b)
								enddecl
		;

		If/v				->	if Expression/e colon EOL*
								(Comment | EOL)*
								Block/b
								$ v = self.lf.select()
								$ v.addRule(self.lf.match(e, b))
								( EOL? Comment* ElseIf/e $ v.addRule(e) $ ) *
								( EOL? Comment* Else/e   $ v.addRule(e) $ ) ?
								enddecl
		;

		ElseIf/b			->	else if Expression/e colon EOL*
								Block/b
								$ b = self.lf.match(e, b)
		;

		Else/b				->	else colon EOL*
								Block/b
								$ b = self.lf.match(self.lf._ref("True"), b)
		;

		
	"""

	def __init__( self ):
		"""The SweetC parser is a verbose parser that allows to keep track of
		the last unmatched rules, which is useful when you want to report the
		location of a syntax error."""
		tpg.VerboseParser.__init__(self)
		self._errorContext = None
		self._errorLine    = -1
		self._log          = []
		self._warnings     = []
		self._error        = None
		self.lf            = F
    
	def parseModule( self, name, body ):
		"""Parses a module with the given name, with the given text."""
		# TODO: Ensure that module name follows the naming convention
		self.moduleName = name
		return self(body)
		
	def warning( self, message ):
		"""Adds a triple (message, line number, line text) to the _warnings
		property of the parser."""
		self._warnings.append((message, self.currentLine(), self.currentLineText() ))

	def error( self, message ):
		"""Sets _errorContext to be the current context, _error to the given
		message, and raises a SemanticError exception with the message as
		argument."""
		self._errorContext = self.errorContext()
		self._error        = message
		raise tpg.SemanticError(message)

	def eat(self, name):
		"""Refefinition of the TPG VerboseParser eat method to handle better
		logging."""
		try:
			value = tpg.VerboseParser.eatCSL(self, name)
			self._log  = []
			self._errorContext = None
			return value
		except tpg.WrongToken:
			raise

	def eatCSL(self, name):
		"""Redefines this to keep track of the last unmatched set of rules."""
		try:
			value = tpg.VerboseParser.eatCSL(self, name)
			self._log  = []
			self._errorContext = None
			return value
		except tpg.WrongToken:
			if self._errorContext == None:
				self._errorContext = self.errorContext()
				self._errorLine    = self.currentLine()
			text = self.lexer.input[self.lexer.pos:self.lexer.pos+10].replace('\n', ' ')
			self._log.append("%s:%s\t%s\t%s != %s" % (
				self.lexer.line, self.lexer.row, name, self.stackInfo(), text
			))
			raise
	
	def stackInfo( self ):
		"""Returns a string representing the current call stack, with each
		frame name separated by a dot."""
		name        = None
		callernames = []
		stackdepth  = 0
		while name != self.axiom:
			stackdepth += 1
			name        = sys._getframe(stackdepth+1).f_code.co_name
			if len(callernames) < 10:
				callernames.insert(0, name)
		callernames = '.'.join(callernames)
		return callernames
	
	def currentLineText( self ):
		"""Returns the text of the currently parsed line."""
		return self.getLineAtPos(self.lexer.pos)[2]

	def currentLine( self ):
		"""Returns the number of the currenlty parsed line."""
		return self.lexer.input.count("\n", 0, self.lexer.pos)
	
	def getLineAtPos( self, pos ):
		"""Retruns the (line start, line end, line text) of the line containing
		the given position."""
		start = self.lexer.input.rfind("\n", 0, pos)
		end   = self.lexer.input.find("\n",  pos)
		return (start+1, end, self.lexer.input[start+1:end].strip())

	def errorContext( self ):
		"""Returns the lines surrounding the current line"""
		start, end, second = self.getLineAtPos(self.lexer.pos)
		if start > 0: a, b, first  = self.getLineAtPos(start - 1)
		else: first = ""       
		a, b,       third  = self.getLineAtPos(end   + 1)
		return (first, second, third)

# EOF
