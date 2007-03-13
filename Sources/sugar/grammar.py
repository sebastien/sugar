#!/usr/bin/env python
# Encoding: ISO-8859-1
# vim: ts=4 textwidth=79
# -----------------------------------------------------------------------------
# Project           :   Sugar                         <http://www.ivy.fr/sugar>
# Author            :   Sebastien Pierre                     <sebastien@ivy.fr>
# License           :   Lesser GNU Public License
# -----------------------------------------------------------------------------
# Creation date     :   10-Aug-2005
# Last mod.         :   09-Mar-2007
# -----------------------------------------------------------------------------

import os
from dparser import Parser as DParser
from dparser import Reject
from lambdafactory import modelbase as model
from lambdafactory import interfaces

__doc__ = """
This module implements a Sugar syntax driver for the LambdaFactory program model
library. This module uses the fantastic D parser Python library.
"""

# We instanciate LambdaFactory default factory, which will be used in the
# grammar production rules to create model elements.

F = model.Factory(model)
KEYWORDS = "and or not is var new for in return yield when otherwise end".split()

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
		elif type(o) in (list, tuple):
			t_setCode(process, o, context)
		else:
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
	'''Program: 
		(Comment | EOL) *
		Documentation? 
		Code
	'''
	# FIXME: Add a notion of Module = Slots + Process
	m = F.createModule(F.CurrentModule)
	if t[1]: m.setDocumentation(t[1] and t[1][0])
	f = F.createFunction(F.ModuleInit, ())
	# FIXME: Rename to addStatements
	t_setCode(f,t[2],m)
	m.setSlot(F.ModuleInit, f, True)
	return m

def d_Code(t, spec):
	'''Code : (EOL | (CHECK (Declaration|Condition|Statement|Comment)))* '''
	# FIXME: Declarations should not go into code
	return t_filterOut(None, t[0])

# FIXME: Exchange LINE and STATEMENT
def d_Line(t):
	'''Line : (Select|Allocation|Termination|Expression) ( ';' Line )* '''
	r = [t[0][0]]
	r.extend(t[1])
	r = t_filterOut(";", r)
	return r

def d_Comment(t):
	'''Comment : '#' "[^\\n]*" EOL'''
	return F.comment(t[1])

def d_Documentation(t):
	'''Documentation : ('|' "[^\\n]*" EOL)+'''
	d = t[0]
	d = t_filterOut('|',d)
	return F.doc("\n".join(d))

def d_Statement(t):
	'''Statement : Line EOL '''
	return t[0][0]

def d_Declaration(t):
	'''Declaration : (Main|Function|Class) EOL '''
	return t[0][0]

# ----------------------------------------------------------------------------
# Declarations
# ----------------------------------------------------------------------------

def d_Main(t):
	'''Main: '@main' EOL
		  (INDENT
	      Code
	      DEDENT)?
	   '@end'
	'''
	f = F.createFunction(F.MainFunction , ())
	t_setCode(f, t[2] and t[2][1] or ())
	return f

def d_Function(t):
	'''Function: '@function' NAME Arguments? EOL
		  Documentation?
		  (INDENT
	      Code
	      DEDENT
	      )?
	   '@end'
	'''
	f = F.createFunction(t[1] , t[2] and t[2][0] or ())
	if t[4]: f.setDocumentation(t[4] and t[4][0])
	t_setCode(f, t[5] and t[5][1] or ())
	return f

def d_Class(t):
	# FIXME: Change Name to Reference
	'''Class: '@class' NAME (':' Name (',' Name)* )? EOL
		  Documentation?
		  (INDENT
	      (   ClassAttribute
	      |   ClassMethod
	      |   Attribute
	      |   Method
	      |   Constructor
	      |   Destructor
	      |   MethodGroup
	      |   EOL
	      )*
	      DEDENT) ?
	  '@end'
	'''
	# TODO: Parents support
	parents = []
	parents.extend(t[2])
	parents = t_filterOut(":", parents)
	parents = t_filterOut(",", parents)
	f = F.createClass(t[1] , parents)
	if t[4]: f.setDocumentation(t[4] and t[4][0])
	t_setCode(None, t[5], f)
	return f

def d_Annotation(t):
	'''Annotation: (WhenAnnotation | PostAnnotation| AsAnnotation)'''
	return t[0][0]

def d_WhenAnnotation(t):
	'''WhenAnnotation: '@when' Expression EOL'''
	return F.annotation('when', t[1])

