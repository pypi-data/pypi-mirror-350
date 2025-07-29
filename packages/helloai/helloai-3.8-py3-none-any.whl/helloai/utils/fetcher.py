import os
import uuid
from urllib.request import urlopen
import tempfile
from urllib.parse import urlparse
from zipfile import ZipFile
import gzip
import tarfile
import requests


__all__ = ["fetch", "unzip", "fetch_and_unzip"]


def fetch(url, folder=None, file_name=None):
    if not folder:
        # Temp folder
        folder = tempfile.gettempdir()

    # 폴더가 없으면 만들고, 있으면 안 만든다.
    os.makedirs(folder, exist_ok=True)

    # 파싱
    parts = urlparse(url)
    if not file_name:
        # 확장자 찾기
        file_ext = os.path.splitext(parts.path)[1]
        file_name = os.path.basename(parts.path)  # eds_report.csv
        if not file_name:
            # 임시 파일을 만든다.
            file_name = str(uuid.uuid4()).split("-")[0] + ".tmp"

    with open(os.path.join(folder, file_name), "wb") as my_file:
        data = requests.get(url)
        my_file.write(data.content)
        return os.path.join(folder, file_name)

    return None


def unzip(path):
    path_to_zip_file = path
    directory_to_extract_to = os.path.dirname(path_to_zip_file)

    # 확장자 찾기
    file_ext = os.path.splitext(path_to_zip_file)[1]

    if file_ext in (".gz", ".gzip", ".bzip2", ".lzma"):
        tar = tarfile.open(path_to_zip_file, mode="r:*")
        dir_name = tar.getmembers()[0].name.split("/")[0]

        tar.extractall(path=directory_to_extract_to)
        tar.close()
        return os.path.join(directory_to_extract_to, dir_name)
    elif file_ext in (".zip",):
        with ZipFile(path_to_zip_file, "r") as zipObj:
            dir_name = zipObj.namelist()[0].split("/")[0]
            zipObj.extractall(path=directory_to_extract_to)
            return os.path.join(directory_to_extract_to, dir_name)
    return None


def fetch_and_unzip(url, folder=None, file_name=None):
    return unzip(fetch(url, folder, file_name))
