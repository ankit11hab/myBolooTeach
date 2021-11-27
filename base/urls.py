from django.urls import path
from . import views
from .views import QuestionDetailView

urlpatterns = [
    path('', views.home, name='home'),
    path('question/<pk>', QuestionDetailView.as_view(), name='question-detail'),
]
