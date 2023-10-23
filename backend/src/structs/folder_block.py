# Libraries
import struct

# Global
FOLDER_BLOCK_SIZE = 64
CONTENT_SIZE = 16


# ----------------------------------- Folder Block ------------------------------------
class FolderBlock:
    # Constructor
    def __init__(self):
        self.content = [
            Content() for _ in range(4)
        ]  # Content[4] -> 4 * 16 bytes = 64 bytes

    def pack(self):
        content_pack = b"".join([content.pack() for content in self.content])

        return content_pack

    @classmethod
    def unpack(cls, data):
        content_unpack = [
            Content.unpack(data[i : i + CONTENT_SIZE])
            for i in range(0, len(data), CONTENT_SIZE)
        ]

        folder_bloc = cls()
        folder_bloc.content = content_unpack

        return folder_bloc

    def show_folder_block(self):
        # Print unpacked FolderBlock
        print("\nUnpacked FolderBlock:")
        for i, content in enumerate(self.content):
            print("----------------")
            print(f"Content {i+1}:")
            print("Name:", content.name)
            print("Inode:", content.inode)

    def create_folder_block(
        self,
        parent_inode,
        grandfather_inode,
    ):
        # Father
        self.content[0].name = "."
        self.content[0].inode = parent_inode
        # Grandfather
        self.content[1].name = ".."
        self.content[1].inode = grandfather_inode

    def evaluate_folder_block(self, name):
        for content in self.content:
            if content.name == name:
                return content.inode
        return -1

    def get_free_content(self):
        for i, content in enumerate(self.content):
            if content.name == " ":
                return i
        return -1


# ----------------------------------- Folder Content ------------------------------------
class Content:
    # Constructor
    def __init__(self, name=" ", inode=-1):
        self.name = name  # Char[12] -> 12 bytes
        self.inode = inode  # Int    -> 4 bytes
        # Data ->   16 bytes

    def pack(self):
        name_pack = struct.pack("12s", self.name.encode("utf-8"))
        inode_pack = struct.pack("i", self.inode)

        return name_pack + inode_pack

    @classmethod
    def unpack(cls, data):
        name_unpack = (
            struct.unpack("12s", data[:12])[0].decode("utf-8").replace("\x00", "")
        )
        inode_unpack = struct.unpack("i", data[12:16])[0]

        content = cls(name_unpack, inode_unpack)
        return content
