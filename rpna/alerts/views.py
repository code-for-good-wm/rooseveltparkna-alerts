from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as force_login
from django.contrib.auth import logout as force_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _

from rpna.core.models import Profile
from rpna.core.utils import allow_debug

from .forms import LoginCodeForm, LoginForm, SetupForm
from .models import Event, User
from .utils import generate_code, send_text_message


def welcome(request):
    if language := request.GET.get("lang"):
        translation.activate(language)

    if request.user.is_authenticated:
        return redirect("rpna:setup")

    if request.method == "POST" or request.GET.get("number"):
        form = LoginForm(request.POST or request.GET)
        if form.is_valid():
            number = form.cleaned_data["number"]
            request.session["number"] = number
            user = User.objects.get_or_create(username=number)[0]
            profile = Profile.objects.get_or_create(user=user)[0]
            profile.joined_at = timezone.now()
            profile.save()
            code = generate_code(user)

            if "debug" in request.POST and allow_debug(request):
                force_login(request, user)
                return redirect("rpna:setup")

            send_text_message(
                number,
                _(
                    "Welcome to Roosevelt Park Neighborhood Association's messaging system!"
                )
                + "\n\n"
                + _("Your confirmation code is")
                + ": "
                + code,
            )
            profile.received_count += 1
            profile.save()
            response = redirect("rpna:login")
            if language:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
            return response
    else:
        form = LoginForm()

    context = {"form": form, "allow_debug": allow_debug(request)}
    return render(request, "welcome.html", context)


def login(request):
    username = request.session.get("number")
    if not username:
        messages.error(request, _("Unable to verify code. Please try again."))
        return redirect("rpna:welcome")

    if request.method == "POST":
        form = LoginCodeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["code"]

            if user := authenticate(username=username, password=password):
                profile: Profile = user.profile  # type: ignore
                profile.valid = True
                profile.save()
                force_login(request, user)
                return redirect("rpna:setup")

            messages.error(request, _("Invalid confirmation code. Please try again."))
            return redirect("rpna:login")
    else:
        form = LoginCodeForm()

    context = {"form": form}
    return render(request, "login.html", context)


def logout(request):
    force_logout(request)
    response = redirect("rpna:welcome")
    response.delete_cookie(settings.LANGUAGE_COOKIE_NAME)
    return response


@login_required
def setup(request):
    if request.user.is_staff:
        messages.info(request, _("Staff user is now logged out."))
        return redirect("rpna:logout")

    if "delete" in request.POST:
        request.user.delete()
        messages.info(
            request, _("Good bye! You will no longer receive text messages from us.")
        )
        return redirect("rpna:welcome")

    if request.method == "POST":
        form = SetupForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save()
            translation.activate(profile.language)
            send_text_message(
                profile.number,
                _(
                    "You're all set to receive alerts from Roosevelt Park Neighborhood Association!"
                )
                + "\n\n"
                + _("Configure your preferences")
                + ": "
                + settings.BASE_URL,
            )
            profile.received_count += 1
            profile.updated_at = timezone.now()
            profile.save()
            messages.success(request, _("Successfully updated your preferences."))
            response = redirect("rpna:setup")
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, profile.language)
            return response
    else:
        form = SetupForm(instance=request.user.profile)

    context = {"form": form}
    return render(request, "setup.html", context)


def alert(request, language: str, pk: int):
    event = get_object_or_404(Event, pk=pk)
    context = {"event": event, "spanish": language == "es"}
    return render(request, "alert.html", context)
