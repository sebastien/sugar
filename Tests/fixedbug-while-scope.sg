# PROBLEM: The 'cell' function overrides the 'cell' variable defined locally
# in the 'while' look of the 'continue' method
@module Cells
@class Stream

	@method continue
	| Continues the execution of the stream, until the list of cells
	| is empty.
		# We could do self :: {v|...}
		while hasNext()
			var v = next()
			var cell = v[0]
			# We take the 'triggerLimit' into account to absorb
			# the effect of feedback loops.
			when cellsCount[cell id] is Undefined
				cell trigger (v[1], v[2])
				cellsCount[cell id] = 1
			when cellsCount[cell id] < cell triggerLimit
				cell trigger (v[1], v[2])
				cellsCount[cell id] += 1
			end
		end
	@end
@end

@function cell name, states
	return new Cell(name, states)
@end


# EOF

