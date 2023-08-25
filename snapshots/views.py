from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import AreaOfLife, Snapshot
from .serializers import AOLSerializer, SnapshotSerializer

# Create your views here.
@api_view()
def area_of_life_list(request):
    """
    Retrieves a list of all AOLs.
    """
    queryset = AreaOfLife.objects.all()
    serializer = AOLSerializer(queryset, many=True)
    
    return Response(serializer.data)


@api_view()
def area_of_life_detail(request, pk):
    """
    Retrieves a single AOL.
    """
    area_of_life = get_object_or_404(AreaOfLife, id=pk)
    serializer = AOLSerializer(area_of_life)
    
    return Response(serializer.data)

@api_view()
def snapshot_list(request):
    """
    Retrieves a list of all AOLs.
    """
    queryset = Snapshot.objects.all()
    serializer = SnapshotSerializer(queryset, many=True)
    
    return Response(serializer.data)


@api_view()
def snapshot_detail(request, pk):
    """
    Retrieves a single AOL.
    """
    snapshot = get_object_or_404(Snapshot, id=pk)
    serializer = SnapshotSerializer(snapshot)
    
    return Response(serializer.data)


@api_view()
def today_snapshot_list(request, pk):
    """
    Retrieves a list of all snapshots for today's date.
    """

    today = timezone.now().date()
    yesterday = today - timezone.timedelta(days=1)
    last_week = today - timezone.timedelta(days=7)
    last_month = today - relativedelta(months=1)
    last_year = today - relativedelta(years=1)

    today_snapshot = Snapshot.objects.filter(created__in=[today], area_of_life=pk)
    yesterday_snapshot = Snapshot.objects.filter(created__in=[yesterday], area_of_life=pk)
    last_week_snapshot = Snapshot.objects.filter(created__in=[last_week], area_of_life=pk)
    last_month_snapshot = Snapshot.objects.filter(created__in=[last_month], area_of_life=pk)
    last_year_snapshot = Snapshot.objects.filter(created__in=[last_year], area_of_life=pk)

    snapshots = [today_snapshot, yesterday_snapshot, last_week_snapshot, last_month_snapshot, last_year_snapshot]

    if today_snapshot:
        queryset = Snapshot.objects.filter(created__in=[today, yesterday, last_week, last_month, last_year], area_of_life=pk)
        # queryset = snapshots
        serializer = SnapshotSerializer(queryset, many=True)

        return Response(serializer.data)
    else:
        return Response({'message': 'No snapshots for today.'})