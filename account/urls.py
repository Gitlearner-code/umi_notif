from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/',views.login_view, name='login_view'),
    path('logout/',views.logout_view, name='logout'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password-reset.html'), name='password_reset_confirm'),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='account/password-reset-complete.html'
        ),
        name='password_reset_complete',
    ),
    path('password-reset/<int:user_id>/', views.trigger_account_email, name='trigger_account_email'),

    ]