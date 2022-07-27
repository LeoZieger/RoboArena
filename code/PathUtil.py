import pathlib


# returns the absolute path to a folder within the code directory
def getDir(dir):
    return (pathlib.Path(__file__).parent / dir).__str__()


# returns the absolute path to a file within a folder within the code directory
def getPath(dir, file):
    return (pathlib.Path(__file__).parent / dir / file).__str__()
