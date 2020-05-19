import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import skimage.measure
import skimage.morphology
import scipy.signal


def SegmentationByTH(nifty_file, Imin, Imax):
    img = nib.load(nifty_file)
    img_data = img.get_data()
    in_range_values_flags = (img_data > Imin) & (img_data < Imax)
    out_range_values_flags = (img_data <= Imin) | (img_data >= Imax)
    img_data[in_range_values_flags] = 1
    img_data[out_range_values_flags] = 0
    nifty_file_name = nifty_file.split(".")[0]
    nib.save(img, nifty_file_name + "_seg_" + str(Imin) + "_" + str(Imax) + ".nii.gz")
    if nifty_file.endswith('.nii.gz'):
        return 1
    return 0


def downTo1ConnectivityComponent(nifty_file_name, segmentation, aorta, has_been_erosion=False):
    seg_img = nib.load(segmentation)
    seg_img_data = seg_img.get_data()
    labels, num_of_components = skimage.measure.label(seg_img_data, return_num=True)
    min_size = 50000
    enlarge_min_size = 1000
    if aorta == 1:
        min_size = 500
        enlarge_min_size = 100
    while num_of_components > 1:
        min_size += enlarge_min_size
        labels = skimage.morphology.remove_small_objects(labels, min_size)
        labels, num_of_components = skimage.measure.label(labels, return_num=True)
        if (aorta == 1) and (num_of_components == 1) and (not has_been_erosion):
            labels = skimage.morphology.binary_erosion(labels)
            if num_of_components > 1:
                labels, num_of_components = skimage.measure.label(labels, return_num=True)
    labels, num_of_components = skimage.measure.label(labels, return_num=True)
    if num_of_components == 0:
        downTo1ConnectivityComponent(nifty_file_name, segmentation, aorta, True)
    labels = skimage.morphology.dilation(labels)
    labels = skimage.morphology.binary_dilation(labels)
    seg_img_data[labels == True] = 1
    seg_img_data[labels == False] = 0
    if aorta == 0:
        nib.save(seg_img, nifty_file_name + "_SkeletonSegmentation.nii.gz")
    if aorta == 1:
        nib.save(seg_img, nifty_file_name + "_AortaSegmentation.nii.gz")


def SkeletonTHFinder(nifty_file):
    Imax = 1300
    Imin = 150
    SegmentationByTH(nifty_file, Imin, Imax)
    nifty_file_name = nifty_file.split(".")[0]
    connectivity_components = []
    Imins = []
    nifty_seg_files = []
    while Imin < 500:
        Imins.append(Imin)
        SegmentationByTH(nifty_file, Imin, Imax)
        img = nib.load(nifty_file_name + "_seg_" + str(Imin) + "_" + str(Imax) + ".nii.gz")
        img_data = img.get_data()
        nifty_seg_files.append(img)
        num_of_components = skimage.measure.label(img_data, return_num=True)[1]
        connectivity_components.append(num_of_components)
        Imin += 14
    plt.plot(Imins, connectivity_components)
    plt.title("Number of Connectivity Components per Imin")
    plt.xlabel("Imin")
    plt.ylabel("number of connectivity components")
    plt.show()
    minima_index = scipy.signal.argrelextrema(np.array(connectivity_components), np.less)[0][0]
    img_name = nifty_file_name + "_seg_" + str(Imins[minima_index]) + "_" + str(Imax) + ".nii.gz"
    downTo1ConnectivityComponent(nifty_file_name, img_name, 0)
    return Imins[minima_index]


def AortaSegmentation (nifty_file, L1_seg_nifti_file):
    img = nib.load(nifty_file)
    img_data = img.get_data()
    seg = nib.load(L1_seg_nifti_file)
    seg_data = seg.get_data()

    # finding L1's ROI:
    sagittal_plane, coronal_plane, axial_plane = np.nonzero(seg_data)
    min_sagittal, max_sagittal = np.min(sagittal_plane), np.max(sagittal_plane)
    min_coronal, max_coronal = np.min(coronal_plane), np.max(coronal_plane)
    min_axial, max_axial = np.min(axial_plane), np.max(axial_plane)
    sagittal_middle = int((max_sagittal - min_sagittal) / 2)
    coronal_middle = int((max_coronal - min_coronal) / 2)

    # calculating a box around L1:
    box_min_x = min_sagittal + np.int(0.25 * sagittal_middle)
    box_max_x = max_sagittal - sagittal_middle
    box_min_y = min_coronal - np.int(0.75 * coronal_middle)
    box_max_y = max_coronal - 2 * coronal_middle
    box_min_z = min_axial
    box_max_z = max_axial

    # calculating histogram and finding the image inside the box:
    new_img_data = img_data[box_min_x:box_max_x, box_min_y:box_max_y, box_min_z:box_max_z]
    histogram = np.histogram(new_img_data, 256, [0, 256])[0]
    # peak_index = scipy.signal.argrelextrema(np.array(histogram), np.greater)[0][0]
    peak_index = np.argmax(histogram)

    plt.plot(histogram)
    plt.show()

    # turning into binary image according to the thresholding:
    out_indices = (img_data <= (peak_index - 20)) | (img_data >= (peak_index + 20))
    img_data[:] = 0
    img_data[box_min_x:box_max_x, min_coronal - np.int(0.625 * coronal_middle):box_max_y,
             box_min_z:box_max_z] = 1
    img_data[out_indices] = 0

    # saving the image and downloading to 1 connectivity component:
    nifty_file_name = nifty_file.split(".")[0]
    img_name = nifty_file_name + "_Aorta_Seg_.nii.gz"
    nib.save(img, img_name)
    downTo1ConnectivityComponent(nifty_file_name, img_name, 1)


def evaluateSegmentation(GT_seg, est_seg):
    gt_img = nib.load(GT_seg)
    gt_img_data = gt_img.get_data()
    est_img = nib.load(est_seg)
    est_img_data = est_img.get_data()

    # finding ROI and crop the image according to that:
    sagittal_plane, coronal_plane, axial_plane = np.nonzero(est_img_data)
    low_values_flag = gt_img_data < 1
    gt_img_data[:] = 0
    gt_img_data[np.amin(sagittal_plane):np.amax(sagittal_plane), np.amin(coronal_plane):np.amax(
        coronal_plane), np.amin(axial_plane):np.amax(axial_plane)] = 1
    gt_img_data[low_values_flag] = 0

    # calculate the VOD_result and the DICE_result:
    union = np.sum(np.logical_or(est_img_data, gt_img_data))
    intersection = np.sum(np.logical_and(est_img_data, gt_img_data))
    VOD_result = 1 - intersection / union
    DICE_result = 2 * intersection / union
    return VOD_result, DICE_result

AortaSegmentation("Case1_CT.nii.gz", "Case1_L1.nii.gz")