from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as force_login
from django.contrib.auth import logout as force_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from rpna.core.helpers import allow_debug

from .forms import LoginCodeForm, LoginForm
from .models import User


def index(request):
    return render(request, "index.html")


def logout(request):
    force_logout(request)
    return redirect("rpna:index")


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data["number"]
            user: User = User.objects.get_or_create(username=number)[0]

            if "debug" in request.POST and allow_debug(request):
                force_login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
                return redirect("rpna:setup")

            # send_text_message(number, "foobar")
            messages.success(request, f"Message sucesfully sent to {number}.")
            request.session["number"] = number
            request.session["code"] = 123
            return redirect("rpna:login-code")
    else:
        form = LoginForm()

    context = {"form": form, "allow_debug": allow_debug(request)}
    return render(request, "login.html", context)


def login_code(request):
    if request.method == "POST":
        form = LoginCodeForm(request.POST)
        if form.is_valid():
            number = request.session.get("number")
            user = User.objects.get(username=number)
            code = form.cleaned_data["code"]
            print((request.user, code))  # TODO: check code
            force_login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            return redirect("rpna:setup")
    else:
        form = LoginCodeForm()

    context = {"form": form}
    return render(request, "code.html", context)


@login_required
def setup(request):
    return render(request, "setup.html")
