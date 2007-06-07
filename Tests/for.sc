for x in 0..10 
	print x
end

(0..10) :: {i|print i}


var a = 0
for i in a..(a+10)
end

for i in (a)..(a+10)
end

# Iterates from 0 to 10
for i in (a)..(a+10)
	print (i)
end

# Iterates from 0 to 10, by step of 2
for i in (a)..(a+10) step 2
	print (i)
end
