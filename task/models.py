from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=45)
    creationDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
