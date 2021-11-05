import datetime

from django.http import HttpResponse

import log


def current_datetime(request):
    log.debug(request)
    now = datetime.datetime.now()
    html = f"<html><body>Welcome to rpna.<br>It is now {now}.</body></html>"
    return HttpResponse(html)
