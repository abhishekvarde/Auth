from django.db import models
import datetime
from bson import utc

class video_class(models.Model):
    channel_id = models.IntegerField(default=0)
    video = models.FileField(upload_to='video')
    length_of_video = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    playlist = models.CharField(max_length=100, default='video')
    tags = models.CharField(max_length=255)
    url = models.URLField()
    thumb_image = models.ImageField(upload_to='thumb_image')
    views = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    is_downloadable = models.BooleanField(default=False)
    is_sharable = models.BooleanField(default=False)

    def get_time_diff(self):
        if self.uploaded_on:
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - self.uploaded_on
            return timediff.total_seconds()/60
# PlayList
