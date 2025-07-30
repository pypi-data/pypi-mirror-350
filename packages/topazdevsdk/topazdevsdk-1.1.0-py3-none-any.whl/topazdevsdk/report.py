from . import file as f

global rdir
global filename
rdir = '_REPORTS'
filename = None

# =================
def init(file, file_name):
    """
    Initialize the report file with a given name and write the header.
    
    :param file: The file object to write to.
    :param file_name: The name of the report file.
    :return: None
    """
    global rdir
    global filename
    filename = file_name
    filename_ext = f'{rdir}/{filename}.md'

    f.createdir(rdir)
    if (not f.exist(filename_ext)):
        f.create(filename_ext)

    f.write(filename_ext, f'# Test sheet **{filename}**\n\n')
    code(file)

# ------------------------------------
def section(title: str, text: str):
    """
    Add a section to the report file with a given title and text.
    
    :param title: The title of the section.
    :param text: The text content of the section.
    :return: None
    """
    global rdir
    global filename
    if filename is None:
        raise ValueError("The report file name is not defined. Please call init() or set the filename variable.")
    filename_ext = f'{rdir}/{filename}.md'

    f.add(filename_ext, f'## {title}\n\n')
    f.add(filename_ext, f'{text}\n\n')

# ------------------------------------
def title(title: str, indent: int = 2):
    """
    Add a title section to the report file with a given title.
    
    :param title: The title of the section.
    :param indent: The indentation level for the title (default is 2).
    :return: None
    """
    global rdir
    global filename
    if filename is None:
        raise ValueError("The report file name is not defined. Please call init() or set the filename variable.")
    filename_ext = f'{rdir}/{filename}.md'

    f.add(filename_ext, f'\n{("#" * indent)} {title}\n\n')

# ------------------------------------
def text(text: str, indent: int = 0):
    """
    Add a text to the report file
    
    :param text: The text content.
    :param indent: The indentation level for the text (default is 0).
    :return: None
    """
    global rdir
    global filename
    if filename is None:
        raise ValueError("The report file name is not defined. Please call init() or set the filename variable.")
    filename_ext = f'{rdir}/{filename}.md'

    f.add(filename_ext, f'\n{(" " * indent)}{text}\n\n')

# --------------------
def code(file):
    """
    Add a section to the report file with the test code.
    This function reads the content of the provided file and adds it to the report file.

    :param file: The file object to read the test code from.
    :return: None
    """
    global rdir
    global filename
    if filename is None:
        raise ValueError("The report file name is not defined. Please call init() or set the filename variable.")
    filename_ext = f'{rdir}/{filename}.md'
    code = f.read(file)

    f.add(filename_ext, f'\n## Test code\n\n')
    f.add(filename_ext, f'```python\n{code}\n```\n\n')

# =========================================================
def start(type: str = 'bullet', title: str = "Conduct of the test"):
    """
    Start a new section in the report file with a given title and type.

    :param type: The type of section (e.g., 'table', 'bullet').
    :param title: The title of the section.
    :return: None
    """
    global rdir
    global filename
    if filename is None:
        raise ValueError("The report file name is not defined. Please call init() or set the filename variable.")
    filename_ext = f'{rdir}/{filename}.md'

    if type.lower() == 'table':
        f.add(filename_ext, f'\n## {title}\n\n')
        table(['Type', 'Description', 'State'])
    elif type.lower() == 'bullet':
        f.add(filename_ext, f'\n## {title}\n\n')
    else:
        f.add(filename_ext, f'\n## {title}\n\n')

# ------------------------------------------------
def table(column: list[str]):
    """
    Add a table header to the report file with a given list of column names.
    
    :param column: A list of column names for the table header.
    :return: None
    """
    global rdir
    global filename
    if filename is None:
        raise ValueError("The report file name is not defined. Please call init() or set the filename variable.")
    filename_ext = f'{rdir}/{filename}.md'
    if column is None:
        raise ValueError("The column list is not defined. Please provide a list of column names.")
    if len(column) == 0:
        raise ValueError("The column list is empty. Please provide a list of column names.")
    else:
        entete = '|'
        sous_entete = '|'
        for col in column:
            entete += f' {col} |'
            sous_entete += ' -- |'
        f.add(filename_ext, f'{entete}\n')
        f.add(filename_ext, f'{sous_entete}\n')


