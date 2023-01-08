from django.shortcuts import render

# Create your views here.

from .forms import *
import joblib
import re
from pathlib import Path
import math
from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import os
import nltk
import pycountry
import re
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud, STOPWORDS
import io
import urllib, base64

BASE_DIR = Path(__file__).resolve().parent.parent

API_KEY = ''
API_SECRET_KEY = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

consumerKey = API_KEY
consumerSecret = API_SECRET_KEY
accessToken = ACCESS_TOKEN
accessTokenSecret = ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)


def percentage(part,whole):
     return 100 * float(part)/float(whole)

def text_form(request):
    args = {}
    if request.method == "POST":
        form = TextForm(request.POST)
        args['form'] = form
        if form.is_valid():
            text = form.cleaned_data['text']
            keyword = text
            noOfTweet = 100
            tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang="en").items(noOfTweet)
            positive = 0
            negative = 0
            neutral = 0
            count = 0
            for tweet in tweets:
                #print(tweet.text)
                analysis = TextBlob(tweet.text)
                score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
                neg = score['neg']
                neu = score['neu']
                pos = score['pos']
                comp = score['compound']
                count += 1
            
                if neg > pos:
                    negative += 1
                    #print('negative')
                elif pos > neg:
                    positive += 1
                    #print('positive')
                
                elif pos == neg:
                    neutral += 1


            if (count !=0):
                positive = percentage(positive, noOfTweet)
                negative = percentage(negative, noOfTweet)
                neutral = percentage(neutral, noOfTweet)
                args['first'] = 0
                args['text'] = text
                args['negative'] = math.floor(negative)
                args['neutral'] = math.floor(neutral)
                args['positive'] = math.ceil(positive)
                if (negative<positive):
                    args['conclusion'] = 'Positive'
                else:
                    args['conclusion'] = 'Negative'

            else:
                args['first'] = 2
                args['form'] = form
                args['neutral'] = 0
                args['negative'] = 0
                args['positive'] = 0



    else:
        form = TextForm()
        args['first'] = 1
        args['form'] = form
        args['neutral'] = 0
        args['negative'] = 0
        args['positive'] = 0


    return render(request, 'mainpage.html',args)



def text_form_products(request):
    args = {}
    if request.method == "POST":
        form = TextForm(request.POST)
        args['form'] = form
        if form.is_valid():
            text = form.cleaned_data['text']
            keyword = text
            noOfTweet = 100
            tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang="en").items(noOfTweet)
            positive = 0
            negative = 0
            neutral = 0
            subjectivity_pos = 0
            subjectivity_neg = 0
            tweet_list = []
            try:
                for tweet in tweets:
                    #print(tweet.text)
                    analysis = TextBlob(tweet.text)
                    tweet_list.append(tweet.text)
                    score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
                    neg = score['neg']
                    neu = score['neu']
                    pos = score['pos']
                    comp = score['compound']
                
                    if neg > pos:
                        negative += 1
                        subjectivity_neg += analysis.sentiment.subjectivity
                        #print('negative')
                    elif pos > neg:
                        positive += 1
                        subjectivity_pos += analysis.sentiment.subjectivity
                        #print('positive')
                    
                    elif pos == neg:
                        neutral += 1



                args['subjectivity_pos'] = math.floor(subjectivity_pos*100/positive)
                args['subjectivity_neg'] = math.floor(subjectivity_neg*100/negative)
                positive = percentage(positive, noOfTweet)
                negative = percentage(negative, noOfTweet)
                neutral = percentage(neutral, noOfTweet)
                args['first'] = 0
                args['text'] = text
                args['negative'] = math.floor(negative)
                args['neutral'] = math.floor(neutral)
                args['positive'] = math.ceil(positive)

                stopwords = set(STOPWORDS)
                wc = WordCloud(background_color="white",max_words=3000,stopwords=stopwords,repeat=True).generate(str(tweet_list))
                plt.figure(figsize=(32,18))
                plt.axis('off')
                plt.imshow(wc, interpolation="bilinear", aspect='auto')
                fig = plt.gcf()
                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                string = base64.b64encode(buf.read())

                uri = 'data:image/png;base64,' + urllib.parse.quote(string)
                args['image'] = uri


                if (negative<positive):
                    args['conclusion'] = 'Positive'
                else:
                    args['conclusion'] = 'Negative'
            
            except:
                args['first'] = 2
                args['form'] = form
                args['neutral'] = 0
                args['negative'] = 0
                args['positive'] = 0
                args['subjectivity_pos'] = 0
                args['subjectivity_neg'] = 0


    else:
        form = TextForm()
        args['first'] = 1
        args['form'] = form
        args['neutral'] = 0
        args['negative'] = 0
        args['positive'] = 0
        args['subjectivity_pos'] = 0
        args['subjectivity_neg'] = 0


    return render(request, 'products.html',args)

def text_form_handles(request):
    args = {}
    if request.method == "POST":
        form = TextForm(request.POST)
        args['form'] = form
        if form.is_valid():
            text = form.cleaned_data['text']
            userID = text
            try:
                tweets = api.user_timeline(screen_name=userID, count=50, include_rts = False, tweet_mode = 'extended')
                positive = 0
                negative = 0
                neutral = 0
                count = 0
                for tweet in tweets:
                    #print(tweet.full_text)
                    count += 1
                    analysis = TextBlob(tweet.full_text)
                    score = SentimentIntensityAnalyzer().polarity_scores(tweet.full_text)
                    neg = score['neg']
                    neu = score['neu']
                    pos = score['pos']
                    comp = score['compound']
                
                    if neg > pos:
                        negative += 1
                        #print('negative')
                    elif pos > neg:
                        positive += 1
                        #print('positive')
                    
                    elif pos == neg:
                        neutral += 1


                positive = percentage(positive, count)
                negative = percentage(negative, count)
                neutral = percentage(neutral, count)
                args['first'] = 0
                args['text'] = text
                args['negative'] = math.floor(negative)
                args['neutral'] = math.floor(neutral)
                args['positive'] = math.ceil(positive)
                if (negative<positive):
                    args['conclusion'] = 'Positive'
                else:
                    args['conclusion'] = 'Negative'

            except:
                args['first'] = 2
                args['form'] = form
                args['neutral'] = 0
                args['negative'] = 0
                args['positive'] = 0


    else:
        form = TextForm()
        args['first'] = 1
        args['form'] = form
        args['neutral'] = 0
        args['negative'] = 0
        args['positive'] = 0


    return render(request, 'handles.html',args)