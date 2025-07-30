def cut_path(orig:str, cutting: str) -> str:
    cut = orig.removeprefix(cutting)
    return cut