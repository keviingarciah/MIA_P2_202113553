# Libraries
import struct

# Global
EBR_SIZE = 30
logicalPartitionStart = 30  # EBR size


# ------------------------------------ MBR ------------------------------------
class EBR:
    # Constructor
    def __init__(self, status=" ", fit=" ", start=-1, size=-1, next=-1, name=" "):
        self.status = status  # Char   -> 1 byte
        self.fit = fit  # Char   -> 1 byte
        self.start = start  # Int    -> 4 bytes
        self.size = size  # Int    -> 4 bytes
        self.next = next  # Int    -> 4 bytes
        self.name = name  # String -> 16 bytes
        # Data -> 30 bytes

    def pack(self):
        status_pack = struct.pack("c", self.status.encode())
        fit_pack = struct.pack("c", self.fit.encode())
        start_pack = struct.pack("i", self.start)
        size_pack = struct.pack("i", self.size)
        next_pack = struct.pack("i", self.next)
        name_pack = struct.pack("16s", self.name.encode("utf-8"))

        return status_pack + fit_pack + start_pack + size_pack + next_pack + name_pack

    @classmethod
    def unpack(cls, data):
        status_unpack = struct.unpack("c", data[:1])[0].decode()
        fit_unpack = struct.unpack("c", data[1:2])[0].decode()
        start_unpack = struct.unpack("i", data[2:6])[0]
        size_unpack = struct.unpack("i", data[6:10])[0]
        next_unpack = struct.unpack("i", data[10:14])[0]
        name_unpack = (
            struct.unpack("16s", data[14:30])[0].decode("utf-8").replace("\x00", "")
        )

        ebr = cls(
            status_unpack,
            fit_unpack,
            start_unpack,
            size_unpack,
            next_unpack,
            name_unpack,
        )
        return ebr

    def set_ebr(self, fit, size, name):
        self.status = "2"  # Created
        self.fit = fit
        # self.start Dont change
        self.size = size
        self.next = logicalPartitionStart + size + self.start
        self.name = name


def recursive_ebr_operation(file, ebr_index, partition_fit, partition_size, name):
    # Read the packed EBR
    file.seek(ebr_index)
    packed_ebr = file.read(EBR_SIZE)
    ebr = EBR.unpack(packed_ebr)
    # print("EBR start:", ebr.start, "EBR next:", ebr.next)

    if ebr.next == -1:
        # Set EBR data
        ebr.set_ebr(partition_fit, partition_size, name)

        # Create a new EBR
        new_ebr = EBR()
        new_ebr.start = ebr.next

        # Write the previous EBR
        file.seek(ebr_index)
        serialized_ebr = ebr.pack()
        file.write(serialized_ebr)

        # Write the NEW EBR
        new_ebr_index = ebr.next
        file.seek(new_ebr_index)
        # print("New EBR start:", new_ebr.start, "New EBR next:", new_ebr.next)
        new_serialized_ebr = new_ebr.pack()
        file.write(new_serialized_ebr)
    else:
        # Recursively call the function for the next EBR
        recursive_ebr_operation(file, ebr.next, partition_fit, partition_size, name)
