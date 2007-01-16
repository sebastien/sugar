#!/usr/bin/env python
# Encoding: ISO-8859-1
# vim: ts=4 textwidth=79
# -----------------------------------------------------------------------------
# Project           :   Sugar                         <http://www.ivy.fr/sugar>
# Author            :   Sebastien Pierre                     <sebastien@ivy.fr>
# License           :   Lesser GNU Public License
# -----------------------------------------------------------------------------
# Creation date     :   10-Aug-2005
# Last mod.         :   03-Jan-2007
# -----------------------------------------------------------------------------

import os
from dparser import Parser, Reject
from lambdafactory import modelbase as model
from lambdafactory import interfaces

__doc__ = """
This module implements a Sugar syntax driver for the LambdaFactory program model
library. This module uses the fantastic D parser Python library.
"""

# We instanciate LambdaFactory default factory, which will be used in the
# grammar production rules to create model elements.

F = model.Factory(model)
KEYWORDS = "new return yield and or not is".split()

# ----------------------------------------------------------------------------
# Common utilities
# ----------------------------------------------------------------------------

def t_filterOut( c, l ):
	return filter(lambda e:e!=None and e!=c, l)

def t_setCode( process, code, context=None ):
	for o in code:
		#print "SETTING",o,
		if isinstance(o, interfaces.IOperation):
		#	print "as operation"
			process.addOperation(o)
		elif context \
		and  isinstance(o, interfaces.IAssignable) \
		and  isinstance(o, interfaces.IReferencable):
		#	print "as slot"
			context.setSlot(o.getName(), o)
		else:
		#	print "not recognized"
			pass
	return process

def t_split( array, element ):
	res = []
	cur = None
	for a in array:
		if element == a:
			if cur!=None: res.append(cur)
			cur = [a]
		else:
			if cur is None: cur = []
			cur.append(a)
	if cur != None:	res.append(cur)
	return res
	
# ----------------------------------------------------------------------------
# Statements
# ----------------------------------------------------------------------------

def d_Program(t):
	'''Program: Code'''
	# FIXME: Add a notion of Module = Slots + Process
	m = F.createModule(F.CurrentModule)
	f = F.createFunction(F.ModuleInit, ())
	# FIXME: Rename to addStatements
	t_setCode(f,t[0],m)
	m.setSlot(F.ModuleInit, f)
	return m

def d_Code(t):
	'''Code : (Declaration|Statement|Comment|EOL)* '''
	# FIXME: Declarations should not go into code
	return t[0]

def d_Line(t):
	'''Line : (Allocation|Termination|Expression) ( ';' Line )* '''
	r = [t[0][0]]
	r.extend(t[1])
	r = t_filterOut(";", r)
	return r

def d_Comment(t):
	'''Comment : '#' "[^\\n]*" EOL'''
	return F.comment(t[1])

def d_Documentation(t):
	'''Documentation : '!' "[^\\n]*" EOL Documentation? '''
	return t

def d_Statement(t):
	'''Statement : (Match|Allocation|Termination|Expression) ( ';' | '\\n' ) '''
	return t[0][0]

def d_Declaration(t):
	'''Declaration : (Main|Function|Class) EOL '''
	return t[0][0]

# ----------------------------------------------------------------------------
# Declarations
# ----------------------------------------------------------------------------

def d_Main(t):
	'''Main: '@main' EOL
	      Code
	   '@end'
	'''
	f = F.createFunction(F.MainFunction , ())
	t_setCode(f, t[2])
	return f

def d_Function(t):
	'''Function: '@function' NAME Arguments? EOL
		  Documentation?
	      Code
	   '@end'
	'''
	f = F.createFunction(t[1] , t[2] and t[2][0] or ())
	t_setCode(f, t[5])
	return f

def d_Class(t):
	# FIXME: Change Name to Reference
	'''Class: '@class' NAME (':' Name (',' Name)* )? EOL
	      (   ClassAttribute
	      |   ClassMethod
	      |   Attribute
	      |   Method
	      |   Constructor
	      |   Destructor
	      |   EOL
	      )*
	  '@end'
	'''
	# TODO: Parents support
	parents = []
	parents.extend(t[2])
	parents = t_filterOut(":", parents)
	parents = t_filterOut(",", parents)
	f = F.createClass(t[1] , parents)
	t_setCode(None, t[4], f)
	return f

