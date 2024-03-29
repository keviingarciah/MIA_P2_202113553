# Libraries
import datetime
import os
import random
import math

# Modules
from main import mounted_partitions, CARNET
from structs.mbr import MBR, MBR_SIZE
from structs.partition import MountedPartition
from structs.ebr import EBR, recursive_ebr_operation
from structs.superblock import SuperBlock, SUPERBLOCK_SIZE
from structs.inode import INODE_SIZE
from structs.folder_block import FOLDER_BLOCK_SIZE
from structs.journaling import JOURLANING_SIZE


# Script to create a disk
class MKDISK:
    def __init__(self):
        self.size = 0
        self.path = "/"
        self.fit = "FF"
        self.unit = "K"

    # Script to create an empty file
    def create_disk(self):
        # Validate the size and path
        if self.size == 0 or self.path == "/":
            return "[ERROR] Falta un parámetro obligatorio."

        # Validate a positive size
        if self.size < 0:
            return "[ERROR] El tamaño debe ser positivo."

        # Obtener la carpeta donde se encuentra el archivo
        folder = os.path.dirname(self.path)
        # Crear las carpetas si no existen
        os.makedirs(folder, exist_ok=True)

        # Create the file
        with open(self.path, "wb") as file:
            # Get the disk size
            disk_size = 0
            if self.unit == "B":
                disk_size = 1
            elif self.unit == "K":
                disk_size = 1000
            elif self.unit == "M":
                disk_size = 1000000
            # Write the file
            for i in range(0, self.size):
                file.write(b"\x00" * disk_size)

        # Set fit
        disk_fit = ""
        if self.fit == "BF":
            disk_fit = "B"
        elif self.fit == "FF":
            disk_fit = "F"
        elif self.fit == "WF":
            disk_fit = "W"

        # Modify the file
        with open(self.path, "rb+") as file:
            # Set the pointer at the beginning of the file
            file.seek(0)
            # Create the MBR
            mbr = MBR(
                disk_size * self.size,
                datetime.datetime.now(),
                random.randint(0, 1000),
                disk_fit,
            )
            # Serialize the MBR
            serialized_mbr = mbr.pack()
            file.write(serialized_mbr)

            # Succes Message
            return f"[EXITOSO] Se creó el disco {self.path} exitosamente."


# Script to remove a disk
class RMDISK:
    def __init__(self):
        self.path = "/"

    def delete_disk(self):
        # Verify if the file exists
        if os.path.exists(self.path):
            try:
                # Delete the file
                os.remove(self.path)
                return f"[EXITOSO] El disco {self.path} ha sido eliminado exitosamente."

            except Exception as e:
                return f"No se pudo eliminar el disco {self.path}. Error: {e}"
        else:
            return f"El disco {self.path} no existe."


# Script to create a partition
class FDISK:
    def __init__(self):
        self.size = 0
        self.path = "/"
        self.name = " "
        self.unit = "K"
        self.type = "P"
        self.fit = "WF"
        self.delete = "full"
        self.add = 0

    # Create a partition
    def create_partition(self):
        # Validate the size and path
        if self.size == 0 or self.path == "/":
            return "[ERROR] Falta un parámetro obligatorio."

        # Validate a positive size
        if self.size < 0:
            return "[ERROR] El tamaño debe ser positivo."

        # Get the partition size
        partition_size = self.size
        if self.unit == "B":
            partition_size = self.size
        elif self.unit == "K":
            partition_size = 1000 * self.size
        elif self.unit == "M":
            partition_size = 1000000 * self.size

        # Set fit
        partition_fit = ""
        if self.fit == "BF":
            partition_fit = "B"
        elif self.fit == "FF":
            partition_fit = "F"
        elif self.fit == "WF":
            partition_fit = "W"

        # Read the file
        with open(self.path, "rb+") as file:
            # Leer los datos empaquetados del archivo
            packed_mbr = file.read(MBR_SIZE)
            # Unpack MBR
            mbr = MBR.unpack(packed_mbr)

            # Type of partition
            if self.type == "P":
                # Set primary partition data
                condition = mbr.set_primary_partition(
                    self.type, partition_fit, partition_size, self.name
                )
                if condition:
                    # Write the MBR
                    file.seek(0)
                    serialized_mbr = mbr.pack()
                    file.write(serialized_mbr)

                    # Message
                    return f"[EXITOSO] La partición primaria {self.name} ha sido creada exitosamente."
                else:
                    return "[ERROR] No se pudo crear la partición primaria."

            elif self.type == "E":
                # Create the EBR
                first_ebr = EBR()
                # Set extended partition data
                first_ebr_index, condition = mbr.set_extended_partition(
                    self.type, partition_fit, partition_size, self.name
                )
                if condition:
                    first_ebr.start = first_ebr_index
                    # Write the MBR
                    file.seek(0)
                    serialized_mbr = mbr.pack()
                    file.write(serialized_mbr)
                    # Write the EBR
                    file.seek(first_ebr_index)
                    serialized_ebr = first_ebr.pack()
                    file.write(serialized_ebr)

                    # Message
                    return f"[EXITOSO] La partición extendida {self.name} ha sido creada exitosamente."
                else:
                    return "[ERROR] No se pudo crear la partición extendida."

            elif self.type == "L":
                # Set logical partition data (EBR)
                first_ebr_index, condition = mbr.set_logical_partition()

                if condition:
                    recursive_ebr_operation(
                        file, first_ebr_index, partition_fit, partition_size, self.name
                    )

                    # Message
                    return f"[EXITOSO] La partición lógica {self.name} ha sido creada exitosamente."
                else:
                    return "[ERROR] No se pudo crear la partición lógica."


