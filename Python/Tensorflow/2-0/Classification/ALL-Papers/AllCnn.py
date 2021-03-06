############################################################################################
#
# Project:       Peter Moss Leukemia Research Foundation
# Repository:    ALL-IDB Classifiers
# Project:       Tensorflow 2.0 ALL Papers
#
# Author:        Adam Milton-Barker (adammiltonbarker@leukemiaresearchfoundation.ai)
# Contributors:
#
# Title:         AllCnn Wrapper Class
# Description:   Core AllCnn wrapper class for the Tensorflow 2.0 ALL Papers project.
# License:       MIT License
# Last Modified: 2019-12-28
#
############################################################################################

import sys

from Classes.Helpers import Helpers
from Classes.DataP1 import Data as DataP1
from Classes.ModelP1 import Model as ModelP1


class AllCnn():
    """ ALL Papers AllCnn Wrapper Class

    Core AllCnn wrapper class for the Tensorflow 2.0 ALL Papers project.
    """

    def __init__(self):

        self.Helpers = Helpers("Core")

    def paper_1(self):

        self.DataP1 = DataP1(self.model_type)
        self.DataP1.data_and_labels_sort()
        self.DataP1.data_and_labels_prepare()
        self.DataP1.shuffle()
        self.DataP1.get_split()

        self.ModelP1 = ModelP1(self.model_type)
        self.ModelP1.build_network(self.DataP1.X_train.shape[1:])

        self.ModelP1.compile_and_train(self.DataP1.X_train, self.DataP1.X_test,
                                        self.DataP1.y_train, self.DataP1.y_test)
        
        self.ModelP1.save_model_as_json()
        self.ModelP1.save_weights()

        self.ModelP1.predictions(self.DataP1.X_train, self.DataP1.X_test)
        self.ModelP1.evaluate_model(self.DataP1.X_test, self.DataP1.y_test, self.DataP1.y_train)
        self.ModelP1.plot_metrics()
        
        self.ModelP1.confusion_matrix(self.DataP1.y_test)
        self.ModelP1.figures_of_merit(self.DataP1.X_test)


AllCnn = AllCnn()


def main():
    if sys.argv[1] is '1':
        AllCnn.model_type = "model_1"
        AllCnn.paper_1()
    elif sys.argv[1] is '2':
        AllCnn.model_type = "model_2"


if __name__ == "__main__":
    main()
