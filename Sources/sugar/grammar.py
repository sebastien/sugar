#!/usr/bin/env python
# Encoding: ISO-8859-1
# vim: ts=4 textwidth=79
# -----------------------------------------------------------------------------
# Project           :   Sugar                         <http://www.ivy.fr/sugar>
# Author            :   Sebastien Pierre                     <sebastien@ivy.fr>
# License           :   Lesser GNU Public License
# -----------------------------------------------------------------------------
# Creation date     :   2005-08-10
# Last mod.         :   2016-05-05
# -----------------------------------------------------------------------------

import os,sys
from dparser import Parser as DParser
from dparser import Reject
from lambdafactory import modelbase
from lambdafactory import interfaces

__doc__ = """
This module implements a Sugar syntax driver for the LambdaFactory program model
library. This module uses the fantastic D parser Python library.
"""

# We instanciate LambdaFactory default factory, which will be used in the
# grammar production rules to create model elements.

F = modelbase.Factory()

SOURCE_PATH = None

KEYWORDS = "and or not is var new in for return if else break continue raise".split()

OPERATORS_PRIORITY_0 = ["or"]
OPERATORS_PRIORITY_1 = ["and"]
OPERATORS_PRIORITY_2 = "not > >= < <= != is in ==".split() ; OPERATORS_PRIORITY_2.append("is not")
OPERATORS_PRIORITY_3 = "<< >> || &&".split()
OPERATORS_PRIORITY_4 = "+ -".split()
OPERATORS_PRIORITY_5 = "/ * % //".split()
OPERATORS_PRIORITY_6 = "+= -=".split()
OPERATOR_NORM = {
	"||":"|",
	"&&":"&",
}

def getPriority( op ):
	"""Returns the priority for the given operator"""
	if not( type(op) in (str, unicode)) and isinstance(op, interfaces.IOperator):
		op = op.getReferenceName()
	if op in OPERATORS_PRIORITY_0: return 0
	if op in OPERATORS_PRIORITY_1: return 1
	if op in OPERATORS_PRIORITY_2: return 2
	if op in OPERATORS_PRIORITY_3: return 3
	if op in OPERATORS_PRIORITY_4: return 4
	if op in OPERATORS_PRIORITY_5: return 5
	if op in OPERATORS_PRIORITY_6: return 6
	raise Exception("Unknown operator: %s" % (op))

# ----------------------------------------------------------------------------
# Common utilities
# ----------------------------------------------------------------------------

def t_flatten( l, aggregate=None ):
	if aggregate is None: aggregate = []
	if type(l) in (tuple,list):
		for e in l:
			t_flatten(e, aggregate)
	else:
		aggregate.append(l)
	return aggregate

def t_filterOut( c, l ):
	return filter(lambda e:e!=None and e!=c, l)

def t_setCode( process, code, context=None ):
	for i,o in enumerate(code):
		if isinstance(o, interfaces.ISelection) and o.hasAnnotation("if-expression"):
			# We only allow if-expressions within an expression
			o.removeAnnotation("if-expression")
			process.addOperation(o)
		elif isinstance(o, interfaces.IOperation):
			process.addOperation(o)
		elif context \
		and  isinstance(o, interfaces.IAssignable) \
		and  isinstance(o, interfaces.IReferencable):
			assert o.getName(), str(o)
			context.setSlot(o.getName(), o)
		elif type(o) in (list, tuple):
			t_setCode(process, o, context)
		elif isinstance(o, interfaces.IValue):
			process.addOperation(F.evaluate(o))
		elif o and (not isinstance(o, interfaces.IComment)):
			sys.stderr.write("Unsupported a code value: %s\n" % (o))
	return process

def p_ensureReturns( process ):
	if not isinstance(process, interfaces.IProcess) or not process.operations: return process
	last_operation = process.operations[-1]
	ret            = None
	if last_operation:
		if isinstance(last_operation, interfaces.INOP):
			return process
		elif isinstance(last_operation, interfaces.IIteration):
			return process
		elif isinstance(last_operation, interfaces.ITermination):
			return process
		elif isinstance(last_operation, interfaces.ISelection):
			return process
		elif isinstance(last_operation, interfaces.IInterception):
			return process
		elif isinstance(last_operation, interfaces.IInterruption):
			return process
		elif isinstance(last_operation, interfaces.IEmbed):
			return process
		elif isinstance(last_operation, interfaces.IAllocation):
			return process
		elif isinstance(last_operation, interfaces.IAssignment):
			return process
		elif isinstance(last_operation, interfaces.IRepetition) or isinstance(last_operation, interfaces.IIteration):
			# We don't do anything with a repetition, but we annotate them as # last
			last_operation.addAnnotation("last")
			return process
		elif isinstance(last_operation, interfaces.IOperation):
			process.removeOperationAt(-1)
			ret = F.returns(last_operation)
	if ret:
		ret.addAnnotation("implicit")
		process.addOperation(ret)
	return process

def p_cullImplicitReturns( process ):
	"""Removes implicit returns from the given process."""
	if not isinstance(process, interfaces.IProcess): return process
	last_operation = process.operations[-1]
	if last_operation and isinstance(last_operation, interfaces.ITermination) and last_operation.hasAnnotation("implicit"):
		process.removeOperationAt(-1)
		if not last_operation.hasAnnotation("implicit-remove"):
			process.addOperation(last_operation.getReturnedEvaluable().copy())
	return process

def t_split( array, element ):
	"""Splits the given list using the given element."""
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

def t_setLocation(e, nodes):
	"""Sets the source location for the given element."""
	if type(nodes) in (list, tuple):
		so = nodes[0].start_loc.s
		eo = nodes[-1].end
	else:
		so = nodes.start_loc.s
		eo = nodes.end
	e.setOffset(so, eo)
	e.setSourcePath(SOURCE_PATH)
	return e

# ----------------------------------------------------------------------------
# STATEMENTS
# ----------------------------------------------------------------------------

