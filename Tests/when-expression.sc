var a = (when 1 -> 2)
var a = (when 1 -> 2 | when 2 -> 3 | otherwise 3)
var a = (when 1 -> 2 | when 2 -> 3 | when 3-> 4 | otherwise 3)
var b = {e|(when 1->2)}
var b = {e|when 1->2}
