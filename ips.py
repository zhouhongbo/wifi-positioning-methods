""" 定位算法 """
import numpy as np
from scipy.stats import norm
from funcs import *

def kNNEstimation(samples, query, positions, k):
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
        if val[0] == 0:
            prediction[i, :] = pos[0, :]
        else:
            prediction[i, :] = np.mean(pos, axis=0)
    
    return prediction

def randomEstimation(samples, query, positions):
    pos = np.unique(positions, axis=0)
    nPoints = pos.shape[0]
    nQuery = query.shape[0]
    neighbors = np.random.randint(0, nPoints, size=nQuery)
    prediction = pos[neighbors, :]

    return prediction

def stgKNNEstimation(samples, query, positions, stgValue, k):
    def stgSmplsPerAP(rss,stgValue):
        result = [[] for _ in range(rss.shape[1])] # 二维数组，行数与AP数相同
        stgIdx = np.argsort(rss)[:, -stgValue:] # 最强AP的下标
        for i in range(stgIdx.shape[0]):
            for j in range(stgIdx.shape[1]):
                result[stgIdx[i][j]].append(i)
        return result

    samplesList = stgSmplsPerAP(samples, stgValue) # 与MATLAB代码有一点不同是因为最强的K个AP不是固定的
    prediction = np.empty([query.shape[0], 3])

    for i in range(query.shape[0]):  # For each query sample
        fingerprint = query[i, :]
        # Find the strongest AP in the query sample
        stgIdx = np.argsort(fingerprint)[-stgValue:]
        # Get training samples whose strongest APs match those of the query
        allFPIdx = []
        for idx in stgIdx:
            allFPIdx.extend(samplesList[idx])
        # Apply kNN over the training selection 
        fingerprint = fingerprint.reshape(1, 20)
        kNNPrediction = kNNEstimation(samples[allFPIdx,:], fingerprint, positions[allFPIdx,:], k)
        prediction[i] = kNNPrediction
    return prediction

def probEstimation(samples, query, positions, k, ids):
    def probs(M, S, query):
        nRowT = M.shape[0]
        nRowV = query.shape[0]
        PROBS = np.zeros([nRowT, nRowV])

        for i in range(nRowV):
            fp = query[i, :]
            estP = probsFP(M, S, fp)
            PROBS[:, i] = estP
        
        return PROBS
    
    def probsFP(M, S, fp):
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
    
    def estimatesKNN(PROBS, positions, k):
        nRow = PROBS.shape[1]
        estimates = np.zeros([nRow, 3])
        I = np.argsort(-PROBS, axis=0) # 降序排序

        for i in range(nRow):
            # xs = positions[:, 0]
            # ys = positions[:, 1]
            # floor = positions[:, 2]
            # estimates[i, 0] = np.mean(xs[I[0:k, i]])
            # estimates[i, 1] = np.mean(ys[I[0:k, i]])
            # estimates[i, 2] = np.mean(floor[I[0:k, i]])
            estimates[i, :] = np.mean(positions[I[0:k, i], :], axis=0)

        return estimates

    M, S, pos = getMeanAndStd(samples, positions, ids)
    PROBS = probs(M, S, query)
    prediction = estimatesKNN(PROBS, pos, k)

    return prediction