from django.urls import path,include

from website import note_api
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'

urlpatterns = [
    path('auth/',obtain_auth_token),
    path('user/',views.UserRecordView.as_view(), name='users'),
    path('details/',views.PasswordView.as_view()),
    path('<int:pk>/delete/',views.PasswordDeleteAPIView.as_view())

]