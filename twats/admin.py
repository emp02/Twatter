from django.contrib import admin
from .models import Tweet, Follow, TweetLike

admin.site.register(Tweet)
admin.site.register(Follow)
admin.site.register(TweetLike)
# Register your models here.
