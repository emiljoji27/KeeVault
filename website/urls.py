from django.urls import path,include,re_path
from . import views

#app_name='website'
urlpatterns = [
    path('',views.index,name='home'),
    path('login/',views.login,name='log_in'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='log_out'),
    path('generator/',views.generator,name='generator'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('view_details/',views.anonymous,name='anony'),
    re_path(r'^delete/(?P<pk>[0-9]+)/$',views.delete_entry,name='delete_entry'),
    path("password_reset/", views.password_reset_request, name='password__reset'),   
]