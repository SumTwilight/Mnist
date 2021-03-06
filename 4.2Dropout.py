import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

#载入数据集
mnist = input_data.read_data_sets("MNIST_data",one_hot=True)

#每个批次的大小
batch_size = 100
#计算一共有多少个批次
n_batch = mnist.train.num_examples // batch_size

#定义两个placeholder
x = tf.placeholder(tf.float32,[None,784])
y = tf.placeholder(tf.float32,[None,10])
keep_prob=tf.placeholder(tf.float32)


#创建神经网络
W1 = tf.Variable(tf.truncated_normal([784,2000],stddev=0.1))
b1 = tf.Variable(tf.zeros([1,2000]))
#激活层
Layer1 = tf.nn.tanh(tf.matmul(x,W1)+b1)
#drop层
Layer1_drop = tf.nn.dropout(Layer1,keep_prob=keep_prob)

W2 = tf.Variable(tf.truncated_normal([2000,500],stddev=0.1))
b2 = tf.Variable(tf.zeros([1,500]))
Layer2 = tf.nn.tanh(tf.matmul(Layer1_drop,W2)+b2)
Layer2_drop = tf.nn.dropout(Layer2,keep_prob=keep_prob)

W3 = tf.Variable(tf.truncated_normal([500,10],stddev=0.1))
b3 = tf.Variable(tf.zeros([1,10]))

prediction = tf.nn.sigmoid(tf.matmul(Layer2_drop,W3)+b3)

#二次代价函数
# loss = tf.reduce_mean(tf.square(y-prediction))
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=prediction))

#使用梯度下降法
train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

#初始化变量
init = tf.global_variables_initializer()

prediction_2=tf.nn.softmax(prediction)
#结果存放在一个布尔型列表中
correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(prediction_2,1)) #argmax返回一维向量表中最大的值所在的位置
#求准确率
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

saver=tf.train.Saver(max_to_keep=1)
with tf.Session() as sess:
    sess.run(init)
    for epoch in range(21):
        for batch in range(n_batch):
            batch_xs,batch_ys=mnist.train.next_batch(batch_size)
            sess.run(train_step,feed_dict={x:batch_xs,y:batch_ys,keep_prob:0.8})

        acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels,keep_prob:1.0})
        print("Iter "+str(epoch)+",Testing Accuracy "+str(acc))
    saver.save(sess,'./ckpt/mnist.ckpt')