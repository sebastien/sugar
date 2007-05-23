@function f
	var v = 1
	(0..10) :: {
		print ( (v+1) * 2 * (f(v-1) )) / 10
	}
@end

