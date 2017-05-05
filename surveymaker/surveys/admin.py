from django.contrib import admin
from .models import Survey

# Register your models here.


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'ver_online')
    fields = ('code', 'title', 'slug', 'template', 'form')

    def ver_online(self, obj):
        return '<a href="/encuesta/%s" target="_blank">Ver Online</a>' % (obj.slug, )

    ver_online.allow_tags = True

