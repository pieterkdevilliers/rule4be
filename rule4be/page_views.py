from django.contrib.auth.models import User
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from snapshots.models import Snapshot
from snapshots.serializers import SnapshotSerializer
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

            # Set tokens in session
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            request.session['user_id'] = user.id

            user_id = user.id
            user = User.objects.get(id=user_id).username

            # Make an API call using the access token
            api_endpoint = 'https://rule4be-fc4445b7e11b.herokuapp.com/snapshots/api/v1/aols'
            headers = {'Authorization': f'Bearer {access_token}'}

            try:
                response = requests.get(api_endpoint, headers=headers)
                response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
                api_data = response.json()

                context = {
                        'api_data': api_data,
                        }

                return render(request, 'rule4be/aols.html', context)
            except requests.exceptions.RequestException as e:
        # Handle request errors, e.g., network issues, server errors
                return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
        else:
            return JsonResponse({'message': 'Login failed'}, status=401)

    return render(request, 'rule4be/login.html')

@login_required
def load_aols_page(request):
    '''
    Loads the AOLs page for PWA
    '''
    access_token = request.session.get('access_token')

    if not access_token:
        return JsonResponse({'message': 'Access token not found'}, status=401)

    # Make an API call using the access token
    api_endpoint = 'https://rule4be-fc4445b7e11b.herokuapp.com/snapshots/api/v1/aols'
    headers = {'Authorization': f'Bearer {access_token}'}

    try:
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        api_data = response.json()

        return render(request, 'rule4be/aols.html', {'api_data': api_data})
    
    except requests.exceptions.RequestException as e:
        # Handle request errors, e.g., network issues, server errors
        return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

@login_required
def load_today_snapshot_page(request, pk):
    '''
    Loads the today snapshot page for PWA
    '''
    access_token = request.session.get('access_token')

    if not access_token:
        return JsonResponse({'message': 'Access token not found'}, status=401)
    

    request.user = User.objects.get(id=request.session.get('user_id'))
    today = timezone.now().date()
    yesterday = today - timezone.timedelta(days=1)
    last_week = today - timezone.timedelta(days=7)
    last_month = today - relativedelta(months=1)
    last_year = today - relativedelta(years=1)

    today_snapshot = Snapshot.objects.filter(created__in=[today], area_of_life=pk)

    if today_snapshot:
        try:
            queryset = Snapshot.objects.filter(created__in=[today, yesterday, last_week, last_month, last_year], area_of_life=pk, owner=request.user)
            serializer = SnapshotSerializer(queryset, many=True)
        
            api_data = serializer.data

            context = {
                        'api_data': api_data,
                        }

            return render(request, 'rule4be/today.html', context)
    
        except requests.exceptions.RequestException as e:
        # Handle request errors, e.g., network issues, server errors
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)





    


