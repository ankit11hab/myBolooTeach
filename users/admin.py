from django.contrib import admin
from .models import Profile, Submission

# Register your models here.
admin.site.register(Submission)
admin.site.register(Profile)