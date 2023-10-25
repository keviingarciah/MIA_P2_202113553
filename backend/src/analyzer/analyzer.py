# --------------------------- LEXER ---------------------------
# Reserved words
reserved = {
    # Disk commands
    "mkdisk": "MKDISK",
    "rmdisk": "RMDISK",
    "fdisk": "FDISK",
    "mount": "MOUNT",
    "unmount": "UNMOUNT",
    "mkfs": "MKFS",
    # User and group commands
    "login": "LOGIN",
    "logout": "LOGOUT",
    "mkgrp": "MKGRP",
    "rmgrp": "RMGRP",
    "mkusr": "MKUSR",
    "rmusr": "RMUSR",
    "chgrp": "CHGRP",
    # Folder and file commands
    "mkdir": "MKDIR",
    "mkfile": "MKFILE",
    "cat": "CAT",
    "remove": "REMOVE",
    "edit": "EDIT",
    "rename": "RENAME",
    # Extra commands
    "execute": "EXECUTE",
    "pause": "PAUSE",
    # Report commands
    "rep": "REP",
    # Parameters
    "size": "SIZE",
    "path": "PATH",
    "name": "NAME",
    "unit": "UNIT",
    "b": "B",
    "k": "K",
    "m": "M",
    "type": "TYPE",
    "p": "P",
    "e": "E",
    "l": "L",
    "fit": "FIT",
    "bf": "BF",
    "ff": "FF",
    "wf": "WF",
    "delete": "DELETE",
    "full": "FULL",
    "add": "ADD",
    "id": "ID",
    "fs": "FS",
    "2fs": "2FS",  # 2fs = 2FS
    "3fs": "3FS",  # 3fs = 3FS
    "user": "USER",
    "pass": "PASS",
    "grp": "GRP",
    "r": "R",
    "cont": "CONT",
    "file": "FILE",
    #
    "ruta": "RUTA",
}

# Define tokens
tokens = ["DASH", "EQUAL", "IDENTIFIER", "NUMBER", "QUOTED_STRING", "STRING"] + list(
    reserved.values()
)

# Reglas de tokens
t_DASH = r"-"
t_EQUAL = r"="


# Definición de la expresión regular para números positivos y negativos
def t_IDENTIFIER(t):
    r"[0-9]+[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value.lower(), "IDENTIFIER")  # Check for reserved words
    return t


def t_NUMBER(t):
    r"-?\d+"
    t.value = int(t.value)
    return t


# Reglas de tokens
def t_QUOTED_STRING(t):
    r'"(?:[^"\\]|\\.)*"'
    t.value = t.value.strip('"')
    return t


def t_STRING(t):
    r"[a-zA-Z_./][a-zA-Z_0-9./]*"
    t.type = reserved.get(t.value.lower(), "STRING")  # Check for reserved words
    return t


# Reglas de tokens ignorados
t_ignore = " \t"


# Funciones de manejo de tokens
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


# Build lexer
import ply.lex as lex

lexer = lex.lex()

# --------------------------- GRAMMAR ---------------------------
# Imports
from scripts.disk_managment import MKDISK, FDISK, RMDISK, MOUNT, MKFS
from scripts.user_managment import LOGIN, LOGOUT, MKGRP, RMGRP, MKUSR, RMUSR
from scripts.file_managment import MKDIR, MKFILE
from scripts.extra import PAUSE
from scripts.report_generation import REP

# Mensaje
message = "Inicializando..."

# Disk Management
mkdisk_instance = MKDISK()
fdisk_instance = FDISK()
rmdisk_instance = RMDISK()
mount_instance = MOUNT()
mkfs_instance = MKFS()
# User Management
login_instance = LOGIN()
logout_instance = LOGOUT()
mkgrp_instance = MKGRP()
rmgrp_instance = RMGRP()
mkusr_instance = MKUSR()
rmusr_instance = RMUSR()
# File Management
mkdir_instance = MKDIR()
mkfile_instance = MKFILE()
# Extra
pause_instance = PAUSE()
# Report
rep_instance = REP()