def d_ClassAttribute(t):
	'''ClassAttribute: '@shared' NAME (':' Type)?  ('=' Value)? EOL '''
	return F._classattr(t[1], t[2] and t[2][1] or None, t[3] and t[3][1] or None)

def d_ClassMethod(t):
	'''ClassMethod: '@operation' NAME Arguments? EOL
		   Documentation?
	       Code
	  '@end'
	'''
	m = F.createClassMethod(t[1], t[2] and t[2][0] or ())
	t_setCode(m, t[5])
	return m

def d_Annotation(t):
	'''Annotation: WhenAnnotation'''
	return t[0]

def d_WhenAnnotation(t):
	'''WhenAnnotation: '@when' Expression EOL'''
	return F.annotation('when', t[1])

def d_Attribute(t):
	'''Attribute: '@property' NAME (':' Type)? ('=' Value)?  EOL '''
	return F._attr(t[1], t[2] and t[2][1] or None, t[3] and t[3][1] or None)

def d_Method(t):
	'''Method: '@method' NAME Arguments? EOL
	       Annotation*
	       Documentation?
	       Code
	  '@end'
	'''
	m = F.createMethod(t[1], t[2] and t[2][0] or ())
	for ann in t[4]:
		m.annotate(ann)
	t_setCode(m, t[6])
	return m

def d_Constructor(t):
	'''Constructor: '@constructor'  Arguments? EOL
	       Documentation?
	       Code
	  '@end'
	'''
	m = F.createConstructor(t[1] and t[1][0])
	t_setCode(m, t[4])
	return m

def d_Destructor(t):
	'''Destructor: '@destructor' EOL
	       Documentation?
	       Code
	  '@end'
	'''
	m = F.createDestructor()
	t_setCode(m, t[6])
	return m

def d_Condition(t):
	''' Condition: Expression '->' Expression '''
	res = F.select()
	match = F.match(t[0], t[2])
	res.addRule(match)
	return res

def d_Match(t):
	''' Match: '@match' (EOL|':') 
	           Condition
	           ( EOL Condition )*
	           ( EOL '--' Expression)?
	           EOL
	           '@end'
	'''
	conds = []
	conds.append(t[2])
	conds.extend(t_filterOut('',t[3]))
	conds = [m.getRules()[0] for m in conds]
	last = t_filterOut('--', t[4])
	# TODO: Add an 'otherwise'
	if last: conds.append(F.match(F._ref('true'),last[0] ))
	res = F.select()
	map(res.addRule, conds)
	return res

# ----------------------------------------------------------------------------
# Operations
# ----------------------------------------------------------------------------

def d_Termination(t):
	'''Termination : 'return' Expression'''
	return F.returns(t[1])

def d_Iteration(t):
	'''Iteration : Expression '::' Expression'''
	return F.iterate(t[0], t[2])

def d_Comparison(t):
	'''Comparison : Expression ('<' | '>' | '==' | '>=' | '<=' | '<>' | '!='
	                 |'in' |'not' 'in'  | 'is' |'is' 'not') Expression
	'''
	# FIXME: Normalize operators
	# FIXME: t[1] may be a list (not in, is not)
	return F.compute(F._op(" ".join(t[1])),t[0],t[2])

def d_Computation(t):
	'''Computation: Expression ('+'|'-'|'*'|'/'|'%'|'//'|'and'|'or') Expression '''
	# FIXME: Normalize operators
	return F.compute(F._op(t[1][0]),t[0],t[2])

def d_PrefixComputation(t):
	'''PrefixComputation: ('not') Expression '''
	# FIXME: Normalize operators
	print t
	return F.compute(F._op(t[0][0]),t[1])

def d_Assignation(t):
	''' Assignation: Expression '=' Expression '''
	return F.assign(t[0], t[2])

def d_Allocation(t):
	'''Allocation : AllocationD | AllocationS'''
	return t[0]

def d_AllocationS(t):
	'''AllocationS: 'var' NAME (':' Type)?  '''
	return F.allocate(F._slot(t[1],t[2] and t[2][1] or None))

def d_AllocationD(t):
	''' AllocationD: NAME (':' Type)? ':=' Expression? '''
	return F.allocate(F._slot(t[0],t[1] and t[1][1] or None), t[3] and t[3][0] or None)

# ----------------------------------------------------------------------------
# Expressions
# ----------------------------------------------------------------------------

