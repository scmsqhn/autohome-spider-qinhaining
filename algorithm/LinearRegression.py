#!/usr/bin/env python                                                                                  
# coding=utf-8

'''''
代码是什么?
一个置信度64%的汽车价格预测模型

优化步骤:
1. 分布式按置信度权重相加
2. 增加电子组件部分参数
3. 增加品牌估值参数
'''

import sys
sys.path.append('.')
sys.path.append('..')
from matplotlib.pyplot import plot,savefig  
import matplotlib  
matplotlib.use('Agg')
import numpy as np
from pylab import *
from numpy import *
from prtUtil import PrintUtil as prt
from db.RedisHelper import RedisHelper
from db.MongoHelper import MongoHelper
reload(sys)
sys.setdefaultencoding('utf-8')

# 配置打印输出
prtutil = prt()
prtutil.setPrintEnable()


'''''读取遍历文件
'''
def loadDataSet(filename):                          #遍历函数，打开文本文件testSet.txt并进行逐行读取  
    fn = filename
    dataMat = []
    labelMat = []
    fr = open(fn)
    for line in fr.readlines():
        lineArr = line.strip().split()        #去掉文件中换行符且划分文件为行  
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])]) #将X0的值设为1，因为公式w0+w1x1+w2x2  
        labelMat.append(int(lineArr[2]))  
    return dataMat,labelMat  
  
'''''激活函数
'''
def sigmoid(inX):                             #sigmoid函数  
    return 1.0/(1+exp(-inX))  

'''''
'''    
def gradAscent(dataMatIn, classLabels):    #梯度上升算法计算最佳回归系数  
    dataMatrix = mat(dataMatIn)                   #获得输入数据并将样本数组转换为矩阵  
    labelMat = mat(classLabels).transpose()    #将类标签数组转换为项链并将其转置  
    m,n = shape(dataMatrix)                     #得到矩阵的大小  
    alpha = 0.001                        #步长  
    maxCycles = 500                      #迭代次数  
    weights = ones((n,1))                #回归系数初始化为1,n*1的向量  
    for k in range(maxCycles):                  #遍历数组  
        h = sigmoid(dataMatrix*weights)     #h是一个列向量，元素个数等于样本个数，矩阵相乘  
        error = (labelMat - h)                     #误差计算，向量减法运算  
        weights = weights + alpha * dataMatrix.transpose()* error    #矩阵相乘，dataMatrix.transpose()*error就是梯度f(w)  
    return weights  
  
def plotBestFit(weights):                    #画出训练点  
    import matplotlib.pyplot as plt  
    dataMat,labelMat=loadDataSet()      #画点  
    dataArr = array(dataMat)  
    n = shape(dataArr)[0]   
    xcord1 = []; ycord1 = []  
    xcord2 = []; ycord2 = []  
    for i in range(n):  
        if int(labelMat[i])== 1:  
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])  
        else:  
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])  
    fig = plt.figure()  
    ax = fig.add_subplot(111)  
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')  
    ax.scatter(xcord2, ycord2, s=30, c='green')  
    x = arange(-3.0, 3.0, 0.1)                          #画线，x取值区间为[-3.0,3.0],步长为0.1  
    y = (-weights[0]-weights[1]*x)/weights[2]  
    ax.plot(x, y)  
    plt.xlabel('X1')  
    plt.ylabel('X2')  
    plt.show()      #显示  
  
def stocGradAscent0(dataMatrix, classLabels):    #随机梯度上升算法  
    m,n = shape(dataMatrix)  
    alpha = 0.01  
    weights = ones(n)          #初始化单位矩阵，维度为数据集列数  
    for i in range(m):  
        h = sigmoid(sum(dataMatrix[i]*weights))  
        error = classLabels[i] - h  
        weights = weights + alpha * error * dataMatrix[i]  
    return weights  
  
def stocGradAscent1(dataMatrix, classLabels, numIter=150):       #升级后的梯度上升算法——随机梯度下降  
    m,n = shape(dataMatrix)  
    weights = ones(n)           #i初始化单位矩阵  
    for j in range(numIter):  
        dataIndex = range(m)  
        for i in range(m):  
            alpha = 4/(1.0+j+i)+0.0001             #alpha的值每次迭代时都会进行调整，会缓解数据波动或者高频波动  
            randIndex = int(random.uniform(0,len(dataIndex))) #随机选取更新回归系数，减少周期性波动  
            h = sigmoid(sum(dataMatrix[randIndex]*weights))  #梯度计算的结果，一个列向量  
            error = classLabels[randIndex] - h  
            weights = weights + alpha * error * dataMatrix[randIndex]  
            del(dataIndex[randIndex])  
    return weights  
  