def d_Module(t, nodes):
	'''Module:
		(Comment | EOL) *
		ModuleAnnotations?
		Documentation?
		ImportOperations?
		ModuleDeclarations?
		Code
	'''
	# FIXME: Add a notion of Module = Slots + Process
	annotations = t[1] and t[1][0] or ()
	def get_annotation(name,annotations=annotations):
		for a in annotations:
			if a.getName() == name: return a.getContent()
		return None
	# FIXME: Get module if module already exists
	if get_annotation("module"):
		m = F.createModule(get_annotation("module"))
	else:
		m = F.createModule(F.CurrentModule)
	if get_annotation("as"):
		m.setAbstract(True)
	map(m.addAnnotation, annotations)
	if t[2]: m.setDocumentation(t[2] and t[2][0])
	#FIXME: bind the imported module to the slot
	code = []
	import_ops = t_flatten(t[3])
	for import_op in import_ops:
		m.addImportOperation(import_op)
	code.extend(t[4])
	code.extend(t[5])
	if code:
		f = F.createFunction(F.ModuleInit, ())
		# FIXME: Rename to addStatements
		t_setCode(f,code,m)
		m.setSlot(F.ModuleInit, f, True)
	return t_setLocation(m, nodes)

def d_Code(t, spec, nodes):
	'''Code : (EOL | Embed | Specific | Rewrite | (CHECK (Declaration|Condition|With|Statement|Comment)))* '''
	# FIXME: Declarations should not go into code
	return t_filterOut(None, t[0])

def d_Embed(t, nodes):
	'''Embed:
          '@embed' NAME EOL
	      (
	      	  '|' "[^\\n]*" EOL
	      )+
		  '@end'
	'''

	language = t[1]
	code = []
	buf = nodes[0].buf
	indent = _PARSER.requiredIndent
	code = buf[nodes[3].start_loc.s:nodes[3].end]
	lines = []
	for line in code.split("\n"):
		lines.append(line[line.find("|")+1:])
	return t_setLocation(F.embed(language, "\n".join(lines)), nodes)

def d_Rewrite(t, nodes):
	'''Rewrite:
		'@rewrite' '(' NAME ')' (
			":[^\\n]*"
		|	EOL
			( '|' "[^\\n]*" EOL )+
			'@end'
		)
	'''
	target = t[2]
	template = t[-1]
	# We have a multiple-line template
	if template[0] is None:
		buf = nodes[0].buf
		code = buf[nodes[4].start_loc.s:nodes[4].end]
		lines = []
		for line in code.split("\n")[1:-1]:
			lines.append(line[line.find("|")+1:])
		template = "\n".join(lines)
	# Or we have a single line
	else:
		template = template[0][1:]
	return t_setLocation(F.embedTemplate(target, template), nodes)

def d_SpecificTarget(t):
	'''SpecificTarget: "[\+\-]"? NAME'''
	if t[0]: target=t[0][0] + t[1]
	else: target=t="+" + t[1]
	return target

def d_Specific(t, nodes):
	'''Specific:
	      '@specific' SpecificTarget+ EOL
	      Documentation?
	      (
	         (INDENT
	         Code
	         DEDENT)
	      |'@specific'SpecificTarget+ EOL Documentation?
	      )+
	      '@end'
	'''
	lists =  t_flatten(t)
	# We remove the trailing end and filter out unncessary things
	lists = tuple((x for x in lists if x))[:-1]
	def fold_specifics(l):
		"""Returns a list of (TARGETS, CODE) corresponding to the specifics."""
		targets = []
		code    = []
		if l[0] == "@specific": l = l[1:]
		while l and type(l[0]) == str:
			targets.append(l[0])
			l = l[1:]
		while l and l[0] != "@specific":
			code.append(l[0])
			l = l[1:]
		if l:
			res = [(targets, code)]
			res.extend(fold_specifics(l))
			return res
		else:
			return [(targets, code)]
	def match_targets(targets):
		for t in targets:
			if t[0] == "+" and not _PARSER.options.hasTarget(t[1:]): return False
			if t[0] == "-" and _PARSER.options.hasTarget(t[1:]): return False
		return True
	result_code = []
	for targets, code in fold_specifics(lists):
		if match_targets(targets):
			result_code.extend(code)
	return result_code

# FIXME: Exchange LINE and STATEMENT
def d_Line(t):
	'''Line : (Function|Assignment|Select|Allocation|Interruption|Expression) ( ';' Line )* '''
	r = [t[0][0]]
	for e in t[1]:
		if e != ";": r.extend(e)
	return r

def d_Comment(t, nodes):
	'''Comment : '#' "[^\\n]*" EOL'''
	return t_setLocation(F.comment(t[1]), nodes)

def d_Documentation(t, nodes):
	'''Documentation : ('|' "[^\\n]*" EOL)+'''
	d = t[0]
	d = t_filterOut('|',d)
	return t_setLocation(F.doc("\n".join(d)), nodes)

def d_Statement(t):
	'''Statement : Line EOL '''
	return t[0]

def d_Declaration(t):
	'''Declaration : (Main|AbstractFunction|Interface|Function|Class|Exception) EOL | Shared'''
	if type(t[0]) in (tuple,list): return t[0][0]
	else: return t[0]

# ----------------------------------------------------------------------------
# Declarations
# ----------------------------------------------------------------------------

def d_Main(t, nodes):
	'''Main: '@main' NAME? EOL
		  (INDENT
	      Code
	      DEDENT)?
	   '@end'
	'''
	args = t[1] or ["args"]
	args = map(F._param, args)
	f = F.createFunction(F.MainFunction , args)
	t_setCode(f, t[3] and t[3][1] or ())
	return t_setLocation(f, nodes)

def d_Function(t, nodes):
	'''Function: '@function' NAME (':' Type)? Arguments? EOL
		  Documentation?
		  (INDENT
	      Code
	      DEDENT
	      )?
	   '@end'
	'''
	name = t[1]
	args = t[3] and t[3][0] or ()
	f = F.createFunction(name, args)
	if t[5]: f.setDocumentation(t[5] and t[5][0])
	t_setCode(f, t[6] and t[6][1] or ())
	return t_setLocation(f, nodes)

def d_AbstractFunction(t, nodes):
	'''AbstractFunction:
		'@abstract' '@function' NAME (':' Type)?  Arguments? EOL
		Documentation?
	'''
	name = t[2]
	args = t[4] and t[4][0] or ()
	f = F.createFunction(name, args)
	if t[6]: f.setDocumentation(t[5] and t[6][0])
	f.setAbstract(True)
	return t_setLocation(f, nodes)

