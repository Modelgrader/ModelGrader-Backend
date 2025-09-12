from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .controllers.request import CustomRequest


class BaseAPIView:
    """
    Base view class that automatically converts HttpRequest to CustomRequest.
    This is an alternative to middleware or decorators.
    """
    
    def dispatch(self, request, *args, **kwargs):
        """
        Convert the request to CustomRequest before processing.
        """
        # Create a new CustomRequest instance
        custom_request = CustomRequest()
        
        # Copy all attributes from the original request
        for attr in dir(request):
            if not attr.startswith('_') and hasattr(request, attr):
                try:
                    value = getattr(request, attr)
                    setattr(custom_request, attr, value)
                except (AttributeError, TypeError):
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
        
        # Replace the request object
        return super().dispatch(custom_request, *args, **kwargs)


class AuthenticatedAPIView(BaseAPIView):
    """
    Base view class that requires authentication and provides CustomRequest.
    """
    
    def dispatch(self, request, *args, **kwargs):
        """
        Check authentication before processing the request.
        """
        # First convert to CustomRequest
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
        
        # Continue with parent dispatch (which will apply BaseAPIView logic)
        return super().dispatch(request, *args, **kwargs)


def create_custom_api_view(http_methods, require_auth=False):
    """
    Factory function to create API views with CustomRequest support.
    
    Usage:
    # Without authentication
    @create_custom_api_view(['POST'])
    def my_view(request):
        # request is a CustomRequest instance
        pass
    
    # With authentication
    @create_custom_api_view(['POST'], require_auth=True)
    def my_protected_view(request):
        # request is a CustomRequest instance with guaranteed authentication
        pass
    """
    def decorator(view_func):
        if require_auth:
            from .decorators import require_authentication
            return api_view(http_methods)(require_authentication(view_func))
        else:
            from .decorators import with_custom_request
            return api_view(http_methods)(with_custom_request(view_func))
    
    return decorator
