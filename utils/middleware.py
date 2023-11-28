from django.http import JsonResponse


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/healthz":
            data = {"message": "ok"}
            return JsonResponse(data)
        return self.get_response(request)
