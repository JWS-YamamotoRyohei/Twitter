import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.
class Tweet(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    nicevotes = models.IntegerField(default=0)

    def __str__(self):
        return self.tweet_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Likes(models.Model):
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)