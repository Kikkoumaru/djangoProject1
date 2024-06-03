from django import forms

class LoginForm(forms.Form):
    user_id = forms.CharField(label='ユーザーID', max_length=8, required=True)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput, required=True)
