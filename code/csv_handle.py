import pandas as pd
import numpy as np
import csv


class csvHandle:

    def __init__(self, path: str):
        """
        Creates an object that allows for all the needed interaction with the csv file
        Path is the path to the csv file
        """
        self.path = path

    def add_row(self, label: int, right_hand: bool, landmarks: list[float]) -> None:
        """
        Adds a new row to the csv file
        The format of each row is:
        [label: int, right_hand: int, landmark_0, landmark_1, ..., landmark_41]
        """
        hand = 1 if right_hand else 0
        data = [label] + [hand] + landmarks

        with open(self.path, 'a') as f: 
            writer = csv.writer(f)
            writer.writerow(data)

    def prepare_data(self) -> tuple[np.ndarray[np.ndarray[np.float_]], np.ndarray[np.float_]]:
        """
        Returns X and Y data in a format that can be used by the neural network
        X contains all the landmark data
        Y contains all the label data
        The right handedness data is removed
        The csv also get shuffled to avoid long lengths of the same label appearing
        """
        data = pd.read_csv(self.path)

        # Sample(frac=1) takes a random sample whose size is the same as the entire csv file
        # reset_index(drop=True) enables the indices to be reset so the order of the file actually changes
        # data = data.sample(frac=1).reset_index(drop=True)
        data = data.sample(frac=1)

        cols = data.columns
        # First column is the label, second column is handedness, and the remaining columns are landmark data
        Y, X = data[cols[0]], data[cols[2:]]
        X = X.to_numpy()
        Y = Y.to_numpy()
        
        return X, Y
    
    def count_labels(self) -> int:
        """
        Returns how many different labels are present in the data
        """
        data = pd.read_csv(self.path)

        # Only the first column contains label data
        labels = data[[data.columns[0]]]
        # Get rid of unnecessary DataFrame information (indices and column)
        labels = labels.values
        # Labels.values returns a 2d array where each subarray contains only one element
        # It needs to be flattened in order to be usable
        labels = labels.reshape(-1)
        # Convert to a set so only one of each values occurs
        labels = set(labels)
        # The length of the set is the number of unique labels that occur
        n = len(labels)

        return n
    