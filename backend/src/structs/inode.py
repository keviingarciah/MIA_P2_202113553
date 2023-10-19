# Libraries
import struct
import datetime

# Global
INODE_SIZE = 89


# ------------------------------------ Inode ------------------------------------
class Inode:
    # Constructor
    def __init__(
        self,
        uid=-1,
        gid=-1,
        size=-1,
        atime=0,
        ctime=0,
        mtime=0,
        block=[-1] * 15,
        type=" ",
        perm=-1,
    ):
        self.uid = uid  # Int    -> 4 bytes
        self.gid = gid  # Int    -> 4 bytes
        self.size = size  # Int    -> 4 bytes
        self.atime = atime  # Timestamp (float)    -> 4 bytes
        self.ctime = ctime  # Timestamp (float)    -> 4 bytes
        self.mtime = mtime  # Timestamp (float)    -> 4 bytes
        self.block = block  # Int Lista 4 * 15   -> 60 bytes
        self.type = type  # Char    -> 1 byte
        self.perm = perm  # Int    -> 4 bytes
        # Data ->   85 + 4 = 89 bytes

    def pack(self):
        uid_pack = struct.pack("i", self.uid)
        gid_pack = struct.pack("i", self.gid)
        size_pack = struct.pack("i", self.size)
        atime_pack = struct.pack("f", self.atime.timestamp())
        ctime_pack = struct.pack("f", self.ctime.timestamp())
        mtime_pack = struct.pack("f", self.mtime.timestamp())
        block_pack = b"".join([struct.pack("i", block) for block in self.block])
        type_pack = struct.pack("c", self.type.encode())
        perm_pack = struct.pack("i", self.perm)

        return (
            uid_pack
            + gid_pack
            + size_pack
            + atime_pack
            + ctime_pack
            + mtime_pack
            + block_pack
            + type_pack
            + perm_pack
        )

    @classmethod
    def unpack(cls, data):
        uid_unpack = struct.unpack("i", data[0:4])[0]
        gid_unpack = struct.unpack("i", data[4:8])[0]
        size_unpack = struct.unpack("i", data[8:12])[0]
        atime_unpack = datetime.datetime.fromtimestamp(
            struct.unpack("f", data[12:16])[0]
        )
        ctime_unpack = datetime.datetime.fromtimestamp(
            struct.unpack("f", data[16:20])[0]
        )
        mtime_unpack = datetime.datetime.fromtimestamp(
            struct.unpack("f", data[20:24])[0]
        )
        block_unpack = struct.unpack("15i", data[24:84])
        block_unpack = list(block_unpack)
        type_unpack = struct.unpack("c", data[84:85])[0].decode()
        perm_unpack = struct.unpack("i", data[85:89])[0]

        return cls(
            uid_unpack,
            gid_unpack,
            size_unpack,
            atime_unpack,
            ctime_unpack,
            mtime_unpack,
            block_unpack,
            type_unpack,
            perm_unpack,
        )

    def show_inode(self):
        # Print unpacked Inode
        print("\nUnpacked Inode:")
        print("Uid:", self.uid)
        print("Gid:", self.gid)
        print("Size:", self.size)
        print("Atime:", self.atime)
        print("Ctime:", self.ctime)
        print("Mtime:", self.mtime)
        print("Block:", self.block)
        print("Type:", self.type)
        print("Perm:", self.perm)

    def get_free_block(self):
        for i, block in enumerate(self.block):
            if block == -1:
                return i
        return -1

    def create_folder_inode(self, uid, gid, pointer, perm):
        # Set the first inode
        self.uid = uid
        self.gid = gid  # random.randint(0, 1000)
        self.size = 0  # Size of the file
        self.atime = datetime.datetime.now()
        self.ctime = datetime.datetime.now()
        self.mtime = datetime.datetime.now()
        self.block[0] = pointer  # Pointer to folder block 0
        self.type = "0"
        self.perm = perm

    def create_users_file_inode(self, uid, gid, size, pointer, perm):
        # Set the first inode
        self.uid = uid
        self.gid = gid  # random.randint(0, 1000)
        self.size = size  # Size of the file
        self.atime = datetime.datetime.now()
        self.ctime = datetime.datetime.now()
        self.mtime = datetime.datetime.now()
        self.block[0] = pointer  # Pointer to folder block 0
        self.type = "1"
        self.perm = perm

    def create_file_inode(self, uid, gid, size, perm):
        # Set the first inode
        self.uid = uid
        self.gid = gid  # random.randint(0, 1000)
        self.size = size  # Size of the file
        self.atime = datetime.datetime.now()
        self.ctime = datetime.datetime.now()
        self.mtime = datetime.datetime.now()
        self.type = "1"
        self.perm = perm

    def update_inode(self, size, index, pointer):
        # Update inode
        self.size += size
        self.mtime = datetime.datetime.now()
        self.block[index] = pointer
