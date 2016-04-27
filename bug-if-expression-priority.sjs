@class A

	@method m
		return True
	@end

	@method n
		return False
	@end

	@method p0 a
		# This one is correct
		return if a > 0 -> m () | n ()
	@end

	@method p1 a
		# BUG: The result of the expression is not returned
		# it is converted to an `if` statement.
		if a > 0 -> m () | n ()
	@end

	@method p2 a
		# BUG: The else part of the expression has to be put in parens
		a > 0 ? m () | n ()
	@end

	@method p3 a
		# This one is correct
		a > 0 ? m () | (n ())
	@end

@end
