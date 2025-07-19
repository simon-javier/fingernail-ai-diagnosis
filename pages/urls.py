from django.urls import path

from .views import HomePageView, QuestionsFormView, ResultsDetailView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("questions-form/", QuestionsFormView.as_view(), name="questions-form"),
    path("result/<int:pk>/", ResultsDetailView.as_view(), name="result_detail"),
]
