@function f
	:return 'b'
@end

a = {}
a = {a:1}
a = {a:1,b:2,c:3}
a = {a:1,b:2,c:3}
a = {
}
a = {
	a:1
}
a = {
	a:1
	b:1
}
a = {
	a:1, b:1
	c:1
}
a = { a:1, b:1
	c:1
}
a = { a : 'a is a key' }
a = { (f()) : 'f() returns "b" is a key' }
