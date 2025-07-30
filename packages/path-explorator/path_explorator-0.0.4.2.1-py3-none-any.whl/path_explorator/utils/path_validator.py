from ..exceptions import PathGoesBeyondLimits

def raise_if_path_goes_beyond_limits(limit_path: str, path: str):
    if not isinstance(limit_path, str):
        raise TypeError(f'limit path arg must be str, not {type(limit_path)}')
    if not isinstance(path, str):
        raise TypeError(f'path arg must be str, not {type(limit_path)}')
    if not path.startswith(limit_path):
        raise PathGoesBeyondLimits(path)
    return False