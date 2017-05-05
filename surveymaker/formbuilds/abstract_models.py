# encoding: utf-8
from __future__ import unicode_literals
from django.db import models


# Meta Clases
class MetaField(models.Model):
    TEXT = '1'
    BOOLEAN = '2'
    RADIUS = '3'
    MULTIPLE = '4'
    SELECCION = '5'
    FILE_UPLOAD = '6'
    TEXTAREA = '7'
    BIRTHDAY = '8'
    IMAGE_CROP = '9'

    MetaFields_type = (
        (TEXT, 'Texto'),
        (BOOLEAN, 'Verdadero o Falso'),
        (RADIUS, 'Radio'),
        (MULTIPLE, 'Seleccion multiple'),
        (SELECCION, 'Seleccion'),
        (FILE_UPLOAD, 'Cargar documento'),
        (TEXTAREA, 'Textarea'),
        (BIRTHDAY, 'Año-Mes-Día'),
        (IMAGE_CROP, 'Recortar Imagen')
    )

    type = models.CharField(choices=MetaFields_type, default=MetaFields_type[0], max_length=2)
    content = models.CharField(max_length=300, verbose_name='Pregunta')
    label = models.SlugField(max_length=200, verbose_name="label")
    required = models.BooleanField(default=True, verbose_name="Campo obligatorio")
    custom_attr = models.TextField(max_length=255, default="", blank=True, null=True)

    class Meta:
        abstract = True


class MetaSubfield(models.Model):
    content = models.CharField(max_length=200)

    class Meta:
        abstract = True

