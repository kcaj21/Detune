from django.shortcuts import render, redirect
from django.http import HttpResponse
from pytube import YouTube
from .models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
import os
import glob
import subprocess
import librosa
import soundfile
import pyrubberband


def home_view(request):
    
    if request.method == 'POST':
        form = YouTubeForm(request.POST)
        
        if glob.glob('songs/converted_to_wav_file.wav'):
            os.remove('songs/converted_to_wav_file.wav')
        
        if form.is_valid():
            
            #pytube will take youtube video url posted to download the audio from the video
            
            youtube_url = form.cleaned_data["youtube_url"]
            form_steps = form.cleaned_data["steps"]
            yt = YouTube(youtube_url)
            video = yt.streams.filter(only_audio=True).first()
            
            #The audio is temporarily saved as an mp3 file
            
            video.download(filename='temp_audio.mp3', output_path='songs')
            
            
            fs = FileSystemStorage()
            
            temp_url = fs.url('temp_audio.mp3')
            
            # convert mp3 to wav file - calls subprocess to convert with ffmpeg package on local machine. Need to ensure ffmpeg is installed on VM in production (if sticking with this method, PyDub is another option)
            subprocess.call(['ffmpeg', '-i', os.getcwd() + temp_url, 
                 'songs/converted_to_wav_file.wav'])
            
            #librosa will load the mp3 and store the time series (y) and sample rate (sr) variables
            
            #Try instead of librosa: https://pyrubberband.readthedocs.io/en/stable/generated/pyrubberband.pyrb.pitch_shift.html
                        
            # y, sr = librosa.load('songs/converted_to_wav_file.wav')
            
            # new_y = librosa.effects.pitch_shift(y, sr = sr, n_steps=form_steps)
            
            y, sr = soundfile.read('songs/converted_to_wav_file.wav')
            
            new_y = pyrubberband.pitch_shift(y, sr, form_steps)
            
            #soundfile does not support mp3, need to find way to convert from wav back to mp3
            
            soundfile.write("songs/pitchShifted.wav", new_y, sr)
            
            
            convertedWav_url = fs.url('pitchShifted.wav')
            
            return render(request, 'play_audio.html', {'convertedWav_url': convertedWav_url})

    else:
        form = YouTubeForm()
        
    
    return render(request, 'home.html', {'form' : form})
    

#httpstreamresponse