def d_Exception(t, nodes):
	'''Exception:
		'@exception' NAME (':' Expression)? EOL
		Documentation?
		(INDENT
			Attribute
			Method
			Constructor
			Comment
			EOL
		DEDENT)?
		'@end'
	'''
		# TODO: Parents support
	parents = []
	parents.extend(t[2])
	parents = t_filterOut(":", parents)
	parents = t_filterOut(",", parents)
	# FIXME: Doesn't work
	# if not parents: parents.append(F.resolve(F._ref("Exception")))
	c = t_setLocation(F.createClass(t[1] , parents), nodes[1])
	if t[4]: c.setDocumentation(t[4] and t[4][0])
	t_setCode(None, t[5], c)
	return t_setLocation(c, nodes)
	return c


def d_Class(t, nodes):
	# FIXME: Change Name to Reference
	'''Class: '@abstract'? '@class' NAME (':' TypeSymbol (',' TypeSymbol)* )? EOL
		  Annotation*
		  Documentation?
		  (INDENT
	      (   ClassAttribute
	      |   ClassMethod
	      |   AbstractClassMethod
	      |   Attribute
		  |   Accessor
		  |   Mutator
	      |   Method
	      |   AbstractMethod
	      |   Constructor
	      |   Destructor
	      |   MethodGroup
	      |   Comment
	      |   EOL
	      )*
	      DEDENT) ?
	  '@end'
	'''
	# TODO: Parents support
	is_abstract = t[0]
	parents = []
	parents.extend(t[3])
	parents = t_filterOut(":", parents)
	parents = t_filterOut(",", parents)
	parents = map(F._ref, parents)
	c = F.createClass(t[2] , parents)
	if t[5]: c.addAnnotation(t[5])
	if t[6]: c.setDocumentation(t[6] and t[6][0])
	t_setCode(None, t[7], c)
	# FIXME
	if is_abstract: c.setAbstract(True)
	return t_setLocation(c, nodes)

