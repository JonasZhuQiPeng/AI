# -*- coding:utf-8 -*-
import cv2
import tensorflow as tf
import numpy as np
import ResizeImage as image
from sys import path


# 用于将自定义输入图片反转
def reversePic(src):
    # 图像反转
    for i in range(src.shape[0]):
        for j in range(src.shape[1]):
            src[i, j] = 255 - src[i, j]
    return src

def main():
    sess = tf.InteractiveSession()
    # 模型恢复
    saver = tf.train.import_meta_graph('Model_CNN/MyModel.meta')

    saver.restore(sess, 'Model_CNN/MyModel')
    graph = tf.get_default_graph()

    # 获取输入tensor,,获取输出tensor
    input_x = sess.graph.get_tensor_by_name("Mul:0")
    y_conv2 = sess.graph.get_tensor_by_name("final_result:0")

    # 也可以上面注释,通过下面获取输出输入tensor,
    # y_conv2 = tf.get_collection('output')[0]
    # # x= tf.get_collection('x')[0]
    # input_x = graph.get_operation_by_name('Mul').outputs[0]
    # keep_prob = graph.get_operation_by_name('rob').outputs[0]

    path = "pic/img.bmp"
    im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    im = image.resizeImage(im, 20, 20)


    # 默认输入为白底黑字，故反转图像，minist为黑底白字
    im = reversePic(im)
    cv2.namedWindow("Original", cv2.WINDOW_NORMAL);
    cv2.imshow('Original', im)
    cv2.waitKey(0)
    im = image.genImage28(im, path)
    cv2.namedWindow("Resize to 28", cv2.WINDOW_NORMAL);
    cv2.imshow('Resize to 28', im)
    cv2.waitKey(0)
    # im=cv2.threshold(im, , 255, cv2.THRESH_BINARY_INV)[1];

    im = cv2.resize(im, (28, 28), interpolation=cv2.INTER_CUBIC)

    # im=cv2.threshold(im,200,255,cv2.THRESH_TRUNC)[1]
    # im=cv2.threshold(im,60,255,cv2.THRESH_TOZERO)[1]

    # 数据从0~255转为-0.5~0.5
    # img_gray = (im - (255 / 2.0)) / 255
    x_img = np.reshape(im, [-1, 784])
    output = sess.run(y_conv2, feed_dict={input_x: x_img})
    print('the predict is: %d' % (np.argmax(output)))
    # 关闭会话
    sess.close()


if __name__ == '__main__':
    main()