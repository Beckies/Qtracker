from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import Organization, Location, Item
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .forms import OrganizationForm, LocationForm, ItemForm
from django.http import HttpResponseRedirect
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

class OrganizationListView(LoginRequiredMixin, ListView):	
	model = Organization
	login_url = "/login/"

	def head(self, *args, **kwargs):
		last_book = self.get_queryset().latest('updated')
		response = HttpResponse('')
		response['Last-Modified'] = last_book.updated.strftime('%a, %d %b %Y %H:%M:%S GMT')
		return response

	def get_context_data(self, **kwargs):
		context = super(OrganizationListView, self).get_context_data(**kwargs)
		# Add in the Organization
		context['title'] = Organization
		return context


def organization_location(request, id):
	organization = Organization.objects.filter(id=id)[0]
	location_list = organization.location_set.all()
	item_count = 1
	return render(request, 'catalog/location_by_organization.html', context={'location_list':location_list, 'organization':organization, 'item_count':item_count} )

def item(request, pk):
	location = Location.objects.filter(id=pk)[0]
	item_list = location.item_set.all()
	return render(request, 'item.html', context={'item_list':item_list, 'location':location} )



class OrganizationDetail(LoginRequiredMixin, DetailView):
	model = Organization

	def get_context_data(self, **kwargs):
		context = super(OrganizationDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
		context['organization_list'] = Organization.objects.all()
		return context
	
class OrganizationCreateView(LoginRequiredMixin, CreateView):#this class runs the form_valid method of which at end it saves the form
	form_class = OrganizationForm
	template_name = "forms/create.html"
	success_url = "/catalog/org"
	login_url = "/login/"

	def form_valid(self, form):
		instance = form.save(commit=False) #acts like a pre_save
		instance.user= self.request.user #instance.save()
		return super(OrganizationCreateView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(OrganizationCreateView, self).get_context_data(*args,**kwargs)
		context['title'] = 'Add Organization' #adds to dictionary
		context['button'] = 'Create'
		return context

class OrganizationUpdateView(UpdateView):
	form_class = OrganizationForm
	login_url = "/login/"
	template_name = "forms/create.html"
	success_url = "/catalog/org"

	def get_queryset(self):
		return Organization.objects.filter(user=self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super(OrganizationUpdateView, self).get_context_data(*args,**kwargs)
		name = self.get_object().org_name
		context['title'] = f'Update Organization: {name}'
		context['button'] = 'Update'
		return context

class LocationListView(LoginRequiredMixin, ListView):
	queryset = Location.objects.all()
	login_url = "/login/"

class LocationCreateView(LoginRequiredMixin, CreateView):
	form_class = LocationForm
	template_name = "forms/create.html"
	success_url = "/catalog/location"
	login_url = "/login/"
	
	def form_valid(self, form):
		instance = form.save(commit=False) #acts like a pre_save
		instance.user= self.request.user #instance.save()
		return super(LocationCreateView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(LocationCreateView, self).get_context_data(*args,**kwargs)
		context['title'] = 'Add Location'
		context['button'] = 'Create'
		return context

class LocationUpdateView(LoginRequiredMixin, UpdateView):
	form_class = LocationForm
	login_url = "/login/"
	template_name = "forms/create.html"
	success_url = "/catalog/location"

	def get_queryset(self):
		return Location.objects.filter(user=self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super(LocationUpdateView, self).get_context_data(*args,**kwargs)
		org_name = self.get_object().org_id
		loc_name = self.get_object().loc_name
		context['title'] = f'Update {loc_name} in {org_name}'
		context['button'] = 'Update'
		context['message'] = 'Updated Successfully'
		return context



class ItemCreateView(LoginRequiredMixin, CreateView):
	login_url = "/login/"
	form_class = ItemForm
	template_name = "forms/create.html"
	success_url = "/catalog/item"

	def form_valid(self, form):
		instance = form.save(commit=False) #acts like a pre_save
		instance.user= self.request.user #instance.save()
		return super(ItemCreateView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemCreateView, self).get_context_data(*args,**kwargs)
		context['title'] = 'Add Item'
		context['button'] = 'Create'
		context['message'] = 'Item Successfully Created'
		return context

class ItemListView(LoginRequiredMixin, ListView):
	login_url = "/login/"
	queryset = Item.objects.all()

class ItemUpdateView(LoginRequiredMixin, UpdateView):
	form_class = ItemForm
	login_url = "/login/"
	template_name = "forms/create.html"
	success_url = "/catalog/item"

	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemUpdateView, self).get_context_data(*args,**kwargs)
		item_name = self.get_object().item_name
		loc_name = self.get_object().loc_id
		context['title'] = f'Update {item_name} in {loc_name}'
		context['button'] = 'Update'
		#context['message'] = 'Updated Successfully'
		return context

	
def delete_org(request, id):
	org = Organization.objects.filter(pk=id)
	message = f"Successfully deleted { org[0] } from database"
	org.delete()
	queryset = Organization.objects.all()
	return render(request, 'catalog/organization_list.html', context={'message': message, 'object_list': queryset})

def delete_loc(request, id):
	loc = Location.objects.filter(pk=id)
	message = f"Successfully deleted { loc[0] } from database"
	loc.delete()
	queryset = Location.objects.all()
	return render(request, 'catalog/location_list.html', context={'message': message, 'object_list': queryset})

def delete_item(request, id):
	item = Item.objects.filter(pk=id)
	message = f"Successfully deleted { item[0] } from database"
	item.delete()
	queryset = Item.objects.all()
	return render(request, 'catalog/item_list.html', context={'message': message, 'object_list': queryset})

	
def search_organization(request):
	if request.method == "POST":
		search = request.POST['search']
	else:
		search = ""

	organization = Organization.objects.filter(title__contains=search)
	render_to_response
