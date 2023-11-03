# Libraries
from main import mounted_partitions


# Script to pause the execution
class PAUSE:
    def __init__(self):
        pass

    # Pause the execution
    def pause(self):
        # Se manda la pausa
        return "[PAUSA]"


# Script to show mounted partitions
class MOUNTED:
    def __init__(self):
        pass

    # Pause the execution
    def mounted(self):
        # Se muestra la lista de particiones montadas
        output = "[MONTADAS]"

        for partition_id in mounted_partitions:
            output += f"\t{partition_id}\n"

        return output
