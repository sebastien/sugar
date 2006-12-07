
function lambdaTest():

	test := ()->{}
	test  = (a,b)->{}
	test  = (a)->{}
	test  = ()->{print("Hello")}
	test  = ()->{print("Hello"); a:=10; print("a:", a)}
	test  = ()->{
		print("Hello") ; a:=10 ; print("a:", a)
	}
	test  = ()->{
		print("Hello")
		a:=10 ; print("a:", a)
	}
	test  = ()->{
		print("Hello")
		a:=10 ; print("a:", a)
	}
	test = (a)->{
		print ("Hello", a)
	}

end
