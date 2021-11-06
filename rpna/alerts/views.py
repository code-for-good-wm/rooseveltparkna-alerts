from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as force_login
from django.contrib.auth import logout as force_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from rpna.core.helpers import allow_debug, send_text_message

from .forms import LoginCodeForm, LoginForm
from .helpers import generate_code
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
            request.session["number"] = number
            user = User.objects.get_or_create(username=number)[0]
            code = generate_code(user)

            if "debug" in request.POST and allow_debug(request):
                force_login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
                return redirect("rpna:setup")

            send_text_message(
                number,
                "Welcome to Roosevelt Park's messaging system!\n\n"
                f"Your confirmation code is: {code}",
            )
            messages.success(request, f"Message sucesfully sent to {number}.")
            return redirect("rpna:login-code")
    else:
        form = LoginForm()

    context = {"form": form, "allow_debug": allow_debug(request)}
    return render(request, "login.html", context)


def login_code(request):
    username = request.session.get("number")
    if not username:
        messages.error(request, "Unable to verify code. Please try again.")
        return redirect("rpna:login")

    if request.method == "POST":
        form = LoginCodeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["code"]

            if user := authenticate(username=username, password=password):
                force_login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
                messages.success(request, "Sucesfually logged in.")
                return redirect("rpna:setup")

            # TODO: Move this to form validation
            messages.error(request, "Invalid confirmaiton code. Please try again.")
            return redirect("rpna:login-code")
    else:
        form = LoginCodeForm()

    context = {"form": form}
    return render(request, "code.html", context)


@login_required
def setup(request):
    return render(request, "setup.html")
