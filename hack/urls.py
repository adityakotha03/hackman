from django.urls import path
from django.views.generic import TemplateView

from .forms import *
from . import views


urlpatterns = [
    path('textform',views.text_form,name='textform'),
]