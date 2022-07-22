import pathlib

def getDir(dir):
    return (pathlib.Path(__file__).parent / dir).__str__()

def getPath(dir, file):
    return (pathlib.Path(__file__).parent / dir / file).__str__()