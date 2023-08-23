from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import SignUpSerializer


@api_view(['POST'])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create(
                username=data['username'],
                password=make_password(data['password']),
            )
            
            return Response({"details": f"User {user.username} has been registered"}, status=status.HTTP_201_CREATED)
        else: 
            return Response({"error": f"User with this username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors)