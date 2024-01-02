from django.http.response import HttpResponseRedirect


def redirect_referer(func):
    def _(request, *args, **keys):
        func(request, *args, **keys)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return _
