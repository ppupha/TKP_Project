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

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=45)
    description = models.TextField(max_length=300, blank=False)
    deadline = models.DateTimeField(default=timezone.now)
    done = models.BooleanField(default=False)
    creationDate = models.DateField(auto_now_add=True)
    noti = models.CharField(max_length=3, default='000')
    completed_day = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Notification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    creationDate = models.DateTimeField(auto_now_add= True)
    actived = models.BooleanField(default= False)

    def __str__(self):
        return self.task.title