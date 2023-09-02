from django.shortcuts import render
# in your views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from allauth.account.forms import SignupForm
from allauth.account import views as allauth_views
from .serializers import LoginSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    if request.method == 'POST':
        form = SignupForm(request.data)
        if form.is_valid():
            user = form.save(request)
            login(request, user)
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    print(request.data)
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['username']
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

# Create your views here.
