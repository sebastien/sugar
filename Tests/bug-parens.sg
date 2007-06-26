@class Templates
					
	@operation createCitation cit
		var tags_html = html div({_:'tags'}
			'tagged as '
			html ul()
		)
		var cit_html = html div ({_:'citation'}
			html div({_:'text'}, cit getText())
			html div({_:'about'}, 'appears in', '(',  ', ',	')')
		)
		return cit_html
	@end
	
@end
