from django.db import models

# Create your models here.

class AreaOfLife(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.name
    
class Snapshot(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    area_of_life = models.ForeignKey('AreaOfLife', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body