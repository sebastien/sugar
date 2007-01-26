@class Foo
	@method bar a
	@when   a > 5
		print a
	@end
@end

:var f = new Foo()
f bar 1
f bar 5
f bar 6
