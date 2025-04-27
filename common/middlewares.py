from django.shortcuts import redirect

class ClassRoomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        if '/main/' in request.path and not request.user.is_authenticated:
            # redirect to login page
            return redirect('login_view')
            
        response = self.get_response(request)
        return response
           


class HandleEmptyPathMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.path == '/':
            return redirect('home')
        
        response = self.get_response(request)
        return response