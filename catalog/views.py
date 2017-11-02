from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Organization, Location, Item
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .forms import OrganizationForm, LocationForm, ItemForm
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from datetime import timezone
import datetime 

def home(request):
	#order_by orders the list by publication and the [:2] limits result to be displayed
    recently_added_org = Organization.objects.order_by('-timestamp')[:4]
    recently_added_loc = Location.objects.order_by('-timestamp')[:4]
    recently_added_item = Item.objects.order_by('-timestamp')[:4]
    total_orgs = Organization.objects.all().count()
    total_locations = Location.objects.all().count()
    total_items = Item.objects.all().count()
    context = {
        'recently_added_org': recently_added_org,
        'recently_added_loc': recently_added_loc,
        'recently_added_item': recently_added_item,
        'total_orgs': total_orgs,
        'total_locations': total_locations,
        'total_items': total_items,
    }
    return render(request,'home.html', context)

def org_list(request):
	queryset = Organization.objects.all()
	context = {
	'object_list': queryset,
	'title': "Organization"
	}
	return render(request, 'catalog/organization_list.html',context)
 
def save_all(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			instance = form.save(commit=False) #acts like a pre_save
			instance.user= request.user #instance.save()
			instance.last_accessed=datetime.datetime.now()
			form.save()
			data['form_is_valid'] = True
			queryset = Organization.objects.all()
			data['org_list'] = render_to_string('catalog/organization_list_update.html',{'object_list':queryset} )
		else:
			data['form_is_valid'] = False
	context = { 'form':form,'type':"organization"}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

def org_create(request):
	if request.method == 'POST':
		form = OrganizationForm(request.POST)
	else:
		form = OrganizationForm()
	return save_all(request,form,'forms/create.html')

def org_update(request,id):
	org = get_object_or_404(Organization,id=id)
	if request.method == 'POST':
		form = OrganizationForm(request.POST,instance=org)
	else:
		form = OrganizationForm(instance=org)
	return save_all(request,form,'forms/update.html')

def org_delete(request,id):
	data = dict()
	org = get_object_or_404(Organization,id=id)
	if request.method == "POST":
		org.delete()
		data['form_is_valid'] = True
		orgs = Organization.objects.all()
		data['org_list'] = render_to_string('catalog/organization_list_update.html',{'object_list':orgs,"message":'Deleted Successfully'})
	else:
		context = {'org':org}
		data['html_form'] = render_to_string('catalog/organization_delete.html',context,request=request)

	return JsonResponse(data)

# Location CRUD
def location_list(request, org_id):
	organization = Organization.objects.filter(id=org_id)[0]
	location_list = organization.location_set.all()
	item_count = Item.objects.filter(id=org_id).count()
	return render(request, 'catalog/location_list.html', context={'location_list':location_list, 'organization':organization, 'item_count':item_count} )

def item_list(request, item_id):
	location = Location.objects.filter(id=item_id)[0]
	item_list = location.item_set.all()
	return render(request, 'catalog/item_list.html', context={'item_list':item_list, 'location':location} )

def search(request, param):
	if request.method == 'POST':
		search = request.POST['search']
	else:
		search = ""
	organizations = Organization.objects.filter(org_name__contains=search)
	return render_to_response('forms/search_org.html',{'organizations': organizations})

def org_by_id(request):
	return render_to_response('organization_list', Organization.objects.get(id=id))

def loc_list(request):
	queryset = Location.objects.all()
	context = {
	'location_list': queryset,
	'title': "Location",
	'org_th': "Name of Organization"
	}
	return render(request, 'catalog/location_list.html',context )
 
def save_all_loc(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			instance = form.save(commit=False) #acts like a pre_save
			instance.user= request.user #instance.save()
			instance.last_accessed=datetime.datetime.now()
			form.save()
			data['form_is_valid'] = True
			queryset = Location.objects.all()
			data['loc_list'] = render_to_string('catalog/location_by_organization.html',{'location_list':queryset} )
		else:
			data['form_is_valid'] = False
	context = { 'form':form,'type':"Location"}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

def loc_create(request):
	if request.method == 'POST':
		form = LocationForm(request.POST)
	else:
		form = LocationForm()
	return save_all(request,form,'forms/loc_create.html')

def loc_update(request,id):
	loc = get_object_or_404(Organization,id=id)
	if request.method == 'POST':
		form = LocationForm(request.POST,instance=org)
	else:
		form = LocationForm(instance=org)
	return save_all(request,form,'forms/loc_update.html')

def loc_delete(request,id):
	data = dict()
	loc = get_object_or_404(Location,id=id)
	if request.method == "POST":
		loc.delete()
		data['form_is_valid'] = True
		location = Location.objects.all()
		data['org_list'] = render_to_string('catalog/location_by_organization.html',{'object_list':orgs,"message":'Deleted Successfully'})
	else:
		context = {'Loc':location}
		data['html_form'] = render_to_string('catalog/organization_delete.html',context,request=request)

	return JsonResponse(data)
