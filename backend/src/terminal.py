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

# Initialize colorama
init(autoreset=True)


# Get the input from the user
def colored_input(prompt, color):
    return input(f"{color}{prompt}{Fore.RESET}")


# Main function
def main():
    while True:
        # Terminal prompt
        input_text = colored_input("> ", Fore.GREEN)
        analyzer.parse(input_text)


"""
# Run the main function
if __name__ == "__main__":
    main()
"""
