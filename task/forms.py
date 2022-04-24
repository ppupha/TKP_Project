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