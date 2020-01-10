from django import forms

from members.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '아이디를 입력하세요'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '비밀번호를 입력하세요'
        }
    ))


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'name', 'password'
        ]
        widgets = {

            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '아이디를 입력하세요'}),
            'name': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '닉네임을 입력하세요'}),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '비밀번호를 입력하세요'}),
        }
