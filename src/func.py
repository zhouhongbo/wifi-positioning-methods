""" 
一些不好分类的函数 
"""
import numpy as np

def customError(estimationPos, actualPos):
    """计算预测位置与实际位置之间的误差

    Args:
        estimationPos (ndarray): 预测位置
        actualPos (ndarray): 实际位置

    Returns:
        e (ndarray): 误差
    """
    e = np.sqrt(np.sum(np.square(estimationPos - actualPos), axis=1))
    return e

def getMeanAndStd(samples, locations, ids):
    """获取训练集样本的均值和均方差

    Args:
        samples (ndarray): 训练集样本
        positions (ndarray): 训练集样本的位置
        ids (ndarray): 训练集样本的ID

    Returns:
        M (ndarray): 均值
        S (ndarray): 均方差
        pos (ndarray): 位置
    """
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

def convertToTimeVectors(timeNumber):
    """将时间戳转换为年月日时分秒的形式

    Args:
        timeNumber (Number): 时间戳

    Returns:
        year: 年
        month: 月
        day: 日
        hour: 时
        minute: 分
        second: 秒
    
    Test1：
        timeNumber: 20200926142506
        year: 2020
        month: 9
        day: 26
        hour: 14
        minute: 25
        second: 6
    """
    second = timeNumber % 100
    minute = (timeNumber // (10 ** 2)) % 100
    hour = (timeNumber // (10 ** 4)) % 100
    day = (timeNumber // (10 ** 6)) % 100
    month = (timeNumber // (10 ** 8)) % 100
    year = timeNumber // (10 ** 10)
    return year, month, day, hour, minute, second

if __name__ == "__main__":
    # 测试
    timeNumber = 20200926142506
    print(convertToTimeVectors(timeNumber))