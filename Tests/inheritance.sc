class A:

	method foo():
		print("Foo" + self.getClass())
	end

end

class B extends A:

	method foo():
		super().pouet
	end 

end

class C extends B:

	method foo():
		super(A).foo()
		super(B).foo()
	end

end
