from random import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import PhoneNumberForm, VerificationCodeForm, InviteCodeForm
from .serializers import InviteCodeSerializer, UserProfileSerializer, VerificationCodeSerializer, PhoneNumberSerializer
from .models import User, Referral


def login_view(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            return redirect('verify_code')
    else:
        form = PhoneNumberForm()
    return render(request, 'users/login.html', {'form': form})


def verify_code_view(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            return redirect('profile')
    else:
        form = VerificationCodeForm()
    return render(request, 'users/verify_code.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = InviteCodeForm(request.POST)
        if form.is_valid():
            invite_code = form.cleaned_data['invite_code']
            try:
                referrer = User.objects.get(invite_code=invite_code)
                if request.user.activated_invite_code:
                    return render(request, 'users/profile.html', {'error': 'Вы уже активировали инвайт-код'})
                request.user.activated_invite_code = invite_code
                request.user.save()
                Referral.objects.create(user=request.user, invite_code=invite_code)
                return redirect('profile')
            except User.DoesNotExist:
                return render(request, 'users/profile.html', {'error': 'Инвайт-код не найден'})
    else:
        form = InviteCodeForm()
    return render(request, 'users/profile.html', {'form': form, 'user': request.user})


class SendVerificationCodeView(APIView):
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = str(random.randint(1000, 9999))
            # Имитация отправки кода и задержки
            time.sleep(1)
            # В реальном приложении отправляйте код через SMS сервис
            return Response({'message': 'Код отправлен'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            verification_code = serializer.validated_data['verification_code']
            phone_number = request.data.get('phone_number')
            user, created = User.objects.get_or_create(phone_number=phone_number)
            if created:
                user.invite_code = User.generate_invite_code()
                user.save()
            return Response({'message': 'Авторизация успешна'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get(self, request):
        user = request.user
        referrals = [r.user.phone_number for r in user.referrals.all()]
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = InviteCodeSerializer(data=request.data)
        if serializer.is_valid():
            invite_code = serializer.validated_data['invite_code']
            try:
                referrer = User.objects.get(invite_code=invite_code)
                if request.user.activated_invite_code:
                    return Response({'message': 'Вы уже активировали инвайт-код'}, status=status.HTTP_400_BAD_REQUEST)
                request.user.activated_invite_code = invite_code
                request.user.save()
                Referral.objects.create(user=request.user, invite_code=invite_code)
                return Response({'message': 'Инвайт-код активирован'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': 'Инвайт-код не найден'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