def d_Expression(t):
	'''Expression : Condition | Iteration | Instanciation | InvocationOrResolution | Slicing | Assignation | Comparison |
	              PrefixComputation | Computation |   Value | LP Expression RP
	'''
	if len(t) == 1: return t[0]
	else: return t[1]

def d_Value(t):
	'''Value : Litteral|List|Dict|Range|Closure'''
	return t[0]

# ----------------------------------------------------------------------------
# Operations
# ----------------------------------------------------------------------------

def d_Instanciation(t):
	'''Instanciation: 'new' Expression ( Name | Value | LP (Expression (","  Expression )*)?  RP)
	'''
	p = t[2]
	if len(p) == 1:
		return F.instanciate(t[1], *p)
	elif len(p) == 2:
		return F.instanciate(t[1])
	else:
		print len(p), p
		p = t_filterOut(",", p[1:-1])
		return F.instanciate(t[1], *p)

def d_Slicing(t):
	'''Slicing: Expression LB Expression RB '''
	return F.slice(t[0], t[2])

def d_InvocationOrResolution(t):
	'''InvocationOrResolution: Expression ( Name | Value | LP (EOL* Expression EOL* ( (EOL|",") EOL* Expression EOL*)*)?  RP) '''
	p = t[1]
	# NOTE: In some cases (and I don't get why this happens), Invocation
	# matches but Resoltuion doesn't. So we check if expression is a
	# reference (a name) and we make the invocation fail
	if len(p) == 1:
		if isinstance(p[0], interfaces.IReference):
			return F.resolve(p[0], t[0])
		else:
			return F.invoke(t[0], *p)
	elif len(p) == 2:
		return F.invoke(t[0])
	else:
		p = t_filterOut(",", p[1:-1])
		return F.invoke(t[0], *p)

# ----------------------------------------------------------------------------
# Closures
# ----------------------------------------------------------------------------

def d_Closure(t):
	'''Closure: LC (Arguments '|')? (Line|Code)? RC '''
	a = t[1] and t[1][0] or ()
	c = F.createClosure(a)
	t_setCode(c, t[2] and t[2][0] or ())
	return c

def d_Arguments(t):
	'''Arguments: Argument (',' Argument)* '''
	r = [t[0]] ; r.extend(t[1])
	r = filter(lambda e:e!=',', r)
	return r

def d_Argument(t):
	'''Argument: NAME (':' Type)? '''
	return F._arg(t[0], t[1] and t[1][1] or None)

def d_Type(t):
	'''Type: NAME '''
	return t[0]

# ----------------------------------------------------------------------------
# Litterals
# ----------------------------------------------------------------------------

def d_Litteral(t):
	'''Litteral : Integer|Float|String|Name '''
	return t[0]

def d_Integer(t):
	'''Integer : "-?[0-9]+" '''
	return F._number(int(t[0]))

def d_Float(t):
	'''Float : "-?[0-9]+\.[0-9]+" '''
	return F._number(float(t[0]))

def d_String(t):
	'''String : StringSQ|StringDQ '''
	return F._string(t[0])

def d_StringSQ(t):
	'''StringSQ : "'" (STR_NOT_SQUOTE|STR_ESC)* "'" '''
	return "".join(t[1])

def d_StringDQ(t):
	'''StringDQ : '"' (STR_NOT_DQUOTE|STR_ESC)* '"' '''
	return "".join(t[1])

def d_Name(t):
	'''Name : NAME '''
	# FIXME: Maybe add a "_name" to LF
	return F._ref(t[0])

# ----------------------------------------------------------------------------
# Compound
# ----------------------------------------------------------------------------

def d_Range(t):
	'''Range: Expression '..' Expression '''
	return F.enumerate(t[0], t[2])

def d_List(t):
	'''List : LB (Expression ("," Expression)*)? RB '''
	r = t_filterOut(",", t[1])
	l = F._list(*r)
	return l

def d_Dict(t):
	'''Dict : LC ( EOL* DictPair EOL* ( (EOL |"," ) EOL* DictPair EOL*)*)? RC '''
	p = t_filterOut(",", t[1])
	d = F._dict()
	for k,v in p:
		d.setValue(k,v)
	return d

def d_DictPair(t):
	'''DictPair : Expression ':' Expression '''
	return t[0], t[2]

# ----------------------------------------------------------------------------
# Punctuation
# ----------------------------------------------------------------------------

