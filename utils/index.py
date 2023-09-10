from imagekit import ImageSpec
from imagekit.processors import ResizeToCover


class ThumbnailSm(ImageSpec):
    processors = [ResizeToCover(100, 100)]
    format = 'JPEG'
    options = {'quality': 60}


class ThumbnailMd(ImageSpec):
    processors = [ResizeToCover(300, 300)]
    format = 'JPEG'
    options = {'quality': 60}
