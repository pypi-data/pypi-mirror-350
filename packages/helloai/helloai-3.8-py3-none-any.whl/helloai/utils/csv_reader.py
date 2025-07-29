import pandas as pd

__all__ = ["CSVReader"]


class CSVReader:
    def __init__(self, filename):
        self.__filename = filename
    
    def read(self):
        try:
            data = pd.read_csv(self.__filename).to_numpy().tolist()
            return data
        except FileNotFoundError:
            print(f"File {self.filename} not found.")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []