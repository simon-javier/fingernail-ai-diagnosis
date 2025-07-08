from django.urls import path

from .views import HomePageView, QuestionsFormView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("questions-form/", QuestionsFormView.as_view(), name="questions-form"),
]
