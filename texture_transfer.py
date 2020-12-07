from PIL import Image
from utils import load_image
from utils import get_mask
import numpy as np
path = './dataset/transfer/'

block_size = 20
overlap_size = 10
alpha = 0.1
tolerance = 0.01



def quilting(texture_image_name, transfer_image_name):
    texture_image = load_image(path+texture_image_name)
    transfer_image = load_image(path+transfer_image_name)
    [h, w, _] = texture_image.shape
    [out_x, out_y, g] = transfer_image.shape
    blocks = []
    result = np.ones([out_x, out_y, g])*-1

    for i in range(h-block_size+1):
        for j in range(w-block_size+1):
            blocks.append(texture_image[i:i+block_size, j:j+block_size, :])

    blocks = np.array(blocks)
    # fill first top left corner of result image with random block
    result[0:block_size, 0:block_size, :] = blocks[np.random.randint(len(blocks))]

    blocks_in_row = int(np.ceil( (out_x-block_size)/ (block_size-overlap_size) ) + 1)
    blocks_in_col = int(np.ceil( (out_y-block_size)/ (block_size-overlap_size) ) + 1)

    for i in range(blocks_in_row):
        for j in range(blocks_in_col):
            if i == 0 and j == 0:
                continue
            # start and end locations of pixels in result image to be filled
            start_i = i*(block_size-overlap_size)
            start_j = j*(block_size-overlap_size)
            end_i = min(start_i + block_size, out_x)
            end_j = min(start_j + block_size, out_y)

            curr_box_to_fill = result[start_i:end_i, start_j:end_j, :]
            target_block = transfer_image[start_i:end_i, start_j:end_j, :]

            best_block = compare_blocks(blocks, curr_box_to_fill, target_block, block_size, alpha, tolerance)

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

            print("Transfer for {name} {per:.2f}% complete...".format(name=transfer_image_name, per=completion))

    result = np.asarray(result, dtype=np.uint8)
    Image.fromarray(result).save(path+'results/'+texture_image_name.split('.')[0]+'_'+transfer_image_name.split('.')[0]+'_b='+str(block_size)+'_ov='+str(overlap_size)+'_a='+str(tolerance)+'.png')
    return Image.fromarray(result)


def compare_blocks(blocks, curr_box_to_fill, target_block, block_size, alpha, tolerance):
    errors = []
    [p, q, _] = curr_box_to_fill.shape

    for i in range(blocks.shape[0]):
        block_i = blocks[i, :, :, :]
        block_i = block_i[:p, :q, :]
        errors.append(ssd_error(block_i, curr_box_to_fill, target_block, alpha))

    min_err = np.min(errors)
    min_err_blocks = [block[:p, :q, :] for i, block in enumerate(blocks) if errors[i] <= (1.0+tolerance)*min_err]

    r = np.random.randint(len(min_err_blocks))
    return min_err_blocks[r]


def ssd_error(block_i, curr_box_to_fill, target_block, alpha):
    # here correspondance maps is taken to be luminance

    c = curr_box_to_fill
    lum_block_i = np.sum(block_i, axis=2)/3
    lum_c = np.sum(c, axis=2)/3
    lum_target_block = np.sum(target_block, axis=2)/3

    err1 = np.sum((lum_block_i - lum_c)*(lum_block_i - lum_c)*(lum_c != -1.0))
    err2 = np.sum((lum_block_i - lum_target_block)*(lum_block_i - lum_target_block)*(lum_c != -1.0))
    return alpha*np.sqrt(err1) + (1-alpha)*np.sqrt(err2)

if __name__ == "__main__":
    texture_image_name = input("Enter name of texture image present in dataset/transfer:    ")
    transfer_image_name = input("Enter name of transfer image present in dataset/transfer:  ")
    quilting(texture_image_name, transfer_image_name)