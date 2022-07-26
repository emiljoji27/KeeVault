from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from website.models import Notes, PasswordModel
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator



class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notes
        fields=['title','content','note_length']
    
    def get_length_of_note(self,obj):
        return obj.note_length()


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordModel
        fields = (
            'id',
            'name',
            'login_username',
            'login_password',
            'login_url',
            'aes_key',
            'img_url',
        )


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
