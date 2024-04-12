from django.shortcuts import render
from django.http import HttpResponse
from pytube import YouTube
from .forms import *

def home_view(request):
    form = YouTubeForm()
    
    if request.method == 'POST':
        form = YouTubeForm(request.POST)
    
    return render(request, 'home.html', {'form' : form})

#httpstreamresponse