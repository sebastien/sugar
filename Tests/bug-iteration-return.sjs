# PROBLEM: In the JavaScript backend, the 'return True' does not exit the
# function, but only returns from the closure... which is kind of normal, but we
# need to properly define this edge case.
@function f
	0..10 :: {i|
		when i == 9
			return True
		end
	}
	return False
@end
