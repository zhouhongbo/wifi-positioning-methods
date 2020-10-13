""" 
与数据ID相关的函数
"""
import numpy as np

from file import *

def findWeek(pointIds, week):
    """根据week参数处理ID

    Args:
        pointIds (ndarray): 样本的ID
        week (Number): 星期数

    Returns:
        result (ndarray): 样本的ID
    """
    digits = (pointIds // (10 ** 8)) % 100
    result = digits == week
    return result

def findTrainOrTest(pointIds, trainOrTest):
    """根据trainOrTest参数处理ID

    Args:
        pointIds (ndarray): 样本的ID
        trainOrTest (Number): 1 for train， 2 for test, 0 for both

    Returns:
        result (ndarray): 样本的ID
    """
    digits = (pointIds // (10 ** 5)) % 10
    result = digits == trainOrTest
    return result

def findCampNumber(pointIds, campNumber):
    """根据campNumber参数处理ID

    Args:
        pointIds (ndarray): 样本的ID
        campNumber (Number): 样本所在数据集的编号

    Returns:
        result (ndarray): 样本的ID
    """
    digits = (pointIds // (10 ** 6)) % 100
    result = digits == campNumber
    return result

def findSamplesInRage(pointIds, minVal, maxVal):
    """根据样本编号的范围[1, 10]处理ID

    Args:
        pointIds (ndarray): 样本的ID
        minVal (Number): 样本范围的起始位置
        maxVal (Number): 样本范围的结束位置

    Returns:
        result (ndarray): 样本的ID
    """
    digits = pointIds % 100
    result = (digits >= minVal) & (digits <= maxVal)
    return result

def findSample(pointIds, sampleNumber):
    """根据样本的编号处理ID

    Args:
        pointIds (ndarray): 样本的ID
        sampleNumber (Number): 样本的编号

    Returns:
        result (ndarray): 样本的ID
    """
    result = findSamplesInRage(pointIds, sampleNumber, sampleNumber)
    return result

def findPointsInRage(pointIds, minVal, maxVal):
    """根据结点的编号范围处理ID

    Args:
        pointIds (ndarray): 样本的ID
        minVal (Number): 结点的编号起始位置
        maxVal (Number): 结点的编号结束位置

    Returns:
        result (ndarray): 样本的ID
    """
    digits = (pointIds // (10 ** 2)) % (10 ** 3)
    result = (digits >= minVal) & (digits <= maxVal)
    return result

def findPoint(pointIds, pointNumber):
    """根据结点的编号处理ID

    Args:
        pointIds (ndarray): 样本的ID
        pointNumber (Number): 结点的编号

    Returns:
        result (ndarray): 样本的ID
    """
    result = findPointsInRage(pointIds, pointNumber, pointNumber)
    return result

def filterSamples(pointIds, sampleNumber, pointNumber, trainOrTest, campNumber, week):
    """根据sampleNumber, pointNumber, trainOrTest, campNumber, week参数处理ID

    Args:
        pointIds (ndarray): 样本的ID
        sampleNumber (Number): 样本的编号
        pointNumber (Number): 结点的编号
        trainOrTest (Number): 1 for train， 2 for test, 0 for both
        campNumber (Number): 样本所在数据集的编号
        week (Number): 星期数

    Returns:
        result (ndarray): 样本的ID
    """
    result = np.ones(pointIds.shape, dtype=bool)
    result = result & findSample(pointIds,sampleNumber)
    result = result & findPoint(pointIds,pointNumber)
    result = result & findTrainOrTest(pointIds, trainOrTest)
    result = result & findCampNumber(pointIds, campNumber)
    result = result & findWeek(pointIds, week)
    return result

def findSet(pointIds, trainOrTest, campNumber, week):
    """根据trainOrTest, campNumber, week参数处理ID

    Args:
        pointIds (ndarray): 样本的ID
        trainOrTest (Number): 1 for train， 2 for test, 0 for both
        campNumber (Number): 样本所在数据集的编号
        week (Number): 星期数

    Returns:
        result (ndarray): 样本的ID
    """
    result = np.ones(pointIds.shape, dtype=bool)
    result = result & findTrainOrTest(pointIds, trainOrTest)
    result = result & findCampNumber(pointIds, campNumber)
    result = result & findWeek(pointIds, week)
    return result

if __name__ == "__main__":
    # 测试
    data = loadContentSpecific("db", 2, [2, 3], 1)

    # findWeek(data.ids, 1)
    # findTrainOrTest(data.ids, 1)
    # findCampNumber(data.ids, 2)
    # findSamplesInRage(data.ids, 2, 3)
    # findSample(data.ids, 1)
    # findPointsInRage(data.ids, 1, 3)
    # findPoint(data.ids, 2)
    # filterSamples(data.ids, 2, 2, 2, 2, 1)
    # findSet(data.ids, 2, 2, 1)