# Begin
def p_begin(p):
    "begin : command"


# ------------------ COMMAND ------------------
def p_command(p):
    """command : MKDISK mkdisk_parameters
    | RMDISK rmdisk_parameter
    | FDISK fdisk_parameters
    | MOUNT mount_parameters
    | MKFS mkfs_parameters

    | LOGIN login_parameters
    | LOGOUT
    | MKGRP mkgrp_parameter
    | RMGRP rmgrp_parameter
    | MKUSR mkusr_parameters
    | RMUSR rmusr_parameter

    | MKFILE mkfile_parameters
    | MKDIR mkdir_parameters

    | PAUSE

    | REP rep_parameters"""

    # Set scripts instance
    global mkdisk_instance, fdisk_instance, mkfs_instance
    global login_instance, mkusr_instance
    global mkfile_instance, mkdir_instance
    global rep_instance

    # Set message
    global message

    # File management
    if p[1] == "mkdisk":
        message = mkdisk_instance.create_disk()
    elif p[1] == "rmdisk":
        message = rmdisk_instance.delete_disk()
    elif p[1] == "fdisk":
        message = fdisk_instance.create_partition()
    elif p[1] == "mount":
        message = mount_instance.mount_partition()
    elif p[1] == "mkfs":
        message = mkfs_instance.format_partition()
    # User management
    elif p[1] == "login":
        message = login_instance.login()
    elif p[1] == "logout":
        message = logout_instance.logout()
    elif p[1] == "mkgrp":
        message = mkgrp_instance.create_group()
    elif p[1] == "rmgrp":
        message = rmgrp_instance.remove_group()
    elif p[1] == "mkusr":
        message = mkusr_instance.create_user()
    elif p[1] == "rmusr":
        message = rmusr_instance.remove_user()
    # File management
    elif p[1] == "mkfile":
        message = mkfile_instance.create_file()
    elif p[1] == "mkdir":
        message = mkdir_instance.create_folder()
    # Extra
    elif p[1] == "pause":
        message = pause_instance.pause()
    # Report
    elif p[1] == "rep":
        message = rep_instance.create_report()

    # Reset scripts instance
    # -----------------------------
    mkdisk_instance = MKDISK()
    fdisk_instance = FDISK()
    mkfs_instance = MKFS()
    # -----------------------------
    login_instance = LOGIN()
    mkusr_instance = MKUSR()
    # -----------------------------
    mkfile_instance = MKFILE()
    mkdir_instance = MKDIR()
    # -----------------------------
    rep_instance = REP()


# ------------------ MKDISK ------------------
def p_mkdisk_parameters(p):
    """mkdisk_parameters : mkdisk_parameter mkdisk_parameters
    | mkdisk_parameter"""
    pass


def p_mkdisk_parameter(p):
    """mkdisk_parameter : DASH SIZE EQUAL NUMBER
    | DASH PATH EQUAL string_parameter
    | DASH FIT  EQUAL fit_parameter
    | DASH UNIT EQUAL unit_parameter"""
    # Set disk instance
    global mkdisk_instance
    if p[2] == "size":
        mkdisk_instance.size = int(p[4])
    elif p[2] == "path":
        mkdisk_instance.path = p[4]
    elif p[2] == "fit":
        mkdisk_instance.fit = p[4]
    elif p[2] == "unit":
        mkdisk_instance.unit = p[4]

    # print("Opción:", p[2], "Valor:", p[4])


# ------------------ RMDISK ------------------
def p_rmdisk_parameter(p):
    "rmdisk_parameter : DASH PATH EQUAL string_parameter"

    # Set disk instance
    global rmdisk_instance
    rmdisk_instance.path = p[4]

    # print("Opción:", p[2], "Valor:", p[4])


# ------------------ FDISK ------------------
def p_fdisk_parameters(p):
    """fdisk_parameters : fdisk_parameter fdisk_parameters
    | fdisk_parameter"""
    pass


