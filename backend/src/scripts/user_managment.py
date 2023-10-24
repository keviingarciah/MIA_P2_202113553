# Libraries
import re

# Module
from main import mounted_partitions, logged
from structs.user import User
from structs.partition import Partition, MountedPartition
from structs.superblock import SuperBlock, SUPERBLOCK_SIZE


# Script to login
class LOGIN:
    def __init__(self):
        self.user = ""
        self.password = ""
        self.id = ""

    def login(self):
        # Validate logged
        if logged.logged_in:
            return "[ERROR] Ya hay una sesión activa.]"

        # Validate mandatory parameters
        if self.user == "" or self.password == "" or self.id == "":
            return "[ERROR] Faltan parámetros obligatorios."

        # Validate mounted partitions
        if self.id in mounted_partitions:
            pass
        else:
            return f"[ERROR] La partición {self.id} no está montada."

        # Get mounted partition
        mounted_partition = mounted_partitions[self.id]
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

            # Find users.txt
            content, _ = superblock.get_users_file(file, "users.txt")

            # Read the file
            for line in content.split("\n"):
                if line.strip():
                    parts = [part.strip() for part in line.split(",")]
                    # print(parts)
                    if parts[1] == "U":
                        if parts[3] == self.user and parts[4] == str(self.password):
                            # Set user
                            user = User(parts[3], parts[4])
                            # Set logged
                            logged.user = user
                            logged.mounted_partition = mounted_partition
                            logged.logged_in = True

                            return "[EXITOSO] Login exitoso."
            # Message
            return "[ERROR] Login fallido."


# Script to logout
class LOGOUT:
    def __init__(self):
        pass

    def logout(self):
        # Validate logged
        if logged.logged_in:
            # Set logged
            logged.user = User()
            logged.mounted_partition = MountedPartition("", Partition())
            logged.logged_in = False
            return "[EXITOSO] Logout exitoso."
        else:
            return "[ERROR] No hay una sesión activa."


# Script to mkgrp
class MKGRP:
    def __init__(self):
        self.name = ""

    def create_group(self):
        # Validate logged and permissions
        if not logged.logged_in or logged.user.user_name != "root":
            return "[ERROR] No se puede crear el grupo."

        # Validate mandatory parameters
        if self.name == "":
            return "[ERROR] Faltan parámetros obligatorios."

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

            # Find users.txt
            content, pointer = superblock.get_users_file(file, "users.txt")

            # Exists group
            gid = 1

            for line in content.split("\n"):
                if line.strip():
                    parts = [part.strip() for part in line.split(",")]
                    if parts[1] == "G":
                        if not parts[2] == self.name:
                            gid += 1
                        else:
                            return "[ERROR] El grupo ya existe."

            # Set content
            new_content = f"{str(gid)},G,{self.name}\n"
            content += new_content
            clean_content = re.sub(r"[ \t\r\f\v]+", "", content)

            # Set the content in the file
            superblock.set_users_file(file, partition.start, pointer, clean_content)

        # Message
        return "[EXITOSO] Grupo creado exitosamente."


# Script to rmgrp
class RMGRP:
    def __init__(self):
        self.name = ""

    def remove_group(self):
        # Validate logged and permissions
        if not logged.logged_in or logged.user.user_name != "root":
            return "[ERROR] No se puede eliminar el grupo."

        # Validate mandatory parameters
        if self.name == "":
            return "[ERROR] Faltan parámetros obligatorios."

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

            # Find users.txt
            content, pointer = superblock.get_users_file(file, "users.txt")

            # Exists group
            new_lines = []  # Lista para almacenar las líneas del nuevo contenido

            for line in content.split("\n"):
                if line.strip():
                    parts = [part.strip() for part in line.split(",")]
                    if (
                        parts[1] == "G"
                        and parts[2] == self.name
                        and not parts[0] == "0"
                    ):
                        new_lines.append(f"{str(0)},G,{self.name}\n")
                    else:
                        new_lines.append(line)

            # Crea el nuevo contenido uniendo las líneas de la lista
            new_content = "\n".join(new_lines)

            # Set the content in the file
            superblock.set_users_file(
                file, partition.start, pointer, new_content + "\n"
            )

        # Message
        return "[EXITOSO] Grupo eliminado exitosamente!"


# Script to mkusr
class MKUSR:
    def __init__(self):
        self.user = ""
        self.password = ""
        self.group = ""

    def create_user(self):
        # Validate logged and permissions
        if not logged.logged_in or logged.user.user_name != "root":
            return "[ERROR] No se puede crear el usuario.]"

        # Validate mandatory parameters
        if self.user == "" or self.password == "" or self.group == "":
            return "[ERROR] Faltan parámetros obligatorios."

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

            # Find users.txt
            content, pointer = superblock.get_users_file(file, "users.txt")

            # Exists user
            uid = 1
            for line in content.split("\n"):
                if line.strip():
                    parts = [part.strip() for part in line.split(",")]
                    if parts[1] == "U":
                        if not parts[3] == self.user:
                            uid += 1
                        else:
                            return "[ERROR] El usuario ya existe."
            # Exists group
            exists_group = False
            for line in content.split("\n"):
                if line.strip():
                    parts = [part.strip() for part in line.split(",")]
                    if (
                        parts[1] == "G"
                        and parts[2] == self.group
                        and not parts[0] == "0"
                    ):
                        exists_group = True
                        break

            if not exists_group:
                return "[ERROR] El grupo no existe."

            # Set content
            new_content = f"{str(uid)},U,{self.group},{self.user},{self.password}\n"
            content += new_content
            clean_content = re.sub(r"[ \t\r\f\v]+", "", content)

            # Set the content in the file
            superblock.set_users_file(file, partition.start, pointer, clean_content)

        # Message
        return "[EXITOSO] Usuario creado exitosamente."


# Script to rmusr
class RMUSR:
    def __init__(self):
        self.user = ""

    def remove_user(self):
        # Validate logged and permissions
        if not logged.logged_in or logged.user.user_name != "root":
            return "[ERROR] No se puede eliminar el usuario."

        # Validate mandatory parameters
        if self.user == "":
            return "[ERROR] Faltan parámetros obligatorios."

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

            # Find users.txt
            content, pointer = superblock.get_users_file(file, "users.txt")

            # Exists group
            new_lines = []  # Lista para almacenar las líneas del nuevo contenido

            for line in content.split("\n"):
                if line.strip():
                    parts = [part.strip() for part in line.split(",")]
                    if (
                        parts[1] == "U"
                        and parts[3] == self.user
                        and not parts[0] == "0"
                    ):
                        new_lines.append(
                            f"{str(0)},U,{parts[2]},{self.user},{parts[4]}\n"
                        )
                    else:
                        new_lines.append(line)

            # Crea el nuevo contenido uniendo las líneas de la lista
            new_content = "\n".join(new_lines)

            # Set the content in the file
            superblock.set_users_file(
                file, partition.start, pointer, new_content + "\n"
            )

        # Message
        return "[EXITOSO] Usuario eliminado exitosamente."
