from django.shortcuts import render, redirect
from .models import Question
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
    all_submissions = Submission.objects.filter(submitted=True)
    if Submission.objects.filter(question=question, user = request.user).first():
        submission = Submission.objects.filter(question=question, user = request.user).first()
    else:
        submission = Submission(question=question, submitted=False, submitted_answer = "", user = request.user)
        submission.save()
    return render(request, 'base/question_detail.html', {'question':question,'submission':submission,'all_submissions':all_submissions})


@login_required
def answer_form(request,pk):
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
        
        submission = Submission.objects.filter(question=question, user = request.user).first()
        submission.marks_obtd = marks
        submission.submitted = True
        submission.submitted_answer = ans
        submission.save()
        return redirect('question-detail', pk)
    else:
        form = SubmissionForm()
    return render(request, 'base/answer_form.html', {'question':question,'form':form})