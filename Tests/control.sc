:when 1
	print (True)
:end

:when 1 print (True)

:when 2 
	print (True)
:otherwise
	print (False)
:end


:when 1 print True
:otherwise print False

:when 3
	print (True)
:when 4
	print (False)
:otherwise
	print ()
@end


@for i in 0..10
	print i
@end

(0..10) each {i|print i}


a := 0
@for i in a..(a+10)
@end

@for i in (a)..(a+10)
@end

# Iterates from 0 to 10
@for i in (a)..(a+10)
	print (i)
@end

# Iterates from 0 to 10, by step of 2
@for i in (a)..(a+10) step 2
	print (i)
@end

a = 0
@while a < 10
	a = a + 1
@end
