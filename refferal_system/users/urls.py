from .views import SendVerificationCodeView, VerifyCodeView
from .views import ProfileView
from django.urls import path
from .views import login_view, verify_code_view, profile_view

urlpatterns = [
    path('send-verification-code/', SendVerificationCodeView.as_view()),
    path('verify-code/', VerifyCodeView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('login/', login_view, name='login'),
    path('verify-code/', verify_code_view, name='verify_code'),
    path('profile/', profile_view, name='profile'),
]
