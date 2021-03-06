############################################################################################
#
# Project:       Peter Moss Leukemia Research Foundation
# Repository:    ALL-IDB Classifiers
# Project:       Tensorflow 2.0 ALL Papers
#
# Author:        Adam Milton-Barker (adammiltonbarker@leukemiaresearchfoundation.ai)
# Contributors:
#
# Title:         Paper 1 Data Helper Class
# Description:   Data helper class for the Paper 1 Evaluation.
# License:       MIT License
# Last Modified: 2019-12-28
#
############################################################################################

import cv2
import pathlib
import random
import os

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from pathlib import Path

from numpy.random import seed
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import shuffle
from scipy import ndimage
from skimage import transform as tm

from Classes.Helpers import Helpers


class Data():
    """ Data Class

    Data helper class for the Paper 1 Evaluation.
    """

    def __init__(self, model):
        """ Initializes the Data class. """

        self.Helpers = Helpers("Data", False)
        self.model_type = model

        seed(self.Helpers.confs[self.model_type]["data"]["seed"])
        tf.random.set_seed(self.Helpers.confs[self.model_type]["data"]["seed"])

        self.data = []
        self.labels = []

        self.Helpers.logger.info("Data class initialization complete.")

    def data_and_labels_sort(self):
        """ Sorts the training data and labels for your model. """

        data_dir = pathlib.Path(
            self.Helpers.confs[self.model_type]["data"]["train_dir"])
        data = list(data_dir.glob(
            '*' + self.Helpers.confs[self.model_type]["data"]["file_type"]))

        count = 0
        neg_count = 0
        pos_count = 0

        for rimage in data:
            fpath = str(rimage)
            fname = os.path.basename(rimage)

            if "_0" in fname:
                neg_count += 1
            else:
                pos_count += 1
            count += 1

            self.data.append((fpath, 0 if "_0" in fname else 1))
        
        random.Random(self.Helpers.confs[self.model_type]["data"]["seed"]).shuffle(self.data)

        self.Helpers.logger.info("All data: " + str(count))
        self.Helpers.logger.info("Positive data: " + str(pos_count))
        self.Helpers.logger.info("Negative data: " + str(neg_count))

    def data_and_labels_prepare(self):
        """ Prepares the training data for your model. """

        for i in range(len(self.data)):
            fpath = str(self.data[i][0])

            image = self.resize(
                fpath, self.Helpers.confs[self.model_type]["data"]["dim"])

            if image.shape[2] == 1:
                image = np.dstack(
                    [image, image, image])

            self.labels.append(self.data[i][1])
            self.data[i] = image.astype(np.float32)/255.

        self.convert_data()
        self.encode_labels()
        
        self.Helpers.logger.info("All data: " + str(self.data.shape))
        self.Helpers.logger.info("All Labels: " + str(self.labels.shape))

    def convert_data(self):
        """ Converts the training data to a numpy array. """

        self.data = np.array(self.data)
        self.Helpers.logger.info("Data shape: " + str(self.data.shape))

    def encode_labels(self):
        """ One Hot Encodes the labels. """

        encoder = OneHotEncoder(categories='auto')

        self.labels = np.reshape(self.labels, (-1, 1))
        self.labels = encoder.fit_transform(self.labels).toarray()
        self.Helpers.logger.info("Labels shape: " + str(self.labels.shape))

    def shuffle(self):
        """ Shuffles the data and labels. """

        self.data, self.labels = shuffle(self.data, self.labels,
                                         random_state=self.Helpers.confs[self.model_type]["data"]["seed"])

    def get_split(self):
        """ Splits the data and labels creating training and validation datasets. """

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.data, self.labels, test_size=0.255, random_state=self.Helpers.confs[self.model_type]["data"]["seed"])

        self.Helpers.logger.info("Training data: " + str(self.X_train.shape))
        self.Helpers.logger.info("Training labels: " + str(self.y_train.shape))
        self.Helpers.logger.info("Validation data: " + str(self.X_test.shape))
        self.Helpers.logger.info("Validation labels: " + str(self.y_test.shape))

    def resize(self, path, dim):
        """ Resizes an image to the provided dimensions (dim). """

        return cv2.resize(cv2.imread(path), (dim, dim))
