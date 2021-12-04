from django.urls import path
from . import views
from users import views as user_views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('profile', views.profile_update, name='profile_update'),
    path('question/<int:pk>', views.detail_view, name='question-detail'),
    path('answers/<int:pk>', views.answer_form, name='answer-form'),
    path("verify/<phone>", user_views.getPhoneNumberRegistered.as_view(), name="OTP Gen"),
    # Password reset urls
    path("password_reset", user_views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="users/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password/password_reset_complete.html'), name='password_reset_complete'),
]

