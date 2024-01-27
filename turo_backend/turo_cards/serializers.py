from rest_framework import serializers
from rest_framework.response import Response


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','email']

    def validate(self,data):
        if User.objects.filter(email=data['email']).exists():
            print("validate error")
            raise serializers.ValidationError({'error':'User Already Exists'})
        print("out of validate")
        return data

    def create(self,validated_data):
        print("inside create")
        user=User.objects.create_user(username=validated_data['username'] , email=validated_data['email'],password=validated_data['password'])
        print("created successfully")
        return validated_data
    
class LoginSerializer(serializers.Serializer):
      email =serializers.CharField()
      password = serializers.CharField()

      
    #   def validate(self,data):
        
    #     name=User.objects.get(email=data["email"])

    #     user=authenticate(email=data['email'],password=data['password'])
        
    #     if user is not None:
    #         print("user Checking")
    #         refresh = RefreshToken.for_user(user)
    #         return {
    #            'refresh': str(refresh),
    #            'access': str(refresh.access_token),
    #         } 
    #     else:
    #         return {'status':'400','Message':'Invalid Credentials'}
        
    #   def validate(self,data):
    #     if not User.objects.filter(email=data['email']).exists():
    #         raise serializers.ValidationError({'error':'User Already Exists'})
    #     print("validate error")
    #     return data
      
    #   def get_jwt_token(self,data):
    #       print("authentication")
    #       print(data['email'])
    #       print(data['password'])
    #       name=User.objects.get(email=data["email"])
    #       print(name.username)
    #       user=authenticate(username=name.username,password=data['password'])
    #       print(user)
    #       if user is None:
    #         return {'status':'400','message': 'invalid credentials'}
          
    #       refresh = RefreshToken.for_user(user)
    #       print("Hello")
    #       return {'message' : 'login successfully' , 'data': {'token':{'refresh': str(refresh),'access': str(refresh.access_token),}}}
            
class TuroCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuroCards
        fields = "__all__"