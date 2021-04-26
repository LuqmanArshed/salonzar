from django.urls import path
from django.conf import settings

from django.conf.urls.static import static


from . import views 

urlpatterns = [
     path('', views.home, name='home'),
    #  path('user_home', views.user_home, name='user_home'),
     path('login/', views.login_page, name='login_page'),
     path('register/', views.registerPage, name='register_page'),
     path('business_register/', views.business_registerPage, name='busineess_register_page'),
	 path('logout/', views.logoutuser, name='logoutuser'),
      path('selectoption/', views.register_option, name='resgisteroption'),
      path('controller_home/', views.admin_home, name='admin_home'),
   
    
]


if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)