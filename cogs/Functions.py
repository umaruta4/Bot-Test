import os

def load_dir(client, path):
    extension_path = path.split("/")
    extension_path = ".".join(extension_path)
    for filename in os.listdir("./{}".format(path)):
        if filename.endswith('.py'):
            if filename[:-3] == '__init__':
                continue
            client.load_extension("{}.{}".format(extension_path, filename[:-3]))

def unload_dir(client, path):
    extension_path = path.split("/")
    extension_path = ".".join(extension_path)
    for filename in os.listdir("./{}".format(path)):
        if filename.endswith('.py'):
            if filename[:-3] == '__init__':
                continue
            client.unload_extension("{}.{}".format(extension_path, filename[:-3]))

def setup(client):
    pass
