import os

DOWNLOAD_DIR = os.path.dirname(os.path.realpath(__file__)) + "/temp/"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)