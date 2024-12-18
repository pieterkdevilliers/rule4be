from django import forms
from .models import AreaOfLife, Snapshot

class AreaOfLifeForm(forms.ModelForm):
    class Meta:
        model = AreaOfLife
        fields = ['name', 'description', 'is_archived']

class SnapshotForm(forms.ModelForm):
    class Meta:
        model = Snapshot
        fields = ['body', 'image', 'video']