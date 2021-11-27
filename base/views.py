from django.shortcuts import render
from .models import Question
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

# Create your views here.
@login_required
def home(request):
    questions = Question.objects.all()
    return render(request, 'base/home.html',{'questions':questions})

@method_decorator(login_required, name='dispatch')
class QuestionDetailView(DetailView):
    model = Question
