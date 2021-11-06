from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("setup/", views.setup, name="setup"),
    path("<str:language>/<int:pk>", views.alert, name="alert"),
]

app_name = "alerts"
