from rest_framework import generics
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework import status
import requests
from django.core.validators import validate_email
from rest_framework.parsers import MultiPartParser, FormParser
from cloudinary.templatetags import cloudinary

class UserListView(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

class ProfileListView(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = serializers.ProfileSerializer
    def get(self, request, format=None):
        imagens = models.Profile.objects.all()
        serializer = serializers.ProfileSerializer(imagens, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def get_name(request):
    user_id = request.data.get('user_id')
    if(user_id == None):
        return Response({'error':'Falha na requisição.'},status=HTTP_400_BAD_REQUEST)
    try:
        profile = models.Profile.objects.get(user = user_id)
        name = profile.get_name()
        return Response(data={'name': name}, status=HTTP_200_OK)
    except:
        return Response({'error': 'Usuário não existe.'}, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def update_profile(request):
    user_id = request.data.get('user_id')
    name = request.data.get('name')
    email = request.data.get('email')
    photo = request.data.get('photo')

    # Retrieve user and profile data from database
    try:
        user = models.CustomUser.objects.get(id = user_id)
        profile = models.Profile.objects.get(user = user_id)
    except:
        return Response({'error': 'Usuário não existe.'}, status=HTTP_400_BAD_REQUEST)

    profile_name='unchanged'
    profile_photo='unchanged'
    user_email='unchanged'
    # Set name if that is in response
    if(name != None or name):
        profile.set_name(name)
        profile_name = profile.get_name()

    # Set image if that is in response
    if(photo != None or photo):
        profile.set_photo(photo)
        profile_photo = profile.get_photo().url

    if(email != None or email):
        try:
            validate_email(email)
        except:
            return Response({'error': 'Email inválido.'}, status=HTTP_400_BAD_REQUEST)
        # Set new email
        try:
            user.set_email(email)
        except:
            return Response({'error': 'Endereço de email já cadastrado'}, status=HTTP_400_BAD_REQUEST)
        user_email=user.get_email()



    return Response(data={'name': profile_name, 'email': user_email, 'photo': profile_photo}, status=HTTP_200_OK)




@api_view(["POST"])
def get_profile(request):
    user_id = request.data.get('user_id')

    # Request user and profile according to user_id
    try:
        profile = models.Profile.objects.get(user = user_id)
        user = models.CustomUser.objects.get(id = user_id)

    except:
        return Response({'error': 'Usuário inválido.'}, status=HTTP_400_BAD_REQUEST)

    # Get email, name, photo from a certain user/profile
    user_email=user.get_email()
    profile_name = profile.get_name()
    profile_photo = profile.get_photo().url

    return Response(data={'name': profile_name, 'email': user_email, 'photo': profile_photo}, status=HTTP_200_OK)
