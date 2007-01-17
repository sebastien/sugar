@function f
	:return 'b'
@end

a = { a : 'a is a key' }
b = { (f()) : 'f() returns "b" is a key' }
