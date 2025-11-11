"""Module containing mechanism for calculating standard deviation between datasets.
"""

import glob
import os
import numpy as np

from inflammation import models, views

class JSONDataSource:
    """ Data class used to read inflammation data from JSON files in a directory. 
    :param data_dir: Directory containing inflammation JSON files.
    """
    
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
    
    def load_inflammation_data(self, file_identifier: str = 'inflammation*.json') -> list[np.ndarray]:
        """Loads all inflammation data JSON files from a directory.

        :param data_dir: Directory containing inflammation JSON files.
        :return: List of Numpy arrays with inflammation data.
        """
        data_file_paths = glob.glob(os.path.join(self.data_dir, file_identifier))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation data JSON files found in path {self.data_dir}")
        data = map(models.load_json, data_file_paths)
        flattened_data = []
        for dataset in data:
            flattened_data.extend(dataset)
        return flattened_data

class CSVDataSource:
    """ Data class used to read inflammation data from CSV files in a directory. 
    :param data_dir: Directory containing inflammation CSV files.
    """
    
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        
    def load_inflammation_data(self, file_identifier: str = 'inflammation*.csv') -> list[np.ndarray]:
        """Loads all inflammation data CSV files from a directory.

        :param data_dir: Directory containing inflammation CSV files.
        :return: List of Numpy arrays with inflammation data.
        """
        data_file_paths = glob.glob(os.path.join(self.data_dir, file_identifier))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation data CSV files found in path {self.data_dir}")
        data = map(models.load_csv, data_file_paths)
        return list(data) 


def analyse_data(data_source: CSVDataSource|JSONDataSource):
    """Calculates the standard deviation by day between datasets.

    Gets all the inflammation data from CSV files within a directory,
    works out the mean inflammation value for each day across all datasets,
    then plots the graphs of standard deviation of these means.
    """

    data = data_source.load_inflammation_data()


    means_by_day = map(models.daily_mean, data)
    means_by_day_matrix = np.stack(list(means_by_day))

    daily_standard_deviation = np.std(means_by_day_matrix, axis=0)

    graph_data = {
        'standard deviation by day': daily_standard_deviation,
    }
    views.visualize(graph_data)