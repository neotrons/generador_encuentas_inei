from django.contrib import admin
from .models import *
from nested_admin import NestedTabularInline, NestedStackedInline, NestedModelAdmin

# Register your models here.


class OptionsInline(NestedTabularInline):
    model = Option
    extra = 0
    fk_name = 'field'


class FieldInline(NestedStackedInline):
    model = Field
    extra = 0
    inlines = [OptionsInline]
    fk_name = 'fieldset'
    fields = ('type', 'required', 'content', 'label',)

class FielsetInline(NestedStackedInline):
    model = Fieldset
    fk_name = 'block'
    inlines = [FieldInline]
    extra = 0


class BlockInline(NestedStackedInline):
    model = Block
    extra = 0
    inlines = [FielsetInline]
    fk_name = 'form'


@admin.register(Form)
class FormAdmin(NestedModelAdmin):
    list_display = ('id', 'title', 'valid_from', 'valid_to',)
    inlines = [BlockInline]
