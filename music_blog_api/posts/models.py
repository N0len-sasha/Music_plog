from django.db import models

class Post(models.Model):
    name = models.CharField()
    audio = models.FileField(upload_to='audio/', null=True, blank=True)