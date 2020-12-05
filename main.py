from os import listdir
from os.path import isfile, join

path = './dataset/synthesis'

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
print(onlyfiles)