from django.shortcuts import render, redirect
from django.http import HttpResponse
from pytube import YouTube
from .forms import *
from django.core.files.storage import FileSystemStorage
import os
import glob
import librosa
import soundfile


def home_view(request):
    
    if request.method == 'POST':
        form = YouTubeForm(request.POST)
        
        # if glob.glob('songs/temp_audio.mp3'):
        #     os.remove('songs/temp_audio.mp3')
        
        if form.is_valid():
            
            #pytube will take youtube video url posted to download the audio from the video
            
            youtube_url = form.cleaned_data["youtube_url"]
            yt = YouTube(youtube_url)
            video = yt.streams.filter(only_audio=True).first()
            
            #The audio is temporarily saved as an mp3 file
            
            video.download(filename='temp_audio.mp3', output_path='songs')
            
            #librosa will load the mp3 and store the time series (y) and sample rate (sr) variables
            
            fs = FileSystemStorage()
            
            temp_url = fs.url('temp_audio.mp3')
                        
            y, sr = librosa.load('songs/temp_audio.mp3')
            
            new_y = librosa.effects.pitch_shift(y, sr = sr, n_steps=1)
            
            #soundfile does not support mp3, need to find way to convert from wav back to mp3
            
            soundfile.write("songs/pitchShifted.wav", new_y, sr)
            
            # print(new_y)
            
            return render(request, 'play_audio.html', {'mp3_url': temp_url})

    else:
        form = YouTubeForm()
        
    
    return render(request, 'home.html', {'form' : form})
    

#httpstreamresponse