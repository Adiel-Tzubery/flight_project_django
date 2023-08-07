from functools import wraps
from django.core.exceptions import PermissionDenied
from dal.dal import DAL


def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, * args, **kwargs):
            # check if user belong to the group that~ have access to the view.
            # print(request.user.id)
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied(
                    f'Access Denied. user not belong to group {group_name}.')
        return wrapped_view
    return decorator
<<<<<<< HEAD
=======


# if request doesn't have the group, why not get to the group
# manually using the dal?
#  group = DAL.get_user_by_username(username=request.user.username).user_role.group

# one problem, the value of request.user.username is empty string
>>>>>>> 67ead05e66aec98e01d0bd2b95b3906e5918d43f
