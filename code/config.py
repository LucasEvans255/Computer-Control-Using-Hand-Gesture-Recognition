import json


class Config:

    def __init__(self):
        """
        Class for storing configuration data
        Data is accessed using the json_dict attribute, which is a dictionary
        There are 2 valid forms of configuration data

        Config:
        Contains data about settings the user has chosen
        'device': 'cuda'/'cpu'
        'cam_width': int
        'cam_height': int
        'label_to_button': {int: str} - Maps from a label to the string representation of the function it invokes

        Label_to_str:
        {int : str} - Maps from a label to the name of the gesture, which is what the user sees when adding a new gesture
        """
        self.path = None
        self.json_dict = {}

    def save_as(self, path: str) -> None:
        """
        Saves the current configuration data under a new path
        """
        self.path = path

        with open(self.path, 'w') as f:
            json.dump(self.json_dict, f)
    
    def save(self) -> None:
        """
        Saves new configuration data under the current path
        """
        with open(self.path, 'w') as f:
            json.dump(self.json_dict, f)
    
    def load(self, path: str) -> int:
        """
        Attempts to load data from a new path
        Returns an integer detailing wether there was a success or not
        0: An invalid file was loaded
        1: A valid label_to_str file was loaded
        2: A valid config file was loaded
        """
        if not path.endswith('.json'):
            return 0
        
        with open(path, 'r') as f:
            json_dict = json.load(f)

        valid = self._is_valid(json_dict)
        
        if valid != 0:
            self.path = path
            self.json_dict = json_dict
            if valid == 2:
                with open('config_path.txt', 'w') as f:
                    f.write(path)
            return valid
        else:
            return 0
        
    def _is_valid(self, json_dict: dict) -> int:
        """
        Checks if the data in the file is of a valid configuration for either
        0: Invalid
        1: label_to_str
        2: config
        """
        keys = json_dict.keys()
        required = {'device', 'cam_width', 'cam_height', 'label_to_button'}

        all_int = self._all_keys_int(json_dict)

        # If not all of the required keys are present, and they arent all integers (label_to_str)
        if any([r not in keys for r in required]) and not all_int:
            return 0
        if self._all_keys_int(json_dict):
            return 1
        # If it contains all the required keys, but has extra, then it is invalid
        if len(keys) > 4:
            return 0
        # Checks that all the keys in the label_to_button field are integers
        if self._all_keys_int(json_dict['label_to_button']):
            return 2
        # If not it is invalid
        return 0


    def _all_keys_int(self, json_dict: dict) -> bool:
        """
        Returns True if all the keys are integers, otherwise False
        """
        keys = json_dict.keys()
        
        # The keys are all stored as strings
        # If converting from string to integer raises an error, then it must not be an integer
        for key in keys:
            try:
                int(key)
            except ValueError:
                return False
        
        return True
    