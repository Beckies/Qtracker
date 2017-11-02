from django.contrib.auth.decorators import login_required 
from django.shortcuts import render
from . models import Organization, Location, Item
from django.views.generic import ListView
from .forms import OrganizationForm, LocationForm, ItemForm
from django.http import HttpResponseRedirect
import datetime


class OrganizationListView(ListView):	
	queryset = Organization.objects.all()

class LocationListView(ListView):
	queryset = Organization.objects.all() 

class ItemListView(ListView):
	queryset = Location.objects.all()

#@login_required()
@login_required(login_url="/login/")
def create_org(request):
	form = OrganizationForm(request.POST or None)
	if form.is_valid():
		obj = Organization.objects.create(
			org_name = form.cleaned_data.get("org_name"),
			service = form.cleaned_data.get("service"),
			address = form.cleaned_data.get("address"),
			state = form.cleaned_data.get("state"),
			website = form.cleaned_data.get("website"),
			email = form.cleaned_data.get("email"),
			tel = form.cleaned_data.get("tel")
		)
		print(form.cleaned_data.get('service'))
		return HttpResponseRedirect("catalog/organization_list")
	if form.errors:
		print(form.errors)
	template_name ="forms/create.html"
	context = {'form':form, 'title':"Organization"}
	return render(request, template_name, context)


def create_loc(request):
	form = LocationForm()
	if form.is_valid():
		obj = Location.objects.create(
			org_name = form.cleaned_data.get("org_id"),
			loc_name = form.cleaned_data.get("loc_name"),
			loc_desc = form.cleaned_data.get("loc_desc")
		)
		return HttpResponseRedirect("catalog/organization_list")
	if form.errors:
		print(form.errors)
	template_name ="forms/create.html"
	context = {'form':form, 'title':"Location"}
	return render(request, template_name, context)

def create_item(request):
	form = ItemForm()
	if form.is_valid():
		obj = Location.objects.create(
			org_name = form.cleaned_data.get("org_id"),
			loc_name = form.cleaned_data.get("loc_name"),
			loc_desc = form.cleaned_data.get("loc_desc")
		)
		return HttpResponseRedirect("catalog/organization_list")
	if form.errors:
		print(form.errors)
	template_name ="forms/create.html"
	context = {'form':form, 'title':"Item"}
	return render(request, template_name, context)
