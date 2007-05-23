@module jQuery
@as Interface

@interface jQueryEngine
	@group Core
		@abstract @method each fn:Function
		@abstract @method eq   pos:Number
		@abstract @method get
#		@abstract @method get  num:Number
		@abstract @method gt   pos:Number
		@abstract @method index subject:Number
		@abstract @method length:Number
		@abstract @method lt   pos:Number
		@abstract @method size
	@end
@end

# TODO: Variable arguments
#@function jQuery:jQueryEngine selector:String (parent:String)?
@abstract @function jQuery:jQueryEngine selector:String 

# TODO: Multiple dispatch (with type support)
#@abstract @function jQuery:jQueryEngine f:Function
