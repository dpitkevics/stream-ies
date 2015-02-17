from types import StringType

from hachoir_core.error import HachoirError
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_metadata import extractMetadata


class Metadata:
    """
    Class for retrieving metadata for video files
    """

    video_path = StringType('')

    def __init__(self, video_path):
        """
        Initializes class. Sets video_path as class parameter

        :param video_path: string
        :return:
        """

        self.video_path = video_path

    def extract_metadata(self):
        """
        Extracts metadata and returns it
        If video fail is invalid, exception is raised

        :return: list
        """

        filename, realname = unicodeFilename(self.video_path), self.video_path
        parser = createParser(filename, realname)
        if not parser:
            raise HachoirError("Parser not created")

        try:
            metadata = extractMetadata(parser)
        except HachoirError, err:
            print("Metadata extraction error: %s" % unicode(err))
            metadata = None

        if not metadata:
            raise HachoirError("Unable to extract metadata")

        text = metadata.exportPlaintext()

        return text