def d_Interface(t, nodes):
	'''Interface: '@protocol' NAME (':' Expression (',' Expression)* )?  EOL
		Documentation?
		(INDENT
		  (   ClassAttribute
	      |   Attribute
	      |   AbstractMethod
	      |   AbstractMethodGroup
	      |   AbstractClassMethod
	      |   Comment
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
	f = F.createInterface(t[1] , parents)
	if t[4]: f.setDocumentation(t[4] and t[4][0])
	t_setCode(None, t[5], f)
	return t_setLocation(f, nodes)

def d_Annotation(t):
	'''Annotation: (WhenAnnotation|PreAnnotation|PostAnnotation|AsAnnotation|Decorator)'''
	return t[0][0]

def d_FunctionAnnotation(t):
	'''FunctionAnnotation: (WhenAnnotation|PreAnnotation|PostAnnotation|AsAnnotation)'''
	return t[0][0]

def d_ModuleAnnotations(t):
	'''ModuleAnnotations:
		( ModuleAnnotation
		| VersionAnnotation
		| RequiresAnnotation
		| TargetAnnotation
		| AsAnnotation
		)+
	'''
	return t[0]

def d_Decorator(t, nodes):
	'''Decorator: '@[' "[^\]]+" ']' EOL'''
	annotation = t[1].strip()
	i = annotation.find(" ")
	if i == -1:
		name, params = annotation, ""
	else:
		name, params = annotation.split(" ",1)
	return t_setLocation(F.annotation(name, params), nodes)

def d_ModuleAnnotation(t, nodes):
	'''ModuleAnnotation: '@module' (NAME ('.' NAME)*) EOL'''
	return t_setLocation(F.annotation('module', "".join(t_flatten(t[1]))), nodes)

def d_VersionAnnotation(t, nodes):
	'''VersionAnnotation: '@version' VERSION EOL'''
	return t_setLocation(F.annotation('version', t[1]), nodes)

def d_VERSION(t):
	'''VERSION:
		"[0-9]+(.[0-9]+)?(.[0-9]+)?[a-zA-Z_]*"
		(
			'(' "[0-9][0-9]?\-[A-Z][a-z][a-z]-[0-9][0-9]([0-9][0-9])?" ')'
		)?
	'''
	return t[0]

def d_RequiresAnnotation(t, nodes):
	'''RequiresAnnotation: '@requires' DEPENDENCY (',' DEPENDENCY)* EOL'''
	return t_setLocation(F.annotation('requires', t[1:-1]), nodes)

def d_DEPENDENCY(t):
	'''DEPENDENCY: NAME ('(' VERSION ')')? '''
	return t

def d_TargetAnnotation(t, nodes):
	'''TargetAnnotation: '@target' NAME+  EOL'''
	return t_setLocation(F.annotation('target', t[1:-1]), nodes)

def d_WhenAnnotation(t, nodes):
	'''WhenAnnotation: '@when' Expression EOL'''
	return t_setLocation(F.annotation('when', t[1]), nodes)

def d_PreAnnotation(t, nodes):
	'''PreAnnotation: '@pre' Expression EOL'''
	return t_setLocation(F.annotation('pre', t[1]), nodes)

def d_PostAnnotation(t, nodes):
	'''PostAnnotation: '@post' Expression EOL'''
	return t_setLocation(F.annotation('post', t[1]), nodes)

def d_AsAnnotation(t, nodes):
	'''AsAnnotation: '@as' ("[a-zA-Z0-9_\-]+")+ EOL'''
	return t_setLocation(F.annotation('as', t[1]), nodes)

def d_ImportOperations(t):
	'''ImportOperations: (ImportOperation)* '''
	return t[0]

def d_TypeSymbol(t):
	'''
	TypeSymbol: ('*'|NAME ('.' NAME)*)
	'''
	return "".join(t_flatten(t))

def d_ImportSymbol(t, nodes):
	''' ImportSymbol:
		'@import' NAME 'from' TypeSymbol ('as' NAME)? EOL
	'''
	imported_symbol = t[1]
	import_origin   = t[3]
	import_alias    = t[4]
	if import_alias: import_alias = import_alias[-1]
	return t_setLocation(F.importSymbol(imported_symbol, import_origin, import_alias), nodes)

def d_ImportSymbols(t, nodes):
	''' ImportSymbols:
		'@import' (NAME (',' NAME)*) 'from' TypeSymbol EOL
	'''
	imported_symbols = t_filterOut(",", t_flatten(t[1]))
	import_origin    = t[-2]
	if import_origin and type(import_origin)==list: import_origin = import_origin[-1]
	return t_setLocation(F.importSymbols(imported_symbols, import_origin), nodes)

def d_ImportAllSymbols(t, nodes):
	''' ImportAllSymbols:
		'@import' '*' 'from' TypeSymbol EOL
	'''
	import_origin    = t[3]
	return t_setLocation(F.importSymbols("*", import_origin), nodes)

def d_ImportModule(t, nodes):
	'''ImportModule:
		'@import' TypeSymbol ('as' NAME)? EOL
	'''
	module_name = t[1]
	module_alias = t[2] and t[2][-1]
	return t_setLocation(F.importModule(module_name, module_alias), nodes)

def d_ImportModules(t, nodes):
	'''ImportModules:
		'@import' TypeSymbol (',' TypeSymbol)* EOL
	'''
	modules = t_filterOut(",",t_flatten(t[1:-1]))
	return t_setLocation(F.importModules(modules), nodes)

def d_ImportOperation(t):
	'''ImportOperation:
		ImportSymbols
	|	ImportSymbol
	|	ImportModule
	|	ImportAllSymbols
	|	ImportModules
	'''
	return t

def d_ModuleDeclarations(t):
	'''ModuleDeclarations: Shared+'''
	return t[0]

def d_Shared(t, nodes):
	'''Shared:
	    '@shared' NAME (':' Type)? ('=' Expression)?  EOL
	    Annotation*
	    Documentation?
	'''
	s_name  = t[1]
	s_type  = t[2] and t[2][1] or None
	s_value = t[3] and t[3][1] or None
	s = F._moduleattr(s_name, s_type, s_value)
	for ann in t[-2]: s.addAnnotation(ann)
	if t[-1]: s.setDocumentation(t[-1] and t[-1][0])
	return t_setLocation(s, nodes)

def d_Attribute(t, nodes):
	'''Attribute:
		'@property' NAME (':' Type)? ('=' (Value | Expression))?  EOL
		Documentation ?
	 '''
	a = F._attr(t[1], t[2] and t[2][1] or None, t[3] and t[3][1] or None)
	if t[-1]: a.setDocumentation(t[-1] and t[-1][0])
	return t_setLocation(a, nodes)

def d_ClassAttribute(t, nodes):
	'''ClassAttribute:
		'@shared' NAME (':' Type)?  ('=' Expression)? EOL
		Annotation*
		Documentation ?
	'''
	a =  F._classattr(t[1], t[2] and t[2][1] or None, t[3] and t[3][1] or None)
	for ann in t[-2]: a.addAnnotation(ann)
	if t[-1]: a.setDocumentation(t[-1] and t[-1][0])
	return t_setLocation(a, nodes)

def d_MethodGroup(t):
	'''MethodGroup: '@group' "[a-zA-Z0-9_\-]+" EOL
		Annotation*
		Documentation?
	    EOL*
		(Accessor | Mutator | ClassMethod | Method | EOL)*
	   '@end'
	'''
	annotation = F.annotation('as', t[1])
	methods    = t_filterOut('', t[6])
	for m in methods:
		m.addAnnotation(annotation)
		for a in t[3]: m.addAnnotation(a)
	return methods

def d_AbstractMethodGroup(t, nodes):
	'''AbstractMethodGroup: '@group' "[a-zA-Z0-9_\-]+" EOL
		Annotation*
		Documentation?
	    EOL*
		(AbstractClassMethod | AbstractMethod | Comment | EOL)*
	   '@end'
	'''
	return t_setLocation(d_MethodGroup(t), nodes)

def d_Method(t, nodes):
	'''Method: '@method' NAME (':' Type)? Arguments? EOL
	       FunctionAnnotation*
	       Documentation?
	       EOL*
	       (INDENT
	       Code
	       DEDENT) ?
	  '@end'
	'''
	m = F.createMethod(t[1], t[3] and t[3][0] or ())
	m_type = t[2] and t[2][1] or None
	if m_type: m.setReturnTypeDescription(m_type)
	for ann in t[5]:
		m.addAnnotation(ann)
	if t[6]: m.setDocumentation(t[6] and t[6][0])
	t_setCode(m, t[8] and t[8][1] or ())
	return t_setLocation(m, nodes)

def d_AbstractMethod(t, nodes):
	'''AbstractMethod:
		'@abstract' '@method' NAME(':'Type)? Arguments?  EOL
		FunctionAnnotation*
		Documentation?
	'''
	m = F.createMethod(t[2], t[4] and t[4][0] or ())
	m.setAbstract(True)
	for ann in t[6]:
		m.addAnnotation(ann)
	if t[7]: m.setDocumentation(t[7] and t[7][0])
	return t_setLocation(m, nodes)

def d_Accessor(t, nodes):
	'''Accessor:
		'@accessor' NAME(':'Type)? EOL
		   Documentation?
		   EOL*
		   (INDENT
	       Code
	       DEDENT)?
	  '@end'
	'''
	m = F.createAccessor(t[1],())
	m_type = t[2] and t[2][1] or None
	if m_type: m.setReturnTypeDescription(m_type)
	if t[4]: m.setDocumentation(t[4] and t[4][0])
	t_setCode(m, t[6] and t[6][1] or ())
	return t_setLocation(m, nodes)

def d_Mutator(t, nodes):
	'''Mutator:
		'@mutator' NAME(':'Type)? Arguments? EOL
		   Documentation?
		   EOL*
		   (INDENT
	       Code
	       DEDENT)?
	  '@end'
	'''
	m = F.createMutator(t[1], t[3] and t[3][0] or ())
	if t[6]: m.setDocumentation(t[6] and t[6][0])
	t_setCode(m, t[8] and t[8][1] or ())
	return t_setLocation(m, nodes)

def d_ClassMethod(t, nodes):
	'''ClassMethod:
		'@operation' NAME (':'Type)?  Arguments? EOL
		   FunctionAnnotation*
		   Documentation?
		   EOL*
		   (INDENT
	       Code
	       DEDENT)?
	  '@end'
	'''
	m = F.createClassMethod(t[1], t[3] and t[3][0] or ())
	for ann in t[5]:
		m.addAnnotation(ann)
	if t[5]: m.setDocumentation(t[6] and t[6][0])
	t_setCode(m, t[8] and t[8][1] or ())
	return t_setLocation(m, nodes)

def d_AbstractClassMethod(t, nodes):
	'''AbstractClassMethod:  '@abstract' '@operation' NAME (':'Type)?  Arguments? EOL
		   FunctionAnnotation*
		   Documentation?
	'''
	m = F.createClassMethod(t[2], t[4] and t[4][0] or ())
	for ann in t[6]:
		m.addAnnotation(ann)
	if t[7]: m.setDocumentation(t[7] and t[7][0])
	m.setAbstract(True)
	return t_setLocation(m, nodes)

def d_Constructor(t, nodes):
	'''Constructor: '@constructor'  Arguments? EOL
	       (PreAnnotation)*
	       (PostAnnotation)*
	       Documentation?
	       EOL*
	       (INDENT
	       Code
	       DEDENT)?
	  '@end'
	'''
	m = F.createConstructor(t[1] and t[1][0])
	for ann in t[3]: m.addAnnotation(ann)
	for ann in t[4]: m.addAnnotation(ann)
	if t[5]: m.setDocumentation(t[5] and t[5][0])
	t_setCode(m, t[7] and t[7][1] or ())
	return t_setLocation(m, nodes)

def d_Destructor(t, nodes):
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
	return t_setLocation(m, nodes)

def d_With(t, nodes):
	''' With: 'with' Expression EOL+
			(INDENT Code DEDENT) ?
			'end'
	'''
	return t_setLocation(F.withBlock(t[1], t_setCode(F.createBlock(), t[3])), nodes)

def d_Condition(t, nodes):
	''' Condition:
		( ConditionWhenSingleLine | ConditionWhenMultiLine )*
		( ConditionWhenSingleLine
		| ConditionOtherwiseSingleLine
		| ConditionOtherwiseMultiLine 'end' EOL
		| 'end' EOL
		)
	'''
	res = t_setLocation(F.select(), nodes)
	for when in t[0]:
		res.addRule(when)
	r = t[1] and t_filterOut('end', t[1]) or ()
	if r: res.addRule(r[0])
	#match = F.match(t[0], t[-1])
	#res.addRule(match)
	return res

def d_ConditionWhenMultiLine(t, nodes):
	''' ConditionWhenMultiLine:
		"(el)?if" Expression EOL+
			INDENT Code DEDENT
	'''
	return t_setLocation(F.matchProcess(t[1], t_setCode(F.createBlock(), t[4])), nodes)


def d_ConditionWhenSingleLine(t, nodes):
	''' ConditionWhenSingleLine:
		'if' Expression '->' Line EOL
	'''
	return t_setLocation(F.matchProcess(t[1], t_setCode(F.createBlock(), t[3])), nodes)

def d_ConditionOtherwiseMultiLine(t, nodes):
	''' ConditionOtherwiseMultiLine:
		'else' EOL+
			INDENT Code DEDENT
	'''
	return t_setLocation(F.matchProcess(F._ref('True'), t_setCode(F.createBlock(), t[3])), nodes)

def d_ConditionOtherwiseSingleLine(t, nodes):
	''' ConditionOtherwiseSingleLine:
		'else' '->' Line EOL?
	'''
	return t_setLocation(F.matchProcess(F._ref('True'), t_setCode(F.createBlock(), t[2])), nodes)

def d_Select(t, nodes):
	''' Select: 'select' Expression? EOL
				INDENT (EOL|Condition)* DEDENT
	            'end'
	'''
	res = t_setLocation(F.select(), nodes)
	conditions = t_filterOut(None, t[4])
	for condition in conditions:
		for rule in condition.getRules():
			if t[1]:
				rule.setPredicate(F.compute(F._op("=="),t[1][0],rule.getPredicate()))
			res.addRule(rule)
	return res

def d_Match(t):
	''' Match: 'match' Expression  EOL
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

