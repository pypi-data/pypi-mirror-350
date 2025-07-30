# •••••••••••••••••••••••••••••••••••••••
def replace_all(msg, source, destination):
    if type(msg) is dict:
        for k in msg.keys():
            if type(msg[k]) is str:
                msg[k] = msg[k].replace(source, destination)
            else:
                replace_all(msg[k], source, destination)
    elif type(msg) is list:
        for x in range(0, len(msg)):
            if type(msg[x]) is str:
                msg[x] = msg[x].replace(source, destination)
            else:
                replace_all(msg[x], source, destination)
    elif type(msg) is str:
        msg = msg.replace(source, destination)
    return msg

# •••••••••••••••••••••••••••••••••••••••
def replace_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

# •••••••••••••••••••••••••••••••••••••••
# Mse en forme d'un lien Windows en lien WSL
def link_to_wsl(path, defaultpath = ''):
    if path is None:
        path = input()
        if path == '':
            path = defaultpath
    if ':\\' in path:
        splitMap = path.split(':')
        path = replace_all(path, f'{splitMap[0]}:', splitMap[0].lower())
        path = f'/mnt/{path}'
    if '\\' in path:
        path = replace_all(path, '\\', '/')
    if path[-1:] == '/':
        path = path[:-1]
    return path