def d_PostAnnotation(t):
	'''PostAnnotation: '@post' Expression EOL'''
	return F.annotation('post', t[1])

def d_AsAnnotation(t):
	'''AsAnnotation: '@as' ("[a-zA-Z0-9_\-]+")+ EOL'''
	return F.annotation('as', t[1])

def d_Attribute(t):
	'''Attribute: 
		'@property' NAME (':' Type)? ('=' Value)?  EOL
		Documentation ?
	 '''
	a = F._attr(t[1], t[2] and t[2][1] or None, t[3] and t[3][1] or None)
	if t[-1]: a.setDocumentation(t[-1] and t[-1][0])
	return a

def d_ClassAttribute(t):
	'''ClassAttribute: 
		'@shared' NAME (':' Type)?  ('=' Expression)? EOL
		Documentation ? 
	'''
	a =  F._classattr(t[1], t[2] and t[2][1] or None, t[3] and t[3][1] or None)
	if t[-1]: a.setDocumentation(t[-1] and t[-1][0])
	return a

def d_MethodGroup(t):
	'''MethodGroup: '@group' "[a-zA-Z0-9_\-]+" EOL
		Annotation*
		Documentation?
	    EOL*
		(ClassMethod | Method | EOL)* 
	   '@end'
	'''
	annotation = F.annotation('as', t[1])
	methods    = t_filterOut('', t[6])
	for m in methods:
		m.annotate(annotation)
		for a in t[3]: m.annotate(a)
	return methods
	
def d_Method(t):
	'''Method: '@method' NAME Arguments? EOL
	       Annotation*
	       Documentation?
	       EOL*
	       (INDENT
	       Code
	       DEDENT) ?
	  '@end'
	'''
	m = F.createMethod(t[1], t[2] and t[2][0] or ())
	for ann in t[4]:
		m.annotate(ann)
	if t[5]: m.setDocumentation(t[5] and t[5][0])
	t_setCode(m, t[7] and t[7][1] or ())
	return m

def d_ClassMethod(t):
	'''ClassMethod: '@operation' NAME Arguments? EOL
		   Documentation?
		   EOL*
		   (INDENT
	       Code
	       DEDENT)?
	  '@end'
	'''
	m = F.createClassMethod(t[1], t[2] and t[2][0] or ())
	if t[4]: m.setDocumentation(t[4] and t[4][0])
	t_setCode(m, t[6] and t[6][1] or ())
	return m


def d_Constructor(t):
	'''Constructor: '@constructor'  Arguments? EOL
	       (PostAnnotation)*
	       Documentation?
	       EOL*
	       (INDENT
	       Code
	       DEDENT)?
	  '@end'
	'''
	m = F.createConstructor(t[1] and t[1][0])
	for ann in t[3]: m.annotate(ann)
	if t[4]: m.setDocumentation(t[4] and t[4][0])
	t_setCode(m, t[6] and t[6][1] or ())
	return m

def d_Destructor(t):
	'''Destructor: '@destructor' EOL
	       Documentation?
	       EOL*
	       (INDENT
	       Code
	       DEDENT) ?
	  '@end'
	'''
	m = F.createDestructor()
	if t[2]: m.setDocumentation(t[2] and t[2][0])
	t_setCode(m, t[4] and t[4][1] or ())
	return m

def d_Condition(t):
	''' Condition: 
		( ConditionWhenMultiLine  | ConditionWhenSingleLine )*
		( ConditionWhenSingleLine
		| ConditionOtherwiseSingleLine
		| ConditionOtherwiseMultiLine 'end'
		| 'end'
		)
	'''
	res = F.select()
	for when in t[0]:
		res.addRule(when)
	r = t[1] and t_filterOut('end', t[1]) or ()
	if r: res.addRule(r[0])
	#match = F.match(t[0], t[-1])
	#res.addRule(match)
	return res

def d_ConditionWhenMultiLine(t):
	''' ConditionWhenMultiLine: 
		'when' Expression EOL+ 
			INDENT Code DEDENT
	'''
	return F.match(t[1], t_setCode(F.createBlock(), t[4]))

def d_ConditionWhenSingleLine(t):
	''' ConditionWhenSingleLine: 
		'when' Expression '->' Line EOL
	'''
	return F.match(t[1], t_setCode(F.createBlock(), t[3]))

