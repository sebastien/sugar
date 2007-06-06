# PROBLEM: the whens should be aggreated, but they appear as seperate
# SOLUTION: Rewrite this as 'inArea2' as the inArea1 is ambiguous anyway
@function inArea1 pos, area
| This is a snippet that failed parsing at some point
	when (pos[0] < area x)            -> return False
	when (pos[0] > (area x + area w)) -> return False
	when (pos[1] > area y)            -> return False
	when (pos[1] > (area y + area y)) -> return False
	otherwise -> return true
@end

@function inArea2 pos, area
| This is a snippet that failed parsing at some point
	when (pos[0] < area x)
		return False
	when (pos[0] > (area x + area w))
		return False
	when (pos[1] > area y)
		False
	when (pos[1] > (area y + area y))
		False
	otherwise
		return true
	end
@end
