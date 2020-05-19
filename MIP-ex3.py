import nibabel as nib
import numpy as np
from skimage import measure
from skimage import morphology
import copy

I_MIN = -500
I_MAX = 2000


def filterNoiseOnBiggestComponent(labels, lungs=0):
    """
    this function filtering the noise of the largest connectivity component
    :param labels: array of connectivity components
    :param lungs: int. 1- mean we segment the lungs and 0 means we are not
    :return: the biggest component without any noise
    """
    # Compute the largest connected component
    props = measure.regionprops(labels)
    max_component = 0
    for prop in props:
        if prop.area > max_component:
            max_component = prop.area

    # Filtering noise
    labels = morphology.remove_small_objects(labels, max_component)
    labels = morphology.binary_erosion(labels)
    if lungs:
        labels = morphology.remove_small_holes(labels, 10000000)  # I reached this number by
        # trying repeatedly until I found the maximal size of holes to be removed.
    labels = measure.label(labels)
    return labels


def IsolateBody(CT_Scan):
    """
    Isolate the patient’s body from the air and scan gantry by using the following algorithm:
    1. Perform thresholding to remove all pixels with gray level (HU) below -500 and above 2000
    (keep only those between -500 and 2000)
    2. Filter out noise
    3. Compute the largest connected component
    :param CT_Scan: a CT scan
    :return: Body segmentation
    """
    # Thresholding
    img = nib.load(CT_Scan)
    img_data = img.get_data()
    in_range_values_flags = (img_data >= I_MIN) & (img_data <= I_MAX)
    out_range_values_flags = (img_data < I_MIN) | (img_data > I_MAX)
    img_data[in_range_values_flags] = 1
    img_data[out_range_values_flags] = 0

    # filtering the noise from the biggest connectivity component
    labels = measure.label(img_data)
    labels = filterNoiseOnBiggestComponent(labels)
    img_data[labels == True] = 1
    img_data[labels == False] = 0

    scan_name = CT_Scan.split(".")[0]
    nib.save(img, scan_name + "_BodySeg.nii.gz")


def IsolateLungs(body_seg):
    """
    Isolate the lungs by finding the two large cavities inside the body segmentation which
    correspond to the lungs
    :param body_seg: body segmentation from IsolateBody
    :return:
    """
    seg = nib.load(body_seg)
    seg_data = seg.get_data()
    # finding the roi:
    sagittal, coronal, axial = np.nonzero(seg_data)
    min_sagittal, max_sagittal = np.amin(sagittal), np.amax(sagittal)
    min_coronal, max_coronal = np.amin(coronal), np.amax(coronal)
    min_axial, max_axial = np.amin(axial), np.amax(axial)
    one_values = seg_data == 1
    seg_data[:] = 0
    if body_seg.split("_")[0] == "Case3":
        seg_data[int(0.13 * (min_sagittal + max_sagittal)):int(0.87 * (min_sagittal +
                 max_sagittal)), int(2.82 *min_coronal):int(0.8 * max_coronal), int(0.6 * (
                  min_axial + max_axial)):int(0.95 * max_axial)] = 1
    else:
        seg_data[int(0.1 * (min_sagittal + max_sagittal)):int(0.9 * (min_sagittal + max_sagittal)),
                 min_coronal:max_coronal, int(0.6 * (min_axial + max_axial)):max_axial] = 1
    seg_data[one_values] = 0
    labels = measure.label(seg_data)
    labels = filterNoiseOnBiggestComponent(labels, 1)
    seg_data[labels == True] = 1
    seg_data[labels == False] = 0
    scan_name = body_seg.split("_")[0] + "_" + body_seg.split("_")[1]
    nib.save(seg, scan_name + "_LungsSeg.nii.gz")


