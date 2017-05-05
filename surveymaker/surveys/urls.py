from django.conf.urls import url
from .views import SurveyView
urlpatterns = [
    url(r'^(?P<slug>[0-9a-z\-]+)/$', SurveyView.as_view(), name='pagina')
]