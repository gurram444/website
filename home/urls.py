from django.contrib import admin
from django.urls import path
from home import views
from django.conf.urls.static import static
from django.conf import settings
from home.views import *

urlpatterns = [
                  path('', views.Home, name='home'),
                 # path("listing/", Listing.as_view(), name='listing'),
                  #path("ajax/locations/", views.getlocation, name='get_locations'),
                  path('clientregister/', views.clientcreation, name='clientregister'),
                  path('customerregister/', views.customercreation, name='customerregister'),
                  path('login/', views.customerpage, name='customerpage'),
                  path('login_register/', views.login_register, name='login_register'),
                  path('clientlogin/', views.userpage, name='login'),
                  path('accounts/login/userpage/', views.userauthentication, name='userauthentication'),
                  path('search/', views.search, name='search'),
                  path('portfolio/', views.portfolio, name='portfolio'),
                  path('userlist/<int:category_id>/<str:user_type>/', views.user_list, name='user_list'),
                  path('view_profile/(?P<user_id>\d+)/', views.view_profile, name='view_profile'),
                  path('design_photos/<int:user_id>/', views.designphotos, name='design_photos'),
                  #path('view_photos/(?P<user_id>\d+)/', views.view_photos, name='view_photos'),
                  path('send_sms/',views.send_sms_user,name='send_sms'),
                path('filters/',views.filters, name='filters'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
