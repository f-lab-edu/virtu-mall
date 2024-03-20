from typing import Callable

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse


class HealthCheckMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path == "/healthz":
            data = {"message": "ok"}
            return JsonResponse(data)
        return self.get_response(request)
