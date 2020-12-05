from PIL import Image
from utils import load_image
from utils import compare_block
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
import numpy as np

block_size = 28
overlap_size = 10
result_size = 500
threshold = 2

image = load_image(file_path='./dataset/synthesis/t19.png')
[r, c, g] = image.shape
blocks = []
result = np.ones([result_size, result_size, g])*-1

for i in range(r-block_size+1):
    for j in range(c-block_size+1):
        blocks.append(image[i:i+block_size, j:j+block_size, :])

blocks = np.array(blocks)
# fill first top left corner of result image with random block
result[0:block_size, 0:block_size, :] = blocks[np.random.randint(len(blocks))]
# img1 = Image.fromarray(blocks[np.random.randint(len(blocks))], 'RGB')
# img1.show()

blocks_in_row = np.ceil( (result_size-block_size)/ (block_size-overlap_size) ) + 1
blocks_in_row = int(blocks_in_row)
blocks_in_col = blocks_in_row

for i in range(blocks_in_row):
    if i != 1: continue
    for j in range(blocks_in_col):
        if j != 0: continue
        if i == 0 and j == 0:
            continue
        # start and end locations of pixels in result image to be filled
        if i==1 and j==0:
            start_x = i*(block_size-overlap_size)
            start_y = j*(block_size-overlap_size)
            end_x = min(start_x+(block_size-1), result_size-1)
            end_y = min(start_y+(block_size-1), result_size-1)

            curr_box_to_fill = result[start_x:end_x, start_y:end_y, :]
            matched_box = compare_block(blocks, curr_box_to_fill, block_size, threshold)