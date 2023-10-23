# Libraries
import struct
import datetime

# Modules
from structs.partition import Partition, PARTITION_SIZE

# Global
MBR_SIZE = 121
partitionStart = 121  # MBR size


# ------------------------------------ MBR ------------------------------------
class MBR:
    # Constructor
    def __init__(self, size, date, signature, fit):
        self.size = size  # Int -> 4 bytes
        self.date = date  # Timestamp (float) -> 4 bytes
        self.signature = signature  # Int -> 4 bytes
        self.fit = fit  # Char -> 1 byte
        # MBR Data -> 13 bytes
        self.partitions = [
            Partition() for _ in range(4)
        ]  # Partitions[4] -> 4 * 27 bytes = 108 bytes
        # Total -> 121 bytes

    def pack(self):
        size_pack = struct.pack("i", self.size)
        date_pack = struct.pack("f", self.date.timestamp())
        signature_pack = struct.pack("i", self.signature)
        fit_pack = struct.pack("c", self.fit.encode())

        partitions_pack = b"".join([partition.pack() for partition in self.partitions])

        return size_pack + date_pack + signature_pack + fit_pack + partitions_pack

    @classmethod
    def unpack(cls, data):
        size_unpack = struct.unpack("i", data[:4])[0]
        date_unpack = datetime.datetime.fromtimestamp(struct.unpack("f", data[4:8])[0])
        signature_unpack = struct.unpack("i", data[8:12])[0]
        fit_unpack = struct.unpack("c", data[12:13])[0].decode()
        partitions_unpack = [
            Partition.unpack(data[i : i + PARTITION_SIZE])
            for i in range(13, len(data), PARTITION_SIZE)
        ]

        mbr = cls(size_unpack, date_unpack, signature_unpack, fit_unpack)
        mbr.partitions = partitions_unpack

        return mbr

    def show_mbr(self):
        # Print unpacked MBR
        print("\nUnpacked MBR:")
        print("Size:", self.size)
        print("Date:", self.date)
        print("Signature:", self.signature)
        print("Fit:", self.fit)
        for i, partition in enumerate(self.partitions):
            print(f"\nPartition {i + 1}:")
            print("  Status:", partition.status)
            print("  Type:", partition.type)
            print("  Fit:", partition.fit)
            print("  Start:", partition.start)
            print("  Size:", partition.size)
            print("  Name:", partition.name)

    def set_primary_partition(self, typep, fit, size, name):
        global partitionStart
        condition = False

        for partition in self.partitions:
            if partition.size == -1:
                # Set partition data
                partition.status = "2"  # Created
                partition.type = typep
                partition.fit = fit
                partition.start = partitionStart
                partition.size = size
                partition.name = name

                # Set condition to true
                condition = True
                break
            else:
                partitionStart += size

        return condition

    def set_extended_partition(self, typep, fit, size, name):
        global partitionStart
        condition = False

        for partition in self.partitions:
            if partition.type == typep:
                return partitionStart, condition

        for partition in self.partitions:
            if partition.size == -1:
                # Set partition data
                partition.status = "2"  # Created
                partition.type = typep
                partition.fit = fit
                partition.start = partitionStart
                partition.size = size
                partition.name = name

                # Set condition to true
                condition = True
                break
            else:
                partitionStart += size

        return partitionStart, condition

    def set_logical_partition(self):
        condition = False

        for partition in self.partitions:
            if partition.type == "E":
                # Set condition to true
                condition = True

                # Return the extended partition start
                return partition.start, condition

        return 0, condition

    def get_partition_index(self, name):
        for i, partition in enumerate(self.partitions):
            if partition.name == name:
                return i + 1

    def get_partition_by_index(self, index):
        return self.partitions[index - 1]
