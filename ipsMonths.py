import numpy as np
import matplotlib.pyplot as plt

from files import *
from ips import *
from funcs import *

# Common to all methods
monthAmount = 2

# Storage for error
metricRand = [0] * monthAmount
metricKnn = [0] * monthAmount
metricNn = [0] * monthAmount
metricStg = [0] * monthAmount

month = 1
while month <= monthAmount:
    # load current month data
    dataTrain = loadContentSpecific("db", 1, [2, 4], month)
    dataTest = loadContentSpecific("db", 2, [2, 4, 6, 8], month)

    # deal with not seen AP
    dataTrain.rss[dataTrain.rss == 100] = -105
    dataTest.rss[dataTest.rss == 100] = -105

    # random location estimation
    predictionRandom = randomEstimation(dataTrain.rss, dataTest.rss, dataTrain.coords)
    errorRandom = customError(predictionRandom, dataTest.coords)
    metricRand[month-1] = np.percentile(errorRandom, 75)  # 计算75%误差

    # NN method estimation
    knnValue = 1
    predictionNn = kNNEstimation(dataTrain.rss, dataTest.rss, dataTrain.coords, knnValue)
    errorNn = customError(predictionNn, dataTest.coords)
    metricNn[month-1] = np.percentile(errorNn, 75)  # 计算75%误差

    # KNN method estimation
    knnValue = 9
    predictionKnn = kNNEstimation(dataTrain.rss, dataTest.rss, dataTrain.coords, knnValue)
    errorKnn = customError(predictionKnn, dataTest.coords)
    metricKnn[month-1] = np.percentile(errorKnn, 75)  # 计算75%误差

    # Stg method estimation
    stgValue = 3 # AP filtering value
    kValue = 5 # Number of neighbors
    predictionStg = stgKNNEstimation(dataTrain.rss, dataTest.rss, dataTrain.coords, stgValue, kValue)
    errorStg = customError(predictionStg, dataTest.coords)
    metricStg[month-1] = np.percentile(errorStg, 75)  # 计算75%误差

    print(month)
    month += 1

# Display figure "ipsError"
x = [i+1 for i in range(monthAmount)]
plt.plot(x, metricRand, label="Rand")
plt.plot(x, metricNn, label="NN")
plt.plot(x, metricKnn, label="KNN")
plt.plot(x, metricStg, label="Stg")

plt.xlabel("month number", {"size": 15})
plt.ylabel("75 percentile error (m)", {"size": 15})

plt.xlim((1, monthAmount))
plt.ylim((0, 6))

plt.xticks(np.arange(1, monthAmount+1, 1))
plt.yticks(np.arange(0, 7, 1))

plt.legend(loc="upper right")
plt.grid()
plt.show()
