class A:
	def __init__(self):
		pass
	def p(self):
		return 1

class B(A):
	def __init__(self):
		A.__init__(self)
	def p(self):
		return super(B,self).p() + 1

b = B()
b.__class__
print b.__class__.__bases__
print b.p()
