from django.db import models

# Create your models here.


class AreaOfLife(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Snapshot(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    area_of_life = models.ForeignKey('AreaOfLife', on_delete=models.CASCADE)
    body = models.TextField(max_length=1500, null=True, blank=True)
    image = models.ImageField(
        upload_to='snapshot-images/', null=True, blank=True)
    video = models.FileField(
        upload_to='snapshot-videos/', null=True, blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.body
