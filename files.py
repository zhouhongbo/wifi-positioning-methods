""" 处理文件的函数 """
import os
import numpy as np

class Defs:
    """
    模仿结构体，与文件名称相关
    """
    def __init__(self):
            self.test = "tst"
            self.train = "trn"
            self.rss = "rss"
            self.ids = "ids"
            self.time = "tms"
            self.coords = "crd"

class Data:
    """
    保存数据
    """
    def __init__(self, rss, coords, time, ids):
        self.rss = rss
        self.coords = coords
        self.time = time
        self.ids = ids

def getFileNameDefs():
    """返回与文件名称相关的对象

    Returns:
        defs (Defs): 与文件名称相关的对象
    """
    defs = Defs()
    return defs

def getDirContent(dirPath, dirOrFile):
    """返回dirPath目录下的目录或者文件名

    Args:
        dirPath (String): 目录名称
        dirOrFile (Number): 为 1 时返回目录名，否则返回文件名

    Returns:
        (List): 目录或者文件名列表

    Test1:
        dirPath: "db"
        dirOrFile: 1
        list: ['01', '02']
    
    Test2:
        dirPath: "db/01"
        dirOrFile: 0
        list: ['trn01crd.csv','trn01ids.csv','trn01rss.csv','trn01tms.csv','trn02crd.csv','trn02ids.csv','trn02rss.csv','trn02tms.csv',\
                'trn03crd.csv','trn03ids.csv','trn03rss.csv','trn03tms.csv','trn04crd.csv','trn04ids.csv','trn04rss.csv','trn04tms.csv',\
                'tst01crd.csv','tst01ids.csv','tst01rss.csv','tst01tms.csv','tst02crd.csv','tst02ids.csv','tst02rss.csv','tst02tms.csv',\
                'tst03crd.csv','tst03ids.csv','tst03rss.csv','tst03tms.csv','tst04crd.csv','tst04ids.csv','tst04rss.csv','tst04tms.csv',\
                'tst05crd.csv','tst05ids.csv','tst05rss.csv','tst05tms.csv','tst06crd.csv','tst06ids.csv','tst06rss.csv','tst06tms.csv',\
                'tst07crd.csv','tst07ids.csv','tst07rss.csv','tst07tms.csv','tst08crd.csv','tst08ids.csv','tst08rss.csv','tst08tms.csv']
    """
    if dirOrFile == 1:
        list = os.listdir(dirPath)
        list.remove("Readme.txt")
    else:
        list = os.listdir(dirPath)
    return list

def rmPartsAndExt(fileNames, defs):
    """获得训练集和测试集名称

    Args:
        fileNames (List): 月份目录下的所有文件名
        defs (Defs): 参见 getFileNameDefs(); 这里没用上

    Returns:
        result (List): 训练集和测试集名称

    Test1:
        fileNames: ['trn01crd.csv','trn01ids.csv','trn01rss.csv','trn01tms.csv','trn02crd.csv','trn02ids.csv','trn02rss.csv','trn02tms.csv',\
                'trn03crd.csv','trn03ids.csv','trn03rss.csv','trn03tms.csv','trn04crd.csv','trn04ids.csv','trn04rss.csv','trn04tms.csv',\
                'tst01crd.csv','tst01ids.csv','tst01rss.csv','tst01tms.csv','tst02crd.csv','tst02ids.csv','tst02rss.csv','tst02tms.csv',\
                'tst03crd.csv','tst03ids.csv','tst03rss.csv','tst03tms.csv','tst04crd.csv','tst04ids.csv','tst04rss.csv','tst04tms.csv',\
                'tst05crd.csv','tst05ids.csv','tst05rss.csv','tst05tms.csv','tst06crd.csv','tst06ids.csv','tst06rss.csv','tst06tms.csv',\
                'tst07crd.csv','tst07ids.csv','tst07rss.csv','tst07tms.csv','tst08crd.csv','tst08ids.csv','tst08rss.csv','tst08tms.csv']
        defs: 
        result: ['trn01','trn02','trn03','trn04','tst01','tst02','tst03','tst04','tst05','tst06','tst07','tst08']
    """
    fileNames = [item[0:5] for item in fileNames]

    # 去重
    result = []
    hashmap = {}
    for filename in fileNames:
        if filename not in hashmap:
            hashmap[filename] = True
            result.append(filename)

    return result

