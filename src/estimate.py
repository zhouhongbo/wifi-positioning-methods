""" 
所有的定位算法
"""
import math
import numpy as np
from scipy.stats import norm

from func import *

def kNNEstimation(samples, query, positions, k):
    """实现KNN方法

    Args:
        samples (ndarray): 训练集样本
        query (ndarray): 测试集样本
        positions (ndarray): 训练集样本的位置
        k (Number): 最近邻个数

    Returns:
        prediction (ndarray): 预测位置
    """
    samplRows = samples.shape[0]
    queryRows = query.shape[0]
    prediction = np.zeros([queryRows, 3])

    if k > samplRows:
        k = samplRows

    for i in range(queryRows):
        repQuery = np.tile(query[i, :], (samplRows, 1))
        sumDist = np.sqrt(np.sum(np.square(samples - repQuery), axis=1))

        idx = np.argsort(sumDist)[0:k] # 前k小值的索引
        val = sumDist[idx] # 前k小的值

        pos = positions[idx, :]
        if val[0] == 0: # 若存在某训练集样本与测试集样本的欧氏距离为0，则预测位置为该训练集样本的位置
            prediction[i, :] = pos[0, :]
        else:
            prediction[i, :] = np.mean(pos, axis=0)
    
    return prediction
    
def wknnEstimation(samples, query, positions, k):
    """实现WKNN方法

    Args:
        samples (ndarray): 训练集样本
        query (ndarray): 测试集样本
        positions (ndarray): 训练集样本的位置
        k (Number): 最近邻个数

    Returns:
        prediction (ndarray): 预测位置
    """
    samplRows = samples.shape[0]
    queryRows = query.shape[0]
    prediction = np.zeros([queryRows, 3])

    if k > samplRows:
        k = samplRows

    for i in range(queryRows):
        repQuery = np.tile(query[i, :], (samplRows, 1))
        sumDist = np.sqrt(np.sum(np.square(samples - repQuery), axis=1))

        idx = np.argsort(sumDist)[0:k] # 前k小值的索引
        val = sumDist[idx] # 前k小的值

        pos = positions[idx, :]
        if val[0] == 0: # 若存在某训练集样本与测试集样本的欧氏距离为0，则预测位置为该训练集样本的位置
            prediction[i, :] = pos[0, :]
        else:
            # 计算权重
            w = 1 / val
            w = w / np.sum(w)

            prediction[i, :] = np.sum(w * pos.T, axis=1)
    
    return prediction

def randomEstimation(samples, query, positions):
    """随机方法

    Args:
        samples (ndarray): 训练集样本
        query (ndarray): 测试集样本
        positions (ndarray): 训练集样本的位置

    Returns:
        prediction (ndarray): 预测位置
    """
    pos = np.unique(positions, axis=0)
    nPoints = pos.shape[0]
    nQuery = query.shape[0]
    neighbors = np.random.randint(0, nPoints, size=nQuery)
    prediction = pos[neighbors, :]

    return prediction

def stgKNNEstimation(samples, query, positions, stgValue, k):
    """stg方法，是KNN方法的一种改进方法

    Args:
        samples (ndarray): 训练集样本
        query (ndarray): 测试集样本
        positions (ndarray): 训练集样本的位置
        stgValue (Number): 信号最强AP的个数
        k (Number): 最近邻个数
    
    Returns:
        prediction (ndarray): 预测位置
    """
    def stgSmplsPerAP(rss,stgValue): # 返回二维数组，行代表AP，列代表信号最强k个AP为该AP的所有训练集样本下标
        result = [[] for _ in range(rss.shape[1])] # 二维数组，行数与AP数相同
        stgIdx = np.argsort(rss)[:, -stgValue:] # 最强AP的下标
        for i in range(stgIdx.shape[0]):
            for j in range(stgIdx.shape[1]):
                result[stgIdx[i][j]].append(i)
        return result

    samplesList = stgSmplsPerAP(samples, stgValue) # 与MATLAB代码有一点不同是因为最强的K个AP不是固定的
    prediction = np.empty([query.shape[0], 3])

    for i in range(query.shape[0]):  # 遍历测试集样本
        fingerprint = query[i, :]
        # 找到测试样本中最强AP的下标
        stgIdx = np.argsort(fingerprint)[-stgValue:]
        # 找到测试样本中最强AP匹配的训练集样本
        allFPIdx = []
        for idx in stgIdx:
            allFPIdx.extend(samplesList[idx])
        # 对测试样本应用KNN方法
        # fingerprint = fingerprint.reshape(1, 20)
        fingerprint = fingerprint.reshape(1, fingerprint.shape[0])
        kNNPrediction = kNNEstimation(samples[allFPIdx,:], fingerprint, positions[allFPIdx,:], k)
        prediction[i] = kNNPrediction

    return prediction

