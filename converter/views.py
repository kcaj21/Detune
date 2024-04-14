from django.shortcuts import render, redirect
from django.http import HttpResponse
from pytube import YouTube
from .forms import *
from django.core.files.storage import FileSystemStorage

def home_view(request):
    
    if request.method == 'POST':
        form = YouTubeForm(request.POST)
        if form.is_valid():
            youtube_url = form.cleaned_data["youtube_url"]
            yt = YouTube(youtube_url)
            video = yt.streams.filter(only_audio=True).first()
            # video.download(output_path=os.path.join(os.path.expanduser('~'), 'Downloads'))
            video.download(filename='temp_audio.mp3', output_path='songs')
            fs = fs = FileSystemStorage()
            mp3_url = fs.url('temp_audio.mp3')
            
            
            return render(request, 'play_audio.html', {'mp3_url': mp3_url})
    else:
        form = YouTubeForm()
        
    
    return render(request, 'home.html', {'form' : form})
    

#httpstreamresponse
# /home/alex/Coding/Python/detune/temp_audio.mp3