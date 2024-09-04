import datetime
from datetime import datetime, timedelta
import requests
import json
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from dateutil.relativedelta import relativedelta
from snapshots.serializers import SnapshotSerializer
from snapshots.models import AreaOfLife, Snapshot
from snapshots.forms import AreaOfLifeForm, SnapshotForm
from rule4be.ses import send_custom_email
from users.models import UserProfile


def load_signup_page(request):
    '''
    Loads the sign-up page for PWA
    '''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.save()

            # Create a user profile
            user_profile = UserProfile.objects.create(
                user=user,
                trial_end_date=(datetime.now() + timezone.timedelta(days=30)),
            )
            user_profile.save()

            # Automatically log in the user after sign-up
            login(request, user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Set tokens in session
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            request.session['user_id'] = user.id

            # Send a welcome email
            subject = 'Welcome to Rule4!'
            body = 'Thank you for signing up for Rule4. We are glad to have you!'
            send_custom_email(subject, body, user.email)

            aols = request.user.areaoflife_set.all()

            context = {
                'aols': aols,
            }

            return render(request, 'rule4be/aols.html', context)
        else:
            return HttpResponse('Username already exists')
    else:
        return render(request, 'rule4be/signup.html')


def load_login_signup_section(request):
    '''
    Loads the login/signup section for PWA
    '''

    return render(request, 'rule4be/login_signup_section.html')


def load_login_page(request):
    '''
    Loads the login page for PWA.
    If the user is already authenticated, redirects to a different page.
    '''
    if request.user.is_authenticated:
        return redirect('load_aols_page')

    body_class = 'access-page'
    return render(request, 'rule4be/login.html', {'body_class': body_class})


def load_login_form(request):
    '''
    Loads the login form for PWA
    '''
    body_class = 'access-page'
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        user = authenticate(request, username=username, password=password)
        print(user)
        try:
            profile = UserProfile.objects.get(user=user)
            account_status = profile.account_status
        except:
            profile = None
            account_status = None
        context = {
            'profile': profile,
        }

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

            today = timezone.now().date()
            yesterday = today - timedelta(days=1)
            if profile.trial_end_date == yesterday:
                profile.account_status = 'expired_trial'
                profile.save()

            context = {
                'aols': aols,
                'profile': profile,
            }
            if account_status == 'expired_trial' or account_status == 'cancelled_subscription':
                return render(request, 'rule4be/trial_expired.html', context)
            else:
                return redirect('load_aols_page')
                # return render(request, 'rule4be/aols.html', context)
        else:
            print('Login failed')
            return HttpResponse('Login failed')

    elif request.session.get('access_token'):

        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id).username

        aols = request.user.areaoflife_set.all()

        context = {
            'aols': aols,
        }

        return redirect('load_aols_page')
        # return render(request, 'rule4be/aols.html', context)
    else:
        # return redirect('load_aols_page')
        return render(request, 'rule4be/login_form.html', {'body_class': body_class})


def logout_view(request):
    '''
    Logs out the user and redirects to the login page
    '''
    logout(request)
    return redirect('load_login_page')


@login_required
def load_aols_page(request):
    '''
    Loads the AOLs page for PWA
    '''
    body_class = 'main-app'
    aols = request.user.areaoflife_set.all()
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timezone.timedelta(days=1)
                 ).strftime('%Y-%m-%d')
    last_week = (datetime.now() - timezone.timedelta(days=7)
                 ).strftime('%Y-%m-%d')
    last_month = (datetime.now() - relativedelta(months=1)
                  ).strftime('%Y-%m-%d')
    three_months = (datetime.now() - relativedelta(months=3)
                    ).strftime('%Y-%m-%d')
    six_months = (datetime.now() - relativedelta(months=6)
                  ).strftime('%Y-%m-%d')
    last_year = (datetime.now() - relativedelta(years=1)
                 ).strftime('%Y-%m-%d')
    two_years = (datetime.now() - relativedelta(years=2)
                 ).strftime('%Y-%m-%d')
    three_years = (datetime.now() - relativedelta(years=3)
                   ).strftime('%Y-%m-%d')
    five_years = (datetime.now() - relativedelta(years=5)
                  ).strftime('%Y-%m-%d')
    ten_years = (datetime.now() - relativedelta(years=10)
                 ).strftime('%Y-%m-%d')

    for aol in aols:
        aol.snapshots = {
            'today': Snapshot.objects.filter(created=today, area_of_life=aol),
            'yesterday': Snapshot.objects.filter(created=yesterday, area_of_life=aol),
            'last_week': Snapshot.objects.filter(created=last_week, area_of_life=aol),
            'last_month': Snapshot.objects.filter(created=last_month, area_of_life=aol),
            'three_months': Snapshot.objects.filter(created=three_months, area_of_life=aol),
            'six_months': Snapshot.objects.filter(created=six_months, area_of_life=aol),
            'last_year': Snapshot.objects.filter(created=last_year, area_of_life=aol),
            'two_years': Snapshot.objects.filter(created=two_years, area_of_life=aol),
            'three_years': Snapshot.objects.filter(created=three_years, area_of_life=aol),
            'five_years': Snapshot.objects.filter(created=five_years, area_of_life=aol),
            'ten_years': Snapshot.objects.filter(created=ten_years, area_of_life=aol),
        }

    context = {
        'aols': aols,
        'body_class': body_class,
    }

    return render(request, 'rule4be/aols.html', context)


