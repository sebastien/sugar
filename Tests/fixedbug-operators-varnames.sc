@function canEdit
	return isEditable and Application inEditMode() and isEdited is False and isThereAnEditedElement is False
@end
