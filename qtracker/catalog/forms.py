from django import forms
from .models import Organization, Location, Item

# to validate
from .validators import validate_email

class OrganizationForm(forms.ModelForm):
	email = forms.EmailField(validators=[validate_email])
	class Meta:
		model = Organization
		fields = ('org_name', 'service', 'address', 'state', 'email', 'website','tel')


class LocationForm(forms.ModelForm):
	class Meta:
		model = Location
		fields = ('org_id', 'loc_name', 'loc_desc')

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('loc_id', 'item_name', 'org_item_id', 'item_desc')
		