def p_fdisk_parameter(p):
    """fdisk_parameter : DASH SIZE EQUAL NUMBER
    | DASH PATH EQUAL string_parameter
    | DASH NAME EQUAL string_parameter
    | DASH UNIT EQUAL unit_parameter
    | DASH TYPE  EQUAL type_parameter
    | DASH FIT  EQUAL fit_parameter"""
    # Set partition instance
    global fdisk_instance
    if p[2] == "size":
        fdisk_instance.size = int(p[4])
    elif p[2] == "path":
        fdisk_instance.path = p[4]
    elif p[2] == "name":
        fdisk_instance.name = p[4]
    elif p[2] == "unit":
        fdisk_instance.unit = p[4]
    elif p[2] == "type":
        fdisk_instance.type = p[4]
    elif p[2] == "fit":
        fdisk_instance.fit = p[4]

    # print("Opción:", p[2], "Valor:", p[4])


# ------------------ MOUNT ------------------
def p_mount_parameters(p):
    """mount_parameters : mount_parameter mount_parameters
    | mount_parameter"""
    pass


def p_mount_parameter(p):
    """mount_parameter : DASH PATH EQUAL string_parameter
    | DASH NAME EQUAL string_parameter"""
    # Set mount instance
    global mount_instance
    if p[2] == "path":
        mount_instance.path = p[4]
    elif p[2] == "name":
        mount_instance.name = p[4]
    # print("Opción:", p[2], "Valor:", p[4])


# ------------------ MKFS ------------------
def p_mkfs_parameters(p):
    """mkfs_parameters : mkfs_parameter mkfs_parameters
    | mkfs_parameter"""
    pass


def p_mkfs_parameter(p):
    """mkfs_parameter : DASH ID EQUAL id_parameter
    | DASH TYPE EQUAL FULL"""
    # Set mkfs instance
    global mkfs_instance
    if p[2] == "id":
        mkfs_instance.id = p[4]
    elif p[2] == "type":
        mkfs_instance.type = p[4]
    # print("Opción:", p[2], "Valor:", p[4])


# ------------------ LOGIN ------------------
def p_login_parameters(p):
    """login_parameters : login_parameter login_parameters
    | login_parameter"""
    pass


def p_login_parameter(p):
    """login_parameter : DASH USER EQUAL string_parameter
    | DASH PASS EQUAL pass_parameter
    | DASH ID EQUAL id_parameter"""
    # Set login instance
    global login_instance
    if p[2] == "user":
        login_instance.user = p[4]
    elif p[2] == "pass":
        login_instance.password = p[4]
    elif p[2] == "id":
        login_instance.id = p[4]
    # print("Opción:", p[2], "Valor:", p[4])


# ------------------ MKGRP ------------------
def p_mkgrp_parameter(p):
    "mkgrp_parameter : DASH NAME EQUAL string_parameter"
    # Set mkgrp instance
    global mkgrp_instance
    mkgrp_instance.name = p[4]
    # print("Opción:", p[2], "Valor:", p[4])


# ------------------ RMGRP ------------------
def p_rmgrp_parameter(p):
    "rmgrp_parameter : DASH NAME EQUAL string_parameter"
    # Set rmgrp instance
    global rmgrp_instance
    rmgrp_instance.name = p[4]
    # print("Opción:", p[2], "Valor:", p[4])


# ------------------ MKUSR ------------------
def p_mkusr_parameters(p):
    """mkusr_parameters : mkusr_parameter mkusr_parameters
    | mkusr_parameter"""
    pass


def p_mkusr_parameter(p):
    """mkusr_parameter : DASH USER EQUAL string_parameter
    | DASH PASS EQUAL pass_parameter
    | DASH GRP EQUAL string_parameter"""
    # Set mkusr instance
    global mkusr_instance
    if p[2] == "user":
        mkusr_instance.user = p[4]
    elif p[2] == "pass":
        mkusr_instance.password = p[4]
    elif p[2] == "grp":
        mkusr_instance.group = p[4]
    # print("Opción:", p[2], "Valor:", p[4])


