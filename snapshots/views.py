from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import AreaOfLife, Snapshot
from .serializers import AOLSerializer, SnapshotSerializer
from django.contrib.auth.models import User

# Create your views here.
@api_view(['GET', 'POST'])
def area_of_life_list(request):
    """
    Retrieves a list of all AOLs.
    """
    if request.method == 'GET':
        queryset = AreaOfLife.objects.filter(owner=request.user)
        serializer = AOLSerializer(queryset, many=True)
    elif request.method == 'POST':
        serializer = AOLSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
    
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def area_of_life_detail(request, pk):
    """
    Retrieves, edits or deletes a single AOL.
    """
    area_of_life = get_object_or_404(AreaOfLife, id=pk)

    if request.method == 'GET':
        serializer = AOLSerializer(area_of_life)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = AOLSerializer(area_of_life, data=request.data, context={'request': request}, partial=request.method == 'PATCH')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        area_of_life.delete()
        return Response(status=204)
    

@api_view(['GET', 'POST'])
def snapshot_list(request):
    """
    Retrieves a list of all AOLs.
    """
    if request.method == 'GET':
        queryset = Snapshot.objects.filter(owner=request.user)
        serializer = SnapshotSerializer(queryset, many=True)
    elif request.method == 'POST':
        serializer = SnapshotSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
    
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def snapshot_detail(request, pk):
    """
    Retrieves, edits, or deletes a single Snapshot.
    """
    snapshot = get_object_or_404(Snapshot, id=pk)

    if request.method == 'GET':
        serializer = SnapshotSerializer(snapshot)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = SnapshotSerializer(snapshot, data=request.data, context={'request': request}, partial=request.method == 'PATCH')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        snapshot.delete()
        return Response(status=204)


@api_view()
def today_snapshot_list(request, pk):
    """
    Retrieves a list of all snapshots for today's date.
    """
    request.user = User.objects.get(id=request.session.get('user_id'))
    today = timezone.now().date()
    yesterday = today - timezone.timedelta(days=1)
    last_week = today - timezone.timedelta(days=7)
    last_month = today - relativedelta(months=1)
    last_year = today - relativedelta(years=1)

    today_snapshot = Snapshot.objects.filter(created__in=[today], area_of_life=pk)

    if today_snapshot:
        queryset = Snapshot.objects.filter(created__in=[today, yesterday, last_week, last_month, last_year], area_of_life=pk, owner=request.user)
        serializer = SnapshotSerializer(queryset, many=True)

        return Response(serializer.data)
    else:
        return Response({'message': 'No snapshots for today.'})
    