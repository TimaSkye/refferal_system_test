from django import forms
from .models import User
from django.core.exceptions import ValidationError


class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=20, label='Номер телефона')

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('Пользователь с таким номером телефона уже существует')
        return phone_number


class VerificationCodeForm(forms.Form):
    verification_code = forms.CharField(max_length=4, label='Код верификации')
    phone_number = forms.CharField(max_length=20, widget=forms.HiddenInput())


class InviteCodeForm(forms.Form):
    invite_code = forms.CharField(max_length=6, label='Инвайт-код')

    def clean_invite_code(self):
        invite_code = self.cleaned_data['invite_code']
        try:
            User.objects.get(invite_code=invite_code)
        except User.DoesNotExist:
            raise ValidationError('Инвайт-код не найден')
        return invite_code


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'activated_invite_code']
        read_only_fields = ['phone_number', 'invite_code', 'activated_invite_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs['readonly'] = True
        self.fields['invite_code'].widget.attrs['readonly'] = True
        self.fields['activated_invite_code'].widget.attrs['readonly'] = True
