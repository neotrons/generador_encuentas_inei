# encoding: utf-8
from participants.models import Participant
from .dynamic_forms import DynamicForm


class ParticipantForm(DynamicForm):
    extra = {'step': 1, 'class': 'box-register', 'title': '¡Participe aquí!'}

    class Meta:
        model = Participant
        fields = ('id',)

    def __init__(self, *args, **kwargs):
        self.form = kwargs.pop('form')
        kwargs['fields'] = self.form.get_all_fields()

        super(ParticipantForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field] = self.add_extra_attr(self.fields[field])

    def save(self, *args, **kwargs):
        super(ParticipantForm, self).save(*args, **kwargs)

    def is_valid(self):
        self.instance.form = self.form
        return super(ParticipantForm, self).is_valid()