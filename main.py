import numpy as np
from os import listdir
import operator
import cv2
from PIL import Image
import math
import matplotlib.pyplot as plt

# 开始程序
# input： none
# output yourNumber：最后得到的结果
def loadproject():
    while(1):
        print("是否开始识别（Y/N）：")
        initial = input()
        if(initial == 'N'):
            break
        else:
            #getOnePicture()
            #imageToGray()
            #exponentiation()
            # grayToSmaller()
            # canny()
            imgToCanny()
            #binaryToStandard()
            #grayToBinary()

            # trainData, labelVec, testData, testLabelVec = dataSetClassfication()
            # precisionRateTest(trainData, labelVec, testData, testLabelVec)
            # classfication(testData, trainData, labelVec, num = 25)

# 从视频流中截取一帧图片
# input：视频流
# output：yourImage 需要处理的图片
def getOnePicture():
    cameraCapture = cv2.VideoCapture(0)       # 不知道摄像头设备索引
    fps = 30                      #不知道帧率
    size = (int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    videoWriter = cv2.VideoWriter(
        'C:/Users/18139/Desktop/getcamera/first.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'),
        fps, size
    )             # 定义文件放置位置  cv2.VideoWriter_fourcc('I', '4', '2', '0')这里的编码格式也要确定
    success, frame = cameraCapture.read()   # 判断是否取得了有效值   frame应该是某一帧
    numFramesRemaining = 10
    while success and numFramesRemaining > 0:
        cv2.imwrite('C:/Users/18139/Desktop/getcamera/initPicture.jpg', frame)
        videoWriter.write(frame)           # 将读取到的帧写入视频
        success, frame = cameraCapture.read()
        numFramesRemaining -= 1
    cameraCapture.release()
    img1 = cv2.imread('C:/Users/18139/Desktop/getcamera/initPicture.jpg')          # 需要改图片
    cv2.namedWindow("Image")  # 可加可不加，加上的话一般和imshow之间会定义一些窗口事件处理用函数
    cv2.imshow('Image', img1)  # 显示图片
    if cv2.waitKey(1000) == 27 :
        cv2.destroyAllWindows()  # 释放所有窗口


# 数字图像处理1   转为灰度图
# input：yourImage 从视频流中截取的图片
# output：txt 处理后的灰度化图片
def imageToGray():
    img2 = Image.open('C:/Users/18139/Desktop/getcamera/initPicture.jpg').convert("L")
    img2.save('C:/Users/18139/Desktop/getcamera/grayPicture.bmp')
    img2.show()
    img_array = np.array(img2)
    w, h = img_array.shape
    print(w,h)
    fp = open('C:/Users/18139/Desktop/getcamera/array.txt', 'w')
    for i in img_array:
        fp.write(str(i))
    fp.close()

# 数字图像处理2   利用插值法降低像素   暂时用后面的替代
# input: 灰度化图片
# output：降低后像素的图片
def grayToSmaller():
    image2 = Image.open('C:/Users/18139/Desktop/getcamera/grayPicture.bmp')
    img_array = np.array(image2)
    a = img_array.shape
    img_array2 = cv2.resize(img_array, (int(a[1] / 1.5), int(a[0] / 1.5)), interpolation=cv2.INTER_AREA)  # 可更改数据调整
    image3 = Image.fromarray(img_array2)
    image3.save('C:/Users/18139/Desktop/getcamera/picture3.bmp')


# 数字图像处理3 利用canny算子实现边缘检测    高斯滤波  计算梯度值与方向   非极大值抑制（NMS） 双阀值选取（这样精度更高）边缘连接    **************
# input: 降低像素后的图片
# output：边缘检测后的图片
def imgToCanny():
    image = Image.open('C:/Users/18139/Desktop/getcamera/grayPicture.bmp')
    img_array = np.array(image)
    c = 1
    r = 2
    a = c * ((img_array / 255) ** r * 255)
    # image2 = Image.fromarray(a.astype(np.int))
    # image = Image.open('C:/Users/18139/Desktop/getcamera/grayPicture.bmp')
    # img_array = np.array(image)
    img_array2 = cv2.Canny(a, 50, 150)
    image2 = Image.fromarray(img_array2)
    image2.save('C:/Users/18139/Desktop/getcamera/cannyPicture.bmp')
    image2.show()

# 数字图像处理4 A4纸矫正                    **********
# input：顶点提取后的图片
# output：矫正后的图片Y

# 数字图像处理5 插值法将图像化为标准大小    (需要注意的是，插值法会将二值化图片变成非二值化，要在二值化之前进行）
# input：单个图片
# output：标准图并储存
def binaryToStandard():
    image4 = Image.open('C:/Users/18139/Desktop/getcamera/grayPicture.bmp')
    img_array = np.array(image4)
    a = img_array.shape
    b = a[0]/32
    c = a[1]/32
    img_array2 = cv2.resize(img_array, (int(a[1] / c), int(a[0] / b)), interpolation=cv2.INTER_AREA)  # 可更改数据调整
    fp = open('C:/Users/18139/Desktop/getcamera/array2.txt', 'w')
    for i in img_array2:
        fp.write(str(i))
    fp.close()
    image5 = Image.fromarray(img_array2)
    image5.save('C:/Users/18139/Desktop/getcamera/standSizePicture.bmp')

