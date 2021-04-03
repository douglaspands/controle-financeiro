from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path
from .views import LogoutConfirmarView, LogoutConcluidoView

app_name = 'contas'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/confirmar/', LogoutConfirmarView.as_view(), name='logout_confirmar'),
    path('logout/concluido/', LogoutConcluidoView.as_view(), name='logout_concluido'),

    path('recuperar_senha/', PasswordChangeView.as_view(), name='recuperar_senha'),
    path('mudar_senha/concluido/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('reiniciar_senha/', PasswordResetView.as_view(), name='password_reset'),
    path('reiniciar_senha/concluido/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reiniciar/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reiniciar/concluido/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
