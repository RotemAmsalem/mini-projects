from skimage import measure
from skimage import morphology
import matplotlib.pyplot as plt
import imageio
from skimage.color import rgb2gray
import numpy as np
from skimage.feature import ORB


BOTTOM_CAPTION = 1500  # the number on y axis of the caption in bottom of the image


def read_image(filename, representation):
    """
    this function reads an image file and converts it into a given representation (1 for
    grayscale representation and 2 for RGB representation).
    :param filename: the image file name
    :param representation: the representation the function converts the image to
    :return: the image at the given representation (1-grayscale, 2-RGB)
    """
    im = imageio.imread(filename)
    im = im.astype(np.float64)
    if representation == 1 and im.ndim == 3:
        im = rgb2gray(im)
    return im


def findingBiggestComponent(Image):
    """
     this function filtering the noise of the largest connectivity component
    :param Image: the image to reduce to its biggest component
    :return: the biggest component of the image without any noise
    """
    labels = measure.label(Image)
    props = measure.regionprops(labels)
    max_component = 0
    for prop in props:
        if prop.area > max_component:
            max_component = prop.area
    labels = morphology.remove_small_objects(labels, max_component)
    labels = measure.label(labels)
    return labels


def SegmentBloodVessel(Image):
    """
    this function performs segmentation of the blood vessels in the retina.
    :param Image: the image to perform the segmentation on
    :return: the segmentation of the blood vessels
    """
    Image = read_image(Image, 1)
    thresholding = 100  # I checked some options until I got the TH that shows the blood vessels
    # in 2 other cases. 115 worked much better for BL01 and BL03 but not for the others so I
    # compromised on 100 so it will work for BL02 too.
    vessels = Image <= thresholding
    Image[:] = 0
    Image[vessels] = 1
    Image = findingBiggestComponent(Image)
    plt.imshow(Image, cmap='gray')
    plt.ylim(BOTTOM_CAPTION, 0)  # removing the caption at the bottom
    plt.title("Blood Vessels Segmentation")
    plt.show()
    return Image


def FindRetinaFeatures(Image):
    """
    this function finds strong features in the image to use for registration.
    :param Image: the images to find the features in
    :return:
    """
    Image = read_image(Image, 1)
    plt.imshow(Image, cmap='gray')
    orb = ORB(n_keypoints=50, harris_k=20)
    orb.detect_and_extract(Image)
    key_points = orb.keypoints
    plt.scatter(key_points[:, 0], key_points[:, 1])
    plt.ylim(BOTTOM_CAPTION, 0)  # removing the caption at the bottom
    plt.title("Retina Features")
    plt.show()
