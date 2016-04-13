@class A

	@property p

	@method m a, b
		return {p,a,b|
			p = a + b
		}
	@end

	@method n a, b
		return {pp,aa,bb|
			p = a + b
		}
	@end

@end