# -----------------------------------------------
def info(type: str = 'bullet', msg: str = '', state: str = '', indent: int = 0):
    """
    Add an informational message to the report file with a given type, message, and state.

    :param type: The type of message (e.g., 'table', 'bullet').
    :param msg: The informational message to add.
    :param state: The state associated with the message (default is '').
    :param indent: The indentation level for the message (default is 0).
    :return: None
    """
    global rdir
    global filename
    if filename is None:
        raise ValueError("The report file name is not defined. Please call init() or set the filename variable.")
    filename_ext = f'{rdir}/{filename}.md'

    if type.lower() == 'table':
        f.add(filename_ext, f'|   INFO   | {msg} | {state} |\n')
    elif type.lower() == 'bullet':
        f.add(filename_ext, f'{("   " * indent)}- INFO: {msg} {(f"> {state}" if state != "" else "")}\n')
    else:
        f.add(filename_ext, f'{("   " * indent)}INFO: {msg} {(f"> {state}" if state != "" else "")}\n')

# ------------------------------------------------
def error(type: str = 'bullet', msg: str = '', state: str = '', indent: int = 0):
    """
    Add an error message to the report file with a given type, message, and state.

    :param type: The type of message (e.g., 'table', 'bullet').
    :param msg: The error message to add.
    :param state: The state associated with the message (default is '').
    :param indent: The indentation level for the message (default is 0).
    :return: None
    """
    global rdir
    global filename
    if filename is None:
        raise ValueError("The report file name is not defined. Please call init() or set the filename variable.")
    filename_ext = f'{rdir}/{filename}.md'

    if type.lower() == 'table':
        f.add(filename_ext, f'| _ERROR_    | {msg} | {state} |\n')
    elif type.lower() == 'bullet':
        f.add(filename_ext, f'{("   " * indent)}- _ERROR_: {msg} {(f"> {state}" if state != "" else "")}\n')
    else:
        f.add(filename_ext, f'{("   " * indent)}_ERROR_: {msg} {(f"> {state}" if state != "" else "")}\n')

# --------------------------------------------------
def warning(type: str = 'bullet', msg: str = '', state: str = '', indent: int = 0):
    """
    Add a warning message to the report file with a given type, message, and state.

    :param type: The type of message (e.g., 'table', 'bullet').
    :param msg: The warning message to add.
    :param state: The state associated with the message (default is '').
    :param indent: The indentation level for the message (default is 0).
    :return: None
    """
    global rdir
    global filename
    if filename is None:
        raise ValueError("The report file name is not defined. Please call init() or set the filename variable.")
    filename_ext = f'{rdir}/{filename}.md'

    if type.lower() == 'table':
        f.add(filename_ext, f'| _WARNING_   | {msg} | {state} |\n')
    elif type.lower() == 'bullet':
        f.add(filename_ext, f'{("   " * indent)}- _WARNING_: {msg} {(f"> {state}" if state != "" else "")}\n')
    else:
        f.add(filename_ext, f'{("   " * indent)}_WARNING_: {msg} {(f"> {state}" if state != "" else "")}\n')

# ---------------------------------------
def test(type: str = 'bullet', msg: str = '', state: str = 'NOK', indent: int = 0):
    """
    Add a test message to the report file with a given type, message, and state.

    :param type: The type of message (e.g., 'table', 'bullet').
    :param msg: The test message to add.
    :param state: The state associated with the message (default is 'NOK').
    :param indent: The indentation level for the message (default is 0).
    :return: None
    """
    global rdir
    global filename
    if filename is None:
        raise ValueError("The report file name is not defined. Please call init() or set the filename variable.")
    filename_ext = f'{rdir}/{filename}.md'

    if type.lower() == 'table':
        f.add(filename_ext, f'| **TEST**      | {msg} | {state} |\n')
    elif type.lower() == 'bullet':
        f.add(filename_ext, f'{("   " * indent)}- **TEST**: {msg} {(f"> {state}" if state != "" else "")}\n')
    else:
        f.add(filename_ext, f'{("   " * indent)}**TEST**: {msg} {(f"> {state}" if state != "" else "")}\n')

# ---------------------------------------
def less(type: str = 'bullet', msg: str = '', state: str = '', indent: int = 0):
    """
    Add a message to the report file with a given type, message, and state.

    :param type: The type of message (e.g., 'table', 'bullet').
    :param msg: The test message to add.
    :param state: The state associated with the message (default is '').
    :param indent: The indentation level for the message (default is 0).
    :return: None
    """
    global rdir
    global filename
    if filename is None:
        raise ValueError("The report file name is not defined. Please call init() or set the filename variable.")
    filename_ext = f'{rdir}/{filename}.md'

    if type.lower() == 'table':
        f.add(filename_ext, f'|          | {msg} | {state} |\n')
    elif type.lower() == 'bullet':
        f.add(filename_ext, f'{("   " * indent)}- {msg} {(f"> {state}" if state != "" else "")}\n')
    else:
        f.add(filename_ext, f'{("   " * indent)}{msg} {(f"> {state}" if state != "" else "")}\n')