def getAllFileNames(dataFolder, defs):
    """获得所有文件名

    Args:
        dataFolder (String): 数据集目录
        defs (Defs): 参见 getFileNameDefs()

    Returns:
        dirAndFileNames (List): 二维数组，第一列为目录名，第二列为文件名
    
    Test1:
        dataFolder: "db"
        defs:
        dirAndFileNames:[['01', 'trn01']
                         ['01', 'trn02']
                         ['01', 'trn03']
                         ['01', 'trn04']
                         ['01', 'tst01']
                         ['01', 'tst02']
                         ['01', 'tst03']
                         ['01', 'tst04']
                         ['01', 'tst05']
                         ['01', 'tst06']
                         ['01', 'tst07']
                         ['01', 'tst08']
                         ['02', 'trn01']
                         ['02', 'trn02']
                         ['02', 'trn03']
                         ['02', 'trn04']
                         ['02', 'tst01']
                         ['02', 'tst02']
                         ['02', 'tst03']
                         ['02', 'tst04']
                         ['02', 'tst05']
                         ['02', 'tst06']
                         ['02', 'tst07']
                         ['02', 'tst08']]
    """
    dirAndFileNames = []
    dirs = getDirContent(dataFolder, 1)
    for dir in dirs:
        dirPath = dataFolder + "/" + dir
        dirOrFile = 0
        files = getDirContent(dirPath, dirOrFile)
        uniqueFileNames = rmPartsAndExt(files, defs)
        for uniqueFileName in uniqueFileNames:
            dirAndFileNames.append([dir, uniqueFileName])
    return dirAndFileNames

def filterForTrainOrTest(dirAndFileNames, trainOrTest, defs):
    """根据数据集的类型过滤 dirAndFileNames 数组

    Args:
        dirAndFileNames (List): 二维数组，第一列为目录名，第二列为文件名
        trainOrTest (Number): 1 for train， 2 for test, 0 for both
        defs (Defs): 参见 getFileNameDefs()

    Returns:
        result (List): 一维数组，长度与 dirAndFileNames 的行数相同，result[i] = True 表示需要 dirAndFileNames[i] 的数据
    
    Test1:
        dirAndFileNames: 参见 getAllFileNames()
        trainOrTest: 1
        defs:
        result: [True, True, True, True, False, False, False, False, False, False, False, False,\
                 True, True, True, True, False, False, False, False, False, False, False, False]

    Test2:
        dirAndFileNames: 参见 getAllFileNames()
        trainOrTest: 2
        defs:
        result: [False, False, False, False, True, True, True, True, True, True, True, True,\
                 False, False, False, False, True, True, True, True, True, True, True, True]
    
    Test3:
        dirAndFileNames: 参见 getAllFileNames()
        trainOrTest: 0
        defs:
        result: [True, True, True, True, True, True, True, True, True, True, True, True,\
                 True, True, True, True, True, True, True, True, True, True, True, True]
    """
    result = [False] * len(dirAndFileNames)

    if trainOrTest == 1:
        for idx, row in enumerate(dirAndFileNames):
            if row[1][:3] == defs.train:
                result[idx] = True
    elif trainOrTest == 2:
        for idx, row in enumerate(dirAndFileNames):
            if row[1][:3] == defs.test:
                result[idx] = True
    elif trainOrTest == 0:
        result = [True for _ in result]
    
    return result

def filterForCampaingNumbers(dirAndFileNames, campaingNumbers):
    """根据数据集的编号过滤 dirAndFileNames 数组

    Args:
        dirAndFileNames (List): 二维数组，第一列为目录名，第二列为文件名
        campaingNumbers (List): 数据集的编号

    Returns:
        result (List): 一维数组，长度与 dirAndFileNames 的行数相同，result[i] = True 表示需要 dirAndFileNames[i] 的数据
    
    Test1:
        dirAndFileNames: 参见 getAllFileNames()
        campaingNumbers: [2, 4]
        result: [False, True, False, True, False, True, False, True, False, False, False, False,\
                 False, True, False, True, False, True, False, True, False, False, False, False]
    """
    result = [False] * len(dirAndFileNames)

    for idx, row in enumerate(dirAndFileNames):
        number = int(row[1][3:])
        if number in campaingNumbers:
            result[idx] = True

    return result

