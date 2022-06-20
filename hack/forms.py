from logging import PlaceHolder
from django import forms
from django.forms import ModelForm

from .models import *

class TextForm(forms.ModelForm):
    text = forms.CharField(max_length=1000, label='', widget=forms.TextInput(attrs={'placeholder':'Please enter the text in English', 'class':'shadow appearance-none border rounded w-full p-3 text-gray-700 leading-tight focus:ring transform transition hover:scale-105 duration-300 ease-in-out'}))
    class Meta:
        model = Texttyped
        fields = (
            'text',
        )