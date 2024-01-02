import json

from django.http import HttpResponse
from django.shortcuts import render

from message.models import Message


# Create your views here.
def message_help(request):
    return render(request, 'message_help.html')


def get_messages(request):
    if request.method == 'POST':
        if request.POST.get('user_id'):
            messages = (Message.objects.filter(receiver_id=request.POST.get('user_id'),
                                               message_status=0).order_by('-message_time'))
            data = {}
            for message in messages:
                data[message.message_id] = {
                    'message_id': message.message_id,
                    'message_content': message.message_content,
                    'message_time': message.message_time.strftime('%Y-%m-%d %H:%M:%S')
                }
            return HttpResponse(json.dumps({'status': 200, 'data': data, 'msg': '获取成功!'}),
                                content_type='application/json')
        return HttpResponse(json.dumps({'status': 401, 'msg': '参数错误，请勿修改js代码!'}),
                            content_type='application/json')
    return HttpResponse(json.dumps({'status': 400, 'msg': '调用方式错误，请勿修改js代码!'}),
                        content_type='application/json')


def read_message(request):
    if request.method == 'POST':
        if request.POST.get('message_id'):
            message = Message.objects.get(message_id=request.POST.get('message_id'))
            message.message_status = 1
            message.save()
            return HttpResponse(json.dumps({'status': 200, 'msg': '已读成功!'}), content_type='application/json')
        return HttpResponse(json.dumps({'status': 401, 'msg': '参数错误，请勿修改js代码!'}),
                            content_type='application/json')
    return HttpResponse(json.dumps({'status': 401, 'msg': '调用方式错误，请勿修改js代码!'}),
                        content_type='application/json')
