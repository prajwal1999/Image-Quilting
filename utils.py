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
    min_err_blocks_idx = []

    for i in range(blocks.shape[0]):
        [p, q, r] = curr_box_to_fill.shape
        block_i = blocks[i, :, :, :]
        block_i = block_i[0:p, 0:q, 0:r]
        errors.append(ssd_error(block_i, curr_box_to_fill))
    
    errors = np.array(errors)

    for i in range( int(np.ceil(blocks.shape[0]*threshold)) ):
        min_err_idx = np.argmin(errors)
        min_err_blocks_idx.append( min_err_idx )
        errors[min_err_idx] = float('inf')
        print(min_err_idx, np.min(errors))

    # we got best matching blocks indices in min_err_blocks_idx array
    temp_random = np.random.randint(len(min_err_blocks_idx))
    return blocks[min_err_blocks_idx[temp_random]]



