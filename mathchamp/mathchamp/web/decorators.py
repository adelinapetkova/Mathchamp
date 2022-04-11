from functools import wraps
from django.http import HttpResponseRedirect


def students_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        user = request.user
        if user.is_student:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/web/')

    return wrap


def teachers_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        user = request.user
        if user.is_teacher:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/web/')

    return wrap
