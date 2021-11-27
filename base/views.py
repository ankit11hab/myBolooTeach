from django.shortcuts import render
from .models import Question
from django.contrib.auth.decorators import login_required
from users.models import Submission
from .forms import SubmissionForm

# Create your views here.
@login_required
def home(request):
    questions = Question.objects.all()
    return render(request, 'base/home.html',{'questions':questions})

@login_required
def detail_view(request,pk):
    question = Question.objects.get(pk = pk)
    if request.method=='POST':
        form = SubmissionForm(request.POST)
        ans = ""
        marks = 0
        for i in range(1,21):
            txt = "question"+str(i)
            if form[txt].value()==None:
                ans = ans + " "
            else:
                ans = ans+form[txt].value()
                if question.answer_key[i-1]==form[txt].value():
                    marks+=question.marks_per_question
        
        submission = Submission(question=question, marks_obtd = marks, submitted_answer = ans, user = request.user)
        submission.save()
    else:
        form = SubmissionForm()
    return render(request, 'base/question_detail.html', {'question':question, 'form':form})