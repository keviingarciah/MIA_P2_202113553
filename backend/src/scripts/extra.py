# Import
import os
from colorama import Fore, init

# Modules
from analyzer import analyzer

# Inicializar Colorama
init(autoreset=True)


# Script to execute a file script
class EXECUTE:
    def __init__(self, path="/"):
        self.path = path

    # Execute a script
    def execute_script(self):
        # Construir la ruta absoluta al archivo
        script_directory = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(script_directory, self.path)

        try:
            with open(absolute_path, "r+") as file:
                print(Fore.CYAN + "Ejecutando...")
                for line in file:
                    # Eliminar los comentarios (líneas que comienzan con #) y los saltos de línea
                    line = line.split("#")[
                        0
                    ].strip()  # Eliminar comentarios y espacios en blanco
                    if line:  # Ignorar líneas vacías
                        # Ejecutar la instrucción
                        analyzer.parse(line)
        except FileNotFoundError:
            print(Fore.RED + "El archivo no fue encontrado.")
        except Exception as e:
            print(Fore.RED + "Ocurrió un error:", e)


# Script to pause the execution
class PAUSE:
    def __init__(self):
        pass

    # Pause the execution
    def pause(self):
        # Pausar hasta que se oprima una tecla
        input(Fore.CYAN + "Presiona Enter para continuar...")
