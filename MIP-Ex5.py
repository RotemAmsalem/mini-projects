import matplotlib.pyplot as plt
import numpy as np
import utils
import cv2
from sklearn.metrics import mean_squared_error
from scipy.ndimage.filters import gaussian_filter
from skimage.feature import match_descriptors, ORB, canny
from skimage import morphology, measure, transform, segmentation, io, filters
from scipy import signal

BOTTOM_CAPTION = 1500  # the number on y axis of the caption in bottom of the image


def calcPointBasedReg(BLPoints, FUPoints):
    """
    The function finds a 3x3 rigidReg rigid 2D transformation matrix of the two translations and
    rotations of the given points and pairings
    we compute the matrix using the Single Value Decomposition (SVD) code provided in the
    exercise description.
    :param BLPoints: Baseline points
    :param FUPoints: Follow-up points
    :return: a 3x3 rigidReg rigid 2D transformation matrix of the two translations and
    rotations of the given points and pairings
    """
    # 1. Compute the weighted centroids of both point sets:
    BLPoints_centroid = BLPoints.mean(axis=0)
    FUPoints_centroid = FUPoints.mean(axis=0)

    # 2. Compute the centered vectors:
    centered_BLPoints = BLPoints - BLPoints_centroid
    centered_FUPoints = FUPoints - FUPoints_centroid

    # 3. Compute the d × d covariance matrix:
    X = centered_BLPoints.T
    W = np.eye(BLPoints.shape[0])  # I gave each point the same weight (=1)
    Y = centered_FUPoints
    XW = X @ W
    S = XW @ Y

    # 4. Compute the singular value decomposition:
    U, _, V = np.linalg.svd(S)
    sigma = np.eye(V.shape[1])
    sigma[-1, -1] = np.linalg.det(V @ U.T)
    sigma_Ut = sigma @ U.T
    R = V @ sigma_Ut

    # 5. Compute the optimal translation:
    t = -R @ BLPoints_centroid + FUPoints_centroid
    rigidReg = np.eye(3)
    rigidReg[:2, :2] = R
    rigidReg[:2, 2] = t
    return rigidReg


def calcDist(BLPoints, FUPoints, rigidReg):
    """
    This function computes the distance of each transformed point from its matching point in
    pixel units.
    :param BLPoints: Baseline points
    :param FUPoints: Follow-up points
    :param rigidReg: a 3x3 rigidReg rigid 2D transformation matrix of the two translations and
    rotations of the given points and pairings
    :return: a vector of length N represents the distance
    """
    rotation = rigidReg[:2, :2]
    translation = rigidReg[:2, 2:]
    transformation = np.dot(rotation, BLPoints.T) + translation
    distance = np.linalg.norm(transformation.T - FUPoints, axis=1)
    rmse = np.sqrt(mean_squared_error(FUPoints, transformation.T))
    # print("RMSE:", rmse)
    return distance


def calcRobustPointBasedReg(FUPoints, BLPoints):
    """
    this function computes the rigidREg and the inliers using the ransac function from utils
    :param FUPoints: Follow-Up points
    :param BLPoints: BaseLine points
    :return: rigidReg and indexes of the inliners
    """
    minPtNum = 4
    iterNum = 100
    thDist = 200
    thInlrRatio = 0.5
    rigidReg, inliers = utils.ransac(BLPoints, FUPoints, calcPointBasedReg, calcDist, minPtNum,
                                     iterNum, thDist, thInlrRatio)
    return rigidReg, inliers


def FindRetinaFeatures(Image):
    """
    this function finds strong features in the image to use for registration.
    :param Image: the images to find the features in
    :return:
    """
    Image = gaussian_filter(Image, 3)
    orb = ORB(n_keypoints=200)
    orb.detect_and_extract(Image)
    keypoints = orb.keypoints
    descriptors = orb.descriptors
    return keypoints, descriptors


def firstRegistrationAlgorithm(BL_Image, FU_Image):
    """
    this function register the images according to the first algorithm describes in the
    exercise's instructions
    :param BL_Image: base line image
    :param FU_Image: follow up image
    :return: the warped image
    """
    bl_im = io.imread(BL_Image, as_gray=True)[:BOTTOM_CAPTION, :]
    fu_im = io.imread(FU_Image, as_gray=True)[:BOTTOM_CAPTION, :]

    # Features detecting:
    BL_keypoints, BL_descriptors = FindRetinaFeatures(bl_im)
    FU_keypoints, FU_descriptors = FindRetinaFeatures(fu_im)

    # Features matching:
    matches = match_descriptors(BL_descriptors, FU_descriptors, cross_check=True)

    # Pick matched points:
    BLPoints, FUPoints = np.ones_like(BL_keypoints), np.ones_like(FU_keypoints)
    for i in range(2):
        BLPoints[:, i] = BL_keypoints[:, 1 - i]
        FUPoints[:, i] = FU_keypoints[:, 1 - i]
    rigidReg, inliers = calcRobustPointBasedReg(np.array(FUPoints[matches[:, 1]]),
                                                np.array(BLPoints[matches[:, 0]]))
    # Registration:
    warped_img = transform.warp(fu_im, rigidReg)
    new_image = np.zeros((bl_im.shape[0], bl_im.shape[1], 3))
    new_image[:, :, 0] = bl_im
    new_image[:, :, 1] = warped_img
    plt.imshow(new_image)
    plt.title("first registration algorithm for case" + str(BL_Image.split(".")[0][-1]))
    plt.show()
    return warped_img


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
    Image = filters.gaussian(Image)[:BOTTOM_CAPTION, :]
    th = 0.4
    blood_vessels = Image <= th
    Image[:] = 0
    Image[blood_vessels] = 1
    Image = findingBiggestComponent(Image)
    return Image


