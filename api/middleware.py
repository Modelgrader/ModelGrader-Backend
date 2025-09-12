from django.utils.deprecation import MiddlewareMixin
from .controllers.request import CustomRequest


class CustomRequestMiddleware(MiddlewareMixin):
    """
    Middleware to replace Django's HttpRequest with CustomRequest
    for all incoming requests.
    """
    
    def process_request(self, request):
        # Create a new CustomRequest instance
        custom_request = CustomRequest()
        
        # Copy all attributes from the original request to the custom request
        for attr in dir(request):
            if not attr.startswith('_') and hasattr(request, attr):
                try:
                    value = getattr(request, attr)
                    setattr(custom_request, attr, value)
                except (AttributeError, TypeError):
                    # Skip attributes that can't be copied
                    pass
        
        # Copy private attributes that are essential for Django
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
        
        # Replace the request object
        return custom_request
