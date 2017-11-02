#Users
from django.conf import settings

from django.db import models 
import datetime
import uuid # Required for unique book instances

from django.core.urlresolvers import reverse 
from .utils import unique_slug_generator # generates readable urls
from .validators import validate_email

User = settings.AUTH_USER_MODEL

class Organization(models.Model):
	user 		= models.ForeignKey(User)
	org_name	= models.CharField('Name of Organization', max_length=200)
	service 	= models.CharField(max_length=200)
	address 	= models.CharField(max_length=200)
	state 		= models.CharField(max_length= 75)
	email 		= models.EmailField(max_length=75)
	website 	= models.URLField(blank=True)
	tel 		= models.IntegerField()
	timestamp	= models.DateTimeField('Date Created', auto_now_add=True, auto_now=False)
	updated 	= models.DateTimeField('Date Updated', auto_now_add=False, auto_now=True)
	last_accessed = models.DateTimeField()
	slug 		= models.SlugField(null=True, blank=True)
	#User.get_user_model() will get the model from module. User.objects.all() will return the queryset
	#to get user by id do: Organization.objects.filter(user__id=1)

	def __str__(self):
		return self.org_name

	@property
	def title(self):
	    return self.org_name

	def get_absolute_url(self):
		#return reverse('list', kwargs={'slug'=self.slug})
		return reverse('org-list', kwargs={'id':self.id})
	
	class Meta:
		ordering = ['org_name']


class Location(models.Model):
	user 		= models.ForeignKey(User)
	org_id 		= models.ForeignKey(Organization, on_delete=models.CASCADE)
	loc_name	= models.CharField('Name of Location', max_length=200)
	loc_desc 	= models.TextField('Description', max_length=1000)
	timestamp 	= models.DateTimeField('Date Created', auto_now_add=True, auto_now=False)
	updated 	= models.DateTimeField('Date Updated', auto_now_add=False, auto_now=True)
	last_accessed = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.loc_name 

	#def get_absolute_url(self):
		#return reverse('list', kwargs={'slug'=self.slug})
		#return reverse('location-list', kwargs={'id':self.id})
	

class Item(models.Model):
	#association
	user 		= models.ForeignKey(User)
	org_id 		= models.ForeignKey(Organization)
	loc_id 		= models.ForeignKey(Location, on_delete=models.CASCADE)
	#real item data
	item_name	= models.CharField('Name of Item',max_length=200)
	org_item_id = models.CharField(blank=True, max_length=200)
	item_desc 	= models.TextField('Description',max_length=200)
	timestamp	= models.DateTimeField('Date Created', auto_now_add=True, auto_now=False)
	updated 	= models.DateTimeField('Date Updated', auto_now_add=False, auto_now=True)
	last_accessed = models.DateTimeField()

	class Meta:
		ordering = ['-updated', '-timestamp']

	def __str__(self):
		return self.item_name

	def get_absolute_url(self):
		return reverse('item-list', kwargs={'id':self.id})
				
