from pathlib import Path
from ....exceptions import EntityDoesNotExists, EntityIsNotADir
from ....core.explorer.path import PathCreator
from ....utils import cut_path


class DirectoryExplorer:
    def __init__(self, root_dir_abs_path: str):
        self.root_dir = self.__init_root_dir(root_dir_abs_path)
        self._path_creator = PathCreator()

    def __init_root_dir(self, root_dir_abs_path: str):
        if not isinstance(root_dir_abs_path, str):
            raise TypeError(f'root_dir_abs_path type must be str, not {type(root_dir_abs_path)}')
        root_dir = Path(root_dir_abs_path)

        if not root_dir.exists():
            raise EntityDoesNotExists(root_dir)

        return root_dir

    @property
    def root_path(self):
        return self.root_dir.__str__()

    def join_with_root_path(self, path: str):
        joined = self.root_dir.joinpath(Path(path)).__str__()
        return joined

    def get_all_filenames_in_dir(self, dirpath: str):
        """
        Returns names of all FILES in directory
        :param dirpath: directory getting files from
        :return: List of all files (strings) in specified directory
        """
        if not isinstance(dirpath, str):
            raise TypeError(f'dirpath arg must be str, not {type(dirpath)}')
        path = Path(self.root_dir, dirpath)
        if not path.exists():
            raise EntityDoesNotExists(dirpath)
        if not path.is_dir():
            raise EntityIsNotADir(dirpath)
        filenames = [cut_path(str(fname), str(self.root_dir)) for fname in path.iterdir() if fname.is_file()]
        return filenames

    def get_all_entitynames_in_dir(self, dirpath: str):
        """
        Returns all ENTITIES names (entity = any file, folder)
        :param dirpath: directory getting entities from
        :return: list of all entities names (strings) in specified directory
        """
        if not isinstance(dirpath, str):
            raise TypeError(f'dirpath arg must be str, not {type(dirpath)}')
        path = Path(self.root_dir, dirpath)
        if not path.exists():
            raise EntityDoesNotExists(dirpath)
        if not path.is_dir():
            raise EntityIsNotADir(dirpath)
        entities_names = [cut_path(str(entity), str(self.root_dir)) for entity in path.iterdir()]
        return entities_names

    def find_entities_path(self, searching_in: str, pattern: str ) -> list[str]:
        """
        Return list with paths of entity or entities that match a given pattern
        :param searching_in: path to directory in which to find
        :param pattern: pattern of entity name you need to find (example "fname.txt", "*.txt")
        :return: List with absolute paths (Path objects) or None
        """
        if not isinstance(searching_in, str):
            raise TypeError(f'searching_in arg must be str, not {type(searching_in)}')
        if not isinstance(pattern, str):
            raise  TypeError(f'pattern arg must be str, not {type(pattern)}')
        searchable_dir = Path(self.root_dir, searching_in)
        paths = [cut_path(str(path), str(self.root_dir)) for path in searchable_dir.rglob(pattern)]
        return paths

    def is_exists(self, path: str) -> bool:
        """
        Checks if specified path exists
        :param path: path to the entity checking
        :return: exists or not True or False
        """
        if not isinstance(path, str):
            raise TypeError(f'path arg must be str, not {type(path)}')
        entity = Path(self.root_dir, path)
        return entity.exists()
    
    def is_file(self, path:str) -> bool:
        """
        Checks if specified entity is FILE
        :param path: path to entity
        :return: file or not
        """
        if not isinstance(path, str):
            raise TypeError(f'path arg must be str, not {type(path)}')
        entity = Path(self.root_dir, path)
        return entity.is_file()
        
    def is_dir(self, path:str) -> bool:
        """
        Checks if specified entity is DIRECTORY/FOLDER
        :param path: path to entity
        :return: dir or not
        """
        if not isinstance(path, str):
            raise TypeError(f'path arg must be str, not {type(path)}')
        entity = Path(self.root_dir, path)
        return entity.is_dir()

    def get_name(self, path: str) -> str:
        """
        Get name of entity from strlike path
        :param path: strlike path
        :return: str name of entity (example /home/user/hello.txt  will return hello.txt)
        """
        if not isinstance(path, str):
            raise TypeError(f'path arg must be str, not {type(path)}')
        entity_path = Path(self.root_dir, path)
        return entity_path.name



