from django.db import models
# from video.models import video_class


class channel_model(models.Model):
    logo = models.ImageField(upload_to='channel_logo')
    title =models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    followers =models.IntegerField()
    total_views = models.IntegerField()
    # video = models.ManyToOneRel(video_class, on_delete=models.CASCADE,null=True)
    courses = models.CharField(max_length=50)
    playlist = models.CharField(max_length=50)