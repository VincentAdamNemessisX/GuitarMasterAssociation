from django.http import HttpResponse

from custom.goto_controller import redirect_referer
from .function import remove_collection_by_id


# Create your views here.

@redirect_referer
def delete_specific_collection(request):
    if request.method == 'POST':
        collection_id = request.POST.get('collection_id')
        if collection_id is None:
            return HttpResponse({'message': '删除失败!','status': '400'})
        if remove_collection_by_id(collection_id):
            return HttpResponse({'message': '删除成功!', 'status': '200'})
        else:
            return HttpResponse({'message': '删除失败!','status': '400'})