@login_required
def load_today_snapshot_page(request, pk):
    '''Loads the today snapshot page for PWA'''
    print('load_today_snapshot_page')
    access_token = request.session.get('access_token')
    if not access_token:
        return HttpResponse('Access token not found')

    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)
    last_month = today - relativedelta(months=1)
    three_months = today - relativedelta(months=3)
    six_months = today - relativedelta(months=6)
    last_year = today - relativedelta(years=1)
    two_years = today - relativedelta(years=2)
    three_years = today - relativedelta(years=3)
    five_years = today - relativedelta(years=5)
    ten_years = today - relativedelta(years=10)

    today_snapshot = Snapshot.objects.filter(
        created__in=[today], area_of_life=pk)

    if today_snapshot:
        try:
            queryset = Snapshot.objects.filter(
                created__in=[today, yesterday,
                             last_week, last_month, three_months, six_months,
                             last_year, two_years, three_years, five_years, ten_years],
                area_of_life=pk,
                owner=request.user,
            ).order_by('-created')
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
                elif created_date == three_months:
                    snapshot_data['relative_date'] = "3 Months Ago"
                elif created_date == six_months:
                    snapshot_data['relative_date'] = "6 Months Ago"
                elif created_date == last_year:
                    snapshot_data['relative_date'] = "Last Year"
                elif created_date == two_years:
                    snapshot_data['relative_date'] = "2 Years Ago"
                elif created_date == three_years:
                    snapshot_data['relative_date'] = "3 Years Ago"
                elif created_date == five_years:
                    snapshot_data['relative_date'] = "5 Years Ago"
                elif created_date == ten_years:
                    snapshot_data['relative_date'] = "10 Years Ago"
                else:
                    snapshot_data['relative_date'] = created_date
                serialized_data.append(snapshot_data)

            context = {'api_data': serialized_data}

            return render(request, 'rule4be/today.html', context)
        except requests.exceptions.RequestException as e:
            # Handle request errors, e.g., network issues, server errors
            return HttpResponse(f'Error: {str(e)}')
    else:
        context = {'today_snapshot': today_snapshot}
        return render(request, 'rule4be/today.html', context)


@login_required
def load_user_profile(request):
    '''Loads the user profile page for PWA'''
    user = request.user
    profile = UserProfile.objects.get(user=user)
    page_title = f'{user.username}\'s Profile'
    context = {
        'user': user,
        'page_title': page_title,
        'profile': profile,
    }
    return render(request, 'rule4be/profile.html', context)


@login_required
def load_trial_expired_page(request):
    '''Loads the trial expired page for PWA'''
    user = request.user
    profile = UserProfile.objects.get(user=user)
    page_title = 'TRIAL EXPIRED'
    context = {
        'user': user,
        'page_title': page_title,
        'profile': profile,
    }
    return render(request, 'rule4be/trial_expired.html', context)


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
            return HttpResponse('Area of life created successfully')
        else:
            return HttpResponse('Invalid form data')
    else:
        form = AreaOfLifeForm()

        return render(request, 'rule4be/create_aol.html', {'form': form})


@login_required
def edit_aol(request, aol_id):
    ''' Edits an Area of Life '''
    aol = AreaOfLife.objects.get(id=aol_id)
    if request.method == 'POST':
        form = AreaOfLifeForm(request.POST, instance=aol)
        if form.is_valid():
            form.save()
            return HttpResponse('Area of life updated successfully')
        else:
            return HttpResponse('Invalid form data')
    else:
        form = AreaOfLifeForm(instance=aol)
        return render(request, 'rule4be/edit_aol.html', {'form': form, 'aol_id': aol_id})


@login_required
def delete_aol(request, aol_id):
    ''' Deletes an Area of Life '''
    if request.method == 'POST':
        aol = AreaOfLife.objects.get(id=aol_id)
        aol.delete()
        return HttpResponse('Area of life deleted successfully')
    else:
        aol = AreaOfLife.objects.get(id=aol_id)
        return render(request, 'rule4be/delete_aol.html', {'aol': aol})


@login_required
def create_snapshot(request, aol_id):
    '''
    Creates a new Snapshot
    '''
    aol = get_object_or_404(AreaOfLife, id=aol_id)
    if request.method == 'POST':
        form = SnapshotForm(request.POST, request.FILES)
        if form.is_valid():
            snapshot = form.save(commit=False)
            snapshot.owner = request.user
            snapshot.area_of_life = aol
            snapshot.save()
            return HttpResponse('Snapshot created successfully')
        else:
            return HttpResponse('Invalid form data')
    else:
        form = SnapshotForm()

    return render(request, 'rule4be/create_snapshot.html', {'form': form, 'aol_id': aol_id})


############################################################################################################
# Terms and Provacy Policy
############################################################################################################


def terms_and_conditions(request):
    '''Loads the terms and conditions page'''
    return render(request, 'rule4be/terms_and_conditions.html')


def privacy_policy(request):
    '''Loads the privacy policy page'''
    return render(request, 'rule4be/privacy_policy.html')
