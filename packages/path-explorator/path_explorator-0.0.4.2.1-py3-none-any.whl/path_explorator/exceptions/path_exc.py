class PathGoesBeyondLimits(Exception):
    def __init__(self, path):
        msg = f'path {path} goes beyond permitted limits'
        super().__str__(msg)