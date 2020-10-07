""" 定位算法 """
import numpy as np

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