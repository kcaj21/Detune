from django.shortcuts import render, redirect
from django.http import HttpResponse
from pytube import YouTube
from .forms import *
import os

def home_view(request):
    form = YouTubeForm()
    
    if request.method == 'POST':
        form = YouTubeForm(request.POST)
        if form.is_valid():
            youtube_url = form.cleaned_data["youtube_url"]
            yt = YouTube(youtube_url)
            video = yt.streams.filter(only_audio=True).first()
            video.download(output_path=os.path.join(os.path.expanduser('~'), 'Downloads'))
    
    return render(request, 'home.html', {'form' : form})

#httpstreamresponse