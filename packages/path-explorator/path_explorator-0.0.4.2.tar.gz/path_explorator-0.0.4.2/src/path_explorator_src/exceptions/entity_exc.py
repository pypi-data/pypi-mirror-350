class EntityDoesNotExists(Exception):
    def __init__(self, entity_path):
        msg = f"File or directory does not exists at {entity_path}"
        super().__init__(msg)

class EntityIsNotADir(Exception):
    def __init__(self, entity_path):
        msg = f'Entity at {entity_path} is not a directory'
        super().__init__(msg)
