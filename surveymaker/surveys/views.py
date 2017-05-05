from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Survey
# Create your views here.


class SurveyView(TemplateView):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        self.kwargs['survey'] = Survey.objects.get(slug=slug)
        print (Survey.objects.get(slug=slug))
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
        context['form'] = survey.form
        return context