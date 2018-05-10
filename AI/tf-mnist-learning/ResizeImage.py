# encoding: utf-8
import os

from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm

srcDir = '20-pixel-numbers'
dstDir = 'pic'


# 显示图片
def showImg(image):
    plt.imshow(image, cmap=cm.binary)
    plt.show()


# 按比例调整图片大小
def resizeImage(image, width=None, height=None, inter=cv2.INTER_AREA):
    # 获取图像尺寸
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image

    # 高度算缩放比例

    if (w > h):
        newsize = (width, round(h / (w / width)))
    else:
        newsize = (round(w / (h / height)), height)

        # print(newsize)

    # 缩放图像
    newimage = cv2.resize(image, newsize, interpolation=inter)
    print("w:", w)
    print("width:", width)
    print("h:", h)
    print("height:", height)
    print(newsize)

    return newimage


# 创建新的黑色图片
def createBianryImage(bg=(0, 0, 0), width=28, height=28):
    channels = 1

    image = np.zeros((width, height, channels), np.uint8)  # 生成一个空灰度图像
    # cv2.rectangle(image,(0,0),(width,height),bg,1, -1)

    return image.reshape(width, height)


# 两个不同大小的图片合并
def mergeImage(bg, fg, x, y):
    bgH, bgW = bg.shape[:2]
    fgH, fgW = fg.shape[:2]

    for i in range(fgH):
        for j in range(fgW):
            if (y + i < bgH and x + j < bgW):
                # print('xx', y+i, x+j)
                bg[y + i, x + j] = fg[i, j]  # 这里可以处理每个像素点

    return bg


# 求像素重心。传入二值图像，其中白色点算重量，黑色点为空
def getBarycentre(image):
    h, w = image.shape[:2]

    sumWeightW = 0
    sumWeightH = 0

    count = 0

    for i in range(h):
        for j in range(w):
            if (image[i, j] > 128):
                sumWeightW += j
                sumWeightH += i
                count += 1

    if (count == 0):
        count = 1

    print('getBarycentre: ', round(sumWeightW / count), round(sumWeightH / count))
    return (round(sumWeightW / count), round(sumWeightH / count))


def getFileList(strDir, strType='.png'):
    lstSrcFiles = []

    files = os.listdir(strDir)
    for file in files:
        if os.path.splitext(file)[1] == strType:
            lstSrcFiles.append(file)

    return lstSrcFiles

def genImage28(img, file):
    # 求像素重心
    bcW, bcH = getBarycentre(img)

    # 叠加到28x28的黑色图片上
    xOffset = round(28 / 2 - bcW)
    yOffset = round(28 / 2 - bcH)

    print('offset', xOffset, yOffset)
    newImage = mergeImage(createBianryImage(), img, xOffset, yOffset)
    # 另存为
    #cv2.imwrite(dstDir + '/' + file, newImage)
    return newImage
# 读取指定目录下的图片文件，图片为黑白格式，长、宽的最大值为20像素。
# lstSrcFiles = getFileList(srcDir)
# print(lstSrcFiles)
#
# for file in lstSrcFiles:
#     binary = cv2.imread(srcDir + '/' + file, cv2.IMREAD_GRAYSCALE)
#
#     # 求像素重心
#     bcW, bcH = getBarycentre(binary)
#
#     # 叠加到28x28的黑色图片上
#     xOffset = round(28 / 2 - bcW)
#     yOffset = round(28 / 2 - bcH)
#
#     print('offset', xOffset, yOffset)
#
#     # 另存为
#     cv2.imwrite(dstDir + '/' + file,
#                 mergeImage(createBianryImage(), binary, xOffset, yOffset))
#     # binary)