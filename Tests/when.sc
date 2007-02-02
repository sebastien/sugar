:when 1
	print 'One'
:end

:when 1
	print 'One'
:when 2
	print 'Two'
:end

:when 1
	print 'One'
:otherwise
	print 'Two'
:end

# Nested when
:when 1
	:when 3
		print "Impossible"
	:when 4
		print "Impossible"
	:end
:otherwise
	print 'Two'
:end

# In closure
:var f = {a|
	:when 1
		:when 3
			print "Impossible"
		:when 4
			print "Impossible"
		:end
	:otherwise
		print 'Two'
	:end
}

@function inArea pos, area
| This is a snippet that failed parsing at some point
	:when (pos[0] < area x)            -> :return false
	:when (pos[0] > (area x + area w)) -> :return false
	:when (pos[1] > area y)            -> :return false
	:when (pos[1] > (area y + area y)) -> :return false
	:otherwise -> :return true
@end