# Script to mount partitions
class MOUNT:
    def __init__(self):
        self.path = "/"
        self.name = " "

    def mount_partition(self):
        # Validate the name and path
        if self.name == " " or self.path == "/":
            return "[ERROR] Falta un parámetro obligatorio."

        # Read the file
        with open(self.path, "rb+") as file:
            # Leer los datos empaquetados del MBR
            packed_mbr = file.read(MBR_SIZE)
            # Unpack MBR
            mbr = MBR.unpack(packed_mbr)
            # Get disk name
            disk_name = os.path.splitext(os.path.basename(self.path))[0]
            # Get partition index and partition
            partition_index = mbr.get_partition_index(self.name)
            # Set partition
            partition = mbr.get_partition_by_index(partition_index)
            # Set new partition id
            partition_id = CARNET + str(partition_index) + disk_name

            if partition_id in mounted_partitions:
                return "[ERROR] La partición ya se encuentra montada."
            else:
                # Set mounted partition
                mounted_partition = MountedPartition(self.path, partition)
                # Add the partition to the global dictionary
                mounted_partitions[partition_id] = mounted_partition

                # Message
                return f"[EXITOSO] La partición {partition_id} ha sido montada exitosamente."


# Script to format partitions
class MKFS:
    def __init__(self):
        self.id = " "
        self.type = "full"
        self.fs = "2fs"

    def format_partition(self):
        # Validate the id
        if self.id == " ":
            return "[ERROR] Falta un parámetro obligatorio."

        # Validate mounted partitions
        if self.id in mounted_partitions:
            pass
        else:
            return "[ERROR] La partición no está montada."

        # Get mounted partition
        mounted_partition = mounted_partitions[self.id]
        # Set partition
        partition = mounted_partition.get_partition()
        # print("Partition:", partition.name)

        # numerador = (partition_montada.size - sizeof(Structs::Superblock)
        # denrominador base = (4 + sizeof(Structs::Inodes) + 3 * sizeof(Structs::Fileblock))
        # temp = "2" ? 0 : sizeof(Structs::Journaling)
        # denrominador = base + temp
        # n = floor(numerador / denrominador)

        # Calculus
        numerator = partition.size - SUPERBLOCK_SIZE
        denominator = (
            4 + INODE_SIZE + 3 * FOLDER_BLOCK_SIZE
        )  # 64 bytes to FileBlock, FolderBlock and PointerBlock
        temp = 0 if self.fs == "2fs" else JOURLANING_SIZE  # Journaling size
        denominator += temp
        n = math.floor(numerator / denominator)

        # Set superblock data
        new_superblock = SuperBlock()

        new_superblock.free_blocks_count = 3 * n
        new_superblock.free_inodes_count = n

        date = datetime.datetime.now()
        new_superblock.mount_time = date
        new_superblock.unmount_time = date
        new_superblock.mount_count = 1

        new_superblock.create_ext2(n, partition, mounted_partition.path)
        return "[EXITOSO] Se formateó la partición exitosamente con el formato ext2."
