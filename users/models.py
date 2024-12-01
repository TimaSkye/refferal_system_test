from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    invite_code = models.CharField(max_length=6, null=True, blank=True)
    activated_invite_code = models.CharField(max_length=6, null=True, blank=True)


class Referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    invite_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
