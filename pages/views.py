from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"


class QuestionsFormView(LoginRequiredMixin, TemplateView):
    template_name = "questions-form.html"
    login_url = "home"
    redirect_field_name = "redirect_to"
