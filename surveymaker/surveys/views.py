from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from formbuilds.forms import ParticipantForm
from .models import Survey
# Create your views here.


class SurveyView(FormView):
    form_class = ParticipantForm

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        survey = Survey.objects.get(slug=slug)
        self.kwargs['survey'] = survey
        self.kwargs['form'] = survey.form
        return super(SurveyView, self).get(request, *args, **kwargs)

    def get_template_names(self):
        survey = self.kwargs.get('survey')
        print(survey)
        template = '_'.join(('template', str(survey.template)),)
        return '/'.join(('surveys', template, 'page.html'))

    def get_context_data(self, **kwargs):
        context = super(SurveyView, self).get_context_data(**kwargs)
        survey = self.kwargs.get('survey')
        context['survey'] = survey
        context['objform'] = survey.form
        #context['form'] = survey.form
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(form=self.kwargs['form'], **self.get_form_kwargs())