def d_Interruption(t):
	'''Interruption: Termination|Breaking|Continue|Pass|Except'''
	return t[0]

def d_Termination(t):
	'''Termination : 'return' Expression'''
	return F.returns(t[1])

def d_Breaking(t):
	'''Breaking : 'break' '''
	return F.breaks()

def d_Continue(t):
	'''Continue : 'continue' '''
	return F.continues()

def d_Pass(t):
	'''Pass : 'pass' '''
	return F.nop()

def d_Except(t):
	'''Except: 'raise' Expression '''
	return F.exception(t[1])

def d_Iteration(t):
	'''Iteration : FilterExpression|MapExpression|IterationExpression|ForIteration|WhileIteration'''
	return t[0]

def d_IterationExpression(t):
	'''IterationExpression : Expression '::' Expression'''
	return F.iterate(t[0], p_cullImplicitReturns(t[2]))

def d_MapExpression(t):
	'''MapExpression : Expression '::=' Expression'''
	return F.map(t[0], t[2])

def d_FilterExpression(t):
	'''FilterExpression : Expression '::?' Expression ('=' Expression)?'''
	return F.filter(t[0], t[2], t[3][1] if t[3] else None)

# FIXME: This should not be argumnets, but the same thing as the l-value for an
# assignment
def d_ForIteration(t):
	'''ForIteration :
		'for' Arguments 'in' Expression EOL
		(INDENT Code DEDENT)?
		'end'
	'''
	expr    = t[3]
	args    = t[1]
	body    = t[5] and t[5][1] or ()
	process = F.createClosure(args)
	process.addAnnotation(F.annotation("iteration", True))
	t_setCode(process, body)
	return F.iterate(expr, process)

def d_WhileIteration(t):
	'''WhileIteration :
		'while' Expression EOL
		(INDENT Code DEDENT)?
		'end'
	'''
	cond    = t[1]
	body    = t[3] and t[3][1] or ()
	process = F.createBlock()
	process.addAnnotation(F.annotation("iteration", True))
	t_setCode(process, body)
	return F.repeat(cond, process)


