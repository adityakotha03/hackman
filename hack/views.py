from django.shortcuts import render

# Create your views here.

from .forms import *
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
import pickle
import joblib
import re
from pathlib import Path
import math

BASE_DIR = Path(__file__).resolve().parent.parent



stemmer = PorterStemmer()
cv = pickle.load(open(str(BASE_DIR.joinpath('hack/bow_sentiment')),"rb"))
classifier = joblib.load(str(BASE_DIR.joinpath('hack/SVM_Model')))

def processText(text):
    text = text.lower()
    text = re.sub('((www.[^s]+)|(https?://[^s]+))','',text)
    text = re.sub('@[^s]+','',text)
    text = re.sub('[s]+', ' ', text)
    text = re.sub(r'#([^s]+)', r'1', text)
    return text
 
def stem_words(text):
    word_tokens = word_tokenize(text)
    stems = [stemmer.stem(word) for word in word_tokens]
    return stems

def text_form(request):
    args = {}
    if request.method == "POST":
        form = TextForm(request.POST)
        args['form'] = form
        if form.is_valid():
            text = form.cleaned_data['text']
            #print(processText(text))
            tokenized_tweet = " ".join(stem_words(processText(text)))
            tokenized_tweet = " ".join([w for w in str(tokenized_tweet).split() if len(w)>2])
            list_pred = [tokenized_tweet]
            #print(list_pred)
            X_fresh = cv.transform(list_pred)
            y_pred_probability = classifier.predict_proba(X_fresh)
            y_pred = classifier.predict(X_fresh)
            #y_pred = 0 -> negative; 2 -> +ve ; 1 ->neutral
            #print(y_pred)
            #['neutral',-ve,+ve]
            print(y_pred_probability)
            args['first'] = 0
            args['text'] = text
            args['neutral'] = math.floor((y_pred_probability[0][0])*100)
            args['negative'] = math.floor((y_pred_probability[0][1])*100)
            args['positive'] = math.ceil((y_pred_probability[0][2])*100)
            if y_pred==2:
                args['conclusion'] = 'Positive'
            elif y_pred==1:
                args['conclusion'] = 'Negative'
            elif y_pred==0:
                args['conclusion'] = 'Neutral'

    else:
        form = TextForm()
        args['first'] = 1
        args['form'] = form
        args['neutral'] = 0
        args['negative'] = 0
        args['positive'] = 0


    return render(request, 'mainpage.html',args)


 
#text = 'Today is a very good day what do you think #happylife https://classroom.google.com/u/1/h'               #Input text



