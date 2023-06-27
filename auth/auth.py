from functools import wraps
from django.core.exceptions import PermissionDenied


def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, * args, **kwargs):
            # check if user belong to the group that have access to the view.
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied(f'Access Denied. user not belong to group {group_name}.')
        return wrapped_view
    return decorator