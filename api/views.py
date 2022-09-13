from sqlite3 import IntegrityError
from api.serializers import PasswordSerializer
from website.aes import *
from website.models import Notes, PasswordModel
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import generics,mixins,permissions,authentication
from api.authentication import TokenAuthentication
import random

def key_gen():
    length=28
    random_key=''
    characters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?><:;0123456789')
    for x in range(length):
           random_key += random.choice(characters)
    return random_key

logo_url={
    'google':'https://www.freepnglogos.com/uploads/google-logo-png/google-logo-png-suite-everything-you-need-know-about-google-newest-0.png',
    'twitter':'https://www.freepnglogos.com/uploads/twitter-logo-png/twitter-bird-symbols-png-logo-0.png',
    'spotify':'https://www.freepnglogos.com/uploads/spotify-logo-png/spotify-icon-marilyn-scott-0.png',
    'instagram':'https://www.freepnglogos.com/uploads/pics-photos-instagram-logo-png-4.png',
    'netflix':'https://www.freepnglogos.com/uploads/netflix-logo-app-png-16.png',
    'snapchat':'https://www.freepnglogos.com/uploads/snapchat-logo-png-0.png'
}

class UserDetailsView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, format=None):
        user=self.request.user
        users = User.objects.filter(username=user)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserRecordView(APIView):
    #permission_classes = [IsAdminUser]

    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
          try:
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
          except Exception as e:
            return Response(
            {
                "error": True,
                "error_msg": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class PasswordView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=self.request.user
        data=PasswordModel.objects.filter(username=user)
        serializer=PasswordSerializer(data,many=True)       
        data = serializer.data
        key_list=logo_url.keys()
        key='5Zy0gKVE(@J$GVtZcWilxil^h47&'
        d=AESCipher(key)
        for i in data:
            login_pass=i['login_password']
            aes_key=i['aes_key']
            login_url=i['login_url']
            e=AESCipher(d._unpad(d.decrypt(aes_key)))
            i['login_password']=e._unpad(e.decrypt(login_pass))
            i.pop('aes_key')
            for j in key_list:
              if j in login_url.split('.'):
                 i['img_url']=logo_url[j]

        return Response(data)      


    def post(self, request):
        user=self.request.user
        data=request.data
        data['username']=user
        login_pass=data['login_password']
        key='5Zy0gKVE(@J$GVtZcWilxil^h47&'
        key_new=key_gen()
        key_new=key_new[0:28]
        d=AESCipher(key_new)
        login_pass=d.encrypt(d._pad(login_pass))
        e=AESCipher(key)
        data['login_password']=login_pass
        aes_key=e.encrypt(e._pad(key_new))
        data['aes_key']=aes_key
        data['img_url']='https://www.survivorsuk.org/wp-content/uploads/2017/01/no-image.jpg'
        serializer = PasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class PasswordDeleteAPIView(generics.DestroyAPIView):
    queryset=PasswordModel.objects.all()
    serializer_class=PasswordSerializer
    lookup_field='pk'
    permission_classes=[IsAuthenticated]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        print("delete successful")