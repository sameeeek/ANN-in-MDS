# -*- coding: utf-8 -*-
"""ODE_FirstOrder.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W6WehmGO2K5_JExhUPouGvmCBSz_mSMd
"""

"""
This is an attempt to predict the solution of a first order ODE using a neural network. 

The work is inspired by: http://dx.doi.org/10.1109/72.712178
"""

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

A = 1
del_x = np.sqrt(np.finfo(np.float32).eps)

alpha = 0.01
epochs = 500
display_steps = epochs/10

def cal_psi_t(x):
  psi_t = A + x*neuron(x)

  return psi_t

def diff(x):
  return (cal_psi_t(x + del_x) - cal_psi_t(x))/del_x

def RHS(x):
  rhs = 2*x
  return rhs

def LHS(x):
  lhs = diff(x)
  return lhs

optimizer = tf.optimizers.SGD(alpha)

# tf.random.set_seed(5)

w = {
    'h1': tf.Variable(tf.random.normal([1, 32])),
    'h2': tf.Variable(tf.random.normal([32, 32])),
    'out':  tf.Variable(tf.random.normal([32, 1])),
}

b = {
    'b1': tf.Variable(tf.random.normal([32])),
    'b2': tf.Variable(tf.random.normal([32])),
    'out':tf.Variable(tf.random.normal([1]))
}

def neuron(x):
  x = np.array([[[x]]], dtype='float32')
  l1 = tf.add(tf.matmul(x, w['h1']), b['b1'])
  #print(l1.shape)
  l1 = tf.nn.sigmoid(l1)
  
  l2 = tf.add(tf.matmul(l1, w['h2']), b['b2'])
  l2 = tf.nn.sigmoid(l2)

  output = tf.matmul(l2, w['out']) + b['out']

  return output

def RMSLoss():
  summ = []
  for x in np.linspace(0, 1, 10):
    del_NN = LHS(x)
    summ.append((del_NN - RHS(x))**2)
  return tf.reduce_sum(tf.abs(summ))

def train_step():
  with tf.GradientTape() as tape:
    loss = RMSLoss()
  trainable_variables = list(w.values()) + list(b.values())
  gradients = tape.gradient(loss, trainable_variables)
  optimizer.apply_gradients(zip(gradients, trainable_variables))

for i in range(epochs):
    train_step()
    if i % display_steps == 0:
        print("loss: %f " % (RMSLoss()))

from matplotlib.pyplot import figure

figure(figsize=(10,10))
# True Solution (found analytically)
def true_solution(x):
    return x**2 + 1

X = np.linspace(0, 1, 100)
result = []
for i in X:
  # result.append(f(i))
  result.append(cal_psi_t(i).numpy()[0][0][0])

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

