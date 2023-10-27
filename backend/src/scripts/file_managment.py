# Modules
from main import logged
from structs.superblock import SuperBlock, SUPERBLOCK_SIZE
from structs.journaling import Journaling, JOURLANING_SIZE


# Script to create a file
class MKFILE:
    def __init__(self):
        self.path = "/"
        self.size = 0
        self.r = False
        self.cont = "/"

    def create_file(self):
        # Validate logged and permissions
        if not logged.logged_in:
            return "[ERROR] Usuario no loggeado."

        # Mandatory parameters
        if self.path == "/":
            return "[ERROR] No hay un directorio para crear el archivo."

        # Negative size
        if self.size < 0:
            return "[ERROR] El tamaño del archivo no puede ser negativo."

        # Read content file
        content_file = ""
        if self.cont != "/":
            with open(self.cont, "r", encoding="utf-8") as file:
                content_file = file.read()

        # Get the path of the file
        path = self.path.split("/")
        path.pop(0)
        # Get the name of the file
        file_name = path.pop(len(path) - 1)

        # Get mounted partition
        mounted_partition = logged.get_mounted_partition()
        # Set partition
        partition = mounted_partition.get_partition()

        # Get SuperBlock
        with open(mounted_partition.path, "rb+") as file:
            # Set pointer
            file.seek(partition.start)
            # Read SuperBlock
            packed_superblock = file.read(SUPERBLOCK_SIZE)
            # Unpack SuperBlock
            superblock = SuperBlock.unpack(packed_superblock)

            # Create folders
            if self.r:
                superblock.create_folder(file, path, partition.start, self.r)

            # Create file
            content_file, err = superblock.create_file(
                file, partition.start, path, file_name, self.size, content_file
            )

            if not err:
                # Journaling
                if superblock.fyle_system_type == 3:
                    # Get firs journaling
                    journaling_start = partition.start + SUPERBLOCK_SIZE
                    first_journaling = superblock.get_first_journaling(
                        file, journaling_start
                    )
                    # Get and increase count journaling
                    journaling_pointer = first_journaling.count
                    # Increase count
                    superblock.increase_count_journaling(
                        file, journaling_start, first_journaling
                    )

                    # Add journaling
                    new_journaling = Journaling()
                    new_journaling.add("mkfile", self.path, content_file)
                    # Serialize the journaling
                    serialized_journaling = new_journaling.pack()
                    # Write the journaling
                    file.seek(journaling_start + (JOURLANING_SIZE * journaling_pointer))
                    file.write(serialized_journaling)

                # Message
                return "[EXITOSO] Archivo creado con éxito."


# Script to create a folder
class MKDIR:
    def __init__(self):
        self.path = "/"
        self.r = False

    def create_folder(self):
        # Validate logged and permissions
        if not logged.logged_in:
            return "[ERROR] Usuario no loggeado."

        # Mandatory parameters
        if self.path == "/":
            return "[ERROR] No hay un directorio para crear la carpeta."

        # Get the path of the file
        path = self.path.split("/")
        path.pop(0)

        # Get mounted partition
        mounted_partition = logged.get_mounted_partition()
        # Set partition
        partition = mounted_partition.get_partition()

        # Get SuperBlock
        with open(mounted_partition.path, "rb+") as file:
            # Set pointer
            file.seek(partition.start)
            # Read SuperBlock
            packed_superblock = file.read(SUPERBLOCK_SIZE)
            # Unpack SuperBlock
            superblock = SuperBlock.unpack(packed_superblock)

            # Create folder block
            superblock.create_folder(file, path, partition.start, self.r)

            # Journaling
            if superblock.fyle_system_type == 3:
                # Get firs journaling
                journaling_start = partition.start + SUPERBLOCK_SIZE
                first_journaling = superblock.get_first_journaling(
                    file, journaling_start
                )
                # Get and increase count journaling
                journaling_pointer = first_journaling.count
                # Increase count
                superblock.increase_count_journaling(
                    file, journaling_start, first_journaling
                )

                # Add journaling
                new_journaling = Journaling()
                new_journaling.add("mkdir", self.path, "")
                # Serialize the journaling
                serialized_journaling = new_journaling.pack()
                # Write the journaling
                file.seek(journaling_start + (JOURLANING_SIZE * journaling_pointer))
                file.write(serialized_journaling)

        # Message
        return "[EXITOSO] Carpeta creada con éxito."
