from rest_framework.decorators import api_view
from api.index import get_media


@api_view(["GET"])
def request_media(request, path):

    if request.method == 'GET':
        response = get_media(request, path)
        return response
