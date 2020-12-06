from os import listdir
from os.path import isfile, join
from quilting import quilting
path = './dataset/synthesis/'

test_images = [f for f in listdir(path) if isfile(join(path, f))]

for img in test_images:
    quilting(path+img, path+'results/'+img.split('.')[0]+'_b=60_ov=10_t=0.01.'+img.split('.')[1])
    