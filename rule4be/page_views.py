from django.contrib.auth.models import User
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime
from snapshots.models import Snapshot
from snapshots.serializers import SnapshotSerializer
import json
from snapshots.models import AreaOfLife, Snapshot
from snapshots.forms import AreaOfLifeForm, SnapshotForm

def load_login_page(request):
    '''
    Loads the login page for PWA
    '''
    
    if request.method == 'POST':

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

            aols = request.user.areaoflife_set.all()

            context = {
                    'aols': aols,
                    }

            return render(request, 'rule4be/aols.html', context)
        else:
            return JsonResponse({'message': 'Login failed'}, status=401)
    
    elif request.session.get('access_token'):

        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id).username

        aols = request.user.areaoflife_set.all()

        context = {
                'aols': aols,
                }
        
        return render(request, 'rule4be/aols.html', context)
    else:

        return render(request, 'rule4be/login.html')


@login_required
def load_aols_page(request):
    '''
    Loads the AOLs page for PWA
    '''
    aols = request.user.areaoflife_set.all()
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timezone.timedelta(days=1)).strftime('%Y-%m-%d')
    last_week = (datetime.now() - timezone.timedelta(days=7)).strftime('%Y-%m-%d')
    last_month = (datetime.now() - relativedelta(months=1)).strftime('%Y-%m-%d')
    last_year = (datetime.now() - relativedelta(years=1)).strftime('%Y-%m-%d')
    
    for aol in aols:
        aol.snapshots = {
            'today' : Snapshot.objects.filter(created=today, area_of_life=aol),
            'yesterday' : Snapshot.objects.filter(created=yesterday, area_of_life=aol),
            'last_week' : Snapshot.objects.filter(created=last_week, area_of_life=aol),
            'last_month' : Snapshot.objects.filter(created=last_month, area_of_life=aol),
            'last_year' : Snapshot.objects.filter(created=last_year, area_of_life=aol),
        }

    context = {
        'aols': aols,
    }

    return render(request, 'rule4be/aols.html', context)


from django.utils import timezone
import datetime

@login_required
def load_today_snapshot_page(request, pk):
    '''Loads the today snapshot page for PWA'''
    access_token = request.session.get('access_token')
    if not access_token:
        return JsonResponse({'message': 'Access token not found'}, status=401)

    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    last_week = today - datetime.timedelta(days=7)
    last_month = today - relativedelta(months=1)
    last_year = today - relativedelta(years=1)

    today_snapshot = Snapshot.objects.filter(created__in=[today], area_of_life=pk)

    if today_snapshot:
        try:
            queryset = Snapshot.objects.filter(
                created__in=[today, yesterday, last_week, last_month, last_year],
                area_of_life=pk,
                owner=request.user
            )
            serialized_data = []
            for snapshot in queryset:
                snapshot_data = SnapshotSerializer(snapshot).data
                created_date = snapshot.created
                if created_date == today:
                    snapshot_data['relative_date'] = "Today"
                elif created_date == yesterday:
                    snapshot_data['relative_date'] = "Yesterday"
                elif created_date == last_week:
                    snapshot_data['relative_date'] = "Last Week"
                elif created_date == last_month:
                    snapshot_data['relative_date'] = "Last Month"
                elif created_date == last_year:
                    snapshot_data['relative_date'] = "Last Year"
                else:
                    snapshot_data['relative_date'] = created_date
                serialized_data.append(snapshot_data)

            context = {'api_data': serialized_data}
            return render(request, 'rule4be/today.html', context)
        except requests.exceptions.RequestException as e:
            # Handle request errors, e.g., network issues, server errors
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    else:
        context = {'today_snapshot': today_snapshot}
        return render(request, 'rule4be/today.html', context)


############################################################################################################
# CRUD Views
############################################################################################################
    
@login_required
def create_aol(request):
    '''
    Creates a new Area of Life
    '''
    if request.method == 'POST':
        form = AreaOfLifeForm(request.POST)
        if form.is_valid():
            aol = form.save(commit=False)
            aol.owner = request.user
            aol.save()
            return JsonResponse({'message': 'Area of life created successfully'})
        else:
            return JsonResponse({'message': 'Invalid form data'}, status=400)
    else:
        form = AreaOfLifeForm()

        return render(request, 'rule4be/create_aol.html', {'form': form})


@login_required
def edit_aol(request, aol_id):
    '''
    Edits an Area of Life
    '''
    aol = AreaOfLife.objects.get(id=aol_id)
    if request.method == 'POST':
        form = AreaOfLifeForm(request.POST, instance=aol)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Area of life updated successfully'})
        else:
            return JsonResponse({'message': 'Invalid form data'}, status=400)
    else:
        form = AreaOfLifeForm(instance=aol)

        return render(request, 'rule4be/edit_aol.html', {'form': form, 'aol_id': aol_id})


@login_required
def delete_aol(request, aol_id):
    ''' Deletes an Area of Life '''
    if request.method == 'POST':
        aol = AreaOfLife.objects.get(id=aol_id)
        aol.delete()
        return JsonResponse({'message': 'Area of life deleted successfully'})
    else:
        aol = AreaOfLife.objects.get(id=aol_id)
        return render(request, 'rule4be/delete_aol.html', {'aol': aol})
    

@login_required
def create_snapshot(request, aol_id):
    '''
    Creates a new Snapshot
    '''
    aol = AreaOfLife.objects.get(id=aol_id)
    if request.method == 'POST':
        form = SnapshotForm(request.POST)
        if form.is_valid():
            snapshot = form.save(commit=False)
            snapshot.owner = request.user
            snapshot.area_of_life = aol
            snapshot.save()
            return JsonResponse({'message': 'Snapshot created successfully'})
        else:
            return JsonResponse({'message': 'Invalid form data'}, status=400)
    else:
        form = SnapshotForm()

        return render(request, 'rule4be/create_snapshot.html', {'form': form, 'aol_id': aol_id})