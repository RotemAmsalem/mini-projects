from imageio import imread
import numpy as np
import scipy.ndimage
from skimage.color import rgb2gray
from . import sol5_utils
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, Activation, Add, Input
from tensorflow.keras.optimizers import Adam


def read_image(filename, representation):
    """
    this function reads an image file and converts it into a given representation (1 for
    grayscale representation and 2 for RGB representation).
    :param filename: the image file name
    :param representation: the representation the function converts the image to
    :return: the image at the given representation (1-grayscale, 2-RGB)
    """
    im = imread(filename)
    if representation == 1 and im.ndim == 3 and im.shape[2] == 3:
        im = rgb2gray(im)
    if im.dtype == np.uint8:
        im = im.astype(np.float64) / 255.0
    if im.dtype != np.float64:
        im = im.astype(np.float64)
    return im


def load_dataset(filenames, batch_size, corruption_func, crop_size):
    """
    This function builds a dataset of pairs of patches comprising (i) an original, clean and
    sharp, image patch with (ii) a corrupted version of same patch. Given a set of images,
    we will generate pairs of image patches on the fly, each time picking a random image,
    applying a random corruption 1 , and extracting a random patch 2.
    :param filenames: A list of file names of clean images.
    :param batch_size: The size of the batch of images for each iteration of Stochastic Gradient
    Descent.
    :param corruption_func: A function receiving a numpy’s array representation of an image as a
    single argument, and returns a randomly corrupted version of the input image.
    :param crop_size: A tuple (height, width) specifying the crop size of the patches to extract.
    :return: a Python’s generator object which outputs random tuples of the form (source_batch,
    target_batch),
    where each output variable is an array of shape (batch_size, height, width, 1), target_batch
    is made of clean
    images, and source_batch is their respective randomly corrupted version according to
    corruption_func(im)
    """
    height, width = crop_size
    im_dict = {}
    while True:
        target_batch = np.zeros((batch_size, height, width, 1), dtype=np.float64)
        source_batch = np.zeros((batch_size, height, width, 1), dtype=np.float64)
        for i in range(batch_size):
            im_name = np.random.choice(filenames)
            if im_name in im_dict:
                im = im_dict[im_name]
            else:
                im = read_image(im_name, 1)
                im_dict[im_name] = im
            ind1 = np.random.choice(im.shape[0] - width * 3)
            ind2 = np.random.choice(im.shape[1] - height * 3)
            cropped_im = im[ind1: ind1 + width * 3, ind2: ind2 + height * 3]
            corrupt_cropped_im = corruption_func(cropped_im)
            new_ind1 = np.random.choice(width * 2)
            new_ind2 = np.random.choice(height * 2)
            target_batch[i, :, :, 0] = cropped_im[new_ind1: new_ind1 + width,
                                       new_ind2: new_ind2 + height]
            source_batch[i, :, :, 0] = corrupt_cropped_im[new_ind1: new_ind1 + width,
                                       new_ind2: new_ind2 + height]
        yield (source_batch - 0.5, target_batch - 0.5)


def resblock(input_tensor, num_channels):
    """
    This function creates a residual block. It takes as input a symbolic input tensor and the
    number of channels for each of its convolutional layers, and returns the symbolic output
    tensor of the layer configuration describe above.
    :param input_tensor: a symbolic input tensor
    :param num_channels: the number of channels
    :return: symbolic output tensor
    """
    output_tensor = Conv2D(num_channels, (3, 3), padding="same")(input_tensor)
    output_tensor = Activation('relu')(output_tensor)
    output_tensor = Conv2D(num_channels, (3, 3), padding="same")(output_tensor)
    output_tensor = Add()([input_tensor, output_tensor])
    output_tensor = Activation('relu')(output_tensor)
    return output_tensor


