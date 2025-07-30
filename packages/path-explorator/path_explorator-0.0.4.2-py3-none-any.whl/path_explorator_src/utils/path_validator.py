from ..exceptions import PathGoesBeyondLimits

def raise_if_path_goes_beyond_limits(limit_path: str, path: str):
    if not isinstance((limit_path, path), str):
        raise TypeError(f'limit path and path args must be str, got {type(limit_path)} and {type(path)} instead')
    if not path.startswith(limit_path):
        raise PathGoesBeyondLimits(path)
    return False