from django.contrib import messages
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
    if not Profile.objects.filter(user=request.user).first().is_verified:
        messages.error(request,'Please verify your account')
        return redirect('login')
    user_profile = Profile.objects.filter(user=request.user).first()
    # if user_profile.first_name == "" or user_profile.mobile_no == "" or user_profile.classs==0:
    #     return redirect('profile_update')
    if user_profile.mobile_no=="" or  user_profile.first_name=="":
        return redirect('profile_update')
    questions = Question.objects.filter(classs=user_profile.classs).order_by('start_time')
    for question in questions:
        if not Submission.objects.filter(question=question, user=request.user):
            Submission(question=question, user=request.user, submitted=False).save()
    submissions = Submission.objects.filter(user = request.user, submitted = True)
    pending_raw = Submission.objects.filter(user = request.user, submitted = False)
    pending = []
    for sub in pending_raw:
        if not sub.question.ended():
            pending.append(sub)
    count1 = len(submissions)
    count2 = len(pending)
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
    return render(request, 'base/home.html', {'questions': questions, 'profile': user_profile, 'submissions': submissions, 'pending': pending, 'count1': count1,'count2': count2, 'submission1': submission1, 'submission2': submission2, 'submission3': submission3, 'submission4': submission4, 'submission5': submission5})


@login_required
def profile_update(request):
    if not Profile.objects.filter(user=request.user).first().is_verified:
        messages.error(request,'Please verify your account')
        return redirect('login')
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        print(form['first_name'].value())
        first_name = form['first_name'].value()
        last_name = form['last_name'].value()
        classs = form['classs'].value()
        mobile_no = form['mobile_no'].value()
        school = form['school'].value()
        user = request.user
        profile = Profile.objects.filter(user=request.user).first()
        profile.first_name=first_name
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        profile.last_name=last_name
        profile.classs=classs
        profile.mobile_no=mobile_no
        profile.school=school
        profile.save()
        return redirect('home')
    else:
        form = ProfileUpdateForm()
    return render(request, 'base/profile_update.html', {'form': form})

@login_required
def detail_view(request, pk):
    if not Profile.objects.filter(user=request.user).first().is_verified:
        messages.error(request,'Please verify your account')
        return redirect('login')
    question = Question.objects.get(pk=pk)
    all_submissions = Submission.objects.filter(
        question=question, submitted=True).order_by('-marks_obtd')
    if Submission.objects.filter(question=question, user=request.user).first():
        submission = Submission.objects.filter(
            question=question, user=request.user).first()
    else:
        submission = Submission(
            question=question, submitted=False, submitted_answer="", user=request.user)
        submission.save()
    return render(request, 'base/question_detail.html', {'question': question, 'submission': submission, 'all_submissions': all_submissions,'profiles':Profile.objects.all()})


@login_required
def answer_form(request, pk):
    if not Profile.objects.filter(user=request.user).first().is_verified:
        messages.error(request,'Please verify your account')
        return redirect('login')
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
