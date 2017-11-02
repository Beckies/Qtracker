from django.urls import reverse_lazy
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from . import views 
from .views import (
	OrganizationListView,
	LocationListView, 
	ItemListView,  
	OrganizationCreateView,
    LocationCreateView,
    ItemCreateView,
	OrganizationUpdateView, 
    LocationUpdateView,
    ItemUpdateView,
    delete_org,
    delete_loc,
    delete_item,
    home,
    organization_location,
)

 
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^home/$', views.home, name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html')),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    
    # url for displaying Organizations, Locations and Items
    url(r'^org/$', OrganizationListView.as_view(), name='org-list'),
    url(r'^location/$', LocationListView.as_view(), name='location-list'),
    url(r'^item/$', ItemListView.as_view(), name='item-list'),
    url(r'^org_loc/(?P<id>\d+)/$', views.organization_location, name='org_loc_list'),
   
    # url for creating new Organization, Location and Item
    url(r'^create/$', OrganizationCreateView.as_view(), name='create'),
    url(r'^loc_create/$', LocationCreateView.as_view(), name='loc_create'),
    url(r'^item_create/$', ItemCreateView.as_view(), name='item_create'),
    
    # url for updating Organizations, Locations and Items
    url(r'^edit/(?P<pk>\d+)/$', OrganizationUpdateView.as_view(), name='org-update'),
    url(r'^edit_loc/(?P<pk>\d+)/$', LocationUpdateView.as_view(), name='loc-update'),
    url(r'^edit_item/(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='item-update'),

    # url for deleting Organizations, Locations and Items
    url(r'^del_org/(?P<id>\d+)/$', views.delete_org, name='org-delete'),
    url(r'^del_loc/(?P<id>\d+)/$', views.delete_loc, name='loc-delete'),
    url(r'^del_item/(?P<id>\d+)/$', views.delete_item, name='item-delete'),

    #url for search
    url(r'^search/$', views.search_organization)
] 