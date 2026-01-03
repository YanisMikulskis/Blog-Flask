import os

def check():
    if os.environ.get('IS_DOCKER') is None:
        return 0
    return 1

is_docker = check()

__all__ = [
    'is_docker'
]
