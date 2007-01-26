
@function a 
	:return 1
@end

@function b a
	:return 1 + a
@end


@function c a, b
	:return 1 + a + b
@end


@function d  a, b, c, d
	:return 1 + a + b + d
@end

@function d  a:int, b:int, c:int, d:int
	:return 1 + a + b + d
@end

