from rest_framework.response import Response

import mimetypes
import os
from urllib.parse import unquote

from django.conf import settings
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes
from .helpers import get_filename_list, zipped_images, is_request_for_image_paths


@api_view(["GET"])
@permission_classes([])
def get_media_path(request, path):
    """
    The get_media_path function is a helper function that takes in the request and
    path of a file. It then checks if the file exists, and returns an error message if
    it does not exist. If it does exist, it will return an HttpResponse with the
    correct headers to serve up the media.
    @param path: Determine the path of the file to be served
    return: A FileResponse object that contains the file specified in the path parameter
    """

    if not os.path.exists(f"{settings.MEDIA_ROOT}/{path}"):
        return Response("No such file exists.", status=404)

    [is_return_images, directory] = is_request_for_image_paths(path)

    if is_return_images:
        # return array of filenames
        files_path = unquote(os.path.join(
            settings.MEDIA_ROOT, directory)).encode("utf-8")
        filenames, total_files = get_filename_list(files_path, request)
        return Response({"filenames": filenames, "total": total_files}, status=200)

    # Guess the MIME type of a file. Like pdf/docx/xlsx/png/jpeg
    mimetype, encoding = mimetypes.guess_type(path, strict=True)
    if not mimetype:
        mimetype = "text/html"
    # By default, percent-encoded sequences are decoded with UTF-8, and invalid
    # sequences are replaced by a placeholder character.
    # Example: unquote('abc%20def') -> 'abc def'.
    file_path = unquote(os.path.join(
        settings.MEDIA_ROOT, path)).encode("utf-8")

    # FileResponse - A streaming HTTP response class optimized for files.
    return FileResponse(open(file_path, "rb"), content_type=mimetype)
