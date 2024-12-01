from rest_framework import serializers

from .models import User


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)


class VerificationCodeSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=4)


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'invite_code', 'activated_invite_code']
        depth = 1
