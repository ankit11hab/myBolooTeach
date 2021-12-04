from django.contrib import admin
from .models import Profile, Submission, phoneModel

# Register your models here.
admin.site.register(Submission)
admin.site.register(Profile)
admin.site.register(phoneModel)
