@module drawing
@import flash display *
@import mx core *

@class DrawingTest: UIComponent

	@constructor
		for i in 20..0
			var sprite = new Sprite()
			sprite graphics beginFill(0xFF0000 * Math random() + 0x00FF00 * Math random() + 0x0000FF * Math random())
			sprite graphics drawRect(10 * Math random(), 10 * Math random(), 400 * Math random(), 400 * Math random())
			sprite graphics endFill()
			sprite x = 40 * Math random()
			sprite y = 40 * Math random()
			sprite alpha =  Math random()
			addChild(sprite)
		end
		x = 0
		y = 0
	@end

@end

# EOF - vim: ts=4 sw=4 noet syn=sugar
