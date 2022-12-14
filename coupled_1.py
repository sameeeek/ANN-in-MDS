# -*- coding: utf-8 -*-
"""Coupled_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RXeV0b3M1XdAwD-RTr2JsycaLT8Svo_p
"""

"""
This is an attempt to predict the solution of a pair of coupled differential equations using a neural network. 

The work is inspired by: http://dx.doi.org/10.1109/72.712178
"""

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

A1 = 0
A2 = 1
del_x = np.sqrt(np.finfo(np.float32).eps)
print(np.finfo(np.float32).eps)
alpha = 0.00001
epochs = 1000
display_steps = epochs/10
loss_vals = []

def cal_psi_t1(x):
  psi_t = A1 + x*neuron1(x)

  return psi_t

def cal_psi_t2(x):
  psi_t = A2 + x*neuron2(x)

  return psi_t

def diff1(x):
  return (cal_psi_t1(x + del_x) - cal_psi_t1(x))/del_x 

def diff2(x):
  return (cal_psi_t2(x + del_x) - cal_psi_t2(x))/del_x

def RHS1(x):
  rhs = np.cos(x)-(1 + x*x + np.power(np.sin(x), 2))
  return rhs

def LHS1(x):
  lhs = diff1(x) - cal_psi_t1(x)*cal_psi_t1(x) - cal_psi_t2(x)
  return lhs

def RHS2(x):
  rhs = 2*x - (1 + x*x)*np.sin(x)
  return rhs

def LHS2(x):
  lhs = diff2(x) - cal_psi_t1(x)*cal_psi_t2(x)
  return lhs

optimizer = tf.optimizers.SGD(alpha)

# tf.random.set_seed(5)

w1 = {
    'h1': tf.Variable(tf.random.normal([1, 32])),
    'h2': tf.Variable(tf.random.normal([32, 32])),
    'out':  tf.Variable(tf.random.normal([32, 1])),
}

b1 = {
    'b1': tf.Variable(tf.random.normal([32])),
    'b2': tf.Variable(tf.random.normal([32])),
    'out':tf.Variable(tf.random.normal([1]))
}

w2 = {
    'h1': tf.Variable(tf.random.normal([1, 32])),
    'h2': tf.Variable(tf.random.normal([32, 32])),
    'out':  tf.Variable(tf.random.normal([32, 1])),
}

b2 = {
    'b1': tf.Variable(tf.random.normal([32])),
    'b2': tf.Variable(tf.random.normal([32])),
    'out':tf.Variable(tf.random.normal([1]))
}

def neuron1(x):
  x = np.array([[[x]]], dtype='float32')
  l1 = tf.add(tf.matmul(x, w1['h1']), b1['b1'])
  #print(l1.shape)
  l1 = tf.nn.sigmoid(l1)
  
  l2 = tf.add(tf.matmul(l1, w1['h2']), b1['b2'])
  l2 = tf.nn.sigmoid(l2)

  output = tf.matmul(l2, w1['out']) + b1['out']

  return output



def neuron2(x):
  x = np.array([[[x]]], dtype='float32')
  l1 = tf.add(tf.matmul(x, w2['h1']), b2['b1'])
  #print(l1.shape)
  l1 = tf.nn.sigmoid(l1)
  
  l2 = tf.add(tf.matmul(l1, w2['h2']), b2['b2'])
  l2 = tf.nn.sigmoid(l2)

  output = tf.matmul(l2, w2['out']) + b2['out']

  return output

def RMSLoss():
  summ = []
  for j in range(10):
    x = np.random.uniform()
    del_NN1 = LHS1(x)
    del_NN2 = LHS2(x)
    summ.append((del_NN1 - RHS1(x))**2 + (del_NN2 - RHS2(x))**2)
  return tf.reduce_sum(tf.abs(summ))

def train_step():
  with tf.GradientTape() as tape:
    loss = RMSLoss()
  trainable_variables = list(w1.values()) + list(b1.values()) + list(w2.values()) + list(b2.values())
  gradients = tape.gradient(loss, trainable_variables)
  optimizer.apply_gradients(zip(gradients, trainable_variables))
train_step()

for i in range(epochs):
    train_step()
    if i % display_steps == 0:
        lv = RMSLoss()
        print("loss: %f " % (lv))
        loss_vals.append(lv.numpy())

from matplotlib.pyplot import figure

figure(figsize=(10,10))
# True Solution (found analitically)
def true_solution(x):
    return x**2 + 1

X = np.linspace(0, 1, 100)
result = []
for i in X:
  # result.append(f(i))
  result.append(cal_psi_t2(i).numpy()[0][0][0])

S = true_solution(X)
  
plt.plot(X, S, label="Original Function")
plt.plot(X, result, label="Neural Net Approximation")
plt.legend(loc=2, prop={'size': 20})
plt.show()

def R_squared(y, y_pred):
  unexplained_error = tf.reduce_sum(tf.square(tf.subtract(y,y_pred)))
  total_error = tf.reduce_sum(tf.square(tf.subtract(y, tf.reduce_mean(y))))
  r2 = tf.subtract(1, tf.math.divide(unexplained_error, total_error))
 
  return r2

print(R_squared(S, result))

from matplotlib.pyplot import figure

figure(figsize=(10,10))
# True Solution (found analitically)
def true_solution(x):
    return np.sin(x)

X = np.linspace(0, 1, 100)
result = []
for i in X:
  # result.append(f(i))
  result.append(cal_psi_t1(i).numpy()[0][0][0])

S = true_solution(X)
  
plt.plot(X, S, label="Original Function")
plt.plot(X, result, label="Neural Net Approximation")
plt.legend(loc=2, prop={'size': 20})
plt.show()

def R_squared(y, y_pred):
  unexplained_error = tf.reduce_sum(tf.square(tf.subtract(y,y_pred)))
  total_error = tf.reduce_sum(tf.square(tf.subtract(y, tf.reduce_mean(y))))
  r2 = tf.subtract(1, tf.math.divide(unexplained_error, total_error))
 
  return r2

print(R_squared(S, result))

from matplotlib.pyplot import figure

figure(figsize=(10,10))
plt.plot(np.log(loss_vals))
plt.title("Loss values")
plt.show()

# print(np.shape(loss_vals))
# print(loss_vals[9][1])
