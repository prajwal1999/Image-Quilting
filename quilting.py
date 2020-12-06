from PIL import Image
from utils import load_image
from utils import compare_blocks, get_mask
import numpy as np
path = './dataset/synthesis/'

block_size = 100
overlap_size = 30
result_size = 400
threshold = 0.01

def quilting(image_name, result_path):
    image = load_image(path+image_name)
    [r, c, g] = image.shape
    blocks = []
    result = np.ones([result_size, result_size, g])*-1
    global block_size
    # pre work
    if r<block_size: block_size = 2*r//3

    for i in range(r-block_size+1):
        for j in range(c-block_size+1):
            blocks.append(image[i:i+block_size, j:j+block_size, :])

    blocks = np.array(blocks)
    # fill first top left corner of result image with random block
    result[0:block_size, 0:block_size, :] = blocks[np.random.randint(len(blocks))]

    blocks_in_row = np.ceil( (result_size-block_size)/ (block_size-overlap_size) ) + 1
    blocks_in_row = int(blocks_in_row)
    blocks_in_col = blocks_in_row

    for i in range(blocks_in_row):
        for j in range(blocks_in_col):
            if i == 0 and j == 0:
                continue
            # start and end locations of pixels in result image to be filled
            start_i = i*(block_size-overlap_size)
            start_j = j*(block_size-overlap_size)
            end_i = min(start_i + block_size, result_size)
            end_j = min(start_j + block_size, result_size)

            curr_box_to_fill = result[start_i:end_i, start_j:end_j, :]
            best_block = compare_blocks(blocks, curr_box_to_fill, block_size, threshold)

            if i==0:
                ov = curr_box_to_fill[:,:overlap_size,:]
                mask = get_mask(best_block, ov, None, 'v', overlap_size)
            elif j==0:
                ov = curr_box_to_fill[:overlap_size, :, :]
                mask = get_mask(best_block, None, ov, 'h', overlap_size)
            else:
                ov_v = curr_box_to_fill[:,:overlap_size,:]
                ov_h = curr_box_to_fill[:overlap_size, :, :]
                mask = get_mask(best_block, ov_v, ov_h, 'v+h', overlap_size)

            curr_box_to_fill = curr_box_to_fill*(mask==0)
            result[start_i:end_i, start_j:end_j, :] = curr_box_to_fill + best_block*(mask)

            completion = 100.0/blocks_in_row*(i + j*1.0/blocks_in_col)

            print("Synthesis for {name} {per:.2f}% complete...".format(name=image_name, per=completion))

    result = np.asarray(result, dtype=np.uint8)
    Image.fromarray(result).save(result_path+image_name.split('.')[0]+'_b='+str(block_size)+'_ov='+str(overlap_size)+'_t='+str(threshold)+'.'+image_name.split('.')[1])
    return Image.fromarray(result)
    print('Image saved')
