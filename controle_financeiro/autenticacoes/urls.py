from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path
from .views import LogoutConfirmar, UsuarioCriar

app_name = 'autenticacoes'

urlpatterns = [
    # Login/Logout
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/confirmar/', LogoutConfirmar.as_view(), name='logout_confirmar'),
    path('mudar_senha/', PasswordChangeView.as_view(), name='mudar_senha'),
    path('mudar_senha/concluido/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('recuperar_senha/', PasswordResetView.as_view(), name='password_reset'),
    path('recuperar_senha/solicitar/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('recuperar_senha/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('recuperar_senha/concluido/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Cadastro de usuario
    path('registrar/', UsuarioCriar.as_view(), name='criar'),
]
