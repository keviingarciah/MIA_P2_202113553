# Libraries
import struct

# Global
PARTITION_SIZE = 27


# ------------------------------------ Partition ------------------------------------
class Partition:
    # Constructor
    def __init__(self, status=" ", type=" ", fit=" ", start=-1, size=-1, name=" "):
        self.status = status  # Char   -> 1 byte
        """
        0: Inactive
        1: Active / Mounted
        2: Created
        3: Deleted        
        """

        self.type = type  # Char -> 1 byte
        self.fit = fit  # Char -> 1 byte
        self.start = start  # Int    -> 4 bytes
        self.size = size  # Int    -> 4 bytes
        self.name = name  # String -> 16 bytes
        # Data -> 27 bytes

    def pack(self):
        status_pack = struct.pack("c", self.status.encode())
        type_pack = struct.pack("c", self.type.encode())
        fit_pack = struct.pack("c", self.fit.encode())
        start_pack = struct.pack("i", self.start)
        size_pack = struct.pack("i", self.size)
        name_pack = struct.pack("16s", self.name.encode("utf-8"))

        return status_pack + type_pack + fit_pack + start_pack + size_pack + name_pack

    @classmethod
    def unpack(cls, data):
        status_unpack = struct.unpack("c", data[:1])[0].decode()
        type_unpack = struct.unpack("c", data[1:2])[0].decode()
        fit_unpack = struct.unpack("c", data[2:3])[0].decode()
        start_unpack = struct.unpack("i", data[3:7])[0]
        size_unpack = struct.unpack("i", data[7:11])[0]
        name_unpack = (
            struct.unpack("16s", data[11:27])[0].decode("utf-8").replace("\x00", "")
        )

        partition = cls(
            status_unpack,
            type_unpack,
            fit_unpack,
            start_unpack,
            size_unpack,
            name_unpack,
        )
        return partition


def extract_partition_index(id):
    # cadena = "531Disco2"   id
    index = 3  # Cambia esta posición según tus necesidades

    # Encuentra la primera aparición de dígitos en la cadena
    start = None
    for i, caracter in enumerate(id):
        if caracter.isdigit():
            start = i
            break

    # Si se encontró una secuencia de dígitos, intenta extraer el número en la posición deseada
    if start is not None:
        number = ""
        for i in range(start, len(id)):
            if id[i].isdigit():
                number += id[i]
            else:
                break

        if number:
            partition_index = number[index - 1]
            # print(partition_index)

            return int(partition_index)
        else:
            print("No se encontraron dígitos en la posición especificada.")
    else:
        print("No se encontraron dígitos en el id.")


# ------------------------------------ Mounted Partition ------------------------------------
class MountedPartition:
    # Constructor
    def __init__(self, path, partition):
        self.path = path
        self.partition = partition

    def get_path(self):
        return self.path

    def get_partition(self):
        return self.partition
