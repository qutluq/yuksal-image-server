from rest_framework.decorators import api_view
from api.index import delete_media, get_media, post_media


@api_view(["GET", "POST", "DELETE"])
def request_media(request, path):

    if request.method == 'GET':
        response = get_media(request, path)
        return response

    if request.method == 'POST':
        response = post_media(request, path)
        return response

    if request.method == 'DELETE':
        response = delete_media(request, path)
        return response