def d_Computation(t):
	'''Computation:
		('not' Expression)
	|	(
			Expression ( ( ";\s*\n+\t*" )?
				(
					'+'|'-'|'*'|'/'|'%'|'//'|'and '|'or '
					|'<<' | '>>' | '&&' | '||'
					|'<' | '>' | '==' | '>=' | '<=' | '<>' | '!=' | '.?'
					|'in '  | 'not ' 'in '  | 'is ' |'is not '
				)
				Expression
			)+
		)
	'''
	# FIXME: Normalize operators
	if t[0][0] == 'not':
		return F.compute(F._op('not', 9999), t[0][1])
	else:
		t       = t[0]
		t       = filter(lambda x:type(x) != str or x[0] != ";", t)
		result  = None
		left    = t[0]
		op      = None
		right   = None
		# we iterate on the right operations
		for i in range(len(t) / 2):
			op    = t[i*2+1]
			if type(op) not in (str, unicode):
				op = " ".join(op)
			op = op.strip()
			right = t[i*2+2]
			# If the priority of the current operator is superior to the
			# priority of the previous expresion we reshape the computation from
			#     (A op B) op C
			# into
			#      A op (B op C)
			nop = OPERATOR_NORM.get(op) or op
			if op == ".?":
				result = F.conditionalResolution( left, right )
			elif isinstance(left, interfaces.IComputation) and \
			getPriority(op) > left.getOperator().getPriority():
				left.setRightOperand(F.compute(F._op(nop, getPriority(op)), left.getRightOperand().detach(), right))
				result = left
			else:
				result = F.compute(F._op(nop, getPriority(op)), left, right)
				left   = result
		return result

def d_PrefixComputation(t):
	'''PrefixComputation: ('not') Expression '''
	# FIXME: Normalize operators
	return F.compute(F._op(t[0][0]),t[1])

# FIXME: Rename Assignment ?
def d_Assignment(t, nodes):
	''' Assignment: Expression ('='|'-='|'+='|'?=') Expression '''
	op = t[1][0]
	if op == "=":
		return F.assign(t[0], t[2])
	elif op == "?=":
		# In this case: A ?= B is the equivalent of
		# if not (A) -> A = B
		predicate  = F.compute(F._op('is'), t[0], F._ref("Undefined"))
		assignment = F.assign(t[0].copy(),t[2])
		match      = F.matchExpression(predicate, assignment)
		res        = F.select()
		res.addRule(match)
		return res
	else:
		op = op[0]
		# FIXME: We should clone the expressions here
		c  =  F.compute(F._op(op, getPriority(op)), t[0], t[2])
		return F.assign(t[0].copy().detach(),c)

def d_Allocation(t):
	'''Allocation: AllocationList|AllocationMultiple'''
	return t[0]

def d_AllocationList(t):
	'''AllocationList: 'var' AllocationSingle (',' AllocationSingle)*'''
	head = t[1]
	tail = [t[2][_ * 2 + 1] for _ in range(len(t[2])/2)]
	return [head] + tail if tail else head

def d_AllocationSingle(t):
	'''AllocationSingle: NAME (':' Type)?  ('=' Expression)?'''
	return F.allocate(F._slot(t[0],t[1] and t[1][1] or None), t[2] and t[2][1] or None)

def d_AllocationMultiple(t):
	'''AllocationMultiple: 'var'
		NAME (':' Type)?
		(',' (NAME (':' Type)?) )*
		('|' (NAME (':' Type)?) )?
	  '=' Expression'''
	# This first bit is to extract our heads and tails from the parsed data
	d = t[:t.index("=")]
	expression   = t[t.index("=")+1]
	heads = [d[1]]
	heads.extend(d[2])
	heads.extend(d[3])
	heads.extend(d[4])
	heads = "".join(heads).split(",")
	tail = heads[-1].split("|")
	if len(tail) == 2:
		heads[-1] = tail[0]
		tail = tail[1]
	else:
		tail = None
	code = []
	# NOTE: The grammar rule we wrote may override AllocationSingle in many
	# situations, so we've got to take it into account
	if len(heads) == 1 and not tail:
		var = heads[0]
		var = var.split(":") ; vartype = None
		if len(var) == 1:var = var[0]
		else:var, vartype = var
		return F.allocate(F._slot(var, vartype), expression)
	# Here we're in the situation where we have a multiple allocation with
	# decomposition. The decomposition has many heads and maybe a tail. We'll
	# do a trick and get the tail or last head, and use the last variable
	# as a temporary slot.
	# FIXME: This does not preserve consistent typing
	last_var = (tail or heads[-1]).split(":", 1)
	code.append(F.allocate(F._slot(last_var[0], None), expression.copy()))
	for i, var in enumerate(heads):
		var    = var.split(":", 1) ; var_type = None
		if len(var) == 2: var, var_type = var
		else: var=var[0]
		access = F.access(F.resolve(F._ref(last_var[0])), F._number(i))
		if var == last_var[0]:
			code.append(F.assign(F._ref(var), access))
		else:
			code.append(F.allocate(F._slot(var, var_type), access))
	# And maybe a tail too
	if tail:
		var = tail.split(":") ; vartype = None
		if len(var) == 2: var, var_type = var
		else: var=var[0]
		code.append(F.assign(F._ref(var),F.slice(F.resolve(F._ref(var)), F._number(len(heads)))))
	return code

def d_Interception(t):
	'''Interception:
	   'try' EOL
	        INDENT Code DEDENT
	    ('catch' NAME EOL
	        INDENT Code DEDENT
	    )?
	    ('finally' EOL
	        INDENT Code DEDENT
	    )?
	    'end'
	'''
	try_catch   = t[5]
	try_finally = t[6]
	try_code = F.createBlock()
	t_setCode(try_code, t[3])
	if try_catch:
		arg        = F._param(try_catch[1])
		closure    = F.createClosure([arg])
		t_setCode(closure, try_catch[4])
		try_catch  = closure
	if try_finally:
		try_finally = F.createBlock()
		t_setCode(try_finally, t[6][3])
	return F.intercept(try_code, try_catch, try_finally)

# ----------------------------------------------------------------------------
# EXPRESSIONS
# ----------------------------------------------------------------------------

def d_Expression(t):
	'''Expression : Interception | Iteration | Instanciation | Slicing |
	   InvocationOrResolution |
	   ConditionExpression |
	   Assignment |
	   Computation | Value | LP Expression RP
	'''
	if len(t) == 1:
		return t[0]
	else:
		# This is a bit dirty, but we need to fix the computation priority
		# here (I did not manage to do it in a cleaner way)
		if isinstance(t[1], interfaces.IComputation):
			t[1].getOperator().setPriority(interfaces.Constants.PARENS_PRIORITY)
		return t[1]

