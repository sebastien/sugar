
@class Point

	@property x:double
	@property y:double
@end

@class Shape

	@shared    COUNT:int
	@property  points:List
	
	@constructor ()
	@end

	@method addPoint( point:Point )
		return points append(point)
	@end

	@operation shapeCount()
		return COUNT
	@end

@end

@class Rectangle:Shape

	@constructor ()
		0..4 do { points add(new Point()) }
	@end

@end
