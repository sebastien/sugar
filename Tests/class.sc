@class Point

	@property xdouble
	@property ydouble

@end

@class Shape

	@shared    COUNTint
	@property  pointsList
	
	@constructor 
		points = []
	@end

	@method addPoint pointPoint
		return points append(point)
	@end

	@operation shapeCount
		return COUNT
	@end

@end

@class RectangleShape

	@constructor 
		0..4 :: { points add(new Point()) }
	@end

@end
