from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register/", views.register_view, name="register_view"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("profile/", views.profile_view, name="profile_view"),
    path("password/change/", views.change_password, name="change_password"),
    path("email/change/", views.change_email, name="change_email"),
    path(
        "email/change/confirm/",
        views.email_change_confirm_view,
        name="email_change_confirm_view",
    ),
    path("withdrawl/request/", views.request_withdrawal, name="request_withdrawal"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
