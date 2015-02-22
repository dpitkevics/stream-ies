import os


DOWNLOAD_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep + "temp" + os.sep

CACHE_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep + "cache" + os.sep

RESOURCES_DIR = os.path.dirname(os.path.realpath(__file__)) + os.sep + "resources" + os.sep

VIDEO_FORMATS = (
    'mp4',
    'avi',
    'mov',
)