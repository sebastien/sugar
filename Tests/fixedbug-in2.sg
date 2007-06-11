
# BUG: It seems like 'innerHTML' is parsed as 'in nerHTML'
@function getPageContent
	var iframe  = $("#editableArea")[0]
	var content = Undefined
	when (jQuery browser msie)
		# PROBLEM
		content = iframe contentWindow document body innerHTML
		# SOLUTION
		#content = (iframe contentWindow document body innerHTML)
	otherwise
		# PROBLEM
		content = iframe contentWindow body innerHTML
		# SOLUTION
		#content = (iframe contentWindow body innerHTML)
	end
	return content
@end
