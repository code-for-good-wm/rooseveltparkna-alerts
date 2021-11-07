from django.conf import settings


def allow_debug(request) -> bool:
    if not settings.ALLOW_DEBUG:
        return False
    if request.GET.get("debug") == "false":
        return False
    if request.GET.get("debug"):
        return True
    return settings.DEBUG
