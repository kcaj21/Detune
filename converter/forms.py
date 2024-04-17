# from django.forms import ModelForm
from django import forms
from django.forms import ModelForm
from .models import *


# class YouTubeForm(forms.Form):
#     youtube_url = forms.URLField(label='YouTube Video URL')

class YouTubeForm(ModelForm):
    class Meta:
        model = Song
        fields = ['youtube_url', 'steps']
        labels = {
            'youtube_url' : '',
            'steps' : 'Number of Semitones'
            
        }
        widgets = {
            'youtube_url' : forms.TextInput(attrs={
                'placeholder': 'enter youtube video url...',
                'class': ' text-xl text-center text-slate-500 border-2 rounded-md border-[#50C878]'
            }),
            'steps': forms.NumberInput(attrs={   
                'max': '14',
                'min': '-14',
                'class': 'w-12 mt-4 text-xl text-center text-slate-500 border-2 rounded-md border-[#50C878]'
            })        
        }