# ------------------ RMUSR ------------------
def p_rmusr_parameter(p):
    "rmusr_parameter : DASH USER EQUAL string_parameter"
    # Set rmusr instance
    global rmusr_instance
    rmusr_instance.user = p[4]
    # print("Opción:", p[2], "Valor:", p[4])


# ------------------ MKFILE ------------------
def p_mkfile_parameters(p):
    """mkfile_parameters : mkfile_parameter mkfile_parameters
    | mkfile_parameter"""
    pass


def p_mkfile_parameter(p):
    """mkfile_parameter :  DASH PATH EQUAL string_parameter
    | DASH R
    | DASH SIZE  EQUAL NUMBER
    | DASH CONT  EQUAL string_parameter"""
    # Set mkfile instance
    global mkfile_instance
    if p[2] == "path":
        mkfile_instance.path = p[4]
    if p[2] == "r":
        mkfile_instance.r = True
    if p[2] == "size":
        mkfile_instance.size = p[4]
    if p[2] == "cont":
        mkfile_instance.cont = p[4]
    # print("Opción:", p[2], "Valor:", p[4])


# ------------------ MKDIR ------------------
def p_mkdir_parameters(p):
    """mkdir_parameters : mkdir_parameter mkdir_parameters
    | mkdir_parameter"""
    pass


def p_mkdir_parameter(p):
    """mkdir_parameter :  DASH PATH EQUAL string_parameter
    | DASH R"""
    # Set mkdir instance
    global mkdir_instance
    if p[2] == "path":
        mkdir_instance.path = p[4]
    if p[2] == "r":
        mkdir_instance.r = True


# ------------------ REP ------------------
def p_rep_parameters(p):
    """rep_parameters : rep_parameter rep_parameters
    | rep_parameter"""
    pass


def p_rep_parameter(p):
    """rep_parameter :  DASH NAME EQUAL string_parameter
    | DASH PATH EQUAL string_parameter
    | DASH ID EQUAL id_parameter
    | DASH RUTA EQUAL string_parameter"""
    # Set mkdir instance
    global rep_instance
    if p[2] == "name":
        rep_instance.name = p[4]
    if p[2] == "path":
        rep_instance.path = p[4]
    if p[2] == "id":
        rep_instance.id = p[4]
    if p[2] == "ruta":
        rep_instance.ruta = p[4]
    # print("Opción:", p[2], "Valor:", p[4])


# ------------------ PARAMETERS ------------------
def p_string_parameter(p):
    """string_parameter : STRING
    | QUOTED_STRING
    | FILE"""
    p[0] = p[1]


def p_unit_parameter(p):
    """unit_parameter : B
    | K
    | M"""
    p[0] = p[1]


def p_type_parameter(p):
    """type_parameter : P
    | E
    | L"""
    p[0] = p[1]


def p_fit_parameter(p):
    """fit_parameter : BF
    | FF
    | WF"""
    p[0] = p[1]


def p_delete_parameter(p):
    "delete_parameter : FULL"
    p[0] = p[1]


def p_add_parameter(p):
    "add_parameter : NUMBER"
    p[0] = p[1]


def p_id_parameter(p):
    "id_parameter : IDENTIFIER"
    p[0] = p[1]


def p_fs_parameter(p):
    """fs_parameter : 2FS
    | 3FS"""
    p[0] = p[1]


def p_pass_parameter(p):
    """pass_parameter : STRING
    | QUOTED_STRING
    | NUMBER"""
    p[0] = p[1]


# ------------------ ERRORS ------------------
def p_error(p):
    global message

    if p:
        message = f"[ERROR] Valor no esperado: '{p.value}.'"
    else:
        message = "[ERROR] Error de sintaxis."


# Build grammar
import ply.yacc as yacc

parser = yacc.yacc()


# Parse input
def parse(input):
    parser.parse(input)
    return message
