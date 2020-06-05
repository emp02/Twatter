from django.shortcuts import get_object_or_404, render, redirect
from .models import Tweet, Follow, ReplyToTweet, ReplyToReply, TweetLike, ReplyLike, ReplyToReplyLike
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.utils import timezone

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        latest_tweet_list = Tweet.objects.order_by('-pub_date')[:5]
        context = {'latest_tweet_list': latest_tweet_list}
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
    numLikes = TweetLike.objects.filter(tweet=userTweet).count()
    replies = ReplyToTweet.objects.filter(tweet=userTweet)
    #display tweet w template
    return render(request, 'twats/twat.html', {'tweet': userTweet, 'numLikes': numLikes, 'replies':replies})

def feed(request):
    if request.user.is_authenticated:
        twats = Tweet.objects.order_by('-pub_date')
        following = Follow.objects.filter(user=request.user)
        twatList = []
        for twat in twats:
            for follow in following:
                if twat.user == follow.target:
                    twatList.append(twat)
        context = {'twatList' : twatList}
        return render(request, 'twats/feed.html', context)
    else:
        return render(request, 'twats/feed.html')

def userFeed(request, un):
    u = User.objects.get(username=un)
    #get tweets of user
    tweets = Tweet.objects.filter(user=u)
    context = {'latest_tweet_list': tweets}
    return render(request, 'twats/feed.html', context)

"""
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

"""

def likeTweet(request):
    tw = get_object_or_404(Tweet, id=request.POST.get('tweet_id'))
    un = request.user
    like = TweetLike(user=un, tweet=tw)
    like.save()
    return redirect('index')

def drawNew(request):
    return render(request, 'twats/makeDrawing.html')


def postImage(request, file):
    newImage = Tweet(user=request.user, text=file, pub_date=timezone.now())
    newImage.save()
    return redirect('index')


def reply(request):
    tw = get_object_or_404(Tweet, id=request.POST.get('tweet_id'))
    un = request.user
    reply = ReplyToTweet(user=un, tweet=tw, text=request.POST.get('replyText'))
    reply.save()
    numLikes = TweetLike.objects.filter(tweet=tw).count()
    replies = ReplyToTweet.objects.filter(tweet=tw)
    return render(request, 'twats/twat.html', {'tweet': tw, 'numLikes': numLikes, 'replies': replies})
