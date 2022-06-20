from django.db import models

# Create your models here.

class Texttyped(models.Model):
    text = models.CharField(max_length=1000)
