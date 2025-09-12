from functools import wraps
from .controllers.request import CustomRequest


def with_custom_request(view_func):
    """
    Decorator that wraps a view function to use CustomRequest instead of HttpRequest.
    This is an alternative to the middleware approach.
    
    Usage:
    @api_view([POST])
    @with_custom_request
    def my_view(request):
        # request is now a CustomRequest instance
        token = request.get_token()
        account = request.get_account()
        return Response(...)
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Create a new CustomRequest instance
        custom_request = CustomRequest()
        
        # Copy all attributes from the original request
        for attr in dir(request):
            if not attr.startswith('_') and hasattr(request, attr):
                try:
                    value = getattr(request, attr)
                    setattr(custom_request, attr, value)
                except (AttributeError, TypeError):
                    # Skip attributes that can't be copied
                    pass
        
        # Copy essential private attributes
        essential_attrs = [
            '_body', '_read_started', '_post_parse_error', '_files',
            '_cached_user', '_messages', '_request_cache'
        ]
        
        for attr in essential_attrs:
            if hasattr(request, attr):
                try:
                    setattr(custom_request, attr, getattr(request, attr))
                except (AttributeError, TypeError):
                    pass
        
        # Call the original view with the custom request
        return view_func(custom_request, *args, **kwargs)
    
    return wrapper


def require_authentication(view_func):
    """
    Decorator that requires authentication and automatically provides CustomRequest.
    Returns 401 if the request is not authenticated.
    
    Usage:
    @api_view([POST])
    @require_authentication
    def my_protected_view(request):
        # request is guaranteed to be a CustomRequest with valid authentication
        account = request.get_account()  # This will not be None
        return Response(...)
    """
    from rest_framework.response import Response
    from rest_framework import status
    
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # First apply the custom request wrapper
        custom_request_wrapper = with_custom_request(view_func)
        
        # Create custom request manually for authentication check
        custom_request = CustomRequest()
        for attr in dir(request):
            if not attr.startswith('_') and hasattr(request, attr):
                try:
                    value = getattr(request, attr)
                    setattr(custom_request, attr, value)
                except (AttributeError, TypeError):
                    pass
        
        # Check authentication
        if not custom_request.is_authenticated():
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Call the wrapped view if authenticated
        return custom_request_wrapper(request, *args, **kwargs)
    
    return wrapper
