
function compute():
	return 0
end

# This function returns an iterator because it uses yield
function continuations():
	a := 0
	while True:
		yield a
		a = a + 1
	end
end

function asyncTest():

	future := @compute()
	# The future value is lazily evaluated. When the future is passed, it is not
	# evaluated, but when it is used, it will be evaluated, and will then block
	# the process waiting for the value
	print (future)

	# 
	cont := continuations()
	print (cont.next())

end
