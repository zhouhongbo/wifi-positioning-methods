import os
import csv

def count(): 
    filename = os.listdir(".")[1]
    # 读取信号数据tmpRss中
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # 跳过表头
        tmpRss = [row[1].strip() for row in reader]
    # 计数
    count = 0
    for i in range(len(tmpRss)):
        if tmpRss[i] == "start" or tmpRss[i] == "resume":
            subRss = []
        elif tmpRss[i] == "pause":
            if len(subRss) >= 10: # 数据量大于等于10
                count += 1
        else:
            subRss.append(tmpRss[i])
    return count

if __name__ == "__main__":
    print(count())