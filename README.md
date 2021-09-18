| 这个作业属于哪个课程 | [软件工程](https://edu.cnblogs.com/campus/gdgy/InformationSecurity1912-Softwareengineering) |
| ----------------- |--------------- |
| 这个作业要求在哪里| [个人项目作业](https://edu.cnblogs.com/campus/gdgy/InformationSecurity1912-Softwareengineering/homework/12146) |
| 这个作业的目标 | 设计一个论文查重算法 |
| Github 链接 | https://github.com/eee-qxxtg/3219005450 |

[TOC]

##1. 接口的设计与实现过程

- **核心算法——[simhash算法](https://blog.csdn.net/nanfeng224/article/details/39122859)**
simhash算法分为5个步骤：分词、hash、加权、合并、降维

- **关键函数**
main.py中定义了四个函数：
  - def splitWords(text)  ——  分词
  - def getSimh(s)  ——  hash、加权、合并、降维
  - def getSimilarity(simh1, simh2)  ——  计算海明距离和相似度
  - def test()

simhash算法的代码实现：
  ```python
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
  ```

- **命令行测试**
格式：python main.py [原文文件] [抄袭版论文的文件] [答案文件]
![](https://img2020.cnblogs.com/blog/2525608/202109/2525608-20210915230950388-1513020617.png)


##2. 性能分析及改进
- **性能分析**
使用pycharm自带的profile方法进行性能分析
![](https://img2020.cnblogs.com/blog/2525608/202109/2525608-20210915230804664-1180817818.png)

- **性能改进**
![](https://img2020.cnblogs.com/blog/2525608/202109/2525608-20210916203101168-1271090208.png)
可以看出splitWords函数耗时较多，故用正则表达式匹配过滤对其改进。

  - **原始代码：**
    ```python
    def splitWords(text):
        with open(text, 'r', encoding='UTF-8') as f1:
            f2 = f1.read()
        f1.close()
        length = len(list(jieba.lcut(f2))) 
        s = jieba.analyse.extract_tags(f2, topK=length) 
        return s
    ```
    直接用jieba.lcut处理文本，显得过于臃肿。

  - **改进代码：**
    ```python
    def splitWords(text):
        with open(text, 'r', encoding='UTF-8') as f1:
            f2 = f1.read()
        pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")  
        s = pattern.sub("", f2)
        f1.close()
        length = len(list(jieba.lcut(s)))
        string = jieba.analyse.extract_tags(s, topK=length) 
        return string
    ```
    先用正则表达式匹配过滤，再用jieba.lcut来处理，提高效率。

##3. 单元测试
- 为了方便测试，将test函数修改为：
  ```python
  def test():
      path1 = input("请输入论文原文的路径：")
      path2 = input("请输入抄袭论文的路径：")
      path3 = 'save.txt'
      simhash1 = getSimh(splitWords(path1))
      simhash2 = getSimh(splitWords(path2))
      s1 = getSimilarity(simhash1, simhash2)
      s2 = round(s1, 2)  
      print('文章相似度为:%f' % s2)
      with open(path3, 'a', encoding='utf-8')as f: 
          f.write(path2 + '与原文的相似度为：')
          f.write(json.dumps(s2, ensure_ascii=False) + '\n')
      return s2
  ```

- **新建单元测试文件test.py**
  ```python
  import unittest
  from main import test


  class MyTestCase(unittest.TestCase):
      def test_something1(self):
          self.assertEqual(test(), 0.70)

      def test_something2(self):
          self.assertEqual(test(), 0.71)

      def test_something3(self):
          self.assertEqual(test(), 0.79)

      def test_something4(self):
          self.assertEqual(test(), 0.65)

      def test_something5(self):
          self.assertEqual(test(), 0.55)


  if __name__ == '__main__':
      unittest.main()
  ```

- **测试结果**
![](https://img2020.cnblogs.com/blog/2525608/202109/2525608-20210916203038526-837371660.png)

##4. 异常处理
- **在命令行以“python main.py [原文文件] [抄袭版论文的文件] [答案文件]”的格式运行程序不会出错，但在pycharm中运行报错。**
![](https://img2020.cnblogs.com/blog/2525608/202109/2525608-20210916231745638-854663740.png)
  - **原因：**在读取指定文件时，文件路径不存在，程序出现异常。
  - **解决方法：**用input()语句接收输入，一段时间后未输入则跳出，并引入os.path.exists()方法用于检验文件是否存在，若不存在则做出响应并且结束程序。
  - **代码修改如下：**
    ```python
    def test():
    +   eventlet.monkey_patch()
    +   with eventlet.Timeout(5, False): 
    +       time.sleep(10)
    +       input()
        path1 = ','.join(sys.argv[1:2]) 
        path2 = ','.join(sys.argv[2:3])
        path3 = ','.join(sys.argv[3:])
    +    if not os.path.exists(path1):
    +       print("论文原文不存在！")
    +       exit()
    +   if not os.path.exists(path2):
    +       print("抄袭论文不存在！")
    +       exit()
        simhash1 = getSimh(splitWords(path1))
        simhash2 = getSimh(splitWords(path2))
        s1 = getSimilarity(simhash1, simhash2)
        s2 = round(s1, 2) 
        print('文章相似度为:%f' % s2)
        with open(path3, 'a', encoding='utf-8')as f:  
            f.write(path2 + '与原文的相似度为：')
            f.write(json.dumps(s2, ensure_ascii=False) + '\n')
        return s2
    ```
  - **修改后程序正常运行：**
![](https://img2020.cnblogs.com/blog/2525608/202109/2525608-20210916232534228-418957393.png)


##5. PSP
| PSP2.1                                    | Personal Software Process Stages | 预估耗时（分钟） | 实际耗时（分钟） |
| ----------------------------------------- | -------------------------------- | --------------- | -------------- |
| Planning                                  | 计划                              | 30   | 20   |
| Estimate                                  | 估计这个任务需要多少时间            | 2250  | 2110 |
| Development                               | 开发                              | 1200  | 1000 |
| Analysis                                  | 需求分析 (包括学习新技术)           | 240  | 360  |
| Design Spec                               | 生成设计文档                       | 60   | 30   |
| Design Review                             | 设计复审                           | 30   | 25   |
| Coding Standard                           | 代码规范 (为目前的开发制定合适的规范) | 30   | 30   |
| Design                                    | 具体设计                            | 60   | 40   |
| Coding                                    | 具体编码                            | 200  | 240  |
| Code Review                               | 代码复审                            | 60   | 50   |
| Test                                      | 测试（自我测试，修改代码，提交修改)   | 120  | 80   |
| Reporting                                 | 报告                               | 90   | 90   |
| Test Repor                                | 测试报告                           | 60   | 80   |
| Size Measurement                          | 计算工作量                         | 10   | 15   |
| Postmortem & Process Improvement Plan     | 事后总结, 并提出过程改进计划        | 60   | 50   |
|                                           | 合计                              | 2250 | 2110 |      
