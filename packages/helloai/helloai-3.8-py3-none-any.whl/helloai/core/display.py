import math
import matplotlib.image as img
import matplotlib.pyplot as plt
import numpy as np
from helloai.core.config import *
from helloai.core.image import Image as hImage

__all__ = ["Display", "show"]


class Display:
    def __init__(self):
        self.__is_notebook = is_notebook() or is_colab()
        if not self.__is_notebook:
            raise Exception("이 클래스는 쥬피터노트북 환경에서만 사용 가능합니다")

    # def show(self, img, labels=None):
    #     frame = None
    #     if isinstance(img, hImage):
    #         if img.colorspace == 'gray':
    #             frame = img.frame
    #         elif img.colorspace == 'bgra' or img.colorspace == 'rgra':
    #             frame = img.frame[:,:, (2, 1, 0, 3)]
    #         else:
    #             frame = img.frame[:,:,::-1]
    #     elif isinstance(img, np.ndarray):
    #         frame = img
    #     plt.imshow(frame)


def show(imgs, labels=None):
    if not is_notebook() and not is_colab():
        print("Notebook 환경에서만 사용할 수 있는 함수입니다")
        return

    if isinstance(imgs, hImage):
        plt.imshow(imgs.frame)
        return

    n_col = 3
    n_row = math.ceil(len(imgs) / n_col)
    axes = []
    fig = plt.figure(figsize=(10, 10))

    for idx in range(n_row * n_col):
        if idx > len(imgs) - 1:
            continue
        frame = imgs[idx].frame

        axes.append(fig.add_subplot(n_row, n_col, idx + 1))
        if labels:
            axes[-1].set_title(labels[idx])
        else:
            subplot_title = "Subplot" + str(idx)
            axes[-1].set_title(subplot_title)
        plt.imshow(frame)
    fig.tight_layout()
    plt.show()
