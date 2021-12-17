from django.db import models
from base.models import Question
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Submission(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submitted_answer = models.CharField(max_length=200)
    marks_obtd = models.IntegerField(default=0)
    submitted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_submission = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.id}'

    @property
    def number_of_correct(self):
        if self.question.marks_per_question>0:
            return int(self.marks_obtd/self.question.marks_per_question)
        else:
            return 0

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default = "")
    classs = models.IntegerField(default=0)
    mobile_no = models.CharField(max_length=10, default="")
    school = models.CharField(max_length=200, default="")
    auth_token = models.CharField(max_length=100,default="")
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'