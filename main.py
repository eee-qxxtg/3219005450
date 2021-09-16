# -*- codeing = utf-8 -*-
# @Time : 2021/9/9 16:11
# @Author : eee-qxxtg
# @File : main.py
# @Software : PyCharm


import os
import re
import jieba
import jieba.analyse
import eventlet
import hashlib
import json
import sys
import time


# 分词
def splitWords(text):
    with open(text, 'r', encoding='UTF-8') as f1:
        f2 = f1.read()
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")  # 匹配过滤
    s = pattern.sub("", f2)
    f1.close()
    length = len(list(jieba.lcut(s)))  # length为分词后词的个数
    string = jieba.analyse.extract_tags(s, topK=length)  # 提取主题词
    return string


# simhash
def getSimh(s):
    i = 0
    weight = len(s)
    fv = [0] * 128  # feature vector
    for word in s:  # 计算各个特征向量的hash值
        m = hashlib.md5()  # 获取一个md5加密算法对象
        m.update(word.encode("utf-8"))
        hashc = bin(int(m.hexdigest(), 16))[2:]  # 获取加密后的二进制字符串，并去掉开头的'0b'
        if len(hashc) < 128:  # hash值需在低位以0补齐128位
            dif = 128 - len(hashc)
            for d in range(dif):
                hashc += '0'
        for j in range(len(fv)):  # 给所有特征向量进行加权
            if hashc[j] == '1':  # 合并特征向量的加权结果
                fv[j] += (10 - (10 * i / weight))
            else:
                fv[j] -= (10 - (10 * i / weight))
        i += 1
    simh = ''
    for k in range(len(fv)):  # 降维
        if fv[k] >= 0:  # 对于n-bit签名的累加结果，大于0则置1，否则置0
            simh += '1'
        else:
            simh += '0'
    return simh


# 计算海明距离得出相似度
def getSimilarity(simh1, simh2):
    d = 0
    if len(simh1) != len(simh2):
        d = -1
    else:
        for i in range(len(simh1)):
            if simh1[i] != simh2[i]:
                d += 1
    s = 0.01 * (100 - d * 100 / 128)
    return s


def test():
    eventlet.monkey_patch()
    with eventlet.Timeout(5, False):  # 设置超时时间为5秒
        time.sleep(10)
        input()
    path1 = ','.join(sys.argv[1:2])  # 获取命令行参数 将列表转换为字符串
    path2 = ','.join(sys.argv[2:3])
    path3 = ','.join(sys.argv[3:])
    if not os.path.exists(path1):
        print("论文原文不存在！")
        exit()
    if not os.path.exists(path2):
        print("抄袭论文不存在！")
        exit()
    simhash1 = getSimh(splitWords(path1))
    simhash2 = getSimh(splitWords(path2))
    s1 = getSimilarity(simhash1, simhash2)
    s2 = round(s1, 2)  # 精确到小数点后两位
    print('文章相似度为:%f' % s2)
    with open(path3, 'a', encoding='utf-8')as f:  # 将结果写入指定路径path3
        f.write(path2 + '与原文的相似度为：')
        f.write(json.dumps(s2, ensure_ascii=False) + '\n')
    return s2


if __name__ == '__main__':
    test()
