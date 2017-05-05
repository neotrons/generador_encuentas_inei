# encoding: utf-8
from django.forms import ModelForm
from django import forms
import json
from .models import Field, Upload
#from image_cropping import ImageCropWidget

class DynamicForm(ModelForm):
    TAG = "custom"
    CLASS_CORRECT = "succes_opc"
    CLASS_INCORRECT = "error_opc"

    class Meta:
        abstract = True

    # Este metodo altera el comportamiento normal del constructor
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields')  # Relaciona el Formulario a mostrar y los campos del participante

        super(DynamicForm, self).__init__(*args, **kwargs)  # Crea el objeto

        # Esta parte sirve para crear los campos dinamicos, que seran renderizados posteriormente
        for field in fields:
            id = DynamicForm.generate_tag(field)
            extra_attr = {}
            if field.type == Field.BOOLEAN:  # Agrega un campo boolean
                self.fields[id] = forms.BooleanField(label=field.content, widget=forms.CheckboxInput(
                    attrs={'class': 'text-field '.format(field.label)}))

            elif field.type == Field.RADIUS:  # Agrega un campo radio
                a = []
                choices = field.option_set.all() if hasattr(field, 'option_set') else field.alternative_set.all()
                for subfield in choices:
                    a.append((subfield.content, subfield.content))
                self.fields[id] = forms.ChoiceField(label=field.content, choices=a,
                                                    widget=forms.RadioSelect(attrs={'class': 'opt-select'}))

            elif field.type == Field.MULTIPLE:  # Agrega un campo de Seleccion Multiple
                a = []
                choices = field.option_set.all() if hasattr(field, 'option_set') else field.field.alternative_set.all()
                for subfield in choices:
                    a.append((subfield.id, subfield.content)) #subfield.label
                self.fields[id] = forms.MultipleChoiceField(label=field.content, choices=a,
                                                            widget=forms.CheckboxSelectMultiple,)

            elif field.type == Field.SELECCION or field.type == Field.DEPARTAMENTO or field.type == Field.PROVINCIA or field.type == Field.DISTRITO:
                a = []
                choices = field.option_set.all() if hasattr(field, 'option_set') else field.field.alternative_set.all()
                for subfield in choices:
                    a.append((subfield.content, subfield.content))  # subfield.label
                self.fields[id] = forms.ChoiceField(label=field.content, choices=a, widget=forms.Select(attrs={'class': 'text-field select-op'}))

            elif field.type == Field.FILE_UPLOAD:
                self.fields[id] = forms.FileField(label=field.content,
                                                  widget=forms.ClearableFileInput(
                                                      attrs={'class': 'file_inp_hide upload-input'}), help_text=field.help_text
                                                  )

            elif field.type == Field.TEXTAREA:
                self.fields[id] = forms.CharField(label=field.content, widget=forms.Textarea())

            elif field.type == Field.BIRTHDAY:
                self.fields[id] = forms.DateField(label=field.content, widget=forms.SelectDateWidget(attrs={'class': 'text-field select-santo'},
                                                empty_label=("Día", "Mes", "Año",), years=list(range(2016, 1915, -1))))

            else:  # Por defecto agrega un campo de texto
                self.fields[id] = forms.CharField(label=field.content, widget=forms.TextInput(attrs={'class': 'text-field'}))

            try:
                attrs = json.loads(field.custom_attr)
                for attr in attrs:
                    try:
                        attrs[attr] = " ".join((self.fields[id].widget.attrs[attr], attrs[attr],))
                    except KeyError:
                        pass
                self.fields[id].widget.attrs.update(attrs)
            except:
                pass

            self.fields[id].required = True if field.required else False

    # metodo usado para almacenar los campos en formato json, solo los custom
    def storage_json(self, obj=None):
        data = dict()
        for x in self.cleaned_data:
            if x.startswith("custom_"):
                if self.cleaned_data[x].__class__.__name__ == "InMemoryUploadedFile":
                    upload = Upload()
                    upload.file = self.cleaned_data[x]
                    #upload.promo = obj['promo']
                    #upload.label = x
                    #upload.document = obj['document']
                    upload.save()
                    if upload.file and upload.file is not None:
                        data[x] = upload.file.url
                    else:
                        data[x] = None
                else:
                    data[x] = self.cleaned_data[x]
        # return data
        return json.dumps(data)

    @staticmethod
    def generate_tag(field):
        return "{}_{}_{}".format(DynamicForm.TAG, field.label, field.id)

    @staticmethod
    def generate_tag_choice_id(question, choice=None):
        if choice is None:
            return "id_{}_{}".format(DynamicForm.generate_tag(question), question.correct_answer()[0])
        else:
            return "id_{}_{}".format(DynamicForm.generate_tag(question), choice)

    def add_extra_attr(self, field):
        field_name = field.__class__.__name__
        extra_attr = {}
        widget = field.widget.__class__.__name__

        if field.required:
            extra_attr['required'] = 'required'
            if field_name == 'BooleanField':
                extra_attr['data-restrict'] = 'check'
            if widget == 'RadioSelect':
                pass
            else:
                extra_attr['data-validate-require'] = "Este valor es incorrecto o es requerido"
            field.widget.attrs.update(extra_attr)
        return field


'''
    elif field.type == Field.IMAGE_CROP:
        id = 'cropimg_'+id
        self.fields[id] = forms.ImageField(label=field.content, widget=ImageCropWidget(attrs={'class': 'file_inp_hide upload-input imagen_cropping'}), help_text=field.help_text)
        self.fields['cropbox_' + id] = forms.CharField(widget=forms.HiddenInput(), required=False)
'''