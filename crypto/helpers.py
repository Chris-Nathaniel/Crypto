from functools import wraps

def user_authenticated(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            session_id = request.user.email
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key

        # Store session_id into request so you can use it in the view
        request.session["user"] = session_id
        
        return func(request, *args, **kwargs)
    return wrapper