# 数字图像处理6  图像二值化   全阈值（这个简单）
# input：提取后的图像
# output； 二值化图片
def grayToBinary():
    image3 = Image.open('C:/Users/18139/Desktop/getcamera/standSizePicture.bmp')
    img_array = np.array(image3)
    img_array2 = img_array
    for i in range(img_array.shape[0]-1):
        for j in range(img_array.shape[1]-1):
            if (img_array[i][j] >= 100):
                img_array2[i][j] = 255
            else:
                img_array2[i][j] = 0
    fp = open('C:/Users/18139/Desktop/getcamera/array3.txt', 'w')
    for i in img_array2:
        fp.write(str(i))
    fp.close()
    image4 = Image.fromarray(img_array2)
    image4.save('C:/Users/18139/Desktop/getcamera/binaryPicture.bmp')

# 数字图像处理7  垂直方向分割后水平方向分割（统计方面）      ***
# input：二值化的灰度图
# output：分割后的子图（前期处理会使数字断裂）

# 数字图像处理8 子图进行断裂字符修复（滤波器原理）         ***
# input：分割后子图
# output：修复后的子图

# 数字图像处理9  连通域标记法从左到右分割数字          ***
# input：切割后无断点的子图
# output：多个数字切割后的框图

# 数字图像处理10 切割后的每个数字，分离并进行储存为所需格式      ***
# input：切割后带框图的数字
# output：单个带标签（不是数字标签，是位置标签）的表


# 图像数据矩阵变换为向量
# input：imageFileName 处理后二值化的图片； height 图片高度； weight 图片宽度
# output：imageVec 转化后的行向量
def Mat2Vec(imageFileName, height, weight):
    imageVec = np.zeros((1, height*weight))
    fileread = open(imageFileName)
    for i in range(height):
        linestr = fileread.readline()
        for j in range(weight):
            imageVec[0, 32*i+j] = int(linestr(j))
    return imageVec

# 数据可视化         *****************
# input：trainData 用于训练的数据 ；testData 用于测试的数据； labelVec 数据标签
# output：输出图像
def viewTheData():
    return 0

# 分类并处理标准数据集
# input：filename 数据集地址
# output：trainData 用于训练的数据 ；testData 用于测试的数据； labelVec 数据标签; testLabelVec 测试集标签
def dataSetClassfication():
    height = 32
    weight = 32
    pixels = height*weight       # 这里1024需要换为具体我们数据处理得到的像素点的个数
    print("enter the path to the trainSet:")
    trainSetFileName = input()  # 加入文件名
    print("enter the path to the testSet:")
    testSetFileName = input()
    trainDatalist = listdir(trainSetFileName)
    dataNumber = len(trainDatalist)
    trainData = np.zeros((dataNumber, pixels))
    labelVec = []
    for i in range(dataNumber):
        fileHeadName = trainDatalist[i]
        classNumber = int(fileHeadName.split('_')[0])  # 因为在储存的数据时，文件名第一个字符是具体哪个数字
        labelVec.append(classNumber)
        trainData[i, :] = Mat2Vec(trainSetFileName+'/'+fileHeadName, height, weight)
    testDataList = listdir(testSetFileName)
    testNumber = len(testDataList)
    testData = np.zeros((testNumber, pixels))
    testLabelVec = []
    for i in range(testNumber):
        fileHeadName = testDataList[i]
        classNumber = int(fileHeadName.split('_')[0])
        testLabelVec.append(classNumber)
        testData[1, :] = Mat2Vec(testSetFileName+'/'+fileHeadName, height, weight)
    return trainData, labelVec, testData, testLabelVec

# 准确率测试
# input：trainData 用于训练的数据 ；testData 用于测试的数据； labelVec 数据标签; testLabelVec 测试集标签
# output：precisionRate 准确率
def precisionRateTest(trainData, labelVec, testData, testLabelVec):
    num = 25 # 附近数据个数
    errorCount = 0
    testNumber = len(testLabelVec)
    for i in range(testNumber):
        yourNumber = classfication(testData[i], trainData, labelVec, num)
        print("your number :%d true number :%d" % (yourNumber, testLabelVec[i]))
        if (yourNumber != testLabelVec[i]):
            errorCount += 1
    print("precisionRata: %f%%" %(errorCount/testNumber))

# KNN分类器模型
# input：trainData 训练集；testData 测试集/ yourData 需要分辨的数据； labelVec 数据标签； num 附近数据个数
# output：yourNumber 分类得到的数据
def classfication(testData, trainData, labelVec, num):
    disMat = np.tile(testData, (trainData.shape[0], 1))-trainData
    disMat2 = disMat**2
    disMat3 = disMat2.sum(axis=1)
    disMat4 = disMat3**0.5
    sortDistant = disMat4.argsort()   # 得到索引值
    classCount = {}
    for i in range(num):
        labels = labelVec[sortDistant[i]]
        classCount[labels] = classCount.get(labels, 0) + 1
    sortClaccCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    yourNumber = sortClaccCount[0][0]
    return yourNumber

loadproject()