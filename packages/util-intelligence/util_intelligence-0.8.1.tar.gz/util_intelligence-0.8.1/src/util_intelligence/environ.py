import os


def resource(*args):
    root = os.environ.get('RESOURCE_ROOT', default='./resource')
    return os.path.join(root, *args)