def probEstimation(samples, query, positions, k, ids):
    """基于概率的方法

    Args:
        samples (ndarray): 训练集样本
        query (ndarray): 测试集样本
        positions (ndarray): 训练集样本的位置
        k (Number): 最近邻个数
        ids (ndarray): 样本的ID（需要把特征值删除），根据这个参数把具有相同特征的训练集样本分组

    Returns:
        prediction (ndarray): 预测位置
    """
    def probs(M, S, query): # 计算测试集样本的每一个数据出现在对应AP的概率
        nRowT = M.shape[0]
        nRowV = query.shape[0]
        PROBS = np.zeros([nRowT, nRowV])

        for i in range(nRowV):
            fp = query[i, :]
            estP = probsFP(M, S, fp)
            PROBS[:, i] = estP
        
        return PROBS
    
    def probsFP(M, S, fp): # 计算PROBS变量的一列
        e = 0.5
        nRowT = M.shape[0]
        FP1 = np.tile(fp - e, (nRowT, 1))
        FP2 = np.tile(fp + e, (nRowT, 1))
        D1 = norm.cdf(FP1, M, S) # 当标准差为0时，结果为nan，而MATLAB的结果为1或0，当val < mean时为0， 大于等于mean时为1
        D2 = norm.cdf(FP2, M, S)

        # 处理值为nan的情况
        D1[np.isnan(D1) & (FP1 < M)] = 0
        D1[np.isnan(D1) & (FP1 >= M)] = 1
        D2[np.isnan(D2) & (FP2 < M)] = 0
        D2[np.isnan(D2) & (FP2 >= M)] = 1


        PROBS = D2 - D1
        PROBS[PROBS == 0] = 10 ** (-24)

        P = np.prod(PROBS, axis=1)
        return P
    
    def estimatesKNN(PROBS, positions, k): # 比较概率值的KNN方法
        nRow = PROBS.shape[1]
        estimates = np.zeros([nRow, 3])
        I = np.argsort(-PROBS, axis=0) # 降序排序

        for i in range(nRow):
            estimates[i, :] = np.mean(positions[I[0:k, i], :], axis=0)

        return estimates

    M, S, pos = getMeanAndStd(samples, positions, ids)
    PROBS = probs(M, S, query)
    prediction = estimatesKNN(PROBS, pos, k)

    return prediction

def gaussiankernelEstimation(samples, query, positions, sigma, k):
    """gaussiankernelEstimation Estimate locations based on Gaussian assumption.

    Args:
        samples (ndarray): 训练集样本
        query (ndarray): 测试集样本
        positions (ndarray): 训练集样本的位置
        sigma (Number): 核函数的宽度
        k (Number): 最近邻个数

    Returns:
        prediction (ndarray): 预测位置
    """
    def estimateKNN(cf, positions, k):
        # estimateKNN Estimate position being the average of k-likeliest positions
        idx = np.argsort(-cf, axis=0) # 降序排序
        ests = positions[idx[0:k], :]
        
        estPos = np.mean(ests, axis=0)
        return estPos
    
    numFps = samples.shape[0]
    numQ = query.shape[0]
    prediction = np.zeros([numQ, 3])
    # set optionally not detected APs to NaN, can provide robustness
    samples[samples == -105] = np.nan
    query[query == -105] = np.nan
    # treat each RSS measurement as independent fingerprint and ignore the 6
    # samples that are associated to the same fingerprint location
    for i in range(numQ):
        queryMat = np.tile(query[i, :], (numFps, 1))

        # Associate each point a probability / cost corresponding to the
        # likelihood that the current RSS vector corresponds to that position

        # probability for each AP in each point using Gaussian similarity
        likelihoodMatrix = (1 / math.sqrt(2 * math.pi * (sigma ** 2))) * np.exp(-(samples-queryMat) ** 2 / (2 * (sigma ** 2)))
        # # replace zeros with a very small value
        likelihoodMatrix[np.isnan(likelihoodMatrix)] = math.pow(10, -6)
        # use logaritmic probabilities for incraesed efficiency and stability
        likelihoodMatrix = np.log(likelihoodMatrix)
        # combine individual likelihoods
        costFunction = np.sum(likelihoodMatrix, axis = 1)

        # compute position estimate as average of k most likely positions
        k = min(k, numFps)
        prediction[i, :] = estimateKNN(costFunction, positions, k)
    return prediction