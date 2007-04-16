@class A
	@constructor pa, pb
		a = pa
		b = pb
	@end
@end

@class B: A
	@constructor pb
		super ("I am B", pb)
	@end
@end
