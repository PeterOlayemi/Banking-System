from django.shortcuts import redirect
from urllib.parse import urlencode

def customer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            login_url = '/portal/customer/login/'
            query_string = urlencode({'next': request.get_full_path()})
            redirect_url = f"{login_url}?{query_string}"
            return redirect(redirect_url)
    return wrapper