def d_ConditionOtherwiseMultiLine(t):
	''' ConditionOtherwiseMultiLine: 
		'otherwise' EOL+ 
			INDENT Code DEDENT
	'''
	return F.match(F._ref('true'), t_setCode(F.createBlock(), t[3]))

def d_ConditionOtherwiseSingleLine(t):
	''' ConditionOtherwiseSingleLine: 
		'otherwise' '->' Line EOL?
	'''
	return F.match(F._ref('true'), t_setCode(F.createBlock(), t[2]))

def d_Select(t):
	''' Select: 'select' Expression? EOL
				INDENT (EOL|Condition)* DEDENT
	            'end'
	'''
	res = F.select()
	conditions = t_filterOut(None, t[4])
	for condition in conditions:
		for rule in condition.getRules():
			if t[1]:
				rule.setPredicate(F.compute(F._op("=="),t[1][0],rule.getPredicate()))
			res.addRule(rule)
	return res

def d_Match(t):
	''' Match: 'match' Expression EOL
				INDENT (EOL|Condition)* DEDENT
	            'end'
	'''
	conditions = t_filterOut(None, t[4])
	for condition in conditions:
		for rule in condition.getRules():
			rule.setPredicate(F.compute(F._op("=="),t[1],rule.getPredicate()))
	return conditions

# ----------------------------------------------------------------------------
# Operations
# ----------------------------------------------------------------------------

def d_Termination(t):
	'''Termination : 'return' Expression'''
	return F.returns(t[1])

def d_Iteration(t):
	'''Iteration : IterationExpression | ForIteration'''
	return t[0]

def d_IterationExpression(t):
	'''IterationExpression : Expression '::' Expression'''
	return F.iterate(t[0], t[2])

def d_ForIteration(t):
	'''ForIteration :
		'for' Arguments 'in' Expression EOL
		(INDENT Code DEDENT)?
		'end'
	'''
	expr    = t[3]
	args    = t[1]
	body    = t[5] and t[5][1] or ()
	process = F.createFunction(None, args)
	t_setCode(process, body)
	return F.iterate(expr, process)

def d_Comparison(t):
	'''Comparison : Expression ('<' | '>' | '==' | '>=' | '<=' | '<>' | '!='
	                 |'in' |'not' 'in'  | 'is' |'is' 'not') Expression
	'''
	# FIXME: Normalize operators
	# FIXME: t[1] may be a list (not in, is not)
	return F.compute(F._op(" ".join(t[1])),t[0],t[2])

def d_Computation(t):
	'''Computation: Expression ('+'|'-'|'*'|'/'|'%'|'//'|'+='|'-='|'and'|'or') Expression '''
	# FIXME: Normalize operators
	return F.compute(F._op(t[1][0]),t[0],t[2])

def d_PrefixComputation(t):
	'''PrefixComputation: ('not') Expression '''
	# FIXME: Normalize operators
	return F.compute(F._op(t[0][0]),t[1])

def d_Assignation(t):
	''' Assignation: Expression '=' Expression '''
	return F.assign(t[0], t[2])

def d_Allocation(t):
	'''Allocation: 'var' NAME (':' Type)?  ('=' Expression)?'''
	return F.allocate(F._slot(t[1],t[2] and t[2][1] or None), t[3] and t[3][1] or None)

# ----------------------------------------------------------------------------
# Expressions
# ----------------------------------------------------------------------------

