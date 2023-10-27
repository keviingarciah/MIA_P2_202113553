# Libraries
import os
from graphviz import Source

# Modules
from main import mounted_partitions
from upload_report import upload_report_file
from structs.mbr import MBR, MBR_SIZE
from structs.ebr import EBR, EBR_SIZE
from structs.superblock import SuperBlock, SUPERBLOCK_SIZE
from structs.inode import Inode
from structs.folder_block import FolderBlock
from structs.file_block import FileBlock


# Script to create a report
class REP:
    def __init__(self):
        self.name = ""
        self.path = "/"
        self.id = ""
        self.ruta = "/"

    def create_report(self):
        # Validate mandatory parameters
        if self.name == "" or self.path == "/" or self.id == " ":
            return "[ERROR] Falta un parámetro obligatorio]"

        # Verificar si la clave existe
        mounted_partition = None
        if self.id in mounted_partitions:
            mounted_partition = mounted_partitions[self.id]
        else:
            return f"[ERROR] La partición {self.id} no está montada."

        # Set partition
        partition = mounted_partition.get_partition()

        # Get SuperBlock
        with open(mounted_partition.path, "rb+") as file:
            # Set graphviz code
            graphviz = ""

            # Type of report
            if self.name == "mbr":
                graphviz = mbr_report(file)
            elif self.name == "disk":
                graphviz = disk_report(file)
            elif self.name == "inode":
                graphviz = inode_report(file, partition.start)
            elif self.name == "block":
                graphviz = block_report(file, partition.start)
            elif self.name == "bm_inode":
                graphviz = bm_inode_report(file, partition.start)
            elif self.name == "bm_block":
                graphviz = bm_block_report(file, partition.start)
            elif self.name == "tree":
                graphviz = tree_report(file, partition.start)
            elif self.name == "sb":
                graphviz = sb_report(file, partition.start)
            elif self.name == "file":
                # Validate mandatory parameters
                if self.ruta == "/":
                    return "[ERROR] Falta un parámetro obligatorio"
                graphviz = file_report(file, partition.start, self.ruta)
            else:
                return f"[ERROR] El reporte {self.name} no existe."

            # Verificar si el directorio de salida existe, si no, crearlo
            output_dir = os.path.dirname(self.path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Obtener la extensión del archivo desde el output_path
            nombre_base, extension = os.path.splitext(self.path)

            # Generar la imagen a partir del código DOT de Graphviz
            graph = Source(graphviz)

            # Renderizar y guardar la imagen con la extensión correcta
            graph.render(nombre_base, format=extension[1:], cleanup=True)

            # Upload to AWS
            upload_report_file(self.path)

            # Get file name
            file_name = os.path.basename(self.path)

            # Message
            return f"[EXITOSO] Reporte {self.name} generado con éxito: {file_name}"


# MBR report
def mbr_report(file):
    # Leer los datos empaquetados del archivo
    packed_mbr = file.read(MBR_SIZE)
    # Unpack MBR
    mbr = MBR.unpack(packed_mbr)

    # Begin graphviz
    graphviz = """
    digraph G{
        node [ shape=none fontname=Helvetica ]
        n1 [ label = <
            <table border="0" cellspacing="0" cellborder="1">
                <tr>
                    <td colspan="2" bgcolor="#FFFFCC"><b>Reporte MBR/EBR</b></td>
                </tr>  
    """

    # Disk
    graphviz += f"""
                <tr>
                    <td colspan="2" bgcolor="#D9D9D9"><b>Disco</b></td>
                </tr>    
                <tr>
                    <td bgcolor="#EFEFEF">Tamaño</td>                    
                    <td>{mbr.size}</td>                    
                </tr>   
                <tr>
                    <td bgcolor="#EFEFEF">Fecha de Creación</td>                    
                    <td>{mbr.date}</td>                    
                </tr>  
                <tr>
                    <td bgcolor="#EFEFEF">Asignación</td>                    
                    <td>{mbr.signature}</td>                    
                </tr>  
    """

    # Partitions
    for partition in mbr.partitions:
        if partition.type == "P":
            graphviz += f"""
                <tr>
                    <td colspan="2" bgcolor="#D9D9D9"><b>Partición Primaria</b></td>
                </tr>                        
                <tr>
                    <td bgcolor="#EFEFEF">Nombre</td>                    
                    <td>{partition.name}</td>                    
                </tr> 
                <tr>
                    <td bgcolor="#EFEFEF">Estado</td>                    
                    <td>{partition.status}</td>                    
                </tr>   
                <tr>
                    <td bgcolor="#EFEFEF">Fit</td>                    
                    <td>{partition.fit}</td>                    
                </tr>                      
                <tr>
                    <td bgcolor="#EFEFEF">Tamaño</td>                    
                    <td>{partition.size}</td>                    
                </tr>  
                <tr>
                    <td bgcolor="#EFEFEF">Inicio</td>                    
                    <td>{partition.start}</td>                    
                </tr>  
            """
        elif partition.type == "E":
            graphviz += f"""
                <tr>
                    <td colspan="2" bgcolor="#D9D9D9"><b>Partición Extendida</b></td>
                </tr>                        
                <tr>
                    <td bgcolor="#EFEFEF">Nombre</td>                    
                    <td>{partition.name}</td>                    
                </tr> 
                <tr>
                    <td bgcolor="#EFEFEF">Estado</td>                    
                    <td>{partition.status}</td>                    
                </tr>   
                <tr>
                    <td bgcolor="#EFEFEF">Fit</td>                    
                    <td>{partition.fit}</td>                    
                </tr>                      
                <tr>
                    <td bgcolor="#EFEFEF">Tamaño</td>                    
                    <td>{partition.size}</td>                    
                </tr>  
                <tr>
                    <td bgcolor="#EFEFEF">Inicio</td>                    
                    <td>{partition.start}</td>                    
                </tr>  
            """

            # Iterate logical partitions
            ebr_pointer = partition.start
            while True:
                # Set the pointer to the EBR
                file.seek(ebr_pointer)
                # Read the packed EBR
                packed_ebr = file.read(EBR_SIZE)
                # Unpack EBR
                ebr = EBR.unpack(packed_ebr)

                # Evaluate if the EBR is empty
                if ebr.next == -1:
                    break

                graphviz += f"""
                <tr>
                    <td colspan="2" bgcolor="#D9D9D9"><b>Partición Lógica</b></td>
                </tr>                        
                <tr>
                    <td bgcolor="#EFEFEF">Nombre</td>                    
                    <td>{ebr.name}</td>                    
                </tr> 
                <tr>
                    <td bgcolor="#EFEFEF">Estado</td>                    
                    <td>{ebr.status}</td>                    
                </tr>   
                <tr>
                    <td bgcolor="#EFEFEF">Fit</td>                    
                    <td>{ebr.fit}</td>                    
                </tr>                      
                <tr>
                    <td bgcolor="#EFEFEF">Tamaño</td>                    
                    <td>{ebr.size}</td>                    
                </tr>  
                <tr>
                    <td bgcolor="#EFEFEF">Inicio</td>                    
                    <td>{ebr.start}</td>                    
                </tr>  
                <tr>
                    <td bgcolor="#EFEFEF">Siguiente</td>                    
                    <td>{ebr.next}</td>                    
                </tr>  
                """
                # Update the pointer
                ebr_pointer = ebr.next

    # End of graphviz
    graphviz += """
            </table>
        >]
    }
    """
    return graphviz


# Disk report
def disk_report(file):
    # Leer los datos empaquetados del archivo
    packed_mbr = file.read(MBR_SIZE)
    # Unpack MBR
    mbr = MBR.unpack(packed_mbr)
    # Set total disk size
    total_disk_size = mbr.size
    count_size = 0
    count_partitions = 0

    # Comienza a construir el código de Graphviz
    graphviz = """
    digraph D {
        subgraph cluster_0 {
            bgcolor="white"
            node [style="rounded" style=filled];            
    """
    # Crea el código de Graphviz para cada partición
    graphviz += '''node_A [shape=record label="'''
    graphviz += f"MBR"
    count_size += MBR_SIZE

    # Partitions
    for partition in mbr.partitions:
        graphviz += "|"

        if partition.type == "P":
            # graphviz += f"Primaria\\n{round((partition.size/total_disk_size)*100, 2)}%"
            graphviz += f"Primaria"
            count_size += partition.size
            count_partitions += 1

        elif partition.type == "E":
            graphviz += "{Extendida|{"
            graphviz += f"EBR"
            count_size += EBR_SIZE
            extended_size = EBR_SIZE

            # Iterate logical partitions
            ebr_pointer = partition.start
            while True:
                # Set the pointer to the EBR
                file.seek(ebr_pointer)
                # Read the packed EBR
                packed_ebr = file.read(EBR_SIZE)
                # Unpack EBR
                ebr = EBR.unpack(packed_ebr)

                # Evaluate if the EBR is empty
                if ebr.next == -1:
                    break

                # graphviz += f"|Lógica\\n{round((ebr.size/total_disk_size)*100, 2)}%"
                graphviz += f"|Lógica"
                graphviz += f"|EBR"
                count_size += ebr.size + EBR_SIZE
                extended_size += ebr.size + EBR_SIZE

                # Update the pointer
                ebr_pointer = ebr.next

            count_size += partition.size - extended_size
            # graphviz += f"|Sin Asignar\\n{round((count_size/total_disk_size)*100, 2)}%"
            graphviz += f"|Sin Asignar"
            graphviz += "}}"
            count_partitions += 1

        else:
            # graphviz += f"Sin Asignar\\n{round(((count_size/count_partitions)/total_disk_size)*100, 2)}%"
            graphviz += f"Sin Asignar"
            count_partitions += 1

    # Cierra la definición de subgraph y el digraph
    graphviz += """"];"""
    graphviz += """            
        }
    }            
    """
    return graphviz


# Inode report
def inode_report(file, pointer):
    # Set pointer
    file.seek(pointer)
    # Read SuperBlock
    packed_superblock = file.read(SUPERBLOCK_SIZE)
    # Unpack SuperBlock
    sb = SuperBlock.unpack(packed_superblock)

    # Begin graphviz
    graphviz = """
    digraph G{
        rankdir="LR";
        node [shape=plaintext];
    """

    # Iterate inodes
    for i in range(0, sb.inodes_count):
        # Set pointer
        file.seek(sb.inode_start + (i * sb.inode_size))
        # Read inode
        deserializeInode = file.read(sb.inode_size)
        # Unpack inode
        inode = Inode.unpack(deserializeInode)

        graphviz += f"""  
            table{i} [label=<<table border="0" cellborder="1" cellspacing="0">
                <tr><td colspan="2" bgcolor="#FFFFCC">Inodo {i}</td></tr>
                <tr><td bgcolor="#EFEFEF">UID</td> <td>{inode.uid}</td></tr>
                <tr><td bgcolor="#EFEFEF">GID</td> <td>{inode.gid}</td></tr>
                <tr><td bgcolor="#EFEFEF">Tamaño</td> <td>{inode.size}</td></tr>
                <tr><td bgcolor="#EFEFEF">Creación</td> <td>{inode.ctime}</td></tr>
                <tr><td bgcolor="#EFEFEF">Última Visita</td> <td>{inode.atime}</td></tr>
                <tr><td bgcolor="#EFEFEF">Última Modificación</td> <td>{inode.mtime}</td></tr>
                <tr><td bgcolor="#EFEFEF">Tipo</td> <td>{inode.type}</td></tr>
                <tr><td bgcolor="#EFEFEF">Permiso</td> <td>{inode.perm}</td></tr>
        """
        for j in range(0, 15):
            graphviz += f"""<tr><td bgcolor="#EFEFEF">Bloque {j+1}</td> <td>{inode.block[j]}</td></tr>"""

        graphviz += f"""          
            </table>>];
        """

        # Connect inodes except for the last one
        if i < sb.inodes_count - 1:
            graphviz += f"table{i} -> table{i+1}; "

    # End of graphviz
    graphviz += "}"

    return graphviz


# Block report
def block_report(file, pointer):
    # Set pointer
    file.seek(pointer)
    # Read SuperBlock
    packed_superblock = file.read(SUPERBLOCK_SIZE)
    # Unpack SuperBlock
    sb = SuperBlock.unpack(packed_superblock)

    # Begin graphviz
    graphviz = """
    digraph G{
        rankdir="LR";
        node [shape=plaintext];
    """

    # Set pointer
    file.seek(sb.inode_start)
    # Read Inode
    packed_inode = file.read(sb.inode_size)
    # Unpack Inode
    inode = Inode.unpack(packed_inode)

    # Call recursive function and append its result to graphviz
    content, i = visit_blocks_report(file, sb, inode, 0)
    graphviz += content

    # Table connections
    for j in range(0, i - 1):
        graphviz += f"table{j} -> table{j+1}; "

    # End of graphviz
    graphviz += "}"

    return graphviz


def visit_blocks_report(file, sb, inode, i):
    # Create an empty string to store the content generated by this function
    content = ""

    # Get the pointers
    for index, block_pointer in enumerate(inode.block):
        if block_pointer != -1:
            # Set pointer
            file.seek(sb.block_start + (block_pointer * sb.block_size))
            # Read block
            packed_block = file.read(sb.block_size)

            # Indirect pointer
            if index >= 12:
                pass  # Cambia esto más adelante
            # Folder block
            if inode.type == "0":
                # Unpack folder block
                folder_block = FolderBlock.unpack(packed_block)
                # folder_block.show_folder_block()

                # Create graphviz table
                content += f"""  
                    table{i} [label=<<table border="0" cellborder="1" cellspacing="0">
                        <tr><td colspan="2" bgcolor="#FFFFCC">Bloque de Carpeta {i}</td></tr>
                """
                for j in range(0, 4):
                    content += f"""<tr><td bgcolor="#EFEFEF">{folder_block.content[j].name}</td> <td>{folder_block.content[j].inode}</td></tr>"""

                content += f"""          
                    </table>>];
                """
                # Increase i
                i += 1

                # If has a pointer
                if folder_block.content[2].inode != -1:
                    # Set pointer
                    file.seek(
                        sb.inode_start + (folder_block.content[2].inode * sb.inode_size)
                    )
                    # Read Inode
                    packed_new_inode = file.read(sb.inode_size)
                    # Unpack Inode
                    new_inode = Inode.unpack(packed_new_inode)

                    # Recursive call and append its content to the result
                    new_content, new_i = visit_blocks_report(file, sb, new_inode, i)
                    content += new_content
                    i = new_i

                if folder_block.content[3].inode != -1:
                    # Set pointer
                    file.seek(
                        sb.inode_start + (folder_block.content[3].inode * sb.inode_size)
                    )
                    # Read Inode
                    packed_new_inode = file.read(sb.inode_size)
                    # Unpack Inode
                    new_inode = Inode.unpack(packed_new_inode)

                    # Recursive call and append its content to the result
                    new_content, new_i = visit_blocks_report(file, sb, new_inode, i)
                    content += new_content
                    i = new_i

            # File block
            if inode.type == "1":
                # Unpack file block
                file_block = FileBlock.unpack(packed_block)
                # file_block.show_file_block()

                # Create graphviz table
                content += f"""  
                    table{i} [label=<<table border="0" cellborder="1" cellspacing="0">
                        <tr><td colspan="2" bgcolor="#FFFFCC">Bloque de Archivo {i}</td></tr>
                        <tr><td colspan="2">{file_block.content}</td></tr>
                    </table>>];    
                """
                # Increase i
                i += 1

    return content, i


# Bitmap Inode report
def bm_inode_report(file, pointer):
    # Set pointer
    file.seek(pointer)
    # Read SuperBlock
    packed_superblock = file.read(SUPERBLOCK_SIZE)
    # Unpack SuperBlock
    sb = SuperBlock.unpack(packed_superblock)

    # Calculate the number of inodes
    total_inodes = sb.bitmap_block_start - sb.bitmap_inode_start

    # Get the inode bitmap
    bitmap_content = ""  # Inicializa la cadena del bitmap

    for i in range(total_inodes):
        # Establece el puntero
        file.seek(sb.bitmap_inode_start + i)
        # Lee un byte (carácter '0' o '1')
        char = file.read(1).decode()

        # Agrega el carácter al contenido del bitmap
        bitmap_content += char

        # Agrega un carácter de nueva línea cada 20 caracteres (20 inodos)
        if (i + 1) % 20 == 0:
            bitmap_content += "\n"

    # Separate the content in lines
    content = bitmap_content.replace("\n", "<br/>")

    # Generate the graphviz code
    graphviz = """
    digraph G {{
        node [shape=box, width=2, style="rounded,filled", fillcolor="lightgray"]
        Content [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
    """
    graphviz += f"""   
            <TR><TD WIDTH="200" HEIGHT="100" ALIGN="LEFT" VALIGN="TOP">{content}</TD></TR>
    """

    graphviz += """        
        </TABLE>>]
    }}
    """

    # print(graphviz)

    return graphviz


# Bitmap Block report
def bm_block_report(file, pointer):
    # Set pointer
    file.seek(pointer)
    # Read SuperBlock
    packed_superblock = file.read(SUPERBLOCK_SIZE)
    # Unpack SuperBlock
    sb = SuperBlock.unpack(packed_superblock)

    # Calculate the number of block
    total_blocks = sb.inode_start - sb.bitmap_block_start

    # Create a string to store the bitmap content
    bitmap_content = ""

    # Get the inode bitmap
    bitmap_content = ""  # Inicializa la cadena del bitmap

    for i in range(total_blocks):
        # Establece el puntero
        file.seek(sb.bitmap_inode_start + i)
        # Lee un byte (carácter '0' o '1')
        char = file.read(1).decode()

        # Agrega el carácter al contenido del bitmap
        bitmap_content += char

        # Agrega un carácter de nueva línea cada 20 caracteres (20 inodos)
        if (i + 1) % 20 == 0:
            bitmap_content += "\n"

    # Separate the content in lines
    content = bitmap_content.replace("\n", "<br/>")

    # Generate the graphviz code
    graphviz = """
    digraph G {{
        node [shape=box, width=2, style="rounded,filled", fillcolor="lightgray"]
        Content [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
    """
    graphviz += f"""   
            <TR><TD WIDTH="200" HEIGHT="100" ALIGN="LEFT" VALIGN="TOP">{content}</TD></TR>
    """

    graphviz += """        
        </TABLE>>]
    }}
    """

    # print(graphviz)

    return graphviz


# Tree report
def tree_report(file, pointer):
    # Set pointer
    file.seek(pointer)
    # Read SuperBlock
    packed_superblock = file.read(SUPERBLOCK_SIZE)
    # Unpack SuperBlock
    sb = SuperBlock.unpack(packed_superblock)

    # Begin graphviz
    graphviz = """
    digraph G{
        graph [pad="0.5", nodesep="0.5", ranksep="1"];
        node [shape=plaintext]
        rankdir=LR;
    """

    # Set pointer
    file.seek(sb.inode_start)
    # Read Inode
    packed_inode = file.read(sb.inode_size)
    # Unpack Inode
    inode = Inode.unpack(packed_inode)

    # Call recursive function and append its result to graphviz
    content = visit_tree_report(file, sb, inode, 0)
    graphviz += content

    # End of graphviz
    graphviz += "}"

    return graphviz


def visit_tree_report(file, sb, inode, inode_count):
    # Graphviz the inode
    content = f"""  
        Inode{inode_count} [label=<<table border="0" cellborder="1" cellspacing="0">
            <tr><td colspan="2" bgcolor="#FFFFCC">Inodo {inode_count}</td></tr>
            <tr><td bgcolor="#EFEFEF">Tipo</td> <td>{inode.type}</td></tr>
            <tr><td bgcolor="#EFEFEF">Tamaño</td> <td>{inode.size}</td></tr>            
    """
    for j in range(0, 15):
        content += f"""<tr><td bgcolor="#EFEFEF">Bloque {j+1}</td> <td port='I{j}'>{inode.block[j]}</td></tr>"""
    content += f"""          
        </table>>];
    """

    # Get the pointers
    for index, block_pointer in enumerate(inode.block):
        if block_pointer != -1:
            # Set pointer
            file.seek(sb.block_start + (block_pointer * sb.block_size))
            # Read block
            packed_block = file.read(sb.block_size)

            # Indirect pointer
            if index >= 12:
                pass  # Cambia esto más adelante
            # Folder block
            if inode.type == "0":
                # Unpack folder block
                folder_block = FolderBlock.unpack(packed_block)

                # Graphviz the folder block
                content += f"""  
                    FolderBlock{block_pointer} [label=<<table border="0" cellborder="1" cellspacing="0">
                        <tr><td colspan="2" bgcolor="#FFFFCC">Bloque de Carpeta {block_pointer}</td></tr>
                """
                for j in range(0, 4):
                    content += f"""<tr><td bgcolor="#EFEFEF">{folder_block.content[j].name}</td> <td port='B{j}'>{folder_block.content[j].inode}</td></tr>"""
                content += f"""          
                    </table>>];
                """

                # Connect the inode with the folder block
                content += f"Inode{inode_count}:I{index} -> FolderBlock{block_pointer};"

                # Aux counter
                aux_count_block = 0

                # If has a pointer
                if folder_block.content[2].inode != -1:
                    # Set pointer
                    file.seek(
                        sb.inode_start + (folder_block.content[2].inode * sb.inode_size)
                    )
                    # Read Inode
                    packed_new_inode = file.read(sb.inode_size)
                    # Unpack Inode
                    new_inode = Inode.unpack(packed_new_inode)

                    # Connect the folder block with the inode
                    content += f"FolderBlock{block_pointer}:B2 -> Inode{folder_block.content[2].inode};"

                    # Recursive call and append its content to the result
                    new_content = visit_tree_report(
                        file, sb, new_inode, folder_block.content[2].inode
                    )
                    content += new_content

                if folder_block.content[3].inode != -1:
                    # Set pointer
                    file.seek(
                        sb.inode_start + (folder_block.content[3].inode * sb.inode_size)
                    )
                    # Read Inode
                    packed_new_inode = file.read(sb.inode_size)
                    # Unpack Inode
                    new_inode = Inode.unpack(packed_new_inode)

                    # Connect the folder block with the inode
                    content += f"FolderBlock{block_pointer}:B3 -> Inode{folder_block.content[3].inode};"

                    # Recursive call and append its content to the result
                    new_content = visit_tree_report(
                        file, sb, new_inode, folder_block.content[3].inode
                    )
                    content += new_content

            # File block
            if inode.type == "1":
                # Unpack file block
                file_block = FileBlock.unpack(packed_block)
                # file_block.show_file_block()

                # Create graphviz table
                content += f"""  
                    FileBlock{block_pointer} [label=<<table border="0" cellborder="1" cellspacing="0">
                        <tr><td colspan="2" bgcolor="#FFFFCC">Bloque de Archivo {block_pointer}</td></tr>
                        <tr><td colspan="2">{file_block.content}</td></tr>
                    </table>>];    
                """

                # Connect the inode with the folder block
                content += f"Inode{inode_count}:I{index} -> FileBlock{block_pointer};"

    # Increase inode_count
    inode_count += 1

    return content


# SuperBlock report
def sb_report(file, pointer):
    # Set pointer
    file.seek(pointer)
    # Read SuperBlock
    packed_superblock = file.read(SUPERBLOCK_SIZE)
    # Unpack SuperBlock
    sb = SuperBlock.unpack(packed_superblock)

    # Begin graphviz
    graphviz = """
    digraph G{
        node [ shape=none fontname=Helvetica ]
        n1 [ label = <
            <table border="0" cellspacing="0" cellborder="1">
                <tr>
                    <td colspan="2" bgcolor="#FFFFCC"><b>Reporte Super Bloque</b></td>
                </tr>  
    """

    # Disk
    graphviz += f"""  
                <tr>
                    <td bgcolor="#EFEFEF">Inodos Creados</td>                    
                    <td>{sb.inodes_count}</td>                    
                </tr>   
                <tr>
                    <td bgcolor="#EFEFEF">Bloques Creados</td>                    
                    <td>{sb.blocks_count}</td>                    
                </tr>  
                <tr>
                    <td bgcolor="#EFEFEF">Inodos Libres</td>                    
                    <td>{sb.free_inodes_count}</td>                    
                </tr>   
                <tr>
                    <td bgcolor="#EFEFEF">Bloques Libres</td>                    
                    <td>{sb.free_blocks_count}</td>                    
                </tr>  
                <tr>
                    <td bgcolor="#EFEFEF">Fecha de Montaje</td>                    
                    <td>{sb.mount_time}</td>                    
                </tr> 
                <tr>
                    <td bgcolor="#EFEFEF">Fecha de Desmontaje</td>                    
                    <td>{sb.unmount_time}</td>                    
                </tr> 
                <tr>
                    <td bgcolor="#EFEFEF">Veces Montado</td>                    
                    <td>{sb.mount_count}</td>                    
                </tr> 
                <tr>
                    <td bgcolor="#EFEFEF">Tamaño del Inodo</td>                    
                    <td>{sb.inode_size}</td>                    
                </tr> 
                <tr>
                    <td bgcolor="#EFEFEF">Tamaño del Bloque</td>                    
                    <td>{sb.block_size}</td>                    
                </tr>
                <tr>
                    <td bgcolor="#EFEFEF">Primer Inodo</td>                    
                    <td>{sb.first_inode}</td>                    
                </tr> 
                <tr>
                    <td bgcolor="#EFEFEF">Primer Bloque</td>                    
                    <td>{sb.first_block}</td>                    
                </tr>      
                <tr>
                    <td bgcolor="#EFEFEF">Comienzo de Inodos</td>                    
                    <td>{sb.inode_start}</td>                    
                </tr> 
                <tr>
                    <td bgcolor="#EFEFEF">Comienzo de Bloques</td>                    
                    <td>{sb.block_start}</td>                    
                </tr>  
                <tr>
                    <td bgcolor="#EFEFEF">Comienzo del BitMap Inodos</td>                    
                    <td>{sb.bitmap_inode_start}</td>                    
                </tr> 
                <tr>
                    <td bgcolor="#EFEFEF">Comienzo del BitMap Bloques</td>                    
                    <td>{sb.bitmap_block_start}</td>                    
                </tr>    
                <tr>
                    <td bgcolor="#EFEFEF">Número Mágico</td>                    
                    <td>{sb.magic}</td>                    
                </tr>                    
    """
    # End of graphviz
    graphviz += """
            </table>
        >]
    }
    """
    return graphviz


# File report
def file_report(file, pointer, file_path):
    # Set pointer
    file.seek(pointer)
    # Read SuperBlock
    packed_superblock = file.read(SUPERBLOCK_SIZE)
    # Unpack SuperBlock
    sb = SuperBlock.unpack(packed_superblock)

    # Get the path of the file
    path = file_path.split("/")
    path.pop(0)

    # Get the content of the file
    content = sb.get_file_content(file, path)

    # Separate the content in lines
    content = content.replace("\n", "<br/>")

    # Generate the graphviz code
    graphviz = """
    digraph G {{
        node [shape=box, width=2, style="rounded,filled", fillcolor="lightgray"]
        Content [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
    """
    graphviz += f"""   
            <TR><TD WIDTH="200" HEIGHT="100" ALIGN="LEFT" VALIGN="TOP">{content}</TD></TR>
    """

    graphviz += """        
        </TABLE>>]
    }}
    """

    return graphviz