def filterForMonthNumbers(dirAndFileNames, monthNumbers):
    """根据月份过滤 dirAndFileNames 数组

    Args:
        dirAndFileNames (List): 二维数组，第一列为目录名，第二列为文件名
        monthNumbers (Number): 月份

    Returns:
        result (List): 一维数组，长度与 dirAndFileNames 的行数相同，result[i] = True 表示需要 dirAndFileNames[i] 的数据
    
    Test1:
        dirAndFileNames: 参见 getAllFileNames()
        monthNumbers: 1
        result: [True, True, True, True, True, True, True, True, True, True, True, True,\
                 False, False, False, False, False, False, False, False, False, False, False, False]
    """
    result = [False] * len(dirAndFileNames)

    for idx, row in enumerate(dirAndFileNames):
        monthNumber = int(row[0])
        if monthNumber == monthNumbers:
            result[idx] = True

    return result

def filterFileNames(dirAndFileNames, trainOrTest, campaingNumbers, monthNumbers, defs):
    """根据 trainOrTest, campaingNumbers, monthNumbers 的值过滤 dirAndFileNames 数组

    Args:
        dirAndFileNames (List): 二维数组，第一列为目录名，第二列为文件名
        trainOrTest (Number): 1 for train， 2 for test, 0 for both
        campaingNumbers (List): 数据集的编号
        monthNumbers (Number): 月份
        defs (Defs): 参见 getFileNameDefs()

    Returns:
        result (List): 一维数组，长度与 dirAndFileNames 的行数相同，result[i] = True 表示需要 dirAndFileNames[i] 的数据
    
    Test1:
        dirAndFileNames: 参见 getAllFileNames()
        trainOrTest: 1
        campaingNumbers: [2, 4]
        monthNumbers: 1
        defs:
        result: [False, True, False, True, False, False, False, False, False, False, False, False,\
                 False, False, False, False, False, False, False, False, False, False, False, False]
    """
    result = [True] * len(dirAndFileNames)

    resTrainOrTest = filterForTrainOrTest(dirAndFileNames, trainOrTest, defs)
    resCampaingNumbers = filterForCampaingNumbers(dirAndFileNames, campaingNumbers)
    resMonthNumbers = filterForMonthNumbers(dirAndFileNames, monthNumbers)

    for i in range(len(result)):
        result[i] = result[i] and resTrainOrTest[i] and resCampaingNumbers[i] and resMonthNumbers[i]

    return result

def composeFileContent(fileName, dataFolder, defs):
    """获得 dataFolder 目录下的数据

    Args:
        fileName (String): 数据集和编号
        dataFolder (String): 目录
        defs (Defs): 

    Returns:
        fileContent (Data): dataFolder目录下的数据

    Test1:
        fileName: "trn02"
        dataFolder: "db/01"
    """
    rssPath = dataFolder + "/" + fileName + defs.rss + ".csv"
    rss = np.loadtxt(rssPath, delimiter=",")

    coordsPath = dataFolder + "/" + fileName + defs.coords + ".csv"
    coords = np.loadtxt(coordsPath, delimiter=",")

    timePath = dataFolder + "/" + fileName + defs.time + ".csv"
    time = np.loadtxt(timePath, delimiter=",")

    idsPath = dataFolder + "/" + fileName + defs.ids + ".csv"
    ids = np.loadtxt(idsPath, delimiter=",")

    fileContent = Data(rss, coords, time, ids)

    return fileContent