def d_Expression(t):
	'''Expression : Iteration | Instanciation | Slicing | InvocationOrResolution | Assignation | Comparison |
	              PrefixComputation | Computation | Value | LP Expression RP
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
		p = t_filterOut(",", p[1:-1])
		return F.instanciate(t[1], *p)

def d_Slicing(t):
	'''Slicing: Expression LB Expression RB '''
	return F.slice(t[0], t[2])

def d_InvocationOrResolution(t):
	'''InvocationOrResolution: Expression ( Name | Value | LP (EOL* Expression EOL* ( (EOL|",") EOL* Expression EOL*)*)?  RP ) '''
	p = t[1]
	# NOTE: In some cases (and I don't get why this happens), Invocation
	# matches but Resoltuion doesn't. So we check if expression is a
	# reference (a name) and we make the invocation fail
	if len(p) == 1:
		if isinstance(p[0], interfaces.IList) and len(p[0].getValues()) == 1:
			return F.slice(t[0], p[0].getValue(0))
		if isinstance(p[0], interfaces.IReference):
			return F.resolve(p[0], t[0])
		else:
			return F.invoke(t[0], *p)
	elif len(p) == 2:
		return F.invoke(t[0])
	else:
		if p[0] == "['(']":
			 p = p[1:-1]
		p = t_filterOut(",", p)
		return F.invoke(t[0], *p)

# ----------------------------------------------------------------------------
# Closures
# ----------------------------------------------------------------------------

def d_Closure(t):
	'''Closure: LC (Arguments '|')? (Line| (Line|EOL) (INDENT Code DEDENT)? )? RC '''
	a = t[1] and t[1][0] or ()
	c = F.createClosure(a)
	t_setCode(c, t[2])
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

def d_StringSQ(t, nodes):
	'''StringSQ : "'" (STR_NOT_SQUOTE|STR_ESC)* "'" '''
	buf = nodes[0].buf
	start = nodes[0]
	end   = nodes[-1]
	return buf[start.start_loc.s+1:end.end-1]

def d_StringDQ(t, nodes):
	'''StringDQ : '"' (STR_NOT_DQUOTE|STR_ESC)* '"' '''
	buf = nodes[0].buf
	start = nodes[0]
	end   = nodes[-1]
	return buf[start.start_loc.s+1:end.end-1]

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
	'''List : LB ( (Expression (',' Expression)*)? (EOL INDENT (Expression (',' Expression)* EOL)* DEDENT )? ) RB '''
	r = t_filterOut(",", t[1])
	l = F._list(*r)
	return l

def d_Dict(t):
	'''Dict : LC ( (DictPair (',' DictPair)*)? (EOL INDENT (DictPair (',' DictPair)* EOL)* DEDENT )? ) RC '''
	p = t_filterOut(",", t[1])
	d = F._dict()
	for k,v in p:
		d.setValue(k,v)
	return d

def d_DictPair(t):
	'''DictPair : (DictKey|LP Expression RP) ':' Expression '''
	key =  t[0]
	if len(key) == 1: key = key[0]
	else: key = key[1]
	return key, t[2]

def d_DictKey(t):
	'''DictKey: "[$A-Za-z_]+[\\-$0-9A-Za-z_]*" 
	'''
	return F._string(t[0])

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
	''' EOL: "\\n"+ '''
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

def d_INDENT(t, spec):
	''' INDENT: '''
	st = _PARSER.indentStack
	if spec:
		if len(st) < 2 or not (st[-1] > st[-2]): 
			return Reject
		_PARSER.requiredIndent = st[-1]
		
def d_DEDENT(t, spec):
	''' DEDENT: '''
	st = _PARSER.indentStack
	if spec:
		if len(st) < 2 or not (st[-1] < st[-2]): 
			return Reject
		_PARSER.requiredIndent = st[-1]

def d_CHECK(t, spec):
	''' CHECK: '''
	if spec:
		if not _PARSER.indentStack: return
		if _PARSER.requiredIndent != _PARSER.indentStack[-1]:
			return Reject
	
def skip_whitespace(loc):
	indent = 0
	st = _PARSER.indentStack
	while loc.s < len(loc.buf):
		c = loc.buf[loc.s]
		if c in (' ', '\t'):
			loc.s  += 1
			indent += 1
		elif c == '\n':
			loc.line += 1
			_PARSER.isNewline = True
			return
		else:
			break
	if _PARSER.isNewline:
		_PARSER.isNewline = False
		if not st or st[-1] != indent:
			st.append(indent)
		_PARSER.previousLine = loc.s

# ----------------------------------------------------------------------------
#
# PARSER OPERATIONS
#
# ----------------------------------------------------------------------------

def disambiguate( nodes ):
	# FIXME: This may not be the best way...
	return nodes[0]

# ----------------------------------------------------------------------------
#
# EXTERNAL API
#
# ----------------------------------------------------------------------------

#_PARSER = Parser(make_grammar_file=0)
_PARSER = DParser()

def parse( text, verbose=True ):
	_PARSER.indentStack = []
	_PARSER.isNewline   = True
	_PARSER.requiredIndent = 0
	_PARSER.previousLine   = 0
	res = _PARSER.parse(text,initial_skip_space_fn=skip_whitespace,ambiguity_fn=disambiguate, print_debug_info=(verbose and 1 or 0))
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
		# And ensure that there is an EOL
		if text[-1] != "\n":
			self.warn("No trailing EOL in given code")
			text += "\n"
		# We try to parse the file
		#try:
		if True:
			name = self.pathToModuleName(name)
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
