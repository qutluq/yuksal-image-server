import json
from rest_framework.response import Response

import mimetypes
import os
from urllib.parse import unquote

from django.conf import settings
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes
from .helpers import get_filename_list, is_request_for_image_paths


@api_view(["GET"])
def get_media_path(request, path):
    """
    Returns media file or filenames.

    Parameters:
        path (str): path that may or may not include filename, 

    Returns:
        media(blob): if path includes filename.
        filenames(str[]): if path does not include filename. 
    """

    if not os.path.exists(f"{settings.MEDIA_ROOT}/{path}"):
        return Response("No such file exists.", status=404)

    [is_return_filenames, directory] = is_request_for_image_paths(path)

    if is_return_filenames:
        # return array of filenames
        files_path = unquote(os.path.join(
            settings.MEDIA_ROOT, directory)).encode("utf-8")
        filenames, total_files = get_filename_list(files_path, request)
        return Response(json.dumps({"filenames": filenames, "total": total_files}), status=200)

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
