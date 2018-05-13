from os import makedirs, path


def ensure_dir_exist(file):
    dirs = path.dirname(file)
    if not path.exists(dirs):
        makedirs(dirs)


__all__ = ['ensure_dir_exist', 'conffor', 'csvtor']
