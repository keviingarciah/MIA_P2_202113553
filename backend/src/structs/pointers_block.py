# Libraries
import struct

# Global
POINTERS_BLOCK_SIZE = 64


# ----------------------------------- Pointer Block ------------------------------------
class PointersBlock:
    # Constructor
    def __init__(self, pointers=[-1] * 16):
        self.pointers = pointers  # List[int] de tamaño 16
        # Data ->   16 * 4 = 64 bytes

    def pack(self):
        pointers_pack = b"".join(
            [struct.pack("i", pointer) for pointer in self.pointers]
        )

        return pointers_pack

    @classmethod
    def unpack(cls, data):
        pointers_unpack = struct.unpack("16i", data[0:64])

        pointer_block = cls(pointers_unpack)

        return pointer_block
