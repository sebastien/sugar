@singleton AppState

	@property currentState

	# A Singleton constructor cannot have any arguments
	@constructor
		currentState = 0
	@end

	@group Transitions
		@method state1
			currentState = 1
		@end
		@method state2
			currentState = 2
		@end
	@end

@end
