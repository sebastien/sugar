# ISSUE: What to do when you want to say
# :select

print "POUET"
:select 1
	:when 1
		print 'One'
	:end
:end

print 'HELLO'
:select 2
	:when 1
		print 'One'
	:when 2
		print 'Two'
	:end
:end

print "POUET"
:select 2
	:when 1 -> print 'One'
	:when 2 -> print 'Two'
:end

print "POUET"
:select 2
	:when 1 -> print 'One'
	:when 2
		print 'Two'
	:end
:end


print "POUET"
:select 2
	:when 1 -> print 'One'
	:when 2
		print 'Two'
	:end
:end

print "POUET"
:select 2
	:when @ > 2 -> print 'Greater than two'
	:when @ < 1 -> print 'Lower than one'
	:otherwise  -> print 'Between one and two'
:end
