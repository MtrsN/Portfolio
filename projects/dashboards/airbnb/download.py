
import os
import gzip
import shutil
import requests

from tqdm import tqdm
from paths import Paths, create_folder

def download_gz_file(url, filename):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
    }

    try:

        print(f"Trying to download the file from {url}", end= "\n\n")
    
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:

            file_size = int(response.headers.get('Content-Length', 0))
            
            with open(filename, 'wb') as file:

                with tqdm(unit= "B", total= file_size, leave= True, position= 0, desc= "Download") as pbar:

                    for chunk in response.iter_content(chunk_size= 64):

                        if(chunk):
                            pbar.update(len(chunk))
                            file.write(chunk)
            
            print(f"\n\nFile downloaded successfully and saved as {filename}")

        else:
            print(f"\n\nFailed to download {filename}. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"\n\nn error occurred while downloading {filename}: {e}", end= "\n\n")

def extract_gz_file(gz_file, extract_path):

    try:
        print(f"Extracting {gz_file} to {extract_path}", end= "\n\n")

        with gzip.open(gz_file, 'rb') as f_in:
            with open(extract_path, 'wb') as f_out:
                with tqdm(unit= "B", total= os.path.getsize(gz_file), leave= True, position= 0, desc= "Extract") as pbar:
                    for chunk in iter(lambda: f_in.read(64), b""):
                        f_out.write(chunk)
                        pbar.update(len(chunk))

                shutil.copyfileobj(f_in, f_out)

        print(f"Extraction completed successfully to {extract_path}", end= "\n\n")

    except Exception as e:
        print(f"An error occurred while extracting {gz_file}: {e}", end= "\n\n")

if __name__ == "__main__":

    create_folder(Paths.PATH_DATASETS)
    create_folder(Paths.PATH_DATASETS_CSV)
    
    urls = [
        'https://data.insideairbnb.com/portugal/norte/porto/2024-03-18/data/listings.csv.gz',
        #'https://data.insideairbnb.com/portugal/norte/porto/2024-03-18/data/calendar.csv.gz',
        #'https://data.insideairbnb.com/portugal/norte/porto/2024-03-18/data/reviews.csv.gz'
    ]

    download_paths = [os.path.join(Paths.PATH_DATASETS, i.split('/')[-1]) for i in urls]
    csv_paths = [os.path.join(Paths.PATH_DATASETS_CSV, i.split('/')[-1]).replace(".gz", "") for i in urls]

    for url, download_path in zip(urls, download_paths):

        if(os.path.exists(download_path)):
            print(f"{download_path} already exists. Skipping download.")
            continue

        download_gz_file(url, download_path)
    
    for download_path, csv_path in zip(download_paths, csv_paths):

        if(not os.path.exists(download_path)):
            print(f"{download_path} not found. Skipping extraction")
            continue
            
        extract_gz_file(download_path, csv_path)