# NOTE: This is not working, so I removed it
def d_ConditionExpression2(t):
	''' ConditionExpression2:
		Expression '?' Expression
		('|' Expression '?' Expression) *
		('|' (Expression) +) ?
	'''
	# NOTE: Assignment can be an expression too!
	res = F.select()
	m   = F.matchExpression(t[0], t[2])
	res.addRule(m)
	rules = t[3]
	while rules:
		predicate, _, expression = rules[1:4]
		res.addRule(F.matchExpression(predicate, expression))
		rules = rules[4:]
	if t[4]:
		e = F.matchExpression(F._ref("True"), t[4][1])
		e.addAnnotation("else")
		res.addRule(e)
	# TODO: Should probably have a separate model element
	res.addAnnotation("if-expression")
	return res

def d_ConditionExpression(t):
	''' ConditionExpression:
		'if' Expression '->' Expression
		('|' Expression '->' Expression) *
		('|' Expression) ?
	'''
	# NOTE: Assignment can be an expression too!
	res = F.select()
	m   = F.matchExpression(t[1], t[3])
	res.addRule(m)
	rules = t[4]
	while rules:
		predicate, _, expression = rules[1:4]
		res.addRule(F.matchExpression(predicate, expression))
		rules = rules[4:]
	if t[5]:
		e = F.matchExpression(F._ref("True"), t[5][1])
		e.addAnnotation("else")
		res.addRule(e)
	# TODO: Should probably have a separate model element
	res.addAnnotation("if-expression")
	return res

def d_Value(t):
	'''Value : Litteral|List|Dict|Range|Closure'''
	return t[0]

# ----------------------------------------------------------------------------
# Operations
# ----------------------------------------------------------------------------

def d_Instanciation(t,nodes,spec):
	'''Instanciation: 'new' Expression ( Name | Value | LP (Expression (","  Expression )*)?  RP)
	'''
	# This is a dirty hack to prevent newXXX to be interpreted assert new XXX
	if spec:
		node_new  = nodes[0]
		node_expr = nodes[1]
		if node_expr.start_loc.s - node_new.end == 0:
			return Reject
	p = t[2]
	if len(p) == 1:
		return F.instanciate(t[1], *p)
	elif len(p) == 2:
		return F.instanciate(t[1])
	else:
		p = t_filterOut(",", p[1:-1])
		return F.instanciate(t[1], *p)

def d_Slicing(t):
	'''Slicing: Expression LB Expression (':' Expression? )? RB '''
	if t[3]:
		if len(t[3]) == 1:
			return F.slice(t[0], t[2])
		else:
			return F.slice(t[0], t[2], t[3][1])
	else:
		return F.access(t[0], t[2])

def d_InvocationOrResolution(t):
	'''InvocationOrResolution: Expression "\`"? ( Name | Value | InvocationParameters ) '''
	is_escaped = len(t[1]) > 0
	p = t[2]
	# NOTE: In some cases (and I don't get why this happens), Invocation
	# matches but Resolution doesn't. So we check if expression is a
	# reference (a name) and we make the invocation fail
	if len(p) == 1:
		if not is_escaped:
			if isinstance(p[0], interfaces.IList) and len(p[0].getValues()) == 1:
				return F.access(t[0], p[0].getValue(0).detach())
			if isinstance(p[0], interfaces.IReference):
				return F.resolve(p[0], t[0])
		if type(p[0]) in (tuple, list):
			return F.invoke(t[0], *p[0])
		else:
			return F.invoke(t[0], F._arg(value=p[0]))
	else:
		assert None, "This should not happen !"

def d_InvocationParameters(t):
	'''InvocationParameters:
		LP InvocationParameter? ("," InvocationParameter)*
			(','? EOL INDENT (InvocationParameter EOL+)+ DEDENT)?
		RP
	'''
	r = []
	r.extend(t[1])
	r.extend(t_filterOut(",", t[2]))
	for line in t_filterOut(",", t[3]):
		if line is None: continue
		if type(line) in (tuple,list):
			r.extend(line)
		else:
			r.append(line)
	return r

def d_InvocationParameter(t):
	'''InvocationParameter:
		(NAME '=' Expression)
	|	('...'  '=' Expression)
	|	('...'      Expression)
	|   Expression
	'''
	t = t[0]
	is_list = type(t) is list
	if is_list and len(t) == 3 and t[1] == "=":
		if t[0] == "...":
			r = F._arg(name=t[0],value=t[2],asMap=True)
		else:
			r = F._arg(name=t[0],value=t[2])
	elif is_list and len(t) == 2 and t[0] == "...":
		r = F._arg(value=t[1],asList=True)
	else:
		r = F._arg(value=t)
	return r

# ----------------------------------------------------------------------------
# Closures
# ----------------------------------------------------------------------------

def d_Closure(t):
	'''Closure: LC (Arguments '|')? (Line| (Line|EOL) (INDENT Code DEDENT)? )? RC '''
	a = t[1] and t[1][0] or ()
	c = F.createClosure(a)
	# Here we force a termination in closure, so that they always return a
	# result
	#code = t_filterOut(None, t_flatten(t[2]))
	code = t[2]
	t_setCode(c, code)
	p_ensureReturns(c)
	return c

def d_Arguments(t):
	'''Arguments: Argument (',' Argument)* '''
	r = [t[0]] ; r.extend(t[1])
	r = filter(lambda e:e!=',', r)
	return r

def d_Argument(t):
	'''Argument: NAME (':' Type)? ('?'|'=...'|'...'|'=' (Litteral| Expression )) ? '''
	is_optional = t[2] and t[2][0] == '?'
	is_rest     = t[2] and t[2][0] == '...'
	is_kwrest   = t[2] and t[2][0] == '=...'
	has_value   = t[2] and t[2][0] == '='
	arg_type    = t[1] and t[1][1] or None
	arg = F._param(t[0], arg_type)
	if is_optional: arg.setOptional(True)
	if is_rest: arg.setRest(True)
	if is_kwrest: arg.setKeywordsRest(True)
	if has_value: arg.setDefaultValue(t[2][-1])
	return arg

def d_Type(t):
	'''Type:  NAME ('.' NAME)* | "<[^\\>]+>" '''
	return t[0]

# ----------------------------------------------------------------------------
# Litterals
# ----------------------------------------------------------------------------

def d_Litteral(t):
	'''Litteral : Integer|Float|String|Name '''
	return t[0]

