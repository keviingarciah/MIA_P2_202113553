# Modules
from structs.partition import Partition, MountedPartition


# ------------------------------------ Logged ------------------------------------
class Logged:
    # Constructor
    def __init__(self):
        self.user = User()
        self.mounted_partition = MountedPartition("", Partition)
        self.logged_in = False

    # Getters
    def get_mounted_partition(self):
        return self.mounted_partition


# ------------------------------------ User ------------------------------------
class User:
    # Constructor
    def __init__(self, user_name="", password=""):
        self.user_name = user_name
        self.password = password
        self.group = Group()


# ------------------------------------ Group ------------------------------------
class Group:
    # Constructor
    def __init__(self, group_name="", users=[]):
        self.group_name = group_name
        self.users = users
