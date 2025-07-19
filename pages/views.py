from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView

from nails.models import Nail


class HomePageView(TemplateView):
    template_name = "home.html"


class ResultsDetailView(DetailView):
    model = Nail
    context_object_name = "nail"
    template_name = "result.html"


class QuestionsFormView(LoginRequiredMixin, TemplateView):
    template_name = "questions-form.html"
    login_url = "home"
    redirect_field_name = "redirect_to"
