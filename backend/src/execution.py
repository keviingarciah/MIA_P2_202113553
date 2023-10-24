# Libraries
from colorama import init, Fore
import readline

# Modules
from analyzer import analyzer
from structs.user import Logged

# Global variables
CARNET = "53"

global mounted_partitions
mounted_partitions = {}

global logged
logged = Logged()


# Exec function
def execute(script):
    message = analyzer.parse(script)
    return message
