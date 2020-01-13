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
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '닉네임을 입력하세요'}),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '비밀번호를 입력하세요'}),
        }

    def save(self):
        return User.objects.create_user(
            username=self.cleaned_data['username'],
            name=self.cleaned_data['name'],
            password=self.cleaned_data['password']
        )

    def clean_username(self):
        username_check = User.objects.filter(username=self.cleaned_data['username']).exists()

        if username_check is True:
            raise forms.ValidationError('이미 존재하는 아이디입니다')
        else:
            return self.cleaned_data['username']
