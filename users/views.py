from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
User = get_user_model()

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


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
