from django.http import HttpResponse
from django.shortcuts import render, redirect
from .function import remove_collection_by_id


# Create your views here.

def delete_specific_collection(request):
    if request.method == 'POST':
        collection_id = request.POST.get('collection_id')
        if collection_id is None:
            return HttpResponse({'message': '删除失败!','status': '400'})
        if remove_collection_by_id(collection_id):
            return HttpResponse({'message': '删除成功!', 'status': '200'})
        else:
            return HttpResponse({'message': '删除失败!','status': '400'})
    return render(request, '500.html', {'error': '请求错误!'})