def loadContent(dataFolder, fileNames, result, defs):
    """先用result过滤fileNames，然后加载目标目录下的所有数据

    Args:
        dataFolder (String): 目录
        fileNames (List): getAllFileNames() 的返回值
        result (List): filterFileNames() 的返回值
        defs (Defs): 

    Returns:
        data (Data): 

    Test1:
        dataFolder: "db"
        fileNames: getAllFileNames() 的返回值
        result: filterFileNames() 的返回值
    """
    # 根据result获得文件和目录名
    newFileNames = []
    for idx, row in enumerate(fileNames):
        if result[idx]:
            newFileNames.append(row)
    
    # 遍历
    for idx, row in enumerate(newFileNames):
        fileContent = composeFileContent(row[1], dataFolder + "/" + row[0], defs)
        if idx == 0:
            rss = fileContent.rss.copy()
            coords = fileContent.coords.copy()
            time = fileContent.time.copy()
            ids = fileContent.ids.copy()
        else:
            rss = np.concatenate((rss, fileContent.rss))
            coords = np.concatenate((coords, fileContent.coords))
            time = np.concatenate((time, fileContent.time))
            ids = np.concatenate((ids, fileContent.ids))

    data = Data(rss, coords, time, ids)
    return data

def loadContentSpecific(dataFolder, trainOrTest, campaingNumbers, monthNumbers):
    """根据参数加载所需的数据

    Args:
        dataFolder (String): 目录
        trainOrTest (Number): 1 for train， 2 for test, 0 for both
        campaingNumbers (List): 数据集的编号
        monthNumbers (Number): 月份

    Returns:
        data (Data): [description]
    
    Test1:
        dataFolder: "db"
        trainOrTest: 1
        campaingNumbers: [2, 4]
        monthNumbers: 1
    """
    defs = getFileNameDefs()
    fileNames = getAllFileNames(dataFolder, defs)
    result = filterFileNames(fileNames, trainOrTest, campaingNumbers, monthNumbers, defs)
    data = loadContent(dataFolder, fileNames, result, defs)
    return data

if __name__ == "__main__":
    # 测试用的数据
    dataFolder = "db"
    defs = getFileNameDefs()
    fileNames = ['trn01crd.csv','trn01ids.csv','trn01rss.csv','trn01tms.csv','trn02crd.csv','trn02ids.csv','trn02rss.csv','trn02tms.csv',\
                'trn03crd.csv','trn03ids.csv','trn03rss.csv','trn03tms.csv','trn04crd.csv','trn04ids.csv','trn04rss.csv','trn04tms.csv',\
                'tst01crd.csv','tst01ids.csv','tst01rss.csv','tst01tms.csv','tst02crd.csv','tst02ids.csv','tst02rss.csv','tst02tms.csv',\
                'tst03crd.csv','tst03ids.csv','tst03rss.csv','tst03tms.csv','tst04crd.csv','tst04ids.csv','tst04rss.csv','tst04tms.csv',\
                'tst05crd.csv','tst05ids.csv','tst05rss.csv','tst05tms.csv','tst06crd.csv','tst06ids.csv','tst06rss.csv','tst06tms.csv',\
                'tst07crd.csv','tst07ids.csv','tst07rss.csv','tst07tms.csv','tst08crd.csv','tst08ids.csv','tst08rss.csv','tst08tms.csv']
    dirAndFileNames = [['01', 'trn01'], ['01', 'trn02'], ['01', 'trn03'], ['01', 'trn04'],\
                       ['01', 'tst01'], ['01', 'tst02'], ['01', 'tst03'], ['01', 'tst04'], ['01', 'tst05'], ['01', 'tst06'], ['01', 'tst07'], ['01', 'tst08'],\
                       ['02', 'trn01'], ['02', 'trn02'], ['02', 'trn03'], ['02', 'trn04'],\
                       ['02', 'tst01'], ['02', 'tst02'], ['02', 'tst03'], ['02', 'tst04'], ['02', 'tst05'], ['02', 'tst06'], ['02', 'tst07'], ['02', 'tst08']]
    
    # print(getDirContent(dataFolder, 1))
    # print(rmPartsAndExt(fileNames, defs))
    # print(getAllFileNames(dataFolder, defs))
    # print(filterForTrainOrTest(dirAndFileNames, 0, defs))
    # print(filterForCampaingNumbers(dirAndFileNames, [2, 4]))
    # print(filterForMonthNumbers(dirAndFileNames, 1))
    # print(filterFileNames(dirAndFileNames, 1, [2, 4], 1, defs))
    # print(composeFileContent("trn02", "db/01", defs))
    # print(loadContent(dataFolder, dirAndFileNames, filterFileNames(dirAndFileNames, 1, [2, 4], 1, defs), defs))
    # print(loadContentSpecific(dataFolder, 2, [2, 4, 6, 8], 1))