""" 一些不好分类的函数 """
import numpy as np

def customError(estimationPos, actualPos):
    e = np.sqrt(np.sum(np.square(estimationPos - actualPos), axis=1))
    return e

def getMeanAndStd(samples, locations, ids):

    uids, ic = np.unique(ids, return_inverse=True)
    nCols = samples.shape[1]
    nRows = uids.shape[0]

    M = np.zeros([nRows, nCols])
    S = np.zeros([nRows, nCols])
    pos = np.zeros([nRows, 3])

    for i in range(nRows):
        index = ic == i
        values = samples[index, :]
        M[i, :] = np.mean(values, axis=0)
        S[i, :] = np.std(values, axis=0, ddof=1)
        pos[i, :] = np.mean(locations[index, :], axis=0)

    return M, S, pos