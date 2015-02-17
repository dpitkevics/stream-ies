from types import StringType

from hachoir_core.error import HachoirError
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_core.tools import makePrintable
from hachoir_metadata import extractMetadata
from hachoir_core.i18n import getTerminalCharset


class Metadata:

    video_path = StringType('')

    def __init__(self, video_path):
        self.video_path = video_path

    def extract_metadata(self):
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

        charset = getTerminalCharset()
        for line in text:
            print makePrintable(line, charset)