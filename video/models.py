from django.db import models
from django.apps import apps


class video_class(models.Model):
    video = models.FileField(upload_to='videous')
    length_of_video = models.CharField(max_length=10)
    url = models.URLField()
    thumb_image = models.ImageField(upload_to='thumb_image')
    channel = models.ForeignKey('channel.channel_model', on_delete=models.CASCADE)
    like = models.IntegerField()
    dislike =models.IntegerField()
    description = models.CharField(max_length=200)
    playlist = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    is_downloadable =models.BooleanField()
    is_sharable= models.BooleanField()



