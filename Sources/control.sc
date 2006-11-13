
function controlTest():

	if 1:
		print (True)
	end

	if 2:
		print (True)
	else:
		print (False)
	end

	if 3:
		print (True)
	else if False:
		print (False)
	else:
		print ()
	end

	for i in 0..10:
	end

	for i in 0..10:
		print (i)
	end

	a := 0

	# Iterates from 0 to 10
	for i in (a)..(a+10):
		print (i)
	end

	# Iterates from 0 to 10, by step of 2
	for i in (a)..(a+10)|2:
		print (i)
	end

	a = 0
	while a < 10:
		a = a + 1
	end

end
