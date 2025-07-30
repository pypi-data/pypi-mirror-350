# -*- coding: UTF-8 -*-
# @Time    : 2021/4/6
# @Author  : xiangyuejia@qq.com
# Apache License
# Copyright©2020-2021 xiangyuejia@qq.com All Rights Reserved

import tensorflow as tf

W = tf.Variable([.1], dtype=tf.float32)
b = tf.Variable([-.1], dtype=tf.float32)
x = tf.placeholder(tf.float32)
linear_model = W*x + b
y = tf.placeholder(tf.float32)
loss = tf.reduce_sum(tf.square(linear_model - y))
sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)
print(sess.run(W))
print(sess.run(linear_model, {x: [1, 2, 3, 6, 8]}))
print(sess.run(loss, {x: [1, 2, 3, 6, 8], y: [4.8, 8.5, 10.4, 21.0, 25.3]}))

optimizer = tf.train.GradientDescentOptimizer(0.001)
train = optimizer.minimize(loss)

x_train = [1, 2, 3, 6, 8]
y_train = [4.8, 8.5, 10.4, 21.0, 25.3]

for i in range(10000):
    sess.run(train, {x: x_train, y: y_train})

print('W: %s b: %s loss: %s' % (sess.run(W), sess.run(b), sess.run(loss, {x: x_train , y: y_train})))