def build_nn_model(height, width, num_channels, num_res_blocks):
    """
    This function should return an untrained Keras model, with input dimension the shape of
    (height, width, 1), and all convolutional layers (including resid-ual blocks) with number of
    output channels equal to num_channels, except the very last convolutional layer which should
    have a single output channel.
    :param height: the height of the input
    :param width: the width of the input
    :param num_channels: the number of channels
    :param num_res_blocks: The number of residual blocks
    :return: the complete neural network model
    """
    input_tensor = Input(shape=(height, width, 1))
    output_block = Conv2D(num_channels, (3, 3), padding="same")(input_tensor)
    output_block = Activation('relu')(output_block)
    for i in range(num_res_blocks):
        output_block = resblock(output_block, num_channels)
    output_tensor = Conv2D(1, (3, 3), padding="same")(output_block)
    output_tensor = Add()([input_tensor, output_tensor])
    model = Model(inputs=input_tensor, outputs=output_tensor)
    return model


def train_model(model, images, corruption_func, batch_size, steps_per_epoch, num_epochs,
                num_valid_samples):
    """
    This function divides the images into a training set and validation set, using an 80-20
    split, and generate from each set a dataset with the given batch size and corruption
    function (using the load_dataset function).
    :param model: a general neural network model for image restoration.
    :param images: a list of file paths pointing to image files. You should assume these paths
    are complete, and should append anything to them.
    :param corruption_func: A function receiving a numpy’s array representation of an image as a
    single argument, and returns a randomly corrupted version of the input image.
    :param batch_size: the size of the batch of examples for each iteration of SGD.
    :param steps_per_epoch: The number of update steps in each epoch.
    :param num_epochs: The number of epochs for which the optimization will run.
    :param num_valid_samples: The number of samples in the validation set to test on after every
    poch.
    :return:
    """
    num_of_images = len(images)
    training_set = images[0: int(0.8 * num_of_images)]
    validation_set = images[int(0.8 * num_of_images):]
    height, width = model.input_shape[1], model.input_shape[2]
    train_generator = load_dataset(training_set, batch_size, corruption_func, (height, width))
    valid_generator = load_dataset(validation_set, batch_size, corruption_func, (height, width))
    model.compile(loss="mean_squared_error", optimizer=Adam(beta_2=0.9))
    model.fit_generator(train_generator, steps_per_epoch=steps_per_epoch, epochs=num_epochs,
                        validation_data=valid_generator, validation_steps=num_valid_samples)


def restore_image(corrupted_image, base_model):
    """
    This function restores the corrupted image.
    :param corrupted_image: a grayscale image of shape (height, width) and with values in the
    [0, 1] range of type float64
    :param base_model: a neural network trained to restore small patches. The input and output of
    the network are images with values in the [−0.5, 0.5] range.
    :return: the restored image
    """
    corrupted_image -= 0.5
    a = Input(shape=(corrupted_image.shape[0], corrupted_image.shape[1], 1))
    b = base_model(a)
    new_model = Model(inputs=a, outputs=b)
    new_model.set_weights(base_model.get_weights())
    corrupted_image = corrupted_image[..., np.newaxis]
    restored_image = new_model.predict(corrupted_image[np.newaxis, ...])[0]
    restored_image += 0.5
    restored_image = restored_image.reshape(corrupted_image.shape[0], corrupted_image.shape[1])
    return restored_image.clip(0, 1).astype(np.float64)


def add_gaussian_noise(image, min_sigma, max_sigma):
    """
    This function randomly sample a value of sigma, uniformly distributed between min_sigma and
    max_sigma, followed by adding to every pixel of the input image a zero-mean gaussian random
    variable with standard deviation equal to sigma.
    :param image: a grayscale image with values in the [0, 1] range of type float64.
    :param min_sigma: a non-negative scalar value representing the minimal variance of the
    gaussian distribution.
    :param max_sigma: a non-negative scalar value larger than or equal to min_sigma,
    representing the maximal variance of the gaussian distribution.
    :return: the corrupted image (the image with the gaussian noise).
    """
    sigma = np.random.uniform(min_sigma, max_sigma)
    corrupted = np.random.normal(image, sigma, (image.shape[0], image.shape[1]))
    corrupted = np.round(corrupted * 255) / 255.0
    return corrupted.clip(0, 1).astype(np.float64)


