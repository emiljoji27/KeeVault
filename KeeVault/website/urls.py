from django.urls import path,include
from . import views

#app_name='website'
urlpatterns = [
    path('',views.index,name='home'),
    path('login/',views.login,name='log_in'),
    path('register/',views.register,name='register'),
    # path('profile/',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('generator/',views.generator,name='generator'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('new_entry/',views.new_entry,name='new_entry'),
    path('dashboard/request_access/',views.request_access,name='request_access'),
    path('dashboard/request_access/view_details/',views.view_details,name='view_details'),
    path('view_details/',views.anonymous,name='anony'),
    path(r'^delete/(?P<pk>[0-9]+)/$',views.delete_entry,name='delete_entry'),
    path("password_reset/", views.password_reset_request, name='password__reset'),   
]