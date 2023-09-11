from rest_framework.decorators import api_view
from api.index import get_media, post_media


@api_view(["GET", "POST"])
def request_media(request, path):

    if request.method == 'GET':
        response = get_media(request, path)
        return response

    if request.method == 'POST':
        response = post_media(request, path)
        return response
