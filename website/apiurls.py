from django.urls import path
from website import note_api
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('',note_api.NoteListAPIView.as_view()),
    path('<int:pk>/',note_api.NoteDetailAPIView.as_view()),
    path('<int:pk>/update',note_api.NoteUpdateAPIView.as_view()),
    path('<int:pk>/delete',note_api.NoteDeleteAPIView.as_view()),
    path('listview/',note_api.note_alt_view),
    path('auth/',obtain_auth_token),
    
]