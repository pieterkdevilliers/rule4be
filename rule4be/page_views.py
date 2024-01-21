from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
import json

def load_login_page(request):
    '''
    Loads the login page for PWA
    '''
    if request.method == 'POST':
        print('POST request received')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            user_id = user.id
            return JsonResponse({
                'message': 'Login successful',
                'user_id': user_id,
                'access_token': access_token,
                'refresh_token': refresh_token
            })
        else:
            return JsonResponse({'message': 'Login failed'}, status=401)

    return render(request, 'rule4be/login.html')



    


