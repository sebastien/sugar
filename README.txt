Features:

 - Capture more information than other languages (be explicit)

Influences:

 - Python, for the simplicity and cleanliness of the syntax
 - Eiffel, for the design by contract support
 - Smalltalk, for blocks
 - Io, for the message sending syntax
 - Lisp
 
 Problem:
 
   In {pouet:asdasdd) if pouet is a variable defined elsewhere, it will be
   evaluated and used as a key. We've got to make a way to say that
   it is a litteral key, and not an expression.
   
   I propose that we use pouet :: to disambiguate with pouet : 
   
Todo:

  - Update constructor to be like "new Pouet a, b, c" instead of "new Pouet(a,b,c)"

  	# This should be re-written as
	# @wrapper
	# And also added conditionals like
	# @when jQuery
	# @when Prototype
	
	Problem: 
	
BUGS:

	@property position
	
	@constructor position
		this position = position
	@end
