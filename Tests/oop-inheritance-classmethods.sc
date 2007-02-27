# The goal of this test is to exercise inheritence
@class A
	@shared P = 'P'
	@operation o
		:return P
	@end
	@operation a v
		P = P + v
		:return P
	@end
@end

@class B: A
@end

@class C: B
	@shared P = 'C.P'
@end

print ('A.o', A o())
print ('B.o', B o())
print ('C.o', C o())

print ('A.a("x")', A a('x'))
print ('B.a("y")', B a('y'))
print ('C.a("z")', C a('z'))
