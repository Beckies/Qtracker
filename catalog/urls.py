from django.urls import reverse_lazy
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from . import views 

 
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='registration/login.html')),
    url(r'^home/$', views.home, name='home'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    url(r'^/search_id/$', views.search),
    
    # url for displaying Organizations, Locations and Items
    url(r'^org/$', views.org_list, name='org-list'),
    url(r'^(?P<org_id>\d+)/location$', views.location_list, name='org_loc_list'),
    url(r'^(?P<item_id>\d+)/items$', views.item_list, name='loc_item'),
    url(r'^locations/$', views.loc_list, name='location_all'),
    url(r'^items/$', views.item_list, name='item_all'),
   
    # url for creating new Organization, Location and Item
    url(r'^create/$', views.org_create, name='org_create'),
    # url(r'^loc_create/$', LocationCreateView.as_view(), name='loc_create'),
    # url(r'^item_create/$', ItemCreateView.as_view(), name='item_create'),
    
    # url for updating Organizations, Locations and Items
    url(r'^organization/(?P<id>\d+)/update$', views.org_update, name='org_update'),
    url(r'^location/(?P<id>\d+)/update$', views.loc_update, name='loc_update'),
    # url(r'^edit_item/(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='item-update'),

    # url for deleting Organizations, Locations and Items
    url(r'^organization/(?P<id>\d+)/delete$', views.org_delete, name='org_delete'),
     url(r'^location/(?P<id>\d+)/delete$', views.loc_delete, name='loc_delete'),
    # url(r'^del_item/(?P<id>\d+)/$', views.delete_item, name='item-delete'),

    #url for search
    # url(r'^search/$', views.search_organization)
] 