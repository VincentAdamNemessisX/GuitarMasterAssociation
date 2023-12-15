# Create your views here.
from django.shortcuts import render

from zone.models import Zone


def zone(request):
    if request.method == 'GET':
        zone_info = Zone.objects.filter(zone_id=request.GET.get('zone_id'), zone_status=1).first()
        if zone_info is None:
            return render(request, '500.html', {'error': '请求错误或专区已下线'})
        return render(request, 'zone-' + str(zone_info.zone_layout_mode) + '.html', {'zone': zone_info})
    return render(request, '500.html', {'error': '请求错误或专区已下线'})