def d_Integer(t):
	'''Integer : "-?[0-9]+" | "-?0x[A-Fa-f0-9]+"'''
	return F._number(eval(t[0]))

def d_Float(t):
	'''Float : "-?[0-9]+\.[0-9]+" '''
	return F._number(float(t[0]))

def d_String(t):
	'''String : StringSQ|StringDQ '''
	return F._string(eval(t[0]))

def d_StringSQ(t, nodes):
	'''StringSQ : "'" (STR_NOT_SQUOTE|STR_ESC)* "'" '''
	buf = nodes[0].buf
	start = nodes[0]
	end   = nodes[-1]
	return buf[start.start_loc.s:end.end]

def d_StringDQ(t, nodes):
	'''StringDQ : '"' (STR_NOT_DQUOTE|STR_ESC)* '"' '''
	buf = nodes[0].buf
	start = nodes[0]
	end   = nodes[-1]
	return buf[start.start_loc.s:end.end]

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
	'''List : LB ( (Expression (',' Expression)*)? (CEOL INDENT (Expression (',' Expression)* CEOL)* DEDENT )? ) RB '''
	r = t_filterOut(",", t[1])
	l = F._list(*r)
	return l

def d_Dict(t):
	'''Dict : LC ( (DictPair (',' DictPair)*)? (CEOL INDENT (DictPair (','
	DictPair)* CEOL)* DEDENT )? ) RC '''
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
	''' NAME: "\\\\?[$A-Za-z_]+[$0-9A-Za-z_]*" '''
	if spec and t[0] in KEYWORDS:
		return Reject
	else:
		if t[0][0] == "\\": return t[0][1:]
		return t[0]

def d_EOL(t):
	''' EOL: "\\n"+ '''
	return

def d_CEOL(t):
	''' CEOL: "\\s*(#[^\\n]*)?\\n"+ '''
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

def d_CHECKATLEAST(t, spec):
	''' CHECKATLEAST: '''
	if spec:
		if not _PARSER.indentStack: return
		if _PARSER.requiredIndent > _PARSER.indentStack[-1]:
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
	# In some case, we have ambiguities (and I don't know how to fix this
	# properly).
	def get_name(n):
		if n.symbol == "Expression": return get_name(n.c[0])
		else: return n.symbol
	def get_code(n):
		return n.buf[n.start_loc.s:n.end]
	names = map(get_name, nodes)
	if "Instanciation" in names:
		# This is when we have new_node setAttribute that gets
		# interpreted as new _node.setAttribute
		return filter(lambda n:get_name(n)!="Instanciation", nodes)[0]
	else:
		#print "Ambiguity not supported " + str(names) + "\n" + str(map(get_code,nodes))
		return nodes[0]

# ----------------------------------------------------------------------------
#
# EXTERNAL API
#
# ----------------------------------------------------------------------------

#_PARSER = Parser(make_grammar_file=0)
_PARSER = DParser(make_grammar_file=0)

def parse( text, verbose=True, options=None, environment=None ):
	_PARSER.indentStack = []
	_PARSER.isNewline   = True
	_PARSER.requiredIndent = 0
	_PARSER.previousLine   = 0
	if options is None: options = Options()
	if environment:
		for opt in environment.options.keys():
			options.addTarget(opt)
	_PARSER.options = options
	res = _PARSER.parse(text,initial_skip_space_fn=skip_whitespace,ambiguity_fn=disambiguate, print_debug_info=(verbose and 1 or 0))
	return res

def parseFile( path, verbose=False, options=None, environment=None ):
	f = file(path, 'r') ; t = f.read() ; f.close()
	return parse(t, verbose, options, environment)

# FIXME: Modules should always be asbolutely named
def parseModule(name, text, verbose=False, options=None, environment=None):
	res = parse(text, verbose, options, environment)
	module_name = res.getAnnotation("module")
	if module_name:
		res.setName(module_name.getContent())
	elif name:
		res.setName(name)
	return res

# ------------------------------------------------------------------------------
#
# Parser
#
# ------------------------------------------------------------------------------

class Options:

	def __init__(self):
		self.targets = []

	def addTarget( self, name ):
		"""Adds a target to the options."""
		name = name.upper()
		if name not in self.targets:
				self.targets.append(name)

	def hasTarget(self, name):
		"""Returns True of the given target name is present in the options."""
		name = name.upper()
		return name in self.targets

class Parser:
	"""The parser is a simple API that can be used as an entry point
	to manipulate SweetC source code."""

	def __init__( self, verbose = False ):
		"""Creates a new interpreter."""
		self._warnings = []
		self.verbose   = verbose
		self.options   = Options()
		self._program  = F.createProgram()
		self._program.setFactory(F)
		self.environment = None

	def program( self ):
		"""Returns the program that is implicitely created by parsing the
		different modules."""
		return self._program

	def parse( self, filepath, name=None ):
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
		if name is None:name=self.pathToModuleName(filepath)
		return self.parseModule(name, text, filepath)

	def parseSource( self, source, moduleName=None ):
		return self.parseModule(moduleName, source)

	def parseString( self, source, moduleName=None, sourcepath=None ):
		return self.parseModule(moduleName, source, sourcepath)

	def clean(self):
		for f in "d_parser_mach_gen.g.md5 d_parser_mach_gen.g.d_parser.dat".split():
			if os.path.exists(f):
				os.unlink(f)

	def parseModule( self, name, text, sourcepath=None ):
		global SOURCE_PATH
		SOURCE_PATH = sourcepath
		# And ensure that there is an EOL
		if not text:
			self.warn("The given file is empty")
		if text and text[-1] != "\n":
			self.warn("No trailing EOL in given code")
			text += "\n"
		# Forcing dos-to-unix conversion
		text = text.replace("\r\n", "\n")
		# We try to parse the file
		#try:
		if True:
			name = name and self.pathToModuleName(name)
			res = parseModule(name, text, self.verbose, self.options, self.environment)
			# We set the module file path (for informative purpose only)
			if sourcepath:
				res.setSource("file://" + os.path.abspath(sourcepath))
			# FIXME: Add support for modules which are part of other modules
			if self._program:
				self._program.addModule(res)
			self.clean()
			return ( text, res )
		else:
			self.clean()
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
		res = res.replace("-", "").replace(".", "")
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
