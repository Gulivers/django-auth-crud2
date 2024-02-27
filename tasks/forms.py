from django import forms
from django.forms.models import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important', 'datecompleted',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'datecompleted': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
         
        