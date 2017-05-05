from __future__ import unicode_literals
from formbuilds.models import Form
from django.db import models

# Create your models here.

class Participant(models.Model):
    form = models.ForeignKey(Form)
