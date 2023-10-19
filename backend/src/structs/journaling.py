# Library Imports
import struct
import datetime

# Global
JOURLANING_SIZE = 114


# ------------------------------------ Journaling ------------------------------------
class Journaling:
    # Constructor
    def __init__(self, count=0):
        self.count = count  # Int    -> 4 bytes
        self.content = Information()  # -> 110 bytes
        #   Total: 114 bytes

    def pack(self):
        count_pack = struct.pack("i", self.count)
        content_pack = self.content.pack()

        return count_pack + content_pack

    @classmethod
    def unpack(cls, data):
        count_unpack = struct.unpack("i", data[0:4])[0]

        new_journaling = cls(count_unpack)
        new_journaling.content = Information.unpack(data[4:114])

        return new_journaling

    def add(self, operation, path, content):
        self.content = Information(
            operation[:10], path[:32], content[:64], datetime.datetime.now()
        )


# ------------------------------------ Journaling Info------------------------------------
class Information:
    # Constructor
    def __init__(self, operation="", path="", content="", date=0):
        self.operation = operation  # Char[10]    -> 10 bytes
        self.path = path  # Char[32]    -> 32 bytes
        self.content = content  # Char[64]    -> 64 bytes
        self.date = date  # Timestamp (float)    -> 4 bytes
        # Total: 110 bytes

    def pack(self):
        operation_pack = struct.pack("10s", self.operation.encode("utf-8"))
        path_pack = struct.pack("32s", self.path.encode("utf-8"))
        content_pack = struct.pack("64s", self.content.encode("utf-8"))
        date_pack = struct.pack("f", self.date.timestamp())

        return operation_pack + path_pack + content_pack + date_pack

    @classmethod
    def unpack(cls, data):
        operation_unpack = struct.unpack("10s", data[0:10])[0]
        path_unpack = struct.unpack("32s", data[10:42])[0]
        content_unpack = struct.unpack("64s", data[42:106])[0]
        date_unpack = struct.unpack("f", data[106:110])[0]

        return cls(
            operation_unpack.decode("utf-8").replace("\x00", ""),
            path_unpack.decode("utf-8").replace("\x00", ""),
            content_unpack.decode("utf-8").replace("\x00", ""),
            datetime.datetime.fromtimestamp(date_unpack),
        )
