
# NOTE
# Here is the evolution of the syntaxes
# 0.5:  (a,b,c)->{...}
# 0.6:  {a,b,c|...}

:var test = {x|}
test  = {a,b|}
test  = {a|}
test  = {print("Hello")}
test  = {print("Hello"); :var a=10 ; print("a:", a)}
test  = {
	print("Hello") ; :var a=10 ; print("a:", a)
}

test  = {
	print("Hello")
	:var a=10 ; print("a:", a)
}

test = {a|
	print ("Hello", a)
	:return {x|:return 1 + x}
}
