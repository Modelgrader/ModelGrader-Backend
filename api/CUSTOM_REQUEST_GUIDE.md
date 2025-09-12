# CustomRequest Integration Guide

This guide explains how to integrate CustomRequest with Django views in your ModelGrader-Backend project.

## Overview

CustomRequest extends Django's HttpRequest to provide convenient methods for token-based authentication:
- `get_token()`: Extract bearer token from Authorization header
- `get_account()`: Get Account object associated with the token
- `has_valid_token()`: Check if request has a valid token
- `is_authenticated()`: Check if request has a valid authenticated account

## Implementation Approaches

### 1. Middleware Approach (Recommended) ✅

**Setup**: Already configured in `settings.py`

The middleware automatically converts all HttpRequest objects to CustomRequest instances.

```python
# api/middleware.py
class CustomRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Converts HttpRequest → CustomRequest automatically
```

**Usage in Views**:
```python
@api_view([POST])
def my_view(request):
    # request is automatically a CustomRequest instance
    token = request.get_token()
    account = request.get_account()
    
    if request.is_authenticated():
        return Response({'message': 'Authenticated user'})
    else:
        return Response({'error': 'Not authenticated'}, status=401)
```

**Pros**:
- ✅ Automatic - works with all views
- ✅ No code changes required in existing views
- ✅ Consistent across entire application
- ✅ Works with Django admin and other third-party apps

**Cons**:
- ❌ Global impact - affects all requests
- ❌ Potential compatibility issues with some third-party packages

### 2. Decorator Approach

**Usage**:
```python
from api.decorators import with_custom_request, require_authentication

# Basic custom request
@api_view([POST])
@with_custom_request
def my_view(request):
    # request is now CustomRequest
    token = request.get_token()

# With authentication requirement
@api_view([POST])
@require_authentication
def protected_view(request):
    # request is CustomRequest and guaranteed to be authenticated
    account = request.get_account()  # Will not be None
```

**Pros**:
- ✅ Granular control - apply only where needed
- ✅ Built-in authentication checking option
- ✅ Explicit and clear intent

**Cons**:
- ❌ Must remember to add decorator to each view
- ❌ More verbose than middleware approach

### 3. Factory Function Approach

**Usage**:
```python
from api.base_views import create_custom_api_view

# Without authentication
@create_custom_api_view(['POST'])
def my_view(request):
    # request is CustomRequest
    pass

# With authentication
@create_custom_api_view(['POST'], require_auth=True)
def protected_view(request):
    # request is CustomRequest with guaranteed authentication
    pass
```

**Pros**:
- ✅ Clean syntax
- ✅ Built-in authentication option
- ✅ Combines api_view and custom request logic

**Cons**:
- ❌ Replaces standard @api_view decorator
- ❌ Less familiar to Django developers

## Current Implementation Status

✅ **Active**: Middleware approach is enabled in `settings.py`
- All views in the application now automatically receive CustomRequest instances
- No changes needed to existing view code
- CustomRequest methods are available immediately

## Migration Guide

### From the Old CustomRequest Usage

**Before** (manual wrapping):
```python
def my_view(request):
    custom_req = CustomRequest()
    # manual attribute copying...
    token = custom_req.get_token()
```

**After** (with middleware):
```python
def my_view(request):
    # request is already CustomRequest
    token = request.get_token()
    account = request.get_account()
    
    if request.is_authenticated():
        # Handle authenticated user
        pass
```

### Error Handling

The improved CustomRequest class handles errors gracefully:
- `get_token()` returns `None` if no valid token found
- `get_account()` returns `None` if account doesn't exist or no token
- `has_valid_token()` and `is_authenticated()` return boolean values

```python
@api_view([POST])
def my_view(request):
    account = request.get_account()
    if account is None:
        return Response({'error': 'Authentication required'}, status=401)
    
    # Process authenticated request
    return Response({'user_id': account.id})
```

## Testing

To test if CustomRequest is working:

```python
@api_view([GET])
def test_custom_request(request):
    return Response({
        'type': type(request).__name__,
        'has_token': request.has_valid_token(),
        'is_authenticated': request.is_authenticated(),
        'methods_available': [
            'get_token' in dir(request),
            'get_account' in dir(request),
            'has_valid_token' in dir(request),
            'is_authenticated' in dir(request)
        ]
    })
```

## Troubleshooting

1. **Middleware not working**: Check that `api.middleware.CustomRequestMiddleware` is in `MIDDLEWARE` setting
2. **AttributeError**: Ensure your CustomRequest class is properly imported
3. **Token not found**: Check that Authorization header format is `Bearer <token>`
4. **Account not found**: Verify that the token exists in the Account model

## Recommendations

1. **Use the middleware approach** for new projects or when you want all views to have CustomRequest
2. **Use decorators** if you need granular control or are migrating gradually
3. **Always check authentication** before accessing sensitive data
4. **Handle None values** gracefully when using `get_token()` and `get_account()`
