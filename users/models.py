from django.db import models
from base.models import Question
from django.contrib.auth.models import User

# Create your models here.
class Submission(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submitted_answer = models.CharField(max_length=200)
    marks_obtd = models.IntegerField(default=0)
    submitted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'