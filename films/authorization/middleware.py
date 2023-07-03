from botocore.exceptions import NoCredentialsError
from django.http import JsonResponse

class NoCredentialsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, NoCredentialsError):
            error_message = "Unable to locate AWS credentials. Application is available only in debug mode (set setting.DEBUG = True)."
            response_data = {
                'error': error_message
            }
            return JsonResponse(response_data, status=500)

        return None