def classifyVector(inX, weights):  
    prob = sigmoid(sum(inX*weights))            #判别算法  
    if prob > 0.5: return 1.0             #prob>0.5,返回为1  
    else: return 0.0           #否则，返回0  
  
def colicTest():                      #随机梯度算法实例  
    frTrain = open('horseColicTraining.txt')  
    frTest = open('horseColicTest.txt')         #导入训练集文件  
    trainingSet = []  
    trainingLabels = []  
    for line in frTrain.readlines():  
        currLine = line.strip().split('\t')  
        lineArr =[]  
        for i in range(21):  
            lineArr.append(float(currLine[i]))  
        trainingSet.append(lineArr)          #构建训练数据集  
        trainingLabels.append(float(currLine[21]))     #构建分类标签训练集  
    trainWeights = stocGradAscent1(array(trainingSet), trainingLabels, 1000)  
    errorCount = 0  
    numTestVec = 0.0  
    for line in frTest.readlines():  
        numTestVec += 1.0  
        currLine = line.strip().split('\t')  
        lineArr =[]  
        for i in range(21):  
            lineArr.append(float(currLine[i]))  
        if int(classifyVector(array(lineArr), trainWeights))!= int(currLine[21]):
        #对输入向量分类，currLine[21]为分类标签  
            errorCount += 1  #如果不相等，误差数+1  
    errorRate = (float(errorCount)/numTestVec)     #最后计算误差率：误差数/记录数  
    #print "the error rate of this test is: %f" % errorRate  
    return errorRate  
  
def multiTest():  
    numTests = 10; errorSum=0.0  
    for k in range(numTests):  
        errorSum += colicTest()  
    #print "after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests))  

def train_wb(X, y):
    """
    :param X:N*D的数据
    :param y:X对应的y值
    :return: 返回（w，b）的向量
    """
    #print 'train_wb;'
    if np.linalg.det(X.T * X) != 0:
        # 判断矩阵X与X.T相乘的行列式不为0,
        wb = ((X.T.dot(X).I).dot(X.T)).dot(y)
        #print "(X.T.dot(X).I)", X.T.dot(X).I
        #print '===='
        #print "(X.T.dot(X)", X.T.dot(X)
        #print '===='
        #print "((X.T.dot(X).I).dot(X.T))", ((X.T.dot(X).I).dot(X.T))
        #print '===='
        #print 'wb= ', wb 
        #print '===='
        return wb
        #获得数据的函数，其中数据下载自

    
def test(x, wb):
    return x.T.dot(wb)

def getdata():
    x = []; y = []
    file = open("../data_collection/ex0.txt", 'r')
    for line in file.readlines():
        ##print line
        temp = line.strip().split("\t")
        x.append([float(temp[0]),float(temp[1])])
        y.append(float(temp[2]))
        #prtutil.prt('getdata x y')
    #for ix in x:
        ##print ix
    #for iy in y:
        ##print iy
                
    #print np.mat(x)
    ##print np.mat(y)
    ##print np.mat(y).T

    return (np.mat(x), np.mat(y).T)

def draw(x, y, wb):
    #画回归直线y = wx+b
    a = np.linspace(0, np.max(x)) #横坐标的取值范围
    b = wb[0] + a * wb[1]
    plot(x, y, '.')
    plot(a, b)
    show()

'''''
线性回归demo展示代码
'''
def demoLinearRegression():
  X, y = getdata()
  wb = train_wb(X, y)
  draw(X[:, 1], y, wb.tolist())

def mulitiLinearRegression(xin, yin, size):
  from sklearn.linear_model import LinearRegression