def secondRegistrationAlgorithm(BL_Image, FU_Image):
    """
    this function register the images according to the second algorithm describes in the
    exercise's instructions
    :param BL_Image: base line image
    :param FU_Image: follow up image
    :return: the warped image
    """
    bl_im = io.imread(BL_Image, as_gray=True)[:BOTTOM_CAPTION, :]
    fu_im = io.imread(FU_Image, as_gray=True)[:BOTTOM_CAPTION, :]
    bl_seg = SegmentBloodVessel(bl_im)
    fu_seg = SegmentBloodVessel(fu_im)

    max_angle = 0
    max_result = 0
    max_index = (0, 0)
    best_cross_correlation = None
    for angle in range(-10, 10):
        rotated_bl = transform.rotate(bl_seg, angle)
        cross_correlation = signal.correlate(rotated_bl, fu_seg)
        curr_result = np.max(cross_correlation)
        if curr_result > max_result:
            max_angle = angle
            max_result = curr_result
            max_index = np.where(cross_correlation == curr_result)[0][0], \
                        np.where(cross_correlation == curr_result)[1][0]
            best_cross_correlation = cross_correlation

    # Registration where the translation is the distance between the center of
    # the cross-correlation and the location of the maximal value in the cross-correlation:
    center = best_cross_correlation.shape[0] / 2, best_cross_correlation.shape[1] / 2
    max_angle = np.radians(max_angle)
    rigidReg = np.array([[np.cos(max_angle), np.sin(max_angle), center[1] - max_index[1]],
                         [-np.sin(max_angle), np.cos(max_angle), center[0] - max_index[0]],
                         [0, 0, 1]])

    warped_img = transform.warp(fu_im, rigidReg)
    new_image = np.zeros((bl_im.shape[0], bl_im.shape[1], 3))
    new_image[:, :, 0] = bl_im
    new_image[:, :, 1] = warped_img
    plt.imshow(new_image)
    plt.title("second registration algorithm for case" + str(BL_Image.split(".")[0][-1]))
    plt.show()
    return warped_img


def detectionAlgorithm(BL_Image, FU_Image):
    """
    this function detects the changes in the base line and follow up images
    :param BL_Image: base line image
    :param FU_Image: follow up image
    :return:
    """
    fu_im = io.imread(FU_Image, as_gray=True)[:BOTTOM_CAPTION, :]
    registered_bl = firstRegistrationAlgorithm(FU_Image, BL_Image)  # used for case3
    # registered_bl = secondRegistrationAlgorithm(FU_filename, BL_filename)  # used for case4

    # Normalize both images by columns:
    normalized_bl = registered_bl / np.amax(registered_bl)
    normalized_fu = fu_im / np.amax(fu_im)

    # Subtract FU from BL after registration:
    new_im = normalized_bl - normalized_fu
    above_zero = new_im > 0
    new_im[above_zero] = 0
    new_im = np.abs(new_im)

    fig = plt.figure()
    fig.add_subplot(221)
    plt.imshow(new_im, cmap='gray')
    plt.title("After stages 1-3")

    # remove some of the noise:
    th = 0.2
    above_th = new_im > th
    underneath_th = new_im <= th
    new_im[above_th] = 1
    new_im[underneath_th] = 0

    fig.add_subplot(222)
    plt.imshow(new_im, cmap='gray')
    plt.title("After stage 4")

    # clean noise touching the boundary:
    new_im = segmentation.clear_border(new_im)

    # remove small object:
    new_im = findingBiggestComponent(new_im)

    fig.add_subplot(223)
    plt.imshow(new_im, cmap='gray')
    plt.title("After stage 5-6")

    # Remove Blood Vessels:
    fu_seg = SegmentBloodVessel(fu_im)
    bl_seg = SegmentBloodVessel(registered_bl)
    new_im = np.bitwise_or(fu_seg, bl_seg).astype(int) - new_im
    new_im[new_im < 1] = 0

    fig.add_subplot(224)
    plt.imshow(new_im, cmap='gray')
    plt.title("After stage 7")
    plt.show()

    # Morphologically close:
    new_im = morphology.dilation(new_im)

    # Draw the borders/polygons:
    new_im = canny(new_im)
    new_im = morphology.dilation(new_im)

    fu_im[np.nonzero(new_im)] = 0
    registered_bl[np.nonzero(new_im)] = 0
    fig = plt.figure()
    fig.add_subplot(121)
    plt.imshow(fu_im, cmap='gray')
    plt.title("final output Follow-Up scan")

    fig.add_subplot(122)
    plt.imshow(registered_bl, cmap='gray')
    plt.title("final output Base-Line scan")
    plt.show()
