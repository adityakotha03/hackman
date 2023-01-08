from django.urls import path
from django.views.generic import TemplateView

from .forms import *
from . import views


urlpatterns = [
    path('textform',views.text_form,name='textform'),
    path('textformproducts',views.text_form_products,name='textformproducts'),
    path('textformhandles',views.text_form_handles,name='textformhandles'),
]