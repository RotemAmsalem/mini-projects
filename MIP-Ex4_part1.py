import imageio
import utils
from sklearn.metrics import mean_squared_error
from skimage.color import rgb2gray
from skimage import transform
import matplotlib.pyplot as plt
import numpy as np


def read_image(filename, representation):
    """
    this function reads an image file and converts it into a given representation (1 for
    grayscale representation and 2 for RGB representation).
    :param filename: the image file name
    :param representation: the representation the function converts the image to
    :return: the image at the given representation (1-grayscale, 2-RGB)
    """
    im = imageio.imread(filename)
    if representation == 1:
        im_g = rgb2gray(im)
        return im_g.astype(np.float64)
    elif representation == 2:
        im /= 255
        return im.astype(np.float64)
    else:
        print("Unexpected action")


def plotMatchPoints(inliers, with_or_without_outliers):
    """
    this function plots the matching points of the images
    :param inliers: the indexes of inliers
    :param with_or_without_outliers: either 'no_outliers' or 'with_outliers' according to the
    relevant section
    :return:
    """
    bl_im = read_image('BL01.tif', 1)
    fu_im = read_image('FU01.tif', 1)
    bl_points, fu_points = utils.getPoints(with_or_without_outliers)
    blend_im = np.hstack((bl_im, fu_im))
    plt.imshow(blend_im, cmap='gray')
    for i in range(len(bl_points)):
        x = [bl_points[:, 0][i], fu_points[:, 0][i] + bl_im.shape[1]]
        y = [bl_points[:, 1][i], fu_points[:, 1][i]]
        plt.plot(x, y, mfc='b', c='b', lw=1, ms=10, marker='.')
        if i in inliers:
            plt.plot(x, y, mfc='r', c='r', lw=1, ms=10, marker='.')
        plt.annotate("p" + str(i + 1), (x[0], y[0]))
        plt.annotate("p" + str(i + 1), (x[1], y[1]))
    plt.title("Matching points of BL01 and FU01")
    plt.show()
    return bl_points, fu_points


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
    print("RMSE:", rmse)
    return distance


def displayBothImages(with_or_without_outliers, section=4):
    """
    This function reads both images and get their sets of points with and without outliers and
    computes the rigid registration transformation between them, and applies it to the FU image.
    This function also computes a new image consisting of the transformed FU image overlaid on top
    of the BL image
    :param with_or_without_outliers: either 'eith_outliers' or 'no_outliers' according to the
    relevant section
    :param section: the relevant section 4 or 7 - so we will know how to compute the rigidReg.
    The default is 4 – compute rigidReg with the function calcPointBasedReg and is the section
    is 7 then we compute the rigidReg with the function calcRobustPointBasedReg
    :return: rigidReg and inliers - list of indexes of the inliers
    """
    bl_im = read_image('BL01.tif', 1)
    fu_im = read_image('FU01.tif', 1)
    BLPoints, FUPoints = utils.getPoints(with_or_without_outliers)
    inliers = []
    if section == 7:
        rigidReg, inliers = calcRobustPointBasedReg(FUPoints, BLPoints)  # according to section 7
    else:
        rigidReg = calcPointBasedReg(BLPoints, FUPoints)  # according to section 4
    warped_img = transform.warp(fu_im, rigidReg)
    new_image = np.zeros((bl_im.shape[0], bl_im.shape[1], 3))
    new_image[:, :, 0] = bl_im
    new_image[:, :, 1] = warped_img
    plt.imshow(new_image)
    plt.show()
    return rigidReg, inliers


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


def robustWithOutliers():
    """
    this function activate both "plotMatchPoints" from section 1 with "with_outliers" and
    "displayBothImages" from section 4 with "with_outliers" and with "calcRobustPointBasedReg" in
    order to compute the rigidReg.
    :return:
    """
    rigidReg, inliers = displayBothImages('with_outliers', 7)
    bl, fu = utils.getPoints('with_outliers')
    new_bl = bl[inliers]
    new_fu = fu[inliers]
    calcDist(new_bl, new_fu, rigidReg)
robustWithOutliers()