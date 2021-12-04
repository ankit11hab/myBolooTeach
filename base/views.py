from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import Question
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import Submission, Profile
from .forms import SubmissionForm, ProfileUpdateForm

# Create your views here.


@login_required
def home(request):
    user_profile = Profile.objects.filter(user=request.user).first()
    # if user_profile.first_name == "" or user_profile.mobile_no == "" or user_profile.classs==0:
    #     return redirect('profile_update')
    if not user_profile:
        return redirect('profile_update')
    questions = Question.objects.filter(classs=user_profile.classs)
    for question in questions:
        if not Submission.objects.filter(question=question, user=request.user):
            Submission(question=question, user=request.user, submitted=False).save()
    submissions = Submission.objects.filter(user = request.user, submitted = True)
    pending = Submission.objects.filter(user = request.user, submitted = False)
    count = len(submissions)
    submission1 = len(Submission.objects.filter(
        user=request.user, submitted=True, date_of_submission=datetime.now().date()))
    submission2 = len(Submission.objects.filter(
        user=request.user, submitted=True, date_of_submission=(datetime.now()-timedelta(hours=24)).date()))
    submission3 = len(Submission.objects.filter(
        user=request.user, submitted=True, date_of_submission=(datetime.now()-timedelta(hours=24*2)).date()))
    submission4 = len(Submission.objects.filter(
        user=request.user, submitted=True, date_of_submission=(datetime.now()-timedelta(hours=24*3)).date()))
    submission5 = len(Submission.objects.filter(
        user=request.user, submitted=True, date_of_submission=(datetime.now()-timedelta(hours=24*4)).date()))
    return render(request, 'base/home.html', {'questions': questions, 'profile': user_profile, 'submissions': submissions, 'pending': pending, 'count': count, 'submission1': submission1, 'submission2': submission2, 'submission3': submission3, 'submission4': submission4, 'submission5': submission5})


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        print(form['first_name'].value())
        first_name = form['first_name'].value()
        last_name = form['last_name'].value()
        classs = form['classs'].value()
        mobile_no = form['mobile_no'].value()
        school = form['school'].value()
        profile = Profile(user=request.user, first_name=first_name,
                          last_name=last_name, classs=classs, mobile_no=mobile_no, school=school)
        profile.save()
        return redirect('home')
    else:
        form = ProfileUpdateForm()
    return render(request, 'base/profile_update.html', {'form': form})


@login_required
def detail_view(request, pk):
    question = Question.objects.get(pk=pk)
    all_submissions = Submission.objects.filter(
        question=question, submitted=True)
    if Submission.objects.filter(question=question, user=request.user).first():
        submission = Submission.objects.filter(
            question=question, user=request.user).first()
    else:
        submission = Submission(
            question=question, submitted=False, submitted_answer="", user=request.user)
        submission.save()
    return render(request, 'base/question_detail.html', {'question': question, 'submission': submission, 'all_submissions': all_submissions})


@login_required
def answer_form(request, pk):
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        form = SubmissionForm(question.number_of_question,request.POST)
        ans = ""
        marks = 0
        for i in range(1, question.number_of_question+1):
            txt = "Question "+str(i)
            if form[txt].value() == None:
                ans = ans + " "
            else:
                ans = ans+form[txt].value()
                if question.answer_key[i-1] == form[txt].value():
                    marks += question.marks_per_question

        submission = Submission.objects.filter(
            question=question, user=request.user).first()
        submission.marks_obtd = marks
        submission.submitted = True
        submission.submitted_answer = ans
        submission.save()
        return redirect('question-detail', pk)
    else:
        form = SubmissionForm(n=question.number_of_question)
    return render(request, 'base/answer_form.html', {'question': question, 'form': form})
