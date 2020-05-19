from imageio import imread
from skimage.color import rgb2gray
import numpy as np
import scipy.ndimage
import scipy.signal


def read_image(filename, representation):
    """
    this function reads an image file and converts it into a given representation (1 for
    grayscale representation and 2 for RGB representation).
    :param filename: the image file name
    :param representation: the representation the function converts the image to
    :return: the image at the given representation (1-grayscale, 2-RGB)
    """
    im = imread(filename).astype(np.float64)
    if representation == 1:
        im_g = rgb2gray(im)
        return im_g.astype(np.float64)
    elif representation == 2:
        im /= 255
        return im.astype(np.float64)
    else:
        print("Unexpected action")


def gausian_kernel(size):
    """
    this function computes the 2D gaussian kernel
    :param size: the size of the gaussian kernel in each dimension (an odd integer)
    :return: vector of filter and 2D gaussian kernel
    """
    mat = np.array([1, 1])
    row = np.array([1, 1])
    for i in range(size - 2):
        row = scipy.signal.convolve(row, mat)
    col = row.reshape(1, size)
    conv_mat = scipy.signal.convolve2d(row.reshape(size,1), col).astype(np.float64)
    sum = conv_mat.sum()
    g = (1 / sum) * conv_mat
    return g, col


def reduce(im, filter_vec):
    """
    this function blur the image and then sub-sample it
    :param im: a grayscale image with double values in [0, 1]
    :param filter_vec: a row vector of shape (1, filter_size) used for the pyramid construction
    :return: the reduced image
    """
    filter_mat = scipy.signal.convolve2d(filter_vec, filter_vec.T).astype(np.float64)
    new_im = scipy.ndimage.filters.convolve(im, filter_mat)
    new_im = scipy.ndimage.filters.convolve(new_im, filter_mat.T).astype(np.float64)
    return new_im[::2, ::2]


def build_gaussian_pyramid(im, max_levels, filter_size):
    """
    this function construct a Gaussian pyramid of a given image.
    :param im: a grayscale image with double values in [0, 1]
    :param max_levels: the maximal number of levels1 in the resulting pyramid
    :param filter_size: the size of the Gaussian filter (an odd scalar that represents a squared
    filter) to be used in constructing the pyramid filter
    :return: pyr - the resulting pyramid pyr as a standard python array with maximum length of
    max_levels, where each element of the array is a grayscale image and
    filter_vec - which is row vector of shape (1, filter_size) used for the pyramid construction
    """
    pyr = [im]
    filter_vec = gausian_kernel(filter_size)
    for i in range(max_levels - 1):
        im = reduce(im, filter_vec[0])
        pyr.append(im)
    return pyr, filter_vec[1]


def blur_spatial(im, filter_size):
    """
       this function blur the image
       :param im: a grayscale image with double values in [0, 1]
       :param filter_size: the size of the filter used for the pyramid construction
       :return: the blurred image
       """
    filter_vec = gausian_kernel(filter_size)[1]
    filter_mat = scipy.signal.convolve2d(filter_vec, filter_vec.T).astype(np.float64)
    new_im = scipy.ndimage.filters.convolve(im, filter_mat)
    return new_im.astype(np.float64)
