from plone.namedfile import file
from plone.namedfile.utils import _ensure_data


# backport https://github.com/plone/plone.namedfile/pull/181
def backport_181(orig):
    def getImageInfo(data):
        data = _ensure_data(data)
        size = len(data)
        if size > 30 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            # handle WEBPs
            content_type = "image/webp"
            chunk_type = data[12:16]
            if chunk_type == b"VP8 ":
                # WebP lossy (VP8): width and height are at offset 26–30 (2 bytes each, little endian)
                width = int.from_bytes(data[26:28], "little") & 0x3FFF
                height = int.from_bytes(data[28:30], "little") & 0x3FFF
                return content_type, width, height
            elif chunk_type == b"VP8L":
                # WebP lossless (VP8L): dimensions are encoded in 4 bytes at offset 21–25
                b = data[21:25]
                b0, b1, b2, b3 = b
                width = ((b1 & 0x3F) << 8 | b0) + 1
                height = ((b3 & 0xF) << 10 | b2 << 2 | (b1 >> 6)) + 1
                return content_type, width, height
            elif chunk_type == b"VP8X":
                # Extended WebP (VP8X)
                # Width: bytes 24-26 (little endian, minus 1)
                # Height: bytes 27-29 (little endian, minus 1)
                width_bytes = data[24:27]
                height_bytes = data[27:30]
                width = int.from_bytes(width_bytes, "little") + 1
                height = int.from_bytes(height_bytes, "little") + 1
                return content_type, width, height
        return orig(data)

    return getImageInfo


def apply_backport_181():
    file.getImageInfo = backport_181(file.getImageInfo)
