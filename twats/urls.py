from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('<int:tweet_id>/', views.tweet, name='THEtweet'),
    path('users/<str:un>/', views.userFeed, name='tweet'),
    path('feed/', views.feed, name='myFeed'),
    path('like/', views.likeTweet, name="likeTweet"),
    path('draw/', views.drawNew, name="drawNew"),
    path('postImage/<str:file>', views.postImage, name="postImage"),
    path('reply/', views.reply, name="replyTweet"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