def d_LP(t):
	''' LP : '(' '''
	return str(t)

def d_RP(t):
	''' RP : ')' '''
	return str(t)

def d_LB(t):
	''' LB : '[' '''
	return str(t)

def d_RB(t):
	''' RB : ']' '''
	return str(t)

def d_LC(t):
	''' LC : '{' '''
	return str(t)

def d_RC(t):
	''' RC : '}' '''
	return str(t)

def d_NAME(t, spec):
	''' NAME: "[$A-Za-z_]+[$0-9A-Za-z_]*" '''
	if spec and t[0] in KEYWORDS:
		return Reject
	else:
		return t[0]

def d_EOL(t):
	''' EOL: '\\n' '''
	return

def d_STR_ESC(t):
	r'''STR_ESC: "\\[^]"'''
	return t[0]

def d_STR_NOT_SQUOTE(t):
	r'''STR_NOT_SQUOTE: "[^\\\n\']+" '''
	return t[0]

def d_STR_NOT_DQUOTE(t):
	r'''STR_NOT_DQUOTE: "[^\\\n\"]+" '''
	return t[0]

def d_whitespace(t):
	'whitespace : "[ \t]*"'
	# FIXME: Implement specific Python whitespace function
	return

# ----------------------------------------------------------------------------
#
# PARSER OPERATIONS
#
# ----------------------------------------------------------------------------

def disambiguate( nodes ):
	# FIXME: This may not be the best way...
	print "********AMIBGUITY", nodes
	return nodes[0]

# ----------------------------------------------------------------------------
#
# EXTERNAL API
#
# ----------------------------------------------------------------------------

_PARSER = Parser(make_grammar_file=1)

def parse( text, verbose=True ):
	#res = _PARSER.parse(text, ambiguity_fn=disambiguate,print_debug_info=1)
	res = _PARSER.parse(text,ambiguity_fn=disambiguate, print_debug_info=(verbose and 1 or 0))
	return res

def parseFile( path, verbose=False ):
	f = file(path, 'r') ; t = f.read() ; f.close()
	return parse(t, verbose)

def parseModule( name, text, verbose=False ):
	res = parse(text, verbose)
	res.setName(name)
	return res
# ------------------------------------------------------------------------------
#
# Parser
#
# ------------------------------------------------------------------------------

class Parser:
	"""The parser is a simple API that can be used as an entry point
	to manipulate SweetC source code."""

	def __init__( self, verbose = False ):
		"""Creates a new interpreter."""
		self._warnings = []
		self.verbose   = verbose

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
		return self.parseModule(self.pathToModuleName(filepath), text, filepath)

	def parseModule( self, name, text, sourcepath=None ):
		# We trim the EOF
		text = text[:-1]
		# And ensure that there is an EOL
		if text[-1] != "\n":
			self.warn("No trailing EOL in given code")
			text += "\n"
		# We try to parse the file
		#try:
		if True:
			res = parseModule(name, text, self.verbose)
			# We set the module file path (for informative purpose only)
			if sourcepath:
				res.setSource("file://" + os.path.abspath(sourcepath))
			return ( text, res )
		# And catch possible exceptions
		#except tpg.SyntacticError:
		#	self.syntaxError(sourcepath)
		#	return ( text, None )
		#except tpg.SemanticError:
		#	self.semanticError(sourcepath)
		#	return ( text, None )

	def pathToModuleName(self, modulePath):
		"""The given path must point to a SweetC source file. This method
		will return the fully qualified name of the module pointed by the
		given file."""
		# FIXME: For now, we have a single-level
		res = os.path.splitext(os.path.basename(modulePath))[0]
		res = res.replace("-", "_")
		return res

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

# ----------------------------------------------------------------------------
#
# MAIN
#
# ----------------------------------------------------------------------------

if __name__ == "__main__":
	# This is a simple debug code that is useful for quickly parsing input
	import sys
	from lambdafactory.reporter import DefaultReporter
	from lambdafactory import javascript

	if sys.argv[1] == "--":
		t        = "\n".join(sys.argv[2:]) + '\n'
		print 'Parsing:' + repr(t)
		res      = parse(t)
	else:
		res      = parseFile(sys.argv[1])

	reporter = DefaultReporter
	writer   = javascript.Writer(reporter=reporter)
	resolver = javascript.Resolver(reporter=reporter)
	resolver.flow(res)

	print writer.write(res)

# EOF
