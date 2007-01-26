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
