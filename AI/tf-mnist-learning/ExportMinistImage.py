# !/usr/bin/python3.5
# -*- coding: utf-8 -*-

import os
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

from PIL import Image

# 声明图片宽高
rows = 28
cols = 28

# 要提取的图片数量
images_to_extract = 8000

# 当前路径下的保存目录
save_dir = "./mnist_digits_images"

# 读入mnist数据
mnist = input_data.read_data_sets("MNIST_data/", one_hot=False)

# 创建会话
sess = tf.Session()

# 获取图片总数
shape = sess.run(tf.shape(mnist.train.images))
images_count = shape[0]
pixels_per_image = shape[1]

# 获取标签总数
shape = sess.run(tf.shape(mnist.train.labels))
labels_count = shape[0]

# mnist.train.labels是一个二维张量，为便于后续生成数字图片目录名，有必要一维化(后来发现只要把数据集的one_hot属性设为False，mnist.train.labels本身就是一维)
# labels = sess.run(tf.argmax(mnist.train.labels, 1))
labels = mnist.train.labels

# 检查数据集是否符合预期格式
if (images_count == labels_count) and (shape.size == 1):
    print("dataset include %s images and %s labels in total" % (images_count, labels_count))
    print("each image include %s pixels" % (pixels_per_image))
    print("data type is: %s" % (mnist.train.images.dtype))

    # mnist图像数据的数值范围是[0,1]，需要扩展到[0,255]，以便于人眼观看
    if mnist.train.images.dtype == "float32":
        print("ready to revers[0,1]to binary[0,255]")
        for i in range(0, images_to_extract):
            for n in range(pixels_per_image):
                if mnist.train.images[i][n] != 0:
                    mnist.train.images[i][n] = 255
                    # 由于数据集图片数量庞大，转换可能要花不少时间，有必要打印转换进度
            if ((i + 1) % 50) == 0:
                print("image floats extend:already transfer %s items,need to transfer %s in total" % (i + 1, images_to_extract))

                # 创建数字图片的保存目录
    for i in range(10):
        dir = "%s/%s/" % (save_dir, i)
        if not os.path.exists(dir):
            print("Directory ""%s"" is not existing, create this automatically" % dir)
            os.makedirs(dir)

            # 通过python图片处理库，生成图片
    indices = [0 for x in range(0, 10)]
    for i in range(0, images_to_extract):
        img = Image.new("L", (cols, rows))
        for m in range(rows):
            for n in range(cols):
                img.putpixel((n, m), int(mnist.train.images[i][n + m * cols]))
                # 根据图片所代表的数字label生成对应的保存路径
        digit = labels[i]
        path = "%s/%s/%s.bmp" % (save_dir, labels[i], indices[digit])
        indices[digit] += 1
        img.save(path)
        # 由于数据集图片数量庞大，保存过程可能要花不少时间，有必要打印保存进度
        if ((i + 1) % 50) == 0:
            print("images save progress:saved %s ,need to save %s in total" % (i + 1, images_to_extract))

else:
    print("The number of images and labels is different!")