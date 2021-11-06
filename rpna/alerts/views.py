from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as force_login
from django.contrib.auth import logout as force_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from rpna.core.helpers import allow_debug, send_text_message
from rpna.core.models import Profile

from .forms import LoginCodeForm, LoginForm
from .helpers import generate_code
from .models import Event, User


def index(_request):
    return redirect("rpna:setup")


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
            profile = Profile.objects.get_or_create(user=user)[0]
            profile.joined_at = timezone.now()
            profile.valid = None
            profile.save()
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
                profile: Profile = user.profile  # type: ignore
                profile.valid = True
                profile.save()
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
    if request.user.is_staff:
        messages.info(request, "Staff user is now logged out.")
        return redirect("rpna:logout")
    return render(request, "setup.html")


def alert(request, pk: int):
    event = get_object_or_404(Event, pk=pk)
    return render(request, "alert.html", {"event": event})
