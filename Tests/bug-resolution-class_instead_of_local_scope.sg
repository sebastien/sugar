# BUG:  Class scope is taken instead of closure arguments scope
# DATE: 31-Jul-2008
@class PresenceController

	@property channel
	@property visitors = {}
	@property observers = []

	@constructor
		channel = new channels AsyncChannel  ()
		refresh ()
		update ()
	@end

	@method refresh
		var f = channel get (
			"/api/visitor/all/" + (new Date() getTime())
		) onSucceed {visitors|
			observers :: {o|
				# FIXME: Will be converted to
				# o.setAllVisitors(__this__.visitors)
				# instead of
				# o.setAllVisitors(visitors)
				o setAllVisitors (visitors)
			}
		}
	@end
@end
