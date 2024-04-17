from django.db import models
import uuid
    
class Song(models.Model):
    youtube_url = models.URLField(max_length=500, null=True)
    steps = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
