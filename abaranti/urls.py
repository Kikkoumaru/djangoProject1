# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ... (他のURLパターン)
    path('', views.login_view, name='login'), # ログイン画面をルートURLに設定
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('error/', views.error_view, name='error'),  # エラー画面のURLパターン
    # ... (他のURLパターン)
]
