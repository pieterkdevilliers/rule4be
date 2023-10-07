from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .serializers import UserSerializer

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


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        # Parse the request body as JSON
        data = json.loads(request.body)

        # Get the username and password from the request
        username = data.get('username')
        password = data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Authentication successful
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            # Authentication failed
            return JsonResponse({'message': 'Login failed'}, status=401)

    # Return a 405 Method Not Allowed for other request methods
    return JsonResponse({'message': 'Method not allowed'}, status=405)

