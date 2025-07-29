import os
import pickle


class Cache:
    """
    Static utility class for caching Python objects using pickle.

    Methods:
    --------
    save(obj, filepath):
        Save an object to a file using pickle.

    load(filepath):
        Load an object from a pickle file.

    exists(filepath):
        Check if the cache file exists.
    """

    @staticmethod
    def save(obj, filepath: str) -> None:
        """
        Save an object to a pickle file.

        Parameters:
        -----------
        obj : any
            The Python object to save.
        filepath : str
            The path where the object should be saved.
        """
        with open(filepath, 'wb') as f:
            pickle.dump(obj, f)

    @staticmethod
    def load(filepath: str):
        """
        Load an object from a pickle file.

        Parameters:
        -----------
        filepath : str
            The path to the pickle file.

        Returns:
        --------
        any
            The loaded Python object.
        """
        with open(filepath, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def exists(filepath: str) -> bool:
        """
        Check if a cache file exists.

        Parameters:
        -----------
        filepath : str
            The path to check.

        Returns:
        --------
        bool
            True if the file exists, False otherwise.
        """
        return os.path.isfile(filepath)