from PIL import Image
import numpy as np

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


def load_image(file_path, mode='RGB'):
    img = Image.open(file_path).convert(mode)
    img_arr = np.asarray(img)
    return img_arr


def ssd_error(block_i, curr_box_to_fill):
    c = curr_box_to_fill
    return np.sum( (block_i - c)*(block_i - c)*(c != -1) )


def compare_blocks(blocks, curr_box_to_fill, block_size, tolerance):

    errors = []
    # min_err_blocks_idx = []
    [p, q, _] = curr_box_to_fill.shape

    for i in range(blocks.shape[0]):
        block_i = blocks[i, :, :, :]
        block_i = block_i[:p, :q, :]
        errors.append(ssd_error(block_i, curr_box_to_fill))
    
    # errors = np.array(errors)

    # for i in range( int(np.ceil(blocks.shape[0]*tolerance)) ):
    #     min_err_idx = np.argmin(errors)
    #     min_err_blocks_idx.append( min_err_idx )
    #     errors[min_err_idx] = float('inf')
    #     # print(min_err_idx, np.min(errors))

    # randomly select a 
    # temp_random = np.random.randint(len(min_err_blocks_idx))

    min_err = np.min(errors)
    min_err_blocks = [block[:p, :q, :] for i, block in enumerate(blocks) if errors[i] <= (1.0+tolerance)*min_err]

    r = np.random.randint(len(min_err_blocks))
    return min_err_blocks[r]
    # return blocks[min_err_blocks_idx[temp_random], :p, :q, :]


def get_path(err):
    mask = np.zeros(err.shape)
    [r, c] = err.shape
    for i in range(1, r):
        err[i, 0] = err[i, 0] + min(err[i-1, 0], err[i-1, 1])
        err[i, c-1] = err[i, c-1] + min(err[i-1, c-1], err[i-1, c-2])
        for j in range(1, c-1):
            err[i, j] = err[i, j] + min(err[i-1, j], err[i-1, j-1], err[i-1, j+1])

    min_indices = [0]*r
    min_indices[-1] = np.argmin(err[r-1])

    for i in range(r-2, -1, -1):
        lb = max(min_indices[i+1] - 1, 0)
        ub = min(lb + 3, c)
        min_indices[i] = lb + np.argmin(err[i, lb:ub])

    for i in range(r):
        mask[i, min_indices[i]: ] = 1

    return mask


def get_mask(block, ov_v, ov_h, ov_type, overlap_size):
    
    block = rgb2gray(block)

    mask = np.ones(block.shape)

    if ov_type == 'v':
        ov_v = rgb2gray(ov_v)
        err = np.power(block[:, :overlap_size] - ov_v, 2)
        mask[:, :overlap_size] = get_path(err)

    elif ov_type == 'h':
        ov_h = rgb2gray(ov_h)
        err = np.power(block[:overlap_size, :] - ov_h, 2).transpose()
        mask[:overlap_size, :] = get_path(err).transpose()

    elif ov_type == 'v+h':
        ov_v = rgb2gray(ov_v)
        err = np.power(block[:, :overlap_size] - ov_v, 2)
        mask[:, :overlap_size] = get_path(err)

        ov_h = rgb2gray(ov_h)
        err = np.power(block[:overlap_size, :] - ov_h, 2).transpose()
        mask[:overlap_size, :] = mask[:overlap_size, :]*(get_path(err).transpose())

    mask = np.repeat(np.expand_dims(mask,axis=2),3,axis=2)
    return mask

