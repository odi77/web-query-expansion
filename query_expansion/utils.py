import json
import os


class Utils:
    """
    Utility class for common functions.
    """
    def __init__(self) -> None:
        pass

    def read_json_file(self, path):
        """
        Reads a JSON file from the given path and returns the parsed JSON data.

        Args:
            path (str): The path to the JSON file.

        Returns:
            dict: Parsed JSON data.
        """
        with open(path, 'r') as json_file:
            json_data = json.loads(json_file.read())
            return json_data

    def write_json_file(self, path, file, result):
        """
        Writes JSON data to a file at the specified path with the specified filename.

        Args:
            path (str): The directory path where the file will be written.
            file (str): The name of the JSON file.
            result (dict): The JSON data to be written to the file.
        """
        with open(os.path.join(path, file), 'w') as file:
            file.write(
                json.dumps(
                    result,
                    ensure_ascii=False,
                    indent=4
                )
            )