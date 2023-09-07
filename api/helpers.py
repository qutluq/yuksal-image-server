import os
import zipfile
from django.http import HttpResponse
from django.conf import settings
from urllib.parse import unquote


def extract_filename_directory(path):
    path_segments = path.split('/')

    # extract directory and filename parts from path
    filename = path_segments[-1] if len(path_segments) > 0 else ""
    directory = '/'.join(path_segments[:-1]) if len(path_segments) > 1 else ""

    if (filename != "") & ("." not in filename):
        # if path has not trailing slash, and path is directory
        directory = f"{directory}/{filename}/" if directory != "" else f"{filename}/"
        filename = ""

    return filename, directory


def unquote_path(path):
    unquoted_path = path
    if isinstance(path, (bytes,)):
        unquoted_path = unquote(path.decode("utf-8"))
    return unquoted_path


def is_request_for_images(path):
    filename, directory = extract_filename_directory(path)

    if filename == "":
        return [True, directory]

    return [False, directory]


def zipped_images(path, filenames):
    # Create a ZIP archive
    zip_filename = "images.zip"
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    # Create a ZIP file object
    zipf = zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED)

    unquoted_path = unquote_path(path)

    # Add each file to the ZIP archive
    for filename in filenames:
        filepath = os.path.join(settings.MEDIA_ROOT,
                                unquoted_path, unquote_path(filename))

        zipf.write(filepath)

    # Close the ZIP file
    zipf.close()

    return response
