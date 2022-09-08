from rest_framework import generics,mixins,permissions,authentication
from .models import Notes
from api.serializers import NoteSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes
from django.shortcuts import get_object_or_404
from api.permissions import IsStaffEditorPermission
from api.authentication import TokenAuthentication


class NoteCreateAPIView(generics.CreateAPIView):
    queryset=Notes.objects.all()
    serializer_class=NoteSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance=serializer.validated_data
        print(instance)
        print(instance.get('title'))
        instance=serializer.save()

class NoteDetailAPIView(generics.RetrieveAPIView):
    queryset=Notes.objects.all()
    serializer_class=NoteSerializer
    authentication_classes=[authentication.SessionAuthentication,TokenAuthentication]
    permission_classes=[IsStaffEditorPermission]

class NoteListAPIView(generics.ListAPIView):
    queryset=Notes.objects.all()
    serializer_class=NoteSerializer
    authentication_classes=[authentication.SessionAuthentication]
    permission_classes=[IsStaffEditorPermission] #permissions.DjangoModelPermissions


class NoteUpdateAPIView(generics.UpdateAPIView):
    queryset=Notes.objects.all()
    serializer_class=NoteSerializer

    def perform_update(self, serializer):
        instance=serializer.save()


class NoteDeleteAPIView(generics.DestroyAPIView):
    queryset=Notes.objects.all()
    serializer_class=NoteSerializer

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        print("delete successful")



class NoteMixinView(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,generics.GenericAPIView):

    queryset=Notes.objects.all()
    serializer_class=NoteSerializer
    lookup_field='pk'

    def get(self,request,*args,**kwargs):
        print(args,kwargs)
        pk=kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request,*args,**kwargs)
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def perform_create(self, serializer):
        instance=serializer.validated_data
        print(instance)
        print(instance.get('title'))
        instance=serializer.save()




@api_view(['GET','POST'])
def note_alt_view(request,pk=None,*args,**kwargs):
    method=request.method

    if method=="GET":
        obj=get_object_or_404(Notes,pk=pk)
        data=NoteSerializer(obj).data
        return Response(data)


    if method=="POST":
        serializer=NoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          instance=serializer.save()
          data=serializer.data
          return Response(data)
        return Response({"invalid":"invalid data"},status=400)


import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from api.serializers import NoteSerializer, PasswordSerializer
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def api_home(request):
    serializer=NoteSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance=serializer.save()
        print(instance)
        data=serializer.data
        return Response(data)
    return Response({"invalid":"invalid data"},status=400)