from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    phone = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned = super().clean()
        p = cleaned.get('password')
        cp = cleaned.get('confirm_password')
        phone = cleaned.get('phone') or ''
        if p and cp and p != cp:
            self.add_error('confirm_password', "Passwords do not match.")
        # basic phone validation: digits & optional +, -, spaces
        if phone and not re.match(r'^[\d\+\-\s]{7,20}$', phone):
            self.add_error('phone', "Invalid phone number.")
        return cleaned
