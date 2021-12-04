import base64
from .models import phoneModel
from rest_framework.views import APIView
from rest_framework.response import Response
import pyotp
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
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
from twilio.rest import Client
from django.conf import settings

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
    form = PasswordResetForm()
    return render(request=request, template_name="users/password/password_reset.html", context={"form": form})

#OTP FUNCTIONS
EXPIRY_TIME = 600
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"



class getPhoneNumberRegistered(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            # if Mobile already exists the take this else create New One
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            phoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = phoneModel.objects.get(
                Mobile=phone)  # user Newly created Model
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(
            phone).encode())  # Key is generated
        # TOTP Model for OTP is created
        OTP = pyotp.TOTP(key, interval=EXPIRY_TIME)
        #OTP is sent using Twilio. Check Settings for configuration
        client = Client(settings.TWILIO_ACCOUNT_SID,
                        settings.TWILIO_AUTH_TOKEN)
        response = client.messages.create(
            body='The OTP is '+OTP.now()+'. It will expire in 10 minutes',
            to=phone, from_=settings.TWILIO_PHONE_NUMBER)
        
        
        print("OTP is "+OTP.now())
        return Response({"OTP": OTP.now()}, status=200)

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(
            phone).encode())  # Generating Key
        OTP = pyotp.TOTP(key, interval=EXPIRY_TIME)  # TOTP Model
        if OTP.verify(request.data["otp"]):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            
            return HttpResponse("OK")
        return HttpResponse("OTP is wrong/expired")
