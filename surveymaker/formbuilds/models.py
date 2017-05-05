# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
import datetime
from .abstract_models import *
from django.db import models

# Create your models here.


class Form(models.Model):

    valid_from = models.DateField(blank=False, verbose_name="Válido desde",
                                  help_text="Indica desde cuando aparecera el formulario de registro",
                                  default=datetime.datetime.today)
    valid_to = models.DateField(blank=False, verbose_name="Válido hasta",
                                help_text="Indica hasta cuando aparecera el formulario de registro")
    '''
    promo = models.OneToOneField(Promo, verbose_name="Promoción",
                              help_text="Se indica la promoción asociada a este formulario", blank=False)
    '''
    title = models.CharField(max_length=255, blank=True, null=True, default="", verbose_name="titulo de formulario")
    subtitle = models.CharField(max_length=255, blank=True, null=True, default="",
                                verbose_name="Subtitulo de formulario")
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Formulario"
        verbose_name_plural = "Formularios"

    def __unicode__(self):
        return '{}'.format(self.id)

    def is_available(self):
        """Verifica si se puede acceder aun a la promoción""" #FIXME: Validar tambien si el formulario es programado a futuro
        return self.valid_to >= datetime.datetime.now().date()

    def has_survey(self):
        #return Poll.objects.filter(form = self.id).count() > 0
        pass

    def get_all_fields(self):
        return self.field_set.all()


class Block(models.Model):
    title = models.CharField(max_length=255)
    help_text = models.CharField(max_length=255, default="", blank=True, null=True, verbose_name="Texto de ayuda")
    form = models.ForeignKey(Form)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class Fieldset(models.Model):
    title = models.CharField(max_length=255)
    show = models.BooleanField(default=True)
    block = models.ForeignKey(Block)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


# Field: Son los campos que se usaran para todos los formularios
class Field(MetaField):
    form = models.ForeignKey(Form, blank=True, null=True)
    fieldset = models.ForeignKey(Fieldset, blank=True, null=True, default=None)
    help_text = models.CharField(max_length=255, default="", blank=True, null=True, verbose_name="Texto de ayuda")

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = "Campo"
        verbose_name_plural = "Campos"


class Option(MetaSubfield):
    field = models.ForeignKey(Field, verbose_name="Campo")

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = "Opción"
        verbose_name_plural = "Opciones"