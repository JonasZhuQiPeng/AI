from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import os
import tensorflow as tf
import cv2
import numpy as np
x = tf.placeholder("float", [None, 784], name="Mul")
y_ = tf.placeholder("float", [None,10], name="y_")
keep_prob = tf.placeholder("float", name='rob')
W = tf.Variable(tf.zeros([784,10]), name='x')
b = tf.Variable(tf.zeros([10]), 'y_')

y = tf.nn.softmax(tf.matmul(x,W) + b, name="final_result")

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
init = tf.initialize_all_variables()
sess = tf.InteractiveSession()
sess.run(init)



for i in range(10000):
  batch_xs, batch_ys = mnist.train.next_batch(50)
  train_accuracy = accuracy.eval(feed_dict={x: batch_xs, y_: batch_ys, keep_prob: 1.0})
  print("step %d, training accuracy %g" % (i, train_accuracy))
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys, keep_prob: 0.5})

save_path = 'Model_Simple/'
model_name = 'MyModel'
if not os.path.exists(save_path):
    os.makedirs(save_path)
    save_path_full = os.path.join(save_path, model_name)
    saver = tf.train.Saver()
    saver.save(sess, save_path_full)
    #print(save_path_full)


#print(W.eval(session=sess))

print (sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

# 关闭会话
sess.close()
