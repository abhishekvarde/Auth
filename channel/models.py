from django.db import models


# from video.models import video_class


class channel_model(models.Model):
    logo = models.ImageField(upload_to='channel_logo')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    followers = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    video_id = models.CharField(max_length=100, null=True, default="")
    # courses = models.CharField(max_length=50)  Foreign key to course table
    playlist = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.title
