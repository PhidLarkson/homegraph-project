from django.http import HttpResponseForbidden

class AccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user = request.user

        if request.path == '/add' and not user.is_staff:
            return HttpResponseForbidden("Permission Denied")
        
        if request.path == '/edit' and not user.is_staff:
            return HttpResponseForbidden("Permission Denied")


        return response