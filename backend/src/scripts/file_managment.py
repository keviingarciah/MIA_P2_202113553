# Libraries
from colorama import init, Fore

# Modules
from backend.src.execution import CARNET, mounted_partitions, logged
from structs.superblock import SuperBlock, SUPERBLOCK_SIZE
from structs.inode import Inode, INODE_SIZE
from structs.folder_block import FolderBlock, CONTENT_SIZE
from structs.journaling import Journaling, JOURLANING_SIZE

# Initialize colorama
init(autoreset=True)


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
            print(Fore.RED + "ERROR: Usuario no loggeado.")
            return

        # Mandatory parameters
        if self.path == "/":
            print(Fore.RED + "ERROR: No hay un directorio para crear el archivo.")
            return

        # Negative size
        if self.size < 0:
            print(Fore.RED + "ERROR: El tamaño del archivo no puede ser negativo.")
            return

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
                print(Fore.GREEN + "Archivo creado con éxito.")


# Script to show the content of a file
class CAT:
    def __init__(self):
        self.files = []

    def show_files(self):
        # Validate logged and permissions
        if not logged.logged_in:
            print(Fore.RED + "ERROR: Usuario no loggeado.")
            return

        # Mandatory parameters
        if len(self.files) == 0:
            print(Fore.RED + "ERROR: No hay algún archivo para mostrar su contenido.")
            return

        for file_path in self.files:
            # Get the path of the file
            path = file_path.split("/")
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

            # Get the content of the file
            content = superblock.get_file_content(file, path)

            # Print content
            print(content)


# Script to remove a file
class REMOVE:
    def __init__(self):
        self.path = "/"

    def remove_file(self):
        # Validate logged and permissions
        if not logged.logged_in:
            print(Fore.RED + "ERROR: Usuario no loggeado.")
            return

        # Mandatory parameters
        if self.path == "/":
            print(Fore.RED + "ERROR: No hay un directorio para remover el archivo.")
            return

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

            # Remove file
            superblock.remove_file(file, partition.start, path)


# Script to edit a file
class EDIT:
    def __init__(self):
        self.path = "/"
        self.cont = "/"

    def edit_file(self):
        # Validate logged and permissions
        if not logged.logged_in:
            print(Fore.RED + "ERROR: Usuario no loggeado.")
            return

        # Mandatory parameters
        if self.path == "/" or self.cont == "/":
            print(Fore.RED + "ERROR: No hay un directorio para crear el archivo.")
            return

        # Read content file
        content_file = ""
        with open(self.cont, "r", encoding="utf-8") as file:
            content_file = file.read()

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

            # Edit file
            superblock.edit_file_content(file, partition.start, path, content_file)

        # Message
        print(Fore.GREEN + "Archivo editado con éxito.")


# Script to rename a file
class RENAME:
    def __init__(self):
        self.path = "/"
        self.name = ""

    def rename(self):
        # Validate logged and permissions
        if not logged.logged_in:
            print(Fore.RED + "ERROR: Usuario no loggeado.")
            return

        # Mandatory parameters
        if self.path == "/" or self.name == "":
            print(Fore.RED + "ERROR: Falta un parámetro.")
            return

        # Get the path of the file
        path = self.path.split("/")
        path.pop(0)
        # Actual name of the file
        actual_name = path.pop(len(path) - 1)

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

            # Edit file
            superblock.rename(file, partition.start, path, actual_name, self.name)

        # Message
        print(Fore.GREEN + "Archivo renombrado con éxito.")


# Script to create a folder
class MKDIR:
    def __init__(self):
        self.path = "/"
        self.r = False

    def create_folder(self):
        # Validate logged and permissions
        if not logged.logged_in:
            print(Fore.RED + "ERROR: No se puede crear el usuario.")
            return

        # Mandatory parameters
        if self.path == "/":
            print(Fore.RED + "ERROR: No hay un directorio para crear la carpeta")
            return

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
        print(Fore.GREEN + "Carpeta creada con éxito.")
