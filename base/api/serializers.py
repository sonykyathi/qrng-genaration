from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework import serializers

from base.models import Qrng


class QrngSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qrng
        fields = "__all__"


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
