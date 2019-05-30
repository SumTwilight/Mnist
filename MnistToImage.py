from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
mnist = input_data.read_data_sets("/Users/dudu/Desktop/project/img", one_hot=True)
import scipy.misc
import os
save_dir = './MnistImage/'
if os.path.exists(save_dir) is False:
    os.makedirs(save_dir)
for i in range(20):
    image = mnist.train.images[i,:]
    image = image.reshape(28,28)
    file = save_dir+'mnist_test_%d.jpg' % i
    scipy.misc.toimage(image,cmin=0.0,cmax=1.0).save(file)