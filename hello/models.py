from django.db import models

# Create your models here.
class Requests(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    who = models.CharField(max_length=20)