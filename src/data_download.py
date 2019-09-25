import urllib
import pickle
import gzip
import struct
import os
import shutil
import traceback
import fnmatch
import numpy as np
import logging

class DatasetAccess(object):
    """
    Fetch the MNIST dataset through the link
    Classify the dataset into 10 files by digit types
    """
    def __init__(self, Path, dir, number):
        """
        :param Path: `str` the path for saving the MNIST dataset
        :param dir:  `str` the path for saving the produced images
        :param number: `str` the number we want, here for file making
        """
        self.path = Path
        self.dir = dir
        self.number = number
        self.type = os.path.join(self.path,"digit")

    def safe_mkdir(self):
        """ Create a directory if there isn't one already. """
        try:
            os.makedirs(self.type)
        except OSError:
            pass
        try:
            os.makedirs(self.dir)
        except OSError:
            pass
        try:
            file_path = os.path.join(self.dir, self.number)
            os.mkdir(file_path)
        except OSError:
            pass

    def download_one_file(self,
                          download_url,
                          local_dest,
                          expected_byte=None,
                          unzip_and_remove=False):
        """
        Download the file from download_url into local_dest
        if the file doesn't already exists.
        If expected_byte is provided, check if
        the downloaded file has the same number of bytes.
        If unzip_and_remove is True, unzip the file and remove the zip file
        """
        if os.path.exists(local_dest) or os.path.exists(local_dest[:-3]):
            logging.info('%s already exists' % local_dest)
        else:
            logging.info('Downloading %s' % download_url)
            local_file, _ = urllib.request.urlretrieve(download_url, local_dest)
            file_stat = os.stat(local_dest)
            if expected_byte:
                if file_stat.st_size == expected_byte:
                    logging.info('Successfully downloaded %s' % local_dest)
                    if unzip_and_remove:
                        with gzip.open(local_dest, 'rb') as f_in, open(local_dest[:-3], 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                        os.remove(local_dest)
                else:
                    logging.error('The downloaded file has unexpected number of bytes')

    def download_mnist(self):
        """
        Download and unzip the dataset mnist if it's not already downloaded
        Download from http://yann.lecun.com/exdb/mnist
        """
        url = 'http://yann.lecun.com/exdb/mnist/'
        filenames = ['train-images-idx3-ubyte.gz',
                     'train-labels-idx1-ubyte.gz',
                     't10k-images-idx3-ubyte.gz',
                     't10k-labels-idx1-ubyte.gz']
        expected_bytes = [9912422, 28881, 1648877, 4542]

        for filename, byte in zip(filenames, expected_bytes):
            download_url = url + filename
            local_dest = os.path.join(self.path, filename)
            self.download_one_file(download_url, local_dest, byte, True)

    def parse_data(self, dataset, flatten=False):
        """
        :param dataset: extract the data in th zip file
        :param flatten: data format, flatten or array
        :return: images and labels
        """
        if dataset != 'train' and dataset != 't10k':
            raise NameError('dataset must be train or t10k')

        label_file = os.path.join(self.path, dataset + '-labels-idx1-ubyte')
        with open(label_file, 'rb') as file:
            _, num = struct.unpack(">II", file.read(8))
            labels = np.fromfile(file, dtype=np.int8)  # int8

        img_file = os.path.join(self.path, dataset + '-images-idx3-ubyte')
        with open(img_file, 'rb') as file:
            _, num, rows, cols = struct.unpack(">IIII", file.read(16))
            imgs = np.fromfile(file, dtype=np.uint8).reshape(num, rows, cols)  # uint8
            imgs = imgs.astype(np.float32)
            if flatten:
                imgs = imgs.reshape([num, -1])

        return imgs, labels

    def check_dest(self, file):
        """
        Download the file from download_url into local_dest
        if the file doesn't already exists.
        If expected_byte is provided, check if
        the downloaded file has the same number of bytes.
        If unzip_and_remove is True, unzip the file and remove the zip file
        """
        local_path = os.path.join(self.type, file)
        if os.path.exists(local_path):
            logging.info('%s digit file already exists' % local_path)
        else:
            num = int(file.split('.')[0])
            image = []
            train_data, train_label = self.parse_data('train')
            test_data, test_label = self.parse_data('t10k')
            for data,label in zip(train_data,train_label):
                if label == num:
                    image += [data]

            for data,label in zip(test_data,test_label):
                if label == num:
                    image += [data]
            # print(image)
            with open(local_path, 'wb') as f:
                pickle.dump(image, f)
                f.close()

    def download(self):
        self.safe_mkdir()
        self.download_mnist()
        for i in range(10):
            file = "{0}.pk".format(i)
            self.check_dest(file)

    def read_mnist(self):
        """
        Read in the classified digits dataset in .pk files
        Return all the images from 0 to 9 as a list
        """
        image_set = []
        files = ['0.pk', '1.pk', '2.pk', '3.pk', '4.pk', '5.pk', '6.pk', '7.pk', '8.pk', '9.pk']
        for file in files:
            image_path = os.path.join(self.type, file)
            with open(image_path, 'rb') as f:
                data = pickle.load(f)
                image_set += [data]

        return image_set

    def get_mnist_dataset(self):
        """
        Step 1: download the MNIST dataset
        Step 2: read the dataset from the processed pickle file
        """
        self.download()
        dataset = self.read_mnist()

        return dataset