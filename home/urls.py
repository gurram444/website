from django.contrib import admin
from django.urls import path
from home import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.Home, name='home'),
    path('clientregister/', views.clientcreation, name='clientregister'),
    path('customerregister/',views.customercreation, name='customerregister'),
    path('login_register/', views.login_register, name='login_register'),
    path('accounts/login/', views.userpage, name='login'),
    path('accounts/login/userpage/', views.userauthentication, name='userauthentication'),
    path('search/',views.search, name='search'),
    path('portfolio/',views.portfolio,name='portfolio'),
    path('userlist/<int:category_id>/<str:user_type>/',views.user_list, name='user_list'),
    path('view_profile/(?P<user_id>\d+)/' ,views.view_profile,name='view_profile'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
