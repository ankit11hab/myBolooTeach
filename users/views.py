from django.contrib import auth
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect
import uuid
from users.models import Profile
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.conf import settings
User = get_user_model()

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user = User.objects.filter(username=username).first()
            token = str(uuid.uuid4())
            Profile(user=user,auth_token = token).save()
            send_verification_mail(email,token)
            return redirect('verify_email')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def send_verification_mail(email,token):
    subject = "Verify your account"
    message = f'Click on this link to verify your account: http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    email_to = [email]
    send_mail(subject, message, email_from, email_to, fail_silently=False)

def verify(request, token):
    prof = Profile.objects.filter(auth_token=token).first()
    if prof:
        prof.is_verified = True
        prof.save()
        messages.success(request,'Your account has been verified')
        return redirect('home')
    else:
        messages.error(request,'Email verification failed')
        return redirect('login')


def password_reset_request(request):
    if request.method == "POST":
        form= PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(
                Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "users/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'MyBoloo Teach',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'MyBoloo Teach', [
                                  user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(
                        request, ("Password reset mail sent successfully."))
            else:
                messages.error(request, ("Email not registered with us"))
    form= PasswordResetForm()
    return render(request=request, template_name="users/password/password_reset.html", context={"form": form})

def verify_email(request):
    return render(request,'users/verify_email.html')

