# DESCRIPTION: In this non-functional example copied and trimmed from
# the `physics` module, `False` is not resolved
# to its `false` JS equivalent.
# REVISION: 48b999b020ac86d62fcdb729f1bd503b079b48e4
# DATE: 2016-04-11
@class A

	@property p1         = False
	@property p2:Boolean = True

	@method f a
		if a is Undefined
			return True
		else
			return False
		end
	@end

@end
# EOF
