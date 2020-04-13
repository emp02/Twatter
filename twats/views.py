from django.shortcuts import get_object_or_404, render, redirect
from .models import Tweet, Follow, ReplyToTweet, ReplyToReply, TweetLike, ReplyLike, ReplyToReplyLike
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        twats = Tweet.objects.order_by('-pub_date')
        following = Follow.objects.filter(user=request.user)
        twatList = []
        for twat in twats:
            for follow in following:
                if twat.user == follow.target:
                    twatList.append(twat)
        context = {'twatList' : twatList}
        return render(request, 'users/index.html', context)
    else:
        return render(request, 'users/index.html')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            un = form.cleaned_data['username']
            pw = form.cleaned_data['password1']
            user = authenticate(username=un, password=pw)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    
    context = {'form' : form}
    return render(request, 'registration/register.html', context)


def tweet(request, tweet_id):
    userTweet = get_object_or_404(Tweet, pk=tweet_id) #get tweet by id
    #display tweet w template
    return render(request, 'twats/twat.html', {'tweet': userTweet})

def feed(request):
    latest_tweet_list = Tweet.objects.order_by('-pub_date')[:5]
    context = {'latest_tweet_list': latest_tweet_list}
    return render(request, 'twats/feed.html', context)

def userFeed(request, un):
    u = User.objects.get(username=un)
    #get tweets of user
    tweets = Tweet.objects.filter(user=u)
    context = {'latest_tweet_list': tweets}
    return render(request, 'twats/feed.html', context)

def like(request, post_id, postType, pageName):
    if postType == "Tweet":
        likeObject, Created = TweetLike.objects.get_or_create(user=request.user, post_id=post_id)
    elif postType == "ReplyToTweet":
        likeObject, Created = ReplyLike.objects.get_or_create(user=request.user, post_id=post_id)
    elif postType == "ReplyToReply":
        likeObject, Created = ReplyToReplyLike.objects.get_or_create(user=request.user, post_id=post_id)
    if not Created:
            #unlike
    return redirect(pageName)
    
    
    
    
    