@function main

	# Alternative:
	#   We may do a! instead of a()
	#   This may allow the distinction  between invocation and activation

	a = None
	a ()
	a = a b
	a = a () b

	a b()
	a() b() c()
	a() b c()

	a = a() b() c
	a = a() b c
	a b() c()
	a b c()

	a = a b() c
	a = a b c
	a = a[0]
	a = a["pouet"]

	a[0] pouet()

	# There is a problem here where the '[0]' is interepreted as a value
	a pouet[0]()
	a pouet[0] b()
	a pouet()[0] b()

	# Multi-line invocation
	a(1)
	a(1,2)
	a(1,2,3)

	a(1,2,
		3
	)

	a(1,
		2
		3
	)

	a(
		1
		2
		3
	)

@end
