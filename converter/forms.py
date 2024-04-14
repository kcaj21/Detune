# from django.forms import ModelForm
from django import forms
from .models import *


class YouTubeForm(forms.Form):
    youtube_url = forms.URLField(label='YouTube Video URL')