# Libraries
import struct
import datetime
from colorama import init, Fore

# Modules
from structs.inode import Inode, INODE_SIZE
from structs.folder_block import FolderBlock, FOLDER_BLOCK_SIZE
from structs.file_block import FileBlock
from structs.pointers_block import PointersBlock
from structs.journaling import Journaling, Information, JOURLANING_SIZE

# Global
SUPERBLOCK_SIZE = 68

# Initialize colorama
init(autoreset=True)


# ------------------------------------ Superblock ------------------------------------
class SuperBlock:
    # Constructor
    def __init__(
        self,
        fyle_system_type=-1,
        inodes_count=0,
        blocks_count=0,  # puntero = block.start + (tamaño del bloque * blocks_count)
        free_blocks_count=0,
        free_inodes_count=0,
        mount_time=0,
        unmount_time=0,
        mount_count=0,
        magic=0xEF53,
        inode_size=INODE_SIZE,
        block_size=FOLDER_BLOCK_SIZE,
        first_inode=0,
        first_block=0,
        bitmap_inode_start=-1,
        bitmap_block_start=-1,
        inode_start=-1,
        block_start=-1,
    ):
        self.fyle_system_type = fyle_system_type  # Int    -> 4 bytes
        self.inodes_count = inodes_count  # Int    -> 4 bytes
        self.blocks_count = blocks_count  # Int    -> 4 bytes
        self.free_blocks_count = free_blocks_count  # Int    -> 4 bytes
        self.free_inodes_count = free_inodes_count  # Int    -> 4 bytes
        self.mount_time = mount_time  # Int    -> 4 bytes
        self.unmount_time = unmount_time  # Timestamp (float)    -> 4 bytes
        self.mount_count = mount_count  # Timestamp (float)    -> 4 bytes
        self.magic = magic  # Int    -> 4 bytes
        self.inode_size = inode_size  # Int    -> 4 bytes
        self.block_size = block_size  # Int    -> 4 bytes
        self.first_inode = first_inode  # Int    -> 4 bytes
        self.first_block = first_block  # Int    -> 4 bytes
        self.bitmap_inode_start = bitmap_inode_start  # Int    -> 4 bytes
        self.bitmap_block_start = bitmap_block_start  # Int    -> 4 bytes
        self.inode_start = inode_start  # Int    -> 4 bytes
        self.block_start = block_start  # Int    -> 4 bytes
        # Data ->   68 bytes

    def pack(self):
        fyle_system_type_pack = struct.pack("i", self.fyle_system_type)
        inode_count_pack = struct.pack("i", self.inodes_count)
        block_count_pack = struct.pack("i", self.blocks_count)
        free_block_count_pack = struct.pack("i", self.free_blocks_count)
        free_inode_count_pack = struct.pack("i", self.free_inodes_count)
        mount_time_pack = struct.pack("f", self.mount_time.timestamp())
        unmount_time_pack = struct.pack("f", self.unmount_time.timestamp())
        mount_count_pack = struct.pack("i", self.mount_count)
        magic_pack = struct.pack("i", self.magic)
        inode_size_pack = struct.pack("i", self.inode_size)
        block_size_pack = struct.pack("i", self.block_size)
        first_inode_pack = struct.pack("i", self.first_inode)
        first_block_pack = struct.pack("i", self.first_block)
        bitmap_inode_start_pack = struct.pack("i", self.bitmap_inode_start)
        bitmap_block_start_pack = struct.pack("i", self.bitmap_block_start)
        table_inode_start_pack = struct.pack("i", self.inode_start)
        table_block_start_pack = struct.pack("i", self.block_start)

        return (
            fyle_system_type_pack
            + inode_count_pack
            + block_count_pack
            + free_block_count_pack
            + free_inode_count_pack
            + mount_time_pack
            + unmount_time_pack
            + mount_count_pack
            + magic_pack
            + inode_size_pack
            + block_size_pack
            + first_inode_pack
            + first_block_pack
            + bitmap_inode_start_pack
            + bitmap_block_start_pack
            + table_inode_start_pack
            + table_block_start_pack
        )

    @classmethod
    def unpack(cls, data):
        fyle_system_type_unpack = struct.unpack("i", data[:4])[0]
        inodes_count_unpack = struct.unpack("i", data[4:8])[0]
        blocks_count_unpack = struct.unpack("i", data[8:12])[0]
        free_blocks_count_unpack = struct.unpack("i", data[12:16])[0]
        free_inodes_count_unpack = struct.unpack("i", data[16:20])[0]
        mount_time_unpack = datetime.datetime.fromtimestamp(
            struct.unpack("i", data[20:24])[0]
        )
        unmount_time_unpack = datetime.datetime.fromtimestamp(
            struct.unpack("f", data[24:28])[0]
        )
        mount_count_unpack = struct.unpack("i", data[28:32])[0]
        magic_unpack = struct.unpack("i", data[32:36])[0]
        inode_size_unpack = struct.unpack("i", data[36:40])[0]
        block_size_unpack = struct.unpack("i", data[40:44])[0]
        first_inode_unpack = struct.unpack("i", data[44:48])[0]
        first_block_unpack = struct.unpack("i", data[48:52])[0]
        bitmap_inode_start_unpack = struct.unpack("i", data[52:56])[0]
        bitmap_block_start_unpack = struct.unpack("i", data[56:60])[0]
        table_inode_start_unpack = struct.unpack("i", data[60:64])[0]
        table_block_start_unpack = struct.unpack("i", data[64:68])[0]

        return cls(
            fyle_system_type_unpack,
            inodes_count_unpack,
            blocks_count_unpack,
            free_blocks_count_unpack,
            free_inodes_count_unpack,
            mount_time_unpack,
            unmount_time_unpack,
            mount_count_unpack,
            magic_unpack,
            inode_size_unpack,
            block_size_unpack,
            first_inode_unpack,
            first_block_unpack,
            bitmap_inode_start_unpack,
            bitmap_block_start_unpack,
            table_inode_start_unpack,
            table_block_start_unpack,
        )

    def show_superblock(self):
        # Print unpacked SuperBlock
        print("\nUnpacked SuperBlock:")
        print("Filesystem type:", self.fyle_system_type)
        print("Inodes count:", self.inodes_count)
        print("Blocks count:", self.blocks_count)
        print("Free blocks count:", self.free_blocks_count)
        print("Free inodes count:", self.free_inodes_count)
        print("Mount time:", self.mount_time)
        print("Unmount time:", self.unmount_time)
        print("Mount count:", self.mount_count)
        print("Magic:", self.magic)
        print("Inode size:", self.inode_size)
        print("Block size:", self.block_size)
        print("First inode:", self.first_inode)
        print("First block:", self.first_block)
        print("Bitmap inode start:", self.bitmap_inode_start)
        print("Bitmap block start:", self.bitmap_block_start)
        print("Inode start:", self.inode_start)
        print("Block start:", self.block_start)

    def write_superblock(self, file, pointer):
        # Serialize the SuperBlock
        serialized_superblock = self.pack()
        # Write the SuperBlock
        file.seek(pointer)
        file.write(serialized_superblock)

    def write_inode(self, inode, file, pointer):
        # Serialize the Inode
        serialized_inode = inode.pack()
        # Write the first inode
        file.seek(self.inode_start + (pointer * self.inode_size))
        file.write(serialized_inode)

    def write_inode_bitmap(self, file, pointer):
        # Write the inode bitmap
        file.seek(self.bitmap_inode_start + pointer)
        file.write("1".encode())

    def write_block_bitmap(self, file, pointer):
        # Write the block bitmap
        file.seek(self.bitmap_block_start + pointer)
        file.write("X".encode())

    def get_first_journaling(self, file, pointer):
        # Set pointer
        file.seek(pointer)
        # Read journaling
        packed_journaling = file.read(JOURLANING_SIZE)
        # Unpack journaling
        journaling = Journaling.unpack(packed_journaling)

        return journaling

    def increase_count_journaling(self, file, pointer, first_journaling):
        # Increase the number of journaling
        first_journaling.count += 1
        # Serialize the journaling
        serialized_journaling = first_journaling.pack()
        # Write the journaling
        file.seek(pointer)
        file.write(serialized_journaling)

    # Create ext2 file system
    def create_ext2(self, n, partition, path):
        # print(" ------------ Creando ext2 ------------ ")
        # Filesystem type
        self.fyle_system_type = 2
        # Bitmaps
        self.bitmap_inode_start = partition.start + SUPERBLOCK_SIZE
        self.bitmap_block_start = self.bitmap_inode_start + n
        # Start of the tables
        self.inode_start = self.bitmap_block_start + (3 * n)
        self.block_start = self.inode_start + (n * INODE_SIZE)

        # Read the file
        with open(path, "rb+") as file:
            zero = "0"
            # Write the inode bitmap
            for i in range(n):
                file.seek(self.bitmap_inode_start + i)
                file.write(zero.encode())

            zero = "O"
            # Write the block bitmap
            for i in range(3 * n):
                file.seek(self.bitmap_block_start + i)
                file.write(zero.encode())

            # Create the first inode
            root_inode = Inode()
            root_inode.create_folder_inode(0, 0, self.inodes_count, 777)
            # Serialize the Inode
            serialized_inode = root_inode.pack()
            # Write the first inode
            file.seek(self.inode_start)
            file.write(serialized_inode)
            # Increase the number of inodes and blocks
            self.inodes_count += 1

            # Create the first block
            root_block = FolderBlock()
            root_block.create_folder_block(0, 0)
            # Set to the first block the users.txt inode
            root_block.content[2].name = "users.txt"
            root_block.content[2].inode = 1
            # Serialize the block
            serialized_block = root_block.pack()
            # Write the first block
            file.seek(self.block_start)
            file.write(serialized_block)
            # Increase the number of inodes and blocks
            self.blocks_count += 1

            # Create the users.txt inode
            users_inode = Inode()
            users_inode.create_users_file_inode(1, 1, 100, self.blocks_count, 777)
            # Serialize the Inode
            serialized_inode = users_inode.pack()
            # Write the first inode
            file.seek(self.inode_start + (self.inodes_count * self.inode_size))
            file.write(serialized_inode)
            # Increase the number of inodes and blocks
            self.inodes_count += 1

            # Create the users.txt block
            users_block = FileBlock()
            content = "1,G,root\n1,U,root,root,123\n"
            users_block.set_content(content)
            # Serialize the block
            serialized_block = users_block.pack()
            # Write the first block
            file.seek(self.block_start + (self.blocks_count * self.block_size))
            file.write(serialized_block)
            # Increase the number of inodes and blocks
            self.blocks_count += 1

            # Decrease the number of free blocks and inodes
            self.free_blocks_count -= 2
            self.free_inodes_count -= 2
            # Paint Inode bitmap
            for i in range(self.inodes_count):
                file.seek(self.bitmap_inode_start + i)
                file.write("1".encode())
            # Paint Block bitmap
            for i in range(self.blocks_count):
                file.seek(self.bitmap_block_start + i)
                file.write("X".encode())

            # Serialize the SuperBlock
            serialized_superblock = self.pack()
            # Write the SuperBlock
            file.seek(partition.start)
            file.write(serialized_superblock)

    # Create ext3 file system
    def create_ext3(self, n, partition, path):
        # print(" ------------ Creando ext3 ------------ ")
        # Filesystem type
        self.fyle_system_type = 3
        # Journaling Start
        journaling_start = partition.start + SUPERBLOCK_SIZE
        # Bitmaps
        self.bitmap_inode_start = journaling_start + (JOURLANING_SIZE * n)
        self.bitmap_block_start = self.bitmap_inode_start + n
        # Start of the tables
        self.inode_start = self.bitmap_block_start + (3 * n)
        self.block_start = self.inode_start + (n * INODE_SIZE)

        # Read the file
        with open(path, "rb+") as file:
            zero = "0"
            # Write the inode bitmap
            for i in range(n):
                file.seek(self.bitmap_inode_start + i)
                file.write(zero.encode())

            zero = "O"
            # Write the block bitmap
            for i in range(3 * n):
                file.seek(self.bitmap_block_start + i)
                file.write(zero.encode())

            # Create the first inode
            root_inode = Inode()
            root_inode.create_folder_inode(0, 0, self.inodes_count, 777)
            # Serialize the Inode
            serialized_inode = root_inode.pack()
            # Write the first inode
            file.seek(self.inode_start)
            file.write(serialized_inode)
            # Increase the number of inodes and blocks
            self.inodes_count += 1

            # Create the first block
            root_block = FolderBlock()
            root_block.create_folder_block(0, 0)
            # Set to the first block the users.txt inode
            root_block.content[2].name = "users.txt"
            root_block.content[2].inode = 1
            # Serialize the block
            serialized_block = root_block.pack()
            # Write the first block
            file.seek(self.block_start)
            file.write(serialized_block)
            # Increase the number of inodes and blocks
            self.blocks_count += 1

            # Add journaling
            new_journaling = Journaling()
            new_journaling.add("mkdir", "/", "")
            # Increase the number of journaling
            new_journaling.count += 1

            # Serialize the journaling
            serialized_journaling = new_journaling.pack()
            # Write the journaling
            file.seek(journaling_start)
            file.write(serialized_journaling)

            # Create the users.txt inode
            users_inode = Inode()
            users_inode.create_users_file_inode(1, 1, 100, self.blocks_count, 777)
            # Serialize the Inode
            serialized_inode = users_inode.pack()
            # Write the first inode
            file.seek(self.inode_start + (self.inodes_count * self.inode_size))
            file.write(serialized_inode)
            # Increase the number of inodes and blocks
            self.inodes_count += 1

            # Create the users.txt block
            users_block = FileBlock()
            content = "1,G,root\n1,U,root,root,123\n"
            users_block.set_content(content)
            # Serialize the block
            serialized_block = users_block.pack()
            # Write the first block
            file.seek(self.block_start + (self.blocks_count * self.block_size))
            file.write(serialized_block)
            # Increase the number of inodes and blocks
            self.blocks_count += 1

            # Get the journaling
            first_journaling = self.get_first_journaling(file, journaling_start)
            # Increase the number of journaling
            self.increase_count_journaling(file, journaling_start, first_journaling)

            # Add journaling
            new_journaling = Journaling()
            new_journaling.add("mkfile", "/users.txt", content)
            # Serialize the journaling
            serialized_journaling = new_journaling.pack()
            # Write the journaling
            file.seek(journaling_start + (JOURLANING_SIZE))
            file.write(serialized_journaling)

            # Decrease the number of free blocks and inodes
            self.free_blocks_count -= 2
            self.free_inodes_count -= 2

            # Paint Inode bitmap
            for i in range(self.inodes_count):
                file.seek(self.bitmap_inode_start + i)
                file.write("1".encode())
            # Paint Block bitmap
            for i in range(self.blocks_count):
                file.seek(self.bitmap_block_start + i)
                file.write("X".encode())

            # Serialize the SuperBlock
            serialized_superblock = self.pack()
            # Write the SuperBlock
            file.seek(partition.start)
            file.write(serialized_superblock)

    # Get users file content
    def get_users_file(self, file, filename):
        # Content
        content_list = []
        # Set pointer
        pointer = 0

        # Set pointer
        file.seek(self.inode_start)
        # Read Inode
        packed_inode = file.read(self.inode_size)
        # Unpack Inode
        inode = Inode.unpack(packed_inode)

        # Get the pointers
        for block_pointer in inode.block:
            if block_pointer != -1:
                # Set pointer
                file.seek(self.block_start + (block_pointer * self.block_size))
                # Read block
                packed_block = file.read(self.block_size)
                # Unpack block
                folder_block = FolderBlock.unpack(packed_block)
                # Evaluate folder block
                inode_pointer = folder_block.evaluate_folder_block(filename)

                if inode_pointer != -1:
                    # Set pointer
                    pointer = inode_pointer
                    break

        # Set pointer
        file.seek(self.inode_start + (pointer * self.inode_size))
        # Read Inode
        packed_new_inode = file.read(self.inode_size)
        # Unpack Inode
        new_inode = Inode.unpack(packed_new_inode)

        # Get the pointers
        for new_block_pointer in new_inode.block:
            if new_block_pointer != -1:
                # Set pointer
                file.seek(self.block_start + (new_block_pointer * self.block_size))
                # Read block
                new_packed_block = file.read(self.block_size)

                # Get the type of block
                new_block = FileBlock.unpack(new_packed_block)

                # Get the content
                content = new_block.get_content()
                # Add the content to the list
                content_list.append(content)

        # Get the content
        content = "".join(content_list)

        return content, pointer

    # Set users file content
    def set_users_file(self, file, superblock_pointer, inode_pointer, content_file):
        # Content List
        content_list = []
        # Set the size
        size = len(content_file)

        # Pointer list
        index_list = []
        block_list = []

        # Make the list of content
        for i in range(0, len(content_file), 64):
            content = content_file[i : i + 64]
            content_list.append(content)

        # Set pointer
        file.seek(self.inode_start + (inode_pointer * self.inode_size))
        # Read Inode
        packed_inode = file.read(self.inode_size)
        # Unpack Inode
        inode = Inode.unpack(packed_inode)

        # Iterate blocks of the inode
        for index, block_pointer in enumerate(inode.block):
            if len(content_list) > 0:
                if block_pointer != -1:
                    # Set pointer
                    file.seek(self.block_start + (block_pointer * self.block_size))
                    # Read block
                    packed_block = file.read(self.block_size)
                    # Unpack block
                    file_block = FileBlock.unpack(packed_block)

                    # Set the content
                    file_block.set_content(content_list.pop(0))

                    # Serialize the block
                    serialized_block = file_block.pack()
                    # Write the block
                    file.seek(self.block_start + (block_pointer * self.block_size))
                    file.write(serialized_block)

                elif block_pointer == -1:
                    # Create the first block
                    new_block = FileBlock()

                    # Set the content
                    new_block.set_content(content_list.pop(0))

                    # Serialize the block
                    serialized_block = new_block.pack()
                    # Write the first block
                    file.seek(self.block_start + (self.blocks_count * self.block_size))
                    file.write(serialized_block)

                    # Save the pointers
                    index_list.append(index)
                    block_list.append(self.blocks_count)

                    # Write the block bitmap
                    self.write_block_bitmap(file, self.blocks_count)

                    # Increase the number of blocks
                    self.blocks_count += 1
            else:
                break

        # Update inode
        for index, block in enumerate(block_list):
            inode.update_inode(size, index_list[index], block)

        # Write the inode
        self.write_inode(inode, file, inode_pointer)

        # Write the SuperBlock in the disk
        self.write_superblock(file, superblock_pointer)

    # Create folder
    def create_folder(self, file, folders, superblock_pointer, r):
        # List of pointers
        folders_pointer = []
        inode_pointer = 0
        # Conditional
        create_new_folder = False

        # Get the paths
        for index, folder in enumerate(folders):
            pointer = self.search_folder(file, inode_pointer, folder, folders_pointer)

            if pointer != -1:
                # print("Carpeta encontrada, se seguirá con la búsqueda")
                inode_pointer = pointer

            elif pointer == -1 and len(folders_pointer) == 0:
                # print("La carpeta no existe, creando en el root ahora")
                self.create_folder_root(file, folder)
                folders_pointer.append(self.inodes_count - 1)

            elif pointer == -1 and r and index != len(folders) - 1:
                # print("La carpeta no existe, creando dentro de otra ahora")
                self.create_folder_inode(file, folder, folders_pointer[-1])
                folders_pointer.append(self.inodes_count - 1)

            elif pointer == -1 and not r and index != len(folders) - 1:
                # print("Una carpeta del path no existe")
                break

            elif pointer == -1:
                # print("La carpeta no existe, creando dentro de otra")
                create_new_folder = True

        # Create the final folder
        if create_new_folder:
            # print("Lista de punteros: ", folders_pointer)
            self.create_folder_inode(file, folder, folders_pointer[-1])

        # Write the SuperBlock in the disk
        self.write_superblock(file, superblock_pointer)

    # Search folder
    def search_folder(self, file, inode_pointer, folder, pointers):
        # Set pointer
        file.seek(self.inode_start + (inode_pointer * self.inode_size))
        # Read Inode
        packed_inode = file.read(self.inode_size)
        # Unpack Inode
        inode = Inode.unpack(packed_inode)

        # Get the pointers
        for index, block_pointer in enumerate(inode.block):
            if block_pointer != -1:
                # Set pointer
                file.seek(self.block_start + (block_pointer * self.block_size))
                # Read block
                packed_block = file.read(self.block_size)

                # Indirect pointer
                if index >= 12:
                    pass  # Cambia esto más adelante
                # Folder block
                if inode.type == "0":
                    # Unpack block
                    folder_block = FolderBlock.unpack(packed_block)

                    if folder_block.content[2].name == folder:
                        # Add the pointer
                        pointers.append(folder_block.content[2].inode)

                        # Recursive call
                        self.search_folder(
                            file, folder_block.content[2].inode, folder, pointers
                        )

                        return folder_block.content[2].inode

                    if folder_block.content[3].name == folder:
                        # Add the pointer
                        pointers.append(folder_block.content[3].inode)

                        # Recursive call
                        self.search_folder(
                            file, folder_block.content[3].inode, folder, pointers
                        )

                        return folder_block.content[3].inode

        return -1  # Si no se encuentra en ningún subdirectorio, devuelve -1

    # Create folder in root or in another folder
    def create_folder_root(self, file, folder):
        # Set pointer
        file.seek(self.inode_start)
        # Read Inode
        packed_inode = file.read(self.inode_size)
        # Unpack Inode
        inode = Inode.unpack(packed_inode)

        # Get the pointers
        pointer_index = -1
        pointer_block = -1
        for index, block_pointer in enumerate(inode.block):
            if block_pointer != -1:
                # Set pointer
                file.seek(self.block_start + (block_pointer * self.block_size))
                # Read block
                packed_block = file.read(self.block_size)

                # Indirect pointer
                if index >= 12:
                    pass  # Cambia esto más adelante
                # Folder block
                if inode.type == "0":
                    # Unpack block
                    folder_block = FolderBlock.unpack(packed_block)
                    # Evaluate folder block -> returns the inode pointer
                    content_index = folder_block.get_free_content()

                    # If free content
                    if content_index != -1:
                        # Set in the block
                        folder_block.content[content_index].name = folder
                        folder_block.content[content_index].inode = self.inodes_count

                        # Serialize the block
                        serialized_block = folder_block.pack()
                        # Write the first block
                        file.seek(self.block_start + (block_pointer * self.block_size))
                        file.write(serialized_block)

                        # Create the inode
                        new_inode = Inode()
                        new_inode.create_folder_inode(
                            self.inodes_count,
                            self.inodes_count,
                            self.blocks_count,
                            777,
                        )
                        # Serialize the Inode
                        serialized_inode = new_inode.pack()
                        # Write the first inode
                        file.seek(
                            self.inode_start + (self.inodes_count * self.inode_size)
                        )
                        file.write(serialized_inode)
                        # Write in the bitmap
                        self.write_inode_bitmap(file, self.inodes_count)

                        # Increase the number of inodes
                        self.inodes_count += 1

                        # Create the first block
                        new_block = FolderBlock()
                        new_block.create_folder_block(0, 0)
                        # Serialize the block
                        serialized_block = new_block.pack()
                        # Write the first block
                        file.seek(
                            self.block_start + (self.blocks_count * self.block_size)
                        )
                        file.write(serialized_block)
                        # Write in the bitmap
                        self.write_block_bitmap(file, self.blocks_count)

                        # Increase the number of blocks and first block
                        self.blocks_count += 1
                        break

            elif block_pointer == -1:
                # Set pointer to the index of the block pointer
                pointer_index = index
                # Save to update root inode
                pointer_block = self.blocks_count

                # Create the first block
                new_block = FolderBlock()
                new_block.create_folder_block(0, 0)
                # Set to the first block the users.txt inode
                new_block.content[2].name = folder
                new_block.content[2].inode = self.inodes_count

                # Serialize the block
                serialized_block = new_block.pack()
                # Write the first block
                file.seek(self.block_start + (self.blocks_count * self.block_size))
                file.write(serialized_block)
                # Write in the bitmap
                self.write_block_bitmap(file, self.blocks_count)

                # Increase the number of blocks and first block
                self.blocks_count += 1

                # Create the inode
                new_inode = Inode()
                new_inode.create_folder_inode(
                    self.inodes_count,
                    self.inodes_count,
                    self.blocks_count,
                    777,
                )
                # Serialize the Inode
                serialized_inode = new_inode.pack()
                # Write the first inode
                file.seek(self.inode_start + (self.inodes_count * self.inode_size))
                file.write(serialized_inode)
                # Write in the bitmap
                self.write_inode_bitmap(file, self.inodes_count)

                # Increase the number of inodes
                self.inodes_count += 1

                # Create the first block
                new_block = FolderBlock()
                new_block.create_folder_block(0, 0)
                # Serialize the block
                serialized_block = new_block.pack()
                # Write the first block
                file.seek(self.block_start + (self.blocks_count * self.block_size))
                file.write(serialized_block)
                # Write in the bitmap
                self.write_block_bitmap(file, self.blocks_count)

                # Increase the number of blocks and first block
                self.blocks_count += 1

                break

        if pointer_index != -1:
            # Update inode
            inode.update_inode(0, pointer_index, pointer_block)
            # Write the inode
            self.write_inode(inode, file, 0)

    def create_folder_inode(self, file, folder, pointer):
        # Set pointer
        file.seek(self.inode_start + (pointer * self.inode_size))
        # Read Inode
        packed_inode = file.read(self.inode_size)
        # Unpack Inode
        inode = Inode.unpack(packed_inode)

        # Get the pointers
        pointer_index = -1
        pointer_block = -1

        # Iterate blocks of the inode
        for index, block_pointer in enumerate(inode.block):
            if block_pointer != -1:
                # Set pointer
                file.seek(self.block_start + (block_pointer * self.block_size))
                # Read block
                packed_block = file.read(self.block_size)

                # Indirect pointer
                if index >= 12:
                    pass  # Cambia esto más adelante
                # Folder block
                if inode.type == "0":
                    # Unpack block
                    folder_block = FolderBlock.unpack(packed_block)
                    # Evaluate folder block -> returns the inode pointer
                    content_index = folder_block.get_free_content()

                    # If free content
                    if content_index != -1:
                        # print("Espacio libre en el bloque", content_index)
                        # Set in the block
                        folder_block.content[content_index].name = folder
                        folder_block.content[content_index].inode = self.inodes_count
                        # Serialize the block
                        serialized_block = folder_block.pack()
                        # Write the first block
                        file.seek(self.block_start + (block_pointer * self.block_size))
                        file.write(serialized_block)

                        # Create the inode
                        new_inode = Inode()
                        new_inode.create_folder_inode(
                            self.inodes_count,
                            self.inodes_count,
                            self.blocks_count,
                            777,
                        )
                        # new_inode.show_inode()
                        # Serialize the Inode
                        serialized_inode = new_inode.pack()
                        # Write the first inode
                        file.seek(
                            self.inode_start + (self.inodes_count * self.inode_size)
                        )
                        file.write(serialized_inode)
                        # Write in the bitmap
                        self.write_inode_bitmap(file, self.inodes_count)

                        # Increase the number of inodes
                        self.inodes_count += 1

                        # Create the first block
                        new_block = FolderBlock()
                        new_block.create_folder_block(0, 0)
                        # Serialize the block
                        serialized_block = new_block.pack()
                        # Write the first block
                        file.seek(
                            self.block_start + (self.blocks_count * self.block_size)
                        )
                        file.write(serialized_block)
                        # Write in the bitmap
                        self.write_block_bitmap(file, self.blocks_count)

                        # Increase the number of blocks and first block
                        self.blocks_count += 1
                        break

            elif block_pointer == -1:
                # Set pointer to the index of the block pointer
                pointer_index = index
                # Save to update root inode
                pointer_block = self.blocks_count

                # Create the first block
                new_block = FolderBlock()
                new_block.create_folder_block(0, 0)
                # Set to the first block the users.txt inode
                new_block.content[2].name = folder
                new_block.content[2].inode = self.inodes_count

                # Serialize the block
                serialized_block = new_block.pack()
                # Write the first block
                file.seek(self.block_start + (self.blocks_count * self.block_size))
                file.write(serialized_block)
                # Write in the bitmap
                self.write_block_bitmap(file, self.blocks_count)

                # Increase the number of blocks and first block
                self.blocks_count += 1

                # Create the inode
                new_inode = Inode()
                new_inode.create_folder_inode(
                    self.inodes_count,
                    self.inodes_count,
                    self.blocks_count,
                    777,
                )
                # Serialize the Inode
                serialized_inode = new_inode.pack()
                # Write the first inode
                file.seek(self.inode_start + (self.inodes_count * self.inode_size))
                file.write(serialized_inode)
                # Write in the bitmap
                self.write_inode_bitmap(file, self.inodes_count)

                # Increase the number of inodes
                self.inodes_count += 1

                # Create the first block
                new_block = FolderBlock()
                new_block.create_folder_block(0, 0)
                # Serialize the block
                serialized_block = new_block.pack()
                # Write the first block
                file.seek(self.block_start + (self.blocks_count * self.block_size))
                file.write(serialized_block)
                # Write in the bitmap
                self.write_block_bitmap(file, self.blocks_count)

                # Increase the number of blocks and first block
                self.blocks_count += 1

                break

        if pointer_index != -1:
            # Update inode
            inode.update_inode(0, pointer_index, pointer_block)
            # Write the inode
            self.write_inode(inode, file, pointer)

    # Create file
    def create_file(
        self, file, superblock_pointer, folders, file_name, size, content_file
    ):
        # List of pointers
        folders_pointer = []
        inode_pointer = 0

        # Get the paths
        for folder in folders:
            pointer = self.search_folder(file, inode_pointer, folder, folders_pointer)

            if pointer != -1:
                # print("Carpeta encontrada, se seguirá con la búsqueda")
                inode_pointer = pointer

            else:
                print(Fore.RED + "ERROR: Una carpeta del path no existe")
                return content_file, True

        # Content List
        content_list = []

        # Make content with size
        if content_file == "":
            if size > 0:
                # Iterar desde 0 hasta num-1 y agregar cada número a la cadena resultado
                for i in range(size):
                    content_file += str(i % 10)
        else:
            # Set the size
            size = len(content_file)

        # Make the list of content
        for i in range(0, len(content_file), 64):
            content = content_file[i : i + 64]
            content_list.append(content)

        # Create the file
        self.create_file_inode(file, file_name, size, inode_pointer, content_list)

        # Write the SuperBlock in the disk
        self.write_superblock(file, superblock_pointer)

        return content_file, False

    # Create file in root or in another folder
    def create_file_inode(self, file, file_name, size, pointer, content_list):
        # Set pointer
        file.seek(self.inode_start + (pointer * self.inode_size))
        # Read Inode
        packed_inode = file.read(self.inode_size)
        # Unpack Inode
        inode = Inode.unpack(packed_inode)

        # Get the pointers
        pointer_index = -1
        pointer_block = -1
        for index, block_pointer in enumerate(inode.block):
            if block_pointer != -1:
                # Set pointer
                file.seek(self.block_start + (block_pointer * self.block_size))
                # Read block
                packed_block = file.read(self.block_size)

                # Indirect pointer
                if index >= 12:
                    pass  # Cambia esto más adelante
                # Folder block
                if inode.type == "0":
                    # Unpack block
                    folder_block = FolderBlock.unpack(packed_block)
                    # Evaluate folder block -> returns the inode pointer
                    content_index = folder_block.get_free_content()

                    # If free content
                    if content_index != -1:
                        # Set in the block
                        folder_block.content[content_index].name = file_name
                        folder_block.content[content_index].inode = self.inodes_count

                        # Serialize the block
                        serialized_block = folder_block.pack()
                        # Write the first block
                        file.seek(self.block_start + (block_pointer * self.block_size))
                        file.write(serialized_block)

                        # Create the inode
                        new_inode = Inode()
                        new_inode.create_file_inode(
                            self.inodes_count,
                            self.inodes_count,
                            size,
                            777,
                        )

                        # Create blocks for the file
                        for inode_index_block, content in enumerate(content_list):
                            # self.create_content_file_blocks(file, new_inode, content)

                            # Create the first block
                            new_block = FileBlock()

                            # Set the content
                            new_block.set_content(content)

                            # Serialize the block
                            serialized_block = new_block.pack()
                            # Write the first block
                            file.seek(
                                self.block_start + (self.blocks_count * self.block_size)
                            )
                            file.write(serialized_block)

                            # Update inode
                            new_inode.update_inode(
                                0, inode_index_block, self.blocks_count
                            )
                            # Write in the bitmap
                            self.write_block_bitmap(file, self.blocks_count)

                            # Increase the number of blocks
                            self.blocks_count += 1

                        # Serialize the Inode
                        serialized_inode = new_inode.pack()
                        # Write the first inode
                        file.seek(
                            self.inode_start + (self.inodes_count * self.inode_size)
                        )
                        file.write(serialized_inode)
                        # Write in the bitmap
                        self.write_inode_bitmap(file, self.inodes_count)

                        # Increase the number of inodes
                        self.inodes_count += 1
                        break

            elif block_pointer == -1:
                # Set pointer to the index of the block pointer
                pointer_index = index
                # Save to update root inode
                pointer_block = self.blocks_count

                # Create the first block
                new_block = FolderBlock()
                new_block.create_folder_block(0, 0)
                # Set to the first block the users.txt inode
                new_block.content[2].name = file_name
                new_block.content[2].inode = self.inodes_count

                # Serialize the block
                serialized_block = new_block.pack()
                # Write the first block
                file.seek(self.block_start + (self.blocks_count * self.block_size))
                file.write(serialized_block)
                # Write in the bitmap
                self.write_block_bitmap(file, self.blocks_count)

                # Increase the number of blocks and first block
                self.blocks_count += 1

                # Create the inode
                new_inode = Inode()
                new_inode.create_file_inode(
                    self.inodes_count,
                    self.inodes_count,
                    size,
                    777,
                )

                # Create blocks for the file
                for inode_index_block, content in enumerate(content_list):
                    # self.create_content_file_blocks(file, new_inode, content)

                    # Create the first block
                    new_block = FileBlock()

                    # Set the content
                    new_block.set_content(content)

                    # Serialize the block
                    serialized_block = new_block.pack()
                    # Write the first block
                    file.seek(self.block_start + (self.blocks_count * self.block_size))
                    file.write(serialized_block)

                    # Update inode
                    new_inode.update_inode(0, inode_index_block, self.blocks_count)

                    # Write in the bitmap
                    self.write_block_bitmap(file, self.blocks_count)

                    # Increase the number of blocks
                    self.blocks_count += 1

                # Serialize the Inode
                serialized_inode = new_inode.pack()
                # Write the first inode
                file.seek(self.inode_start + (self.inodes_count * self.inode_size))
                file.write(serialized_inode)
                # Write in the bitmap
                self.write_inode_bitmap(file, self.inodes_count)

                # Increase the number of inodes
                self.inodes_count += 1
                break

        if pointer_index != -1:
            # Update inode
            inode.update_inode(0, pointer_index, pointer_block)
            # Write the inode
            self.write_inode(inode, file, pointer)

    # Get file content
    def get_file_content(self, file, folders):
        # List of pointers
        folders_pointer = []
        inode_pointer = 0

        # Get the paths
        for folder in folders:
            pointer = self.search_folder(file, inode_pointer, folder, folders_pointer)

            if pointer != -1:
                # print("Carpeta encontrada, se seguirá con la búsqueda")
                inode_pointer = pointer

            else:
                print("Una carpeta del path no existe")
                return

        # Content List
        content_list = []

        # Set pointer
        file.seek(self.inode_start + (inode_pointer * self.inode_size))
        # Read Inode
        packed_inode = file.read(self.inode_size)
        # Unpack Inode
        inode = Inode.unpack(packed_inode)

        # Iterate blocks of the inode
        for block_pointer in inode.block:
            if block_pointer != -1:
                # Set pointer
                file.seek(self.block_start + (block_pointer * self.block_size))
                # Read block
                packed_block = file.read(self.block_size)
                # Unpack block
                file_block = FileBlock.unpack(packed_block)

                # Get the content
                content = file_block.get_content()
                # Add to the list
                content_list.append(content)

        # Get file content
        content = "".join(content_list)

        return content

    # Remove file
    def remove_file(self, file, superblock_pointer, folders):
        # List of pointers
        folders_pointer = []
        inode_pointer = 0

        # Get the paths
        for folder in folders:
            pointer = self.search_folder(file, inode_pointer, folder, folders_pointer)

            if pointer != -1:
                # print("Carpeta encontrada, se seguirá con la búsqueda")
                inode_pointer = pointer

            else:
                print("Una carpeta del path no existe")
                return

        # Content List
        content_list = []

        # Set pointer
        file.seek(self.inode_start + (inode_pointer * self.inode_size))
        # Read Inode
        packed_inode = file.read(self.inode_size)
        # Unpack Inode
        inode = Inode.unpack(packed_inode)

        # Iterate blocks of the inode
        for block_pointer in inode.block:
            if block_pointer != -1:
                # Set pointer
                file.seek(self.block_start + (block_pointer * self.block_size))
                # Read block
                packed_block = file.read(self.block_size)
                # Unpack block
                file_block = FileBlock.unpack(packed_block)

                # Get the content
                content = file_block.get_content()
                # Add to the list
                content_list.append(content)

                # Delete the block
                for i in range(self.block_size):
                    file.seek(self.block_start + (block_pointer * self.block_size) + i)
                    file.write("0".encode())

        # Get file content
        content = "".join(content_list)

        return content

    # Edit file content
    def edit_file_content(self, file, superblock_pointer, folders, content_file):
        # List of pointers
        folders_pointer = []
        inode_pointer = 0

        # Get the paths
        for folder in folders:
            pointer = self.search_folder(file, inode_pointer, folder, folders_pointer)

            if pointer != -1:
                # print("Carpeta encontrada, se seguirá con la búsqueda")
                inode_pointer = pointer

            else:
                print("Una carpeta del path no existe")
                return

        # Content List
        content_list = []
        # Set the size
        size = len(content_file)
        # Pointer list
        index_list = []
        block_list = []

        # Make the list of content
        for i in range(0, len(content_file), 64):
            content = content_file[i : i + 64]
            content_list.append(content)

        # Set pointer
        file.seek(self.inode_start + (inode_pointer * self.inode_size))
        # Read Inode
        packed_inode = file.read(self.inode_size)
        # Unpack Inode
        inode = Inode.unpack(packed_inode)

        # Iterate blocks of the inode
        for index, block_pointer in enumerate(inode.block):
            if len(content_list) > 0:
                if block_pointer != -1:
                    # Set pointer
                    file.seek(self.block_start + (block_pointer * self.block_size))
                    # Read block
                    packed_block = file.read(self.block_size)
                    # Unpack block
                    file_block = FileBlock.unpack(packed_block)

                    # Set the content
                    file_block.set_content(content_list.pop(0))

                    # Serialize the block
                    serialized_block = file_block.pack()
                    # Write the block
                    file.seek(self.block_start + (block_pointer * self.block_size))
                    file.write(serialized_block)

                elif block_pointer == -1:
                    # Create the first block
                    new_block = FileBlock()

                    # Set the content
                    new_block.set_content(content_list.pop(0))

                    # Serialize the block
                    serialized_block = new_block.pack()
                    # Write the first block
                    file.seek(self.block_start + (self.blocks_count * self.block_size))
                    file.write(serialized_block)

                    # Save the pointers
                    index_list.append(index)
                    block_list.append(self.blocks_count)

                    # Increase the number of blocks
                    self.blocks_count += 1
            else:
                break

        # Update inode
        for index, block in enumerate(block_list):
            inode.update_inode(size, index_list[index], block)

        # Write the inode
        self.write_inode(inode, file, inode_pointer)

        # Write the SuperBlock in the disk
        self.write_superblock(file, superblock_pointer)

    # Rename file or folder
    def rename(self, file, superblock_pointer, folders, actual_name, new_name):
        # List of pointers
        folders_pointer = []
        inode_pointer = 0

        # Get the paths
        for folder in folders:
            pointer = self.search_folder(file, inode_pointer, folder, folders_pointer)

            if pointer != -1:
                # print("Carpeta encontrada, se seguirá con la búsqueda")
                inode_pointer = pointer

            else:
                print("Una carpeta del path no existe")
                return

        # Set pointer
        file.seek(self.inode_start + (inode_pointer * self.inode_size))
        # Read Inode
        packed_inode = file.read(self.inode_size)
        # Unpack Inode
        inode = Inode.unpack(packed_inode)

        # Iterate blocks of the inode
        for block_pointer in inode.block:
            if block_pointer != -1:
                # Set pointer
                file.seek(self.block_start + (block_pointer * self.block_size))
                # Read block
                packed_block = file.read(self.block_size)
                # Unpack block
                folder_block = FolderBlock.unpack(packed_block)

                # If is the folder or file
                if folder_block.content[2].name == actual_name:
                    # Set the new name
                    folder_block.content[2].name = new_name

                    # Serialize the block
                    serialized_block = folder_block.pack()
                    # Write the block
                    file.seek(self.block_start + (block_pointer * self.block_size))
                    file.write(serialized_block)
                    break

                elif folder_block.content[3].name == actual_name:
                    # Set the new name
                    folder_block.content[3].name = new_name

                    # Serialize the block
                    serialized_block = folder_block.pack()
                    # Write the block
                    file.seek(self.block_start + (block_pointer * self.block_size))
                    file.write(serialized_block)
                    break

        # Write the SuperBlock in the disk
        self.write_superblock(file, superblock_pointer)
