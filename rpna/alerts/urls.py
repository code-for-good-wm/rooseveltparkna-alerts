from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("login/code/", views.login_code, name="login-code"),
    path("logout/", views.logout, name="logout"),
    path("setup/", views.setup, name="setup"),
    path("-/<int:pk>", views.alert, name="alert"),
]

app_name = "alerts"
