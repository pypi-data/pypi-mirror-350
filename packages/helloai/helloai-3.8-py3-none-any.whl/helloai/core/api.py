#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2021- HelloAI Project Contributors
# -----------------------------------------------------------------------------

import io
import re
import urllib
import numpy as np
import pandas as pd
import cv2
import PIL.Image as pImage

# import random as rand
import os
import pprint as pp
# import vnoise

from helloai.core.image import Image
from helloai.core.colors import *

# from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import minmax_scale
import builtins

__all__ = [
    "load_image",
    "read_image",
    'new_image',
    "map",
    "pprint",
    "save_npy",
    "load_npy",
    "list_concatenate",
    "concatenate",
    "save_dataset",
    "load_dataset",
    "one_hot",
    "bounding_box",
    # "flatten",
    "read_csv",
    "save_csv",
    "shape",
    "shuffle",
    "nparray",
    "toarray",
    "tolist",
    "reshape",
]


# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html
def normaliz(data, scaler="minmax"):
    if isinstance(data, list):
        data = np.array(data)
    elif isinstance(data, np.ndarray):
        pass
    else:
        return data

    if scaler == "minmax":
        # scaled_data = minmax_scale(data, axis=0, copy=True)
        scaled_data = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))
        return scaled_data
    elif scaler == "image":
        return data.astype("float32") / 255.0
    else:
        return data

def _rgba_to_bgra(color):
    if len(color) == 4:
        r, g, b, a = color
        return (b, g, r, a)
    elif len(color) == 3:
        # If the input is RGB, assume full opacity
        r, g, b = color
        return (b, g, r, 255)
    else:
        raise ValueError("Input color must be in RGBA or RGB format.")

def new_image(color=(211, 211, 211), size=(builtins.HEIGHT, builtins.WIDTH)):
    """
    특정 컬러의 이미지를 만든다.
    """    
    if len(color) == 3:
        r, g, b = color
        frame = np.zeros((size[0], size[1], 3))
        frame[:, :] = (b, g, r)
    elif len(color) == 4:
        r, g, b, a = color
        frame = np.zeros((size[0], size[1], 4))
        frame[:, :] = (b, g, r, a)


    # # 알파 채널이 있는 이미지를 만든다.
    # frame = np.zeros((builtins.HEIGHT, builtins.WIDTH, 4))
    # # 각 픽셀에 변환된 색상 값을 대입
    # frame[:, :] = _rgba_to_bgra(color)
    frame = frame.astype(np.uint8)
    return Image(frame)


def load_image(filename):
    frame = None
    isWeb = False

    if re.match(r"\w+://", filename):
        # 웹상의 이미지
        with urllib.request.urlopen(filename) as url:
            f = io.BytesIO(url.read())
            pil_image = pImage.open(f)
            frame = np.array(pil_image)
            isWeb = True
    else:
        frame = cv2.imread(filename)

    if isWeb:
        return Image(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR), "bgr")
    else:
        return Image(frame, "bgr")


def read_image(filename):
    return load_image(filename, colorspace)


# vnoise를 이용한 perlin노이즈
# def noise(x, y=None, z=None):
#     n = vnoise.Noise()
#     if y == None:
#         return map(n.noise1(x), -0.5, 0.5, 0, 1)
#     elif z == None:
#         return map(n.noise2(x, y), -0.5, 0.5, 0, 1)
#     else:
#         return map(n.noise3(x, y, z), -0.5, 0.5, 0, 1)


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def pprint(object, stream=None, indent=4, width=80, depth=None):
    """Pretty-print a Python object to a stream [default is sys.stdout]."""
    printer = pp.PrettyPrinter(stream=stream, indent=indent, width=width, depth=depth)
    printer.pprint(object)


def mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def save_npy(path, dataset):
    """
    numpy 파일로 저장
    """
    head_tail = os.path.split(path)
    mkdir(head_tail[0])
    np.save(path, np.array(dataset))


def load_npy(file_name):
    """
    npy로 저장한 파일 읽기
    """
    data = np.load(file_name, allow_pickle=True).item()
    print(file_name, "파일이 로드되었습니다")
    return data


def list_concatenate(x, *args):
    return np.concatenate((x, *args), axis=0)


def concatenate(data, axis=0):
    data = np.concatenate(data, axis=axis)
    return data


def save_dataset(path, dataset):
    save_npy(path, dataset)


def load_dataset(path):
    return np.load(path, allow_pickle=True).item()


def one_hot(labels, data):
    y_train = []
    eyes = np.eye(len(labels))
    for lbl in data:
        idx = labels.index(lbl)
        y_train.append(eyes[idx])
    return np.array(y_train)


def bounding_box(lmks):
    bb = np.array([np.min(lmks, axis=0), np.max(lmks, axis=0)])
    return bb


def reshape(data, shape):
    if isinstance(data, list):
        data = np.array(data)
        data = np.reshape(data, shape)

    if isinstance(data, np.ndarray):
        data = np.reshape(data, shape)
    return data

# https://rfriend.tistory.com/252
def save_csv(filename, data, sep=" ", header=None):
    if isinstance(data, list):
        data = np.array(data)

    if isinstance(data, np.ndarray):
        data = pd.DataFrame(data)

    if header:
        data.to_csv(
            filename,
            sep=sep,
            na_rep="NaN",
            float_format="%.2f",  # 2 decimal places
            columns=header,  # columns to write
            index=False,  # do not write index
        )
    else:
        data.to_csv(
            filename,
            header=False,
            columns=None,
            sep=sep,
            na_rep="NaN",
            float_format="%.2f",  # 2 decimal places
            index=False,  # do not write index
        )

# https://chrisjune-13837.medium.com/python-%EA%B0%80%EB%B3%80%EC%9D%B8%EC%9E%90-%ED%8C%A8%ED%82%B9-%EC%96%B8%ED%8C%A8%ED%82%B9-a47ee2cdcac3
def read_csv(filename, **kwargs):
    df = pd.read_csv(filename, **kwargs)
    return df.to_numpy()


def shape(data):
    if isinstance(data, list):
        return np.array(data).shape
    elif isinstance(data, np.ndarray):
        return data.shape
    elif isinstance(data, Image):
        return data.shape()
    else:
        return None


def shuffle(x_data, y_data):
    np.random.seed(777)
    if not isinstance(x_data):
        x_data = np.array(x_data)

    if not isinstance(y_data):
        y_data = np.array(y_data)

    index = np.arange(len(x_data))
    np.random.shuffle(index)
    return x_data[index], y_data[index]


# ndarray로 바꿔서 반환
def nparray(data):
    if isinstance(data, list):
        return np.array(data)
    elif isinstance(data, Image):
        return data.array
    return data


def toarray(data):
    return nparray(data)


def tolist(data):
    if isinstance(data, np.ndarray):
        return data.tolist()
    return data
