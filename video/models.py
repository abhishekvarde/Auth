from django.db import models


class video_class(models.Model):
    channel_id = models.IntegerField(default=0)
    video = models.FileField(upload_to='video')
    length_of_video = models.IntegerField(default=0)
    url = models.URLField()
    thumb_image = models.ImageField(upload_to='thumb_image')
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    playlist = models.CharField(max_length=100, default='video')
    title = models.CharField(max_length=100)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    is_downloadable = models.BooleanField(default=False)
    is_sharable = models.BooleanField(default=False)
# PlayList