def findingLiverROI(CT_scan, aorta_segmentation):
    """
    finding an ROI in the liver from which we can sample seeds for the MSRG.
    :param CT_scan: a CT scan
    :param aorta_segmentation: a segmentation of the aorta
    :return:
    """
    img = nib.load(CT_scan)
    img_data = img.get_data()
    IsolateBody(CT_scan)
    CT_scan_name = CT_scan.split(".")[0]
    IsolateLungs(CT_scan_name + "_BodySeg.nii.gz")

    lungs = nib.load(CT_scan_name + "_LungsSeg.nii.gz")
    lungs_data = lungs.get_data()

    # lungs's ROI:
    sagittal_lungs, coronal_lungs, axial_lungs = np.nonzero(lungs_data)
    min_sag_lungs, max_sag_lungs = np.amin(sagittal_lungs), np.amax(sagittal_lungs)
    min_cor_lungs, max_cor_lungs = np.amin(coronal_lungs), np.amax(coronal_lungs)
    min_ax_lungs, max_ax_lungs = np.amin(axial_lungs), np.amax(axial_lungs)

    aorta = nib.load(aorta_segmentation)
    aorta_data = aorta.get_data()

    # aorta's ROI:
    sagittal_aorta, coronal_aorta, axial_aorta = np.nonzero(aorta_data)
    min_sag_aorta, max_sag_aorta = np.amin(sagittal_aorta), np.amax(sagittal_aorta)
    min_cor_aorta, max_cor_aorta = np.amin(coronal_aorta), np.amax(coronal_aorta)
    min_ax_aorta, max_ax_aorta = np.amin(axial_aorta), np.amax(axial_aorta)

    # liver's ROI:
    img_data[:] = 0
    if CT_scan.split("_")[0] == "Case1" or CT_scan.split("_")[0] == "Case3":
        img_data[int(1.2 * min_sag_aorta):max_sag_lungs,
                 int(0.9 * min_cor_aorta):int(0.95 * max_cor_lungs),
                 int(1.4 * min_ax_aorta):int(0.7 * max_ax_lungs)] = 1
    else:
        img_data[int(1.2 * min_sag_aorta):max_sag_lungs,
                 int(0.7 * min_cor_aorta):int(0.95 * max_cor_lungs),
                 int(1 * min_ax_aorta):int(0.7 * max_ax_lungs)] = 1
    scan_name = CT_scan.split(".")[0]
    nib.save(img, scan_name + "_LiverROI.nii.gz")


def findSeeds(CT_scan, ROI):
    """
    this function samples seeds from ROI and returns seeds list
    :param CT_scan: a CT_scan
    :param ROI: a roi
    :return: seeds list
    """
    img = nib.load(CT_scan)
    img_data = img.get_data()
    roi_seg = nib.load(ROI)
    roi_seg_data = roi_seg.get_data()
    sagittal, coronal, axial = np.nonzero(roi_seg_data)
    seeds = []
    seeds_data = copy.deepcopy(img_data)
    seeds_data[:] = 0
    x = np.random.choice(sagittal, 200)
    y = np.random.choice(coronal, 200)
    z = np.random.choice(axial, 200)
    num_of_seeds = 0
    while num_of_seeds < 200:
        seed = x[num_of_seeds], y[num_of_seeds], z[num_of_seeds]
        if (img_data[seed] >= -100) & (img_data[seed] <= 200):
            seeds.append(seed)
            seeds_data[seed] = 1
        num_of_seeds += 1
    img_data[::] = seeds_data
    scan_name = CT_scan.split(".")[0]
    nib.save(img, scan_name + "_Seeds.nii.gz")
    return seeds


def cleanLiver(CT_scan):
    """
    this function cleans the liver segmentation and save it
    :param CT_scan: a CT scan
    :return:
    """
    scan_name = CT_scan.split(".")[0]
    seeds = nib.load(scan_name + "_LiverSegBeforeClean.nii.gz")
    seeds_data = seeds.get_data()
    labels, num1 = measure.label(seeds_data, return_num=True)

    # Filtering noise
    labels = morphology.remove_small_holes(labels, 100000000)  # I reached this number by trying
    # repeatedly until I found the maximal size of holes to be removed.
    labels = morphology.binary_erosion(labels)
    labels = morphology.binary_erosion(labels)
    labels = morphology.binary_erosion(labels)
    labels = morphology.binary_dilation(labels)
    labels, num2 = measure.label(labels, return_num=True)
    props = measure.regionprops(labels)
    max_component = 0
    for prop in props:
        if prop.area > max_component:
            max_component = prop.area
    labels = morphology.remove_small_objects(labels, max_component)
    seeds_data[labels == True] = 1
    seeds_data[labels == False] = 0
    nib.save(seeds, scan_name + "_LiverSeg.nii.gz")


