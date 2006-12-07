
main:

	# Numbers
	a  = 0
	a  = (0)
	a  = 0.0
	a  = (0.0)

	# Strings
	a  = "String"
	a  = ("String")

	# Ranges
	a  = 0..1
	a  = (0+1)..(0+10)
	a  = (a)
	a  = (a)..(a+10)

	# Lists
	a  = []
	a  = [1]
	a  = [1, 2]
	a  = [1, 2, 3]
	a  = [[]]
	a  = [[],[]]
	a  = [[],[],[]]

	# Dicts
	a  = {}
	a  = {"key":value}
	a  = {"key":value, "key":value}
	a  = {"key":value, "key":value, "key":value}
	a  = { key:value,   key:value, key:value}
	a  = { 1:value,     2:value, 3:value}
	a  = { (1+4):value,     (2+10):value, (3+20):value}
	

end