#  X = [[6, 2], [8, 1], [10, 0], [14, 2], [18, 0]]
#  y = [[7], [9], [13], [17.5], [18]]
  mylen = len(yin)
  lstRandom = [0 for n in range(size)]
  for i in range(size):
    lstRandom[i] = random.randint(0, mylen)
    
  x = [xin[n] for n in lstRandom]
  y = [yin[n] for n in lstRandom]
  model = LinearRegression()
  model.fit(x, y)
  #print x,y
  
  lstRandom = [0 for n in range(size)]
  for i in range(size):
    lstRandom[i] = random.randint(0, mylen)
    
  X_test = [xin[n] for n in lstRandom]
  y_test = [yin[n] for n in lstRandom]
  print '[x] \n',x,X_test,y_test,y
  #X_test = [[8, 2], [9, 0], [11, 2], [16, 2], [12, 0]]
  #y_test = [[11], [8.5], [15], [18], [11]]
  predictions = model.predict(X_test)
  for i, prediction in enumerate(predictions):
    pass
    print('预测值: %s, 目标值: %s' % (prediction, y_test[i]))
    print('Predicted: %s, Target: %s' % (prediction, y_test[i]))
  print('置信度: %.2f' % model.score(X_test, y_test))
  print('R-squared: %.2f' % model.score(X_test, y_test))
  pass

def reSub(instr):
  import re
  instr = re.sub('[^(\d+(\.\d+)?)]', '', instr)
  return instr
  
  
if __name__=="__main__":

  mongoDB = MongoHelper("autohome", "config")
  dataMod1 = [u"厂商指导价", u"排量(mL)", u"最大扭矩转速(rpm)", \
    u"发动机", u"最大功率(kW)", u"变速箱", u"最大扭矩(N・m)",\
    u"最大马力(Ps)",  u"排量(L)"]
  dataMod4 = [u"厂商指导价", u"气缸数(个)", u"排量(mL)", \
    u"最大扭矩转速(rpm)", \
    u"发动机", u"最大功率(kW)", u"变速箱", u"最大扭矩(N・m)",\
    u"挡位个数", u"最大马力(Ps)",  u"排量(L)", u"每缸气门(个)"]
  dataMod3 = [u"厂商指导价", u"气缸数(个)", u"排量(mL)", \
    u"最大扭矩转速(rpm)", \
    u"发动机", u"最大功率(kW)", u"变速箱", u"最大扭矩(N・m)",\
    u"挡位个数", u"最大马力(Ps)",  u"排量(L)", u"每缸气门(个)"]
  dataMod2 = [u"厂商指导价", u"气缸数(个)", u"排量(mL)", \
    u"最大扭矩转速(rpm)", \
    u"发动机", u"最大功率(kW)", u"座位数(个)", u"变速箱", u"车门数(个)",  u"最大扭矩(N・m)",\
    u"挡位个数", u"最大马力(Ps)",  u"排量(L)", u"每缸气门(个)"]
  dataMod = [u"厂商指导价", u"长度(mm)", u"轴距(mm)", u"气缸数(个)", u"排量(mL)", \
    u"最大扭矩转速(rpm)", u"宽度(mm)",\
    u"发动机", u"最大功率(kW)", u"座位数(个)", u"变速箱", u"车门数(个)",  u"最大扭矩(N・m)",\
    u"挡位个数", u"最大马力(Ps)",  u"排量(L)", u"每缸气门(个)", \
    u"长*宽*高(mm)", u"前轮胎规格", u"后轮胎规格", u"燃油标号"]
  errorCount = 0
  allData = mongoDB.select(None, None)
  mylen = len(allData)
  lstConf = [0 for n in range(mylen)]
  lstPric = [0 for n in range(mylen)]
  j = 0
  for item in allData:
    dataCell = [0 for n in range(0,len(dataMod))]
    i = 0
    try:
      for set in dataMod:
        ##print type(set)
        if isinstance(set, byte):
          import chardet
          ##print chardet.detect(set)
        dataCell[i] = item[set].split('~')[0].split('-')[0].split(' ')[0]
        dataCell[i] = reSub(dataCell[i])
        if dataCell[i] == "":
          #print '[x] 注意该值为空: ',set, item[set]
          dataCell[i] = "0.0"
        dataCell[i] = float(dataCell[i])
        i+=1
      if not dataCell is None:
        lstConf[j] = dataCell    
        j+=1
    except:
      import traceback
      #print traceback.#print_exc()
      errorCount+=1
      continue
  arraySize = 0    
  for i in range(0, len(lstConf)):
    if not lstConf[i] == 0:
      #print i, lstConf[i], lstConf[i][0]
      lstPric[i] = lstConf[i][0]
      lstConf[i] = lstConf[i][1:]
      arraySize = i
  lstPric = np.array(lstPric[:arraySize])
  lstConf = np.array(lstConf[:arraySize])
  #print len(lstConf), len(lstPric)
  mulitiLinearRegression(lstConf, lstPric, arraySize)