# PROBLEM: The for...in is written as
# (for.cell in __this__.cells)
#		if ( (c.id == cell.id) )
#		{
#			return true
#		}
@function cellInQueue cell
| Tells if the given cell is in the waiting queue for this stream
	for cell in cells
		when (c id == cell id) -> return True
	end
	for cell in syncCells
		when (c id == cell id) -> return True
	end
	return False
@end
