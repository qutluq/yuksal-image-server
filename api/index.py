import json
from rest_framework.response import Response

import mimetypes
import os
from urllib.parse import unquote

from django.conf import settings
from django.http import FileResponse
from rest_framework.decorators import api_view

from utils.index import ThumbnailMd, ThumbnailSm
from .helpers import get_filename_list, is_request_for_image_paths


def get_media(request, path):
    """
    Returns media file or filenames.

    Parameters:
        path (str): path that may or may not include filename, 
        size (str): sm or md, if not set main file with the original resolution will be returned

    Returns:
        media(blob): if path includes filename.
        filenames(str[]): if path does not include filename. 
    """

    main_file_path = unquote(os.path.join(
        "media", path)).encode("utf-8")

    if not os.path.exists(main_file_path):
        # main file or directory does not exist
        return Response("No such file exists.", status=404)

    [is_return_filenames, directory] = is_request_for_image_paths(path)

    if is_return_filenames:
        # return array of filenames
        files_path = unquote(os.path.join(
            "media", directory)).encode("utf-8")
        filenames, total_files = get_filename_list(files_path, request)
        return Response(json.dumps({"filenames": filenames, "total": total_files}), status=200)

    # Guess the MIME type of a file. Like pdf/docx/xlsx/png/jpeg
    mimetype, encoding = mimetypes.guess_type(path, strict=True)
    if not mimetype:
        mimetype = "text/html"

    size = request.GET.get("size", "")
    # By default, percent-encoded sequences are decoded with UTF-8, and invalid
    # sequences are replaced by a placeholder character.
    # Example: unquote('abc%20def') -> 'abc def'.
    file_path = unquote(os.path.join(
        "media", size, path)).encode("utf-8")

    valid_sizes = ['sm', 'md']
    if (not os.path.exists(file_path)) & (size in valid_sizes) & mimetype.startswith('image/'):
        # image with size={size} does not exist, create it
        source_file = open(main_file_path, 'rb')
        if (size == 'sm'):
            image_generator = ThumbnailSm(source=source_file)

        if (size == 'md'):
            image_generator = ThumbnailMd(source=source_file)

        result = image_generator.generate()

        dest = open(file_path, 'wb')
        dest.write(result.read())
        dest.close()

    if (size == ""):
        file_path = main_file_path

    return FileResponse(open(file_path, "rb"), content_type=mimetype)
