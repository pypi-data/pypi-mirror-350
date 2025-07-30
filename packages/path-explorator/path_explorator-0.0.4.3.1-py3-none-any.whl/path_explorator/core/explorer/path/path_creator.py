from pathlib import Path


class PathCreator:
    def __init__(self):
        pass
    
    def smart_path(self, *paths):
        if all(isinstance(path, str) for path in paths):
            pass

    def join_strlike_path(self, path1, path2):
        new_path = path1 / path2
        return new_path

    def join_strlike_path_to_pathliblike(self, path1, path2):
        new_path = Path(path1 / path2)
        return new_path

    def join_path(self, path1, path2):
        new_path = Path(path1 / path2)
        return new_path

