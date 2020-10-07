""" 
与数据ID相关的函数
相关注释参考MATLAB代码
"""
import numpy as np
from files import *

def findMonth(pointIds, month):
    digits = (pointIds // (10 ** 8)) % 100
    result = digits == month
    return result

def findTrainOrTest(pointIds, trainOrTest):
    digits = (pointIds // (10 ** 5)) % 10
    result = digits == trainOrTest
    return result

def findCampNumber(pointIds, campNumber):
    digits = (pointIds // (10 ** 6)) % 100
    result = digits == campNumber
    return result

def findSamplesInRage(pointIds, minVal, maxVal):
    digits = pointIds % 100
    result = (digits >= minVal) & (digits <= maxVal)
    return result

def findSample(pointIds, sampleNumber):
    result = findSamplesInRage(pointIds, sampleNumber, sampleNumber)
    return result

def findPointsInRage(pointIds, minVal, maxVal):
    digits = (pointIds // (10 ** 2)) % (10 ** 3)
    result = (digits >= minVal) & (digits <= maxVal)
    return result

def findPoint(pointIds, pointNumber):
    result = findPointsInRage(pointIds, pointNumber, pointNumber)
    return result

def filterSamples(pointIds, sampleNumber, pointNumber, trainOrTest, campNumber, month):
    result = np.ones(pointIds.shape, dtype=bool)
    result = result & findSample(pointIds,sampleNumber)
    result = result & findPoint(pointIds,pointNumber)
    result = result & findTrainOrTest(pointIds, trainOrTest)
    result = result & findCampNumber(pointIds, campNumber)
    result = result & findMonth(pointIds, month)
    return result

def findSet(pointIds, trainOrTest, campNumber, month):
    result = np.ones(pointIds.shape, dtype=bool)
    result = result & findTrainOrTest(pointIds, trainOrTest)
    result = result & findCampNumber(pointIds, campNumber)
    result = result & findMonth(pointIds, month)
    return result

if __name__ == "__main__":
    # 测试
    data = loadContentSpecific("db", 2, [2, 3], 1)

    # findMonth(data.ids, 1)
    # findTrainOrTest(data.ids, 1)
    # findCampNumber(data.ids, 2)
    # findSamplesInRage(data.ids, 2, 3)
    # findSample(data.ids, 1)
    # findPointsInRage(data.ids, 1, 3)
    # findPoint(data.ids, 2)
    # filterSamples(data.ids, 2, 2, 2, 2, 1)
    # findSet(data.ids, 2, 2, 1)