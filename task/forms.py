from django import forms
from .models import Project, Task
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "deadline")
        widgets = {
           'deadline': forms.DateTimeInput(attrs={'class': 'datetimepicker1 form-control' }),
           'title' : forms.TextInput(attrs={'class': 'form-control'}),
           'description' : forms.Textarea(attrs={'class': 'form-control', 'rows':'10'}),
        }