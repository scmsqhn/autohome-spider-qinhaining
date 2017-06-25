#!/usr/bin/env python                                                                                  
# coding=utf-8

from matplotlib.pyplot import plot,savefig  
import matplotlib  
matplotlib.use('Agg')
import numpy as np
from pylab import *
from numpy import *
from prtUtil import PrintUtil as prt


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
    print "the error rate of this test is: %f" % errorRate  
    return errorRate  
  
def multiTest():  
    numTests = 10; errorSum=0.0  
    for k in range(numTests):  
        errorSum += colicTest()  
    print "after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests))  

def train_wb(X, y):
    """
    :param X:N*D的数据
    :param y:X对应的y值
    :return: 返回（w，b）的向量
    """
    print 'train_wb;'
    if np.linalg.det(X.T * X) != 0:
        # 判断矩阵X与X.T相乘的行列式不为0,
        wb = ((X.T.dot(X).I).dot(X.T)).dot(y)
        print "(X.T.dot(X).I)", X.T.dot(X).I
        print '===='
        print "(X.T.dot(X)", X.T.dot(X)
        print '===='
        print "((X.T.dot(X).I).dot(X.T))", ((X.T.dot(X).I).dot(X.T))
        print '===='
        print 'wb= ', wb 
        print '===='
        return wb
        #获得数据的函数，其中数据下载自

#http://download.csdn.net/detail/google19890102/7386709
def getdata():
    x = []; y = []
    file = open("C:\\Users\\cjwbest\\Desktop\\ex0.txt", 'r')
    for line in file.readlines():
        temp = line.strip().split("\t")
        x.append([float(temp[0]),float(temp[1])])
        y.append(float(temp[2]))
    return (np.mat(x), np.mat(y).T)
    
def test(x, wb):
    return x.T.dot(wb)

def getdata():
    x = []; y = []
    file = open("../data_collection/ex0.txt", 'r')
    for line in file.readlines():
        #print line
        temp = line.strip().split("\t")
        x.append([float(temp[0]),float(temp[1])])
        y.append(float(temp[2]))
        #prtutil.prt('getdata x y')
    #for ix in x:
        #print ix
    #for iy in y:
        #print iy
                
    #print np.mat(x)
    #print np.mat(y)
    #print np.mat(y).T

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


if __name__=="__main__":
  prtutil = prt()
  prtutil.setPrintEnable()
  demoLinearRegression()

