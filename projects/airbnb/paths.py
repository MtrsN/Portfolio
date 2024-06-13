
import os

def create_folder(path):

    if not os.path.exists(path):

        print(f"Creating folder at path: {path}", end= "\n\n")
        os.makedirs(path)

    else:
        print(f"Folder already exists at path: {path}", end= "\n\n")

class Paths:

    PATH_FILE = os.path.dirname(os.path.abspath(__file__))
    PATH_ROOT = os.path.dirname(PATH_FILE)
    
    PATH_DATASETS = os.path.join(PATH_ROOT, 'airbnb' + os.sep + 'datasets' + os.sep + 'gz_files')
    PATH_DATASETS_CSV = os.path.join(PATH_ROOT, 'airbnb' + os.sep + 'datasets' + os.sep +  'csv_files')