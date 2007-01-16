1 -> { print 'One' }

:match
	1 -> { print 'One' }
	2 -> { print 'Two' }
	3 -> { print 'Three' }
:end

:match 
	1 -> { print 'One'}
	  -- { print 'Not one' }
:end

@function pouet
	print 'Pouet'
@end

	1 -> pouet

