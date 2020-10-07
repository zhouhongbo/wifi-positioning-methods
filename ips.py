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