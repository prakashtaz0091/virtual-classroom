from django.shortcuts import redirect

def teacher_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'teacher':
            return func(request, *args, **kwargs)
        return redirect('not_authorized')
    return wrapper