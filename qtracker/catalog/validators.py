from django.core.exceptions import ValidationError

def validate_email(value):
	email = value
	if ".edu" in email:
		raise ValidatorsError("We do no accept .edu as mail")


# if we have a predefined list of element and we want user to provide one of it
# CATEGORIES = ['Mexico', 'Egypt', 'france']
#def validate_category(value):
#	if not value in CATEGORIES:
#		raise ValidatorsError("This is not a valid category")
