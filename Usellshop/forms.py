from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=['username','email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email


class CourseForm(forms.ModelForm):
    thumbnail=forms.ImageField()
    class Meta:
        model=Course
        fields='__all__'

class TagForm(forms.ModelForm):
    class Meta:
        model=Tag
        exclude=['course']

class PrerequisiteForm(forms.ModelForm):
    class Meta:
        model=Prerequisite
        exclude=['course']

class LearningForm(forms.ModelForm):
    class Meta:
        model=Learning
        exclude=['course']

class VideoForm(forms.ModelForm):
    video=forms.FileField()
    notes=forms.FileField(required=False)
    class Meta:
        model=Video
        exclude=['course']
