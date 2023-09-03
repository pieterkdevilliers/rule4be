from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from .serializers import UserSerializer
from django.contrib.auth.models import User

@api_view(['POST'])
def user_register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user_data = serializer.validated_data
        print(user_data)

        # Retrieve password values from 'password1' and 'password2' fields
        password1 = user_data.pop('password1')
        password2 = user_data.pop('password2')

        # Check that the passwords match
        if password1 == password2:
            # Hash the password before saving
            user_data['password'] = make_password(password1)
            user = User.objects.create(**user_data)

            # Login the user
            login(request, user)

            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
