""" 
功能：生成rss.csv、tms.csv和ids.csv文件
"""
# filename: 例 "AP1-2.4G (54_75_95_F4_E2_ED).csv"; 
# return rss: 一维数组，所有有效点的后10个数据
# return tms: 一维数组，有效点对应的采集时间
def loadData(filename): 
    import csv
    # 读取信号数据、时间数据到一维数组tmpRss、tmpTms中
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # 跳过表头

        tmpRss = []
        tmpTms = []
        for row in reader:
            tmpRss.append(row[1].strip())
            tmpTms.append(row[0].strip())
        
    # 将tmpRss中的 "-" 改为 "100"    
    for i in range(len(tmpRss)): 
        if tmpRss[i] == "-":
            tmpRss[i] = "100"
    
    # 去除无效点；选取有效点的后10个数据
    rss = []
    tms = []
    for i in range(len(tmpRss)):
        if tmpRss[i] == "start" or tmpRss[i] == "resume":
            subRss = []
            subTms = []
        elif tmpRss[i] == "pause":
            if len(subRss) >= 10: # 只选数据量大于等于10的点
                rss.extend(subRss[-10:]) # 选最后10个元素
                tms.extend(subTms[-10:])
        else:
            subRss.append(tmpRss[i])
            subTms.append(tmpTms[i])
    
    return rss, tms

# return rss: 二维数组，行是AP的名称，列是信号值(还需要行列翻转)
# return tms: 一维数组，有效点对应的采集时间（时间格式还需要转换）
def loadAllData():
    import os
    # 获取所有csv文件的名称
    tmp = os.listdir(".")
    fileName = []
    for val in tmp:
        if val[-3:] == "csv" and val[:2] == "AP":
            fileName.append(val)
    fileName.sort(key = lambda x: int(x.split("-")[0][2:])) # 按AP的编号排序
    
    rss = []
    for val in fileName:
        tmpRss, tms = loadData(val)
        rss.append(tmpRss)
    
    return rss, tms

# 将rss和tms按照Long-Term数据集的格式保存
def saveData(rss, tms, prefix):
    import csv
    # 翻转二维数组
    tmp = [[0] * len(rss) for _ in range(len(rss[0]))]
    for i in range(len(rss)):
        for j in range(len(rss[0])):
            tmp[j][i] = rss[i][j]

    # 将时间格式转换为“年月日时分秒”
    for i in range(len(tms)):
        year = tms[i][0:4]
        month = tms[i][5:7]
        day = tms[i][8:10]
        hour = tms[i][11:13]
        minute = tms[i][14:16]
        second = tms[i][17:19]
        tms[i] = year + month + day + hour + minute + second
    
    # 写入文件
    with open(prefix + "rss.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(tmp)
    
    with open(prefix + "tms.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for val in tms:
            writer.writerow([val])

    print("Success!")

def generateIds(tms, month, datasetNum, datasetType, prefix):
    import csv
    ids = [""] * len(tms)
    pointId = 1
    sampleId = 1
    for i in range(len(ids)):
        # pointIdStr长度为3，sampleIdStr长度为2
        if pointId < 10:
            pointIdStr = "00" + str(pointId)
        else:
            pointIdStr = "0" + str(pointId)
        if sampleId < 10:
            sampleIdStr = "0" + str(sampleId)
        else:
            sampleIdStr = str(sampleId)

        ids[i] = month + datasetNum + datasetType + pointIdStr + sampleIdStr
        
        if sampleId == 10:
            sampleId = 1
            pointId += 1
        else:
            sampleId += 1

    # 写入文件
    with open(prefix + "ids.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for val in ids:
            writer.writerow([val])

if __name__ == "__main__":
    # 参数
    month = "01" # 两位数
    datasetNum = "03" # 两位数
    datasetType = "1" # 1 for trainning, 2 for test

    prefix = "trn" if datasetType == "1" else "tst" # 文件名前缀
    prefix += datasetNum

    # 生成rss.csv, tms.csv
    rss, tms = loadAllData()
    saveData(rss, tms, prefix)

    # 生成ids.csv
    generateIds(tms, month, datasetNum, datasetType, prefix)
