# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""A very simple MNIST classifier.
See extensive documentation at
http://tensorflow.org/tutorials/mnist/beginners/index.md
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

FLAGS = None

def main(_):
    # Import data
    training_set = []
    length = 0
    with open('/Users/christie/Desktop/AIhackathon/adjust data length/training set.csv', 'r') as f:
        for line in f.readlines():
            record = []
            line_vec = line.strip().split(',')
            if length < line_vec.__len__():
                length = line_vec.__len__()

            record.append(line_vec[4:])
            record.append(line_vec[0])
            training_set.append(record)
    print(length)
    length = 0
    test_set = []
    with open('/Users/christie/Desktop/AIhackathon/adjust data length/test set.csv', 'r') as f:
        for line in f.readlines():
            record = []
            line_vec = line.strip().split(',')
            if length < line_vec.__len__():
                length = line_vec.__len__()
            record.append(line_vec[4:])
            record.append(line_vec[0])
            test_set.append(record)
    print(length)

    # mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

    # Create the model
    x = tf.placeholder(tf.float32, [None, 1600]) # 每个input数据是1600的向量  about None  http://learningtensorflow.com/lesson4/
    W = tf.Variable(tf.zeros([1600, 9])) # 输出类别 9 类
    b = tf.Variable(tf.zeros([9]))
    y = tf.matmul(x, W) + b   #
    # Define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, 9])

#########################
    def weight_variable(shape):
        #返回一个随机数  shape是tensor形状
      initial = tf.truncated_normal(shape, stddev=0.1)
      return tf.Variable(initial)

    def bias_variable(shape):
        #返回一个常数  shape是tensor形状
      initial = tf.constant(0.1, shape=shape)
      return tf.Variable(initial)

    # conv2d
    # https://www.tensorflow.org/api_docs/python/tf/nn/conv2d
    def conv2d(x, W):
      return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME') #输入输出一样维度

    def max_pool_3x1(x):
      return tf.nn.max_pool(x, ksize=[1, 3, 1, 1],        # [batch, height, width, channels]   ksize: A list of ints that has length >= 4. The size of the window for each dimension of the input tensor.
                            strides=[1, 3, 1, 1], padding='SAME') #
#########################

    W_conv1 = weight_variable([100, 1, 1, 32])  # [filter_height, filter_width, in_channels, out_channels]
    b_conv1 = bias_variable([32])

    x_sound = tf.reshape(x, [-1,1600,1,1])  # -1代表一维,或者由其他推出   reshape重新定义tensor由外往内  [batch, in_height, in_width, in_channels]
    # https://www.tensorflow.org/api_docs/python/tf/reshape

    # Relu 对比sigmoid。sig过滤过多信息。
    # 实际卷积处
    h_conv1 = tf.nn.relu(conv2d(x_sound, W_conv1) + b_conv1) # 1501*1
    h_pool1 = max_pool_3x1(h_conv1) # 501*1

    W_conv2 = weight_variable([100, 1, 32, 64])
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)  # 402*1
    h_pool2 = max_pool_3x1(h_conv2) # 134*1

    W_fc1 = weight_variable([134 * 1 * 64, 1024]) # 1024 自设？？？
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 134*1*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)  # 这里做了第一次的激活 用relu

# 为了减少过拟合，我们在输出层之前加入dropout
    keep_prob = tf.placeholder("float") # 用一个placeholder来代表一个神经元的输出在dropout中保持不变的概率。这样我们可以在训练过程中启用dropout，在测试过程中关闭dropout
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob) # 随机舍弃一半？？？ 每次training 随机舍弃一部分，防止过拟合。
# 最后，我们添加一个softmax层，就像前面的单层softmax regression一样
    W_fc2 = weight_variable([1024, 9])
    b_fc2 = bias_variable([9])

    y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

# 用更加复杂的ADAM优化器来做梯度最速下降。滚石头，避免局部最优。
    cross_entropy = tf.reduce_mean(  # 交叉熵
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))  # logits？？？
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

# 数据处理
    correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1)) # batch boolean vector
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) # percentage
    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())

    for i in range(203):
      batch = training_set.next_batch(10)
      if i%10 == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x:batch[0], y_: batch[1], keep_prob: 1.0})  # 每个batch，batch[0] 是数据  batch[1]是label
        print("step %d, training accuracy %g"%(i, train_accuracy))
      train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    print("test accuracy %g"%accuracy.eval(feed_dict={
        x: test_set[0], y_: test_set[1], keep_prob: 1.0}))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data',
                      help='Directory for storing input data')
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
