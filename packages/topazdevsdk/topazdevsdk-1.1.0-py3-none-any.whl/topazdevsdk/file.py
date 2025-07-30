import os
import json

# •••••••••••••••••••••••••••••••••••••••
# ••••••••••••• FILES •••••••••••••••••••
# •••••••••••••••••••••••••••••••••••••••
def exist(path):
    """
    Checks if a file or folder exists.

    :param str path: Path to the file or folder.
    """
    if os.path.exists(path):
        return True
    else:
        return False

# •••••••••••••••••••••••••••••••••••••••
def open_read(path, encoding='utf-8'):
    """
    Opens a file in read mode and returns the file object.

    :param str path: Path to the file.
    """
    if exist(path):
        file = open(path, 'r', errors="ignore", encoding=encoding)
        return file
    else:
        print(f"The file {path} does not exist")
        return False

# •••••••••••••••••••••••••••••••••••••••
def read(path, encoding='utf-8'):
    """
    Opens a file in read mode and returns its content as bytes/text.

    :param str path: Path to the file.
    """
    if exist(path):
        file = open_read(path, encoding=encoding)
        return file.read()
    else:
        print(f"The file {path} does not exist")
        return False

# •••••••••••••••••••••••••••••••••••••••
def write_check(path, data):
    """
    Writes to a file (overwriting) with existence check.

    :param str path: Path to the file.
    :param data: Data to write to the file.
    """
    if exist(path):
        file = open(path, 'w', encoding="utf-8")
        file.write(data)
        file.close()
        return True
    else:
        print(f"The file {path} does not exist")
        return False

# •••••••••••••••••••••••••••••••••••••••
def write(path, data, encoding='utf-8'):
    """
    Writes to a file (overwriting) without checking if the file exists.

    :param str path: Path to the file.
    :param data: Data to write to the file.
    """
    file = open(path, 'w', encoding=encoding)
    file.write(data)
    file.close()
    return True

# •••••••••••••••••••••••••••••••••••••••
def add(path, data, encoding='utf-8'):
    """
    Appends data to a file with existence check.

    :param str path: Path to the file.
    :param data: Data to append to the file.
    """
    if exist(path):
        file = open(path, 'a', encoding=encoding)
        file.write(data)
        file.close()
        return True
    else:
        print(f"The file {path} does not exist")
        return False

# •••••••••••••••••••••••••••••••••••••••
def replace(path, value, line: int, encoding='utf-8'):
    """
    Replaces a line in a file with existence check.

    :param str path: Path to the file.
    :param value: Data to replace in the file.
    """
    if exist(path):
        file = open(path, 'r', encoding=encoding)
        data = file.readlines()
        file.close()

        data[line] = value

        file = open(path, 'w', encoding=encoding) 
        file.writelines(data)
        file.close()
        return True
    else:
        print(f"The file {path} does not exist")
        return False

# •••••••••••••••••••••••••••••••••••••••
def replace_last(path, value, line: int = 1, encoding='utf-8'):
    """
    Replaces a line from the end in a file with existence check.

    :param str path: Path to the file.
    :param value: Data to replace in the file.
    """
    if exist(path):
        file = open(path, 'r', encoding=encoding)
        data = file.readlines()
        file.close()
        l = len(data)-line

        data[l] = value

        file = open(path, 'w', encoding=encoding) 
        file.writelines(data)
        file.close()
        return True
    else:
        print(f"The file {path} does not exist")
        return False

# •••••••••••••••••••••••••••••••••••••••
def check_in_line(path, value, line: int, encoding='utf-8'):
    """
    Checks if a value is present in a specific line of a file.
    """
    if exist(path):
        file = open(path, 'r', encoding=encoding)
        data = file.readlines()
        file.close()
        if value in data[line]:
            return True
        else:
            return False
    else:
        print(f"The file {path} does not exist")
        return False

# •••••••••••••••••••••••••••••••••••••••
def check_line(path, value, line: int, encoding='utf-8'):
    """
    Checks if a line in a file matches a value.
    """
    if exist(path):
        file = open(path, 'r', encoding=encoding)
        data = file.readlines()
        file.close()
        if value == data[line]:
            return True
        else:
            return False
    else:
        print(f"The file {path} does not exist")
        return False

# •••••••••••••••••••••••••••••••••••••••
def create(path, encoding='utf-8'):
    """
    Creates a file.

    :param str path: Path to the file.
    """
    file = open(path, 'w', encoding=encoding)
    file.close()
    return True

# •••••••••••••••••••••••••••••••••••••••
def delete(path):
    """
    Deletes a file with existence check.

    :param str path: Path to the file.
    """
    if exist(path):
        os.remove(path)
        return True
    else:
        print(f"Cannot delete file {path} because it does not exist")
        return False

# •••••••••••••••••••••••••••••••••••••••
def copy(source, destination):
    """
    Copies a file with existence check.

    :param str source: Path to the source file.
    :param str destination: Path to the destination file.
    """
    if exist(source):
        if not exist(destination):
            os.system(f'copy "{source}" "{destination}"')
            return True
        else:
            print(f"The file {destination} already exists")
            return False
    else:
        print(f"The file {source} does not exist")
        return False

# •••••••••••••••••••••••••••••••••••••••
# ••••••••••••• FOLDERS •••••••••••••••••
# •••••••••••••••••••••••••••••••••••••••
def createdir(path):
    """
    Creates a folder with existence check.

    :param str path: Path to the folder.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False

# •••••••••••••••••••••••••••••••••••••••
def listdirs(dirs, path):
    """
    Lists files and folders in the selected folder.

    :param str path: Path to the folder.
    """
    for file in os.listdir(path):
        d = os.path.join(path, file)
        if os.path.isdir(d):
            dirs.append(d)
            listdirs(dirs, d)
    return dirs

# •••••••••••••••••••••••••••••••••••••••
def currentdir():
    """
    Returns the current folder

    :return: Path to the current folder + Name of the current folder
    """
    # get the path of the current directory
    path = os.getcwd()
    # get the name of the current directory
    repn = os.path.basename(path)
    return path, repn

# •••••••••••••••••••••••••••••••••••••••
def copy_dir(source, destination):
    """
    Copies a folder with existence check.

    :param str source: Path to the source folder.
    :param str destination: Path to the destination folder.
    """
    if exist(source):
        if not exist(destination):
            os.system(f'xcopy "{source}" "{destination}" /E /I')
            return True
        else:
            print(f"The folder {destination} already exists")
            return False
    else:
        print(f"The folder {source} does not exist")
        return False

# •••••••••••••••••••••••••••••••••••••••
# ••••••••••••• JSON ••••••••••••••••••••
# •••••••••••••••••••••••••••••••••••••••
def json_read(path):
    """
    Reads a JSON file and returns the data as an object.

    :param str path: Path to the file.
    """
    if exist(path):
        file = open_read(path=path)
        data = json.load(file)
        file.close()
        return data
    else:
        print(f"The file {path} does not exist")
        return False
    
# •••••••••••••••••••••••••••••••••••••••
def json_write(path, data):
    """
    Writes to a JSON file (overwriting) with existence check.

    :param str path: Path to the file.
    :param data: Data to write to the file.
    """
    if exist(path):
        file = open(path, 'w', encoding='utf-8')
        json.dump(data, file, indent=4, ensure_ascii=False)
        file.close()
        return True
    else:
        print(f"The file {path} does not exist")
        return False

# •••••••••••••••••••••••••••••••••••••••
def json_loads(data):
    """
    Converts raw data to a JSON object.
    
    :param data: Data to format.
    """
    return json.loads(data)