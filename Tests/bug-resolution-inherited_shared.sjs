@class M
	@shared S="From M"
	@constructor
		print (S)
	@end
@end

@class A:M
	@shared S="From A"
@end

@class B:A
	@shared S="From B"
@end

new M()
new A()
new B()
