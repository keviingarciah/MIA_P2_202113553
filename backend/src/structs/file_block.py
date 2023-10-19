# Libraries
import struct

# Global
FILE_BLOCK_SIZE = 64


# ----------------------------------- File Block ------------------------------------
class FileBlock:
    # Constructor
    def __init__(self, content=" "):
        self.content = content  # Char[64] -> 64 bytes

    def pack(self):
        content_pack = struct.pack("64s", self.content.encode("utf-8"))

        return content_pack

    @classmethod
    def unpack(cls, data):
        content_unpack = (
            struct.unpack("64s", data[0:64])[0].decode("utf-8").replace("\x00", " ")
        )

        file_block = cls(content_unpack)

        return file_block

    def set_content(self, content):
        self.content = content

    def get_content(self):
        return self.content

    def show_file_block(self):
        # Print unpacked FileBlock
        print("\nUnpacked FileBlock:")
        print("----------------")
        print(self.content)
