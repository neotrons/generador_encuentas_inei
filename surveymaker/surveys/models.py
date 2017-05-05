from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from formbuilds.models import Form
# Create your models here.


class Survey(models.Model):
    TEMPLATE_CHOICES = (
        (1, 'Template Default'),
        (2, 'Template LGTB')
    )
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=255, blank=True, null=True, default="", verbose_name="titulo de Encuesta")
    slug = models.SlugField(verbose_name="url encuesta")
    template = models.IntegerField(choices=TEMPLATE_CHOICES)
    form = models.OneToOneField(Form)

    def __unicode__(self):
        return '{} - {}'.format(self.code, self.title)

    def save(self, **kwargs):
        if self.pk is None:
            form = Form()
            form.valid_from = datetime.now()
            form.title = self.title
            form.save()
            self.form = form

        super(Survey, self).save(**kwargs)
