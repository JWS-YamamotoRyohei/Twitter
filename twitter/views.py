from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from .forms import TweetForm
from django.utils import timezone

def index(request):
    latest_tweet_list = Tweet.objects.all().order_by('-pub_date')[:5]
    context = {'latest_tweet_list': latest_tweet_list}
    return render(request, 'twitter/index.html', context)

@login_required
def tweetlist(request):
    latest_tweet_list = Tweet.objects.all().order_by('-pub_date')[:5]
    context = {'latest_tweet_list': latest_tweet_list}
    return render(request, 'twitter/tweetlist.html', context)

@login_required
def detail(request, tweet_id):
    user = request.user
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if request.method == 'POST':
            tweet.nicevotes += 1
            tweet.save()
            context = {'user':user,'tweet': tweet}
            return render(request, 'twitter/detail.html', context)

    context = {'user':user,'tweet': tweet}
    return render(request, 'twitter/detail.html', context)


def results(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    return render(request, 'twitter/results.html', {'tweet': tweet})

@login_required

def tweet_new(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.pub_date =timezone.now()
            tweet.save()
            return redirect('twitter:detail',tweet_id=tweet.pk)
    else:
        form = TweetForm()
    return render(request, 'twitter/tweet_new.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('twitter:tweetlist')
    else:
        form = SignUpForm()

    context = {'form':form}
    return render(request, 'twitter/signup.html', context)