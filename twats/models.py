from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    #poster of tweet
    text = models.CharField(max_length=200)
    isRetweet = False
    originalTwatter = None
    created_at = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.text

    def was_pubished_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_user(self):
        return self.user

class ReplyToTweet(models.Model):
    #prep for future
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

class ReplyToReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(ReplyToTweet, on_delete = models.CASCADE)
    text = models.CharField(max_length=200)

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class ReplyLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(ReplyToTweet, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ReplyToReplyLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(ReplyToReply, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    #u can follow ppl which doesn't mean much at this point but at least it's possible?
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)    #follower
    target = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)    #following

    class Meta:
        unique_together = ('user', 'target')
