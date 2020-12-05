from PIL import Image
import numpy as np

def load_image(file_path, mode='RGB'):
    img = Image.open(file_path).convert(mode)
    img_arr = np.asarray(img)
    return img_arr

def ssd_error(block_i, curr_box_to_fill):
    c = curr_box_to_fill
    return np.sum( (block_i - c)*(block_i - c)*((c+0.99)>0.1) )

def compare_block(blocks, curr_box_to_fill, block_size, threshold):

    errors = []

    for i in range(blocks.shape[0]):
        [p, q, r] = curr_box_to_fill.shape
        block_i = blocks[i, :, :, :]
        block_i = block_i[0:p, 0:q, 0:r]
        errors.append(ssd_error(block_i, curr_box_to_fill))
    print(errors)
    print(min(errors), max(errors))

