from django.contrib import admin
from .models import Organization, Location, Item

class OrganizationAdmin(admin.ModelAdmin):
	#Register the Admin classes for Book using the decorator
	list_display= ('org_name','service', 'website', 'address','timestamp')

	#groups the items to be displayed in each fieldset with name Book Details and Availability
	fieldsets = (
        ('Organization Info', {
            'fields': ('org_name','service')
        }),
        ('Contact Info', {
            'fields': ('tel', 'email', 'website', 'address', 'state')
        }),
    )

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	list_display = ('loc_name', 'loc_desc')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ('item_name', 'item_desc', 'timestamp')
		
admin.site.register(Organization, OrganizationAdmin)