def learn_denoising_model(num_res_blocks=5, quick_mode=False):
    """
     This function trains a network which expect patches of size 24×24 , using 48 channels for
     all but the last layer. The corruption we will use is a gaussian noise with sigma in the
     range [0, 0.2]. We use 100 images in a batch, 100 steps per epoch, 5 epochs overall and
     1000 samples for testing on the validation set. The above function has a single argument
     used solely for the presubmission phase. If quick_mode equals True, instead of the above
     arguments, we use only 10 images in a batch, 3 steps per epoch, just 2 epochs and only 30
     samples for the validation set.
    :param num_res_blocks: The number of residual blocks, its default value is 5
    :param quick_mode: an argument used solely for the presubmission phase, its default value is
    False
    :return: a trained denoising model
    """
    im_lst = sol5_utils.images_for_denoising()
    corruption_func = lambda im: add_gaussian_noise(im, 0, 0.2)
    model = build_nn_model(24, 24, 48, num_res_blocks)
    if not quick_mode:
        train_model(model, im_lst, corruption_func, 100, 100, 5, 1000 / 100)
    else:
        train_model(model, im_lst, corruption_func, 10, 3, 2, 30 / 10)
    return model


def add_motion_blur(image, kernel_size, angle):
    """
     This function simulates motion blur on the given image using a square kernel of size
     kernel_size where the line has the given angle in radians, measured relative to the positive
     horizontal axis.
    :param image: a grayscale image with values in the [0, 1] range of type float64.
    :param kernel_size: an odd integer specifying the size of the kernel (even integers are
    ill-defined).
    :param angle: an angle in radians in the range [0, π).
    :return: the corrupted image (the image with the motion blur).
    """
    kernel = sol5_utils.motion_blur_kernel(kernel_size, angle)
    corrupted = scipy.ndimage.filters.convolve(image, kernel)
    return corrupted


def random_motion_blur(image, list_of_kernel_sizes):
    """
    This function amples an angle at uniform from the range [0, π), and choses a kernel size at
    uniform from the list list_of_kernel_sizes, followed by applying the previous function with
    the given image and the randomly sampled parameters.
    :param image: a grayscale image with values in the [0, 1] range of type float64.
    :param list_of_kernel_sizes: a list of odd integers.
    :return: the corrupted image rounded to the nearest fraction i/255 and clipped to [0, 1].
    """
    angle = np.random.uniform(0, np.pi)
    kernel_size = np.random.choice(list_of_kernel_sizes)
    corrupted = add_motion_blur(image, kernel_size, angle)
    corrupted = np.round(corrupted * 255) / 255.0
    return corrupted.clip(0, 1).astype(np.float64)


def learn_deblurring_model(num_res_blocks=5, quick_mode=False):
    """
    This function trains a network which expect patches of size 16×16, and have 32 channels in
    all layers except the last. The dataset should use a random motion blur of kernel size equal
    to 7. We use 100 images in a batch, 100 steps per epoch, 10 epochs overall and 1000 samples
    for testing on the validation set. The above function has a single argument used solely for
    the presubmission phase. If quick_mode equals True, instead of the above arguments,
    we use only 10 images in a batch, 3 steps per epoch, just 2 epochs and only 30 samples for
    the validation set.
    :param num_res_blocks: the number of residual blocks, its default value is 5
    :param quick_mode: an argument used solely for the presubmission phase, its default value is
    False
    :return: a trained deblurring model
    """
    im_lst = sol5_utils.images_for_deblurring()
    corruption_func = lambda im: random_motion_blur(im, [7])
    model = build_nn_model(16, 16, 32, num_res_blocks)
    if not quick_mode:
        train_model(model, im_lst, corruption_func, 100, 100, 10, 1000 / 100)
    else:
        train_model(model, im_lst, corruption_func, 10, 3, 2, 30 / 10)
    return model
