from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm  # forms.pyで定義したLoginForm
from .models import Employee


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']

            # ユーザー認証
            user = authenticate(request, username=user_id, password=password)

            if user is not None:
                login(request, user)
                # ロールに応じたリダイレクト
                if user.role == Employee.Role.RECEPTION:
                    return redirect('menu_reception')  # 受付用メニュー
                elif user.role == Employee.Role.DOCTOR:
                    return redirect('menu_doctor')    # 医師用メニュー
            else:
                messages.error(request, 'ユーザーIDまたはパスワードが正しくありません。')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
