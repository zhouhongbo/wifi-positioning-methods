""" 一些不好分类的函数 """
import numpy as np

def customError(estimationPos, actualPos):
    e = np.sqrt(np.sum(np.square(estimationPos - actualPos), axis=1))
    return e