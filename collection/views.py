from custom.goto_controller import redirect_referer
from .function import remove_collection_by_id


# Create your views here.

@redirect_referer
def delete_specific_collection(request):
    if request.method == 'POST':
        collection_id = request.POST.get('collection_id')
        remove_collection_by_id(collection_id)
