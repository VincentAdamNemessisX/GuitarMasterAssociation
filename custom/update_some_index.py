from django.shortcuts import redirect
from django.utils import timezone

from zone.models import Zone


def update_zone_active_time(func):
    def _(request, *args, **keys):
        func(request, *args, **keys)
        zone_info = Zone.objects.get(zone_id=request.GET.get('zone_id'))
        zone_info.zone_last_active_time = timezone.now()
        return None

    return _