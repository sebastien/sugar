
@function populateColumns tiles=uis tiles
	var types = filter (by_type, {return len(_1) > 1})
	# We balance the tiles with multiple attributes
	for tui in by_type ["+"]
		var t = (tui getAttribute "data-type" split ",") :: {[_, len(types[_])]}
	end
@end