def multipleSeedsRG(CT_scan, ROI):
    """
    this function preforms a liver segmentataion by using the following algorithm:
    1. Extract N seeds points inside the ROI.
    2. Perform Seeded Region Growing with N initial points
    :param CT_scan: a CT_scan
    :param ROI: ROI
    :return: Liver segmentation
    """
    img = nib.load(CT_scan)
    img_data = img.get_data()
    visit = np.zeros_like(img_data)

    # entering first neighbor:
    findSeeds(CT_scan, ROI)
    seeds_name = CT_scan.split(".")[0] + "_Seeds.nii.gz"
    seeds = nib.load(seeds_name)
    seeds_data = seeds.get_data()
    visit[seeds_data == 1] = 1
    cube = morphology.dilation(seeds_data, morphology.cube(3, np.uint8))
    neighbors = np.subtract(cube, seeds_data)
    neighbors[visit == 1] = 0
    visit[neighbors == 1] = 1

    num_of_iterations = 0
    while np.sum(neighbors) > 0 and num_of_iterations < 40:
        num_of_iterations += 1
        neighbors_only_values = np.zeros_like(img_data)
        neighbors_only_values[neighbors == 1] = img_data[neighbors == 1]  # the value of each
        # neighbor where there is one and 0 where there is no neighbor
        mean = np.mean(img_data[seeds_data == 1])  # the mean value of all values of all the seed
        # in the image
        seeds_data[np.absolute(np.subtract(mean, neighbors_only_values)) < 40] = 1

        # update neighbors:
        cube = morphology.dilation(seeds_data, morphology.cube(3, np.uint8))
        neighbors = np.subtract(cube, seeds_data)
        neighbors[visit == 1] = 0
        visit[neighbors == 1] = 1

    scan_name = CT_scan.split(".")[0]
    nib.save(seeds, scan_name + "_LiverSegBeforeClean.nii.gz")
    cleanLiver(CT_scan)


def evaluateSegmentation(GT_segmentation,est_segmentation):
    """
    this function evaluate my results versus the GT segmentations
    :param GT_segmentation: the ground truth segmentations:
    :param est_segmentation: my segmentation
    :return: Volume Overlap Difference and Dice Coefficient
    """
    gt_seg = nib.load(GT_segmentation)
    gt_seg_data = gt_seg.get_data()
    est_seg = nib.load(est_segmentation)
    est_seg_data = est_seg.get_data()

    # calculate the VOD_result and the DICE_result:
    norma_sum = np.sum(est_seg_data) + np.sum(gt_seg_data)
    intersection = np.sum(np.logical_and(est_seg_data, gt_seg_data))
    VOD_result = 1 - intersection / norma_sum
    DICE_result = 2 * intersection / norma_sum
    return VOD_result, DICE_result


def segmentLiver(CT_nifti_file_name, aorta_segmentation_name, output_file_name):
    """
    MSRG Liver Segmentation. this function saves liver segmentation nifti file (under the given
    name)
    :param CT_nifti_file_name: CT scan
    :param aorta_segmentation_name: aorta segmentation
    :param output_file_name: the name of the liver segmentation to be saved
    :return:
    """
    findingLiverROI(CT_nifti_file_name, aorta_segmentation_name)
    roi_name = CT_nifti_file_name.split(".")[0] + "_LiverROI.nii.gz"
    multipleSeedsRG(CT_nifti_file_name, roi_name)
    liver = nib.load(CT_nifti_file_name.split(".")[0] + "_LiverSeg.nii.gz")
    nib.save(liver, output_file_name)

