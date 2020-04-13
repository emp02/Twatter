from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('<int:tweet_id>/', views.tweet, name='THEtweet'),
    path('users/<str:un>/', views.userFeed, name='tweet'), 
    path('')
]