from os import listdir
from os.path import isfile, join
from quilting import quilting
path = './dataset/synthesis/'

test_images = [f for f in listdir(path) if isfile(join(path, f))]

for (index, img) in enumerate(test_images):
    quilting(img, path+'results/')
    print( str(index+1) +" out of "+str(len(test_images))+" done")
    
