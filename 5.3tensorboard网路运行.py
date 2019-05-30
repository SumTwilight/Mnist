import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
# 载入数据
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)



# 批次的大小
batch_size = 128
n_batch = mnist.train.num_examples // batch_size

# 参数概要
def variable_summaries(var):
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean',mean) # 平均值
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.summary.scalar('stddev',stddev) # 标准差
        tf.summary.scalar('max', tf.reduce_max(var)) # 最大值
        tf.summary.scalar('min', tf.reduce_min(var)) # 最小值
        tf.summary.histogram('histogram',var) # 直方图


# 命名空间
with tf.name_scope('input'):
    x = tf.placeholder(tf.float32, [None,784],name="X-input")
    y = tf.placeholder(tf.float32, [None, 10],name='y-input')

# 创建一个简单的神经网络
with tf.name_scope('layer'):
    with tf.name_scope('weights'):
        W = tf.Variable(tf.zeros([784,10]),name='W')
        variable_summaries(W)
    with tf.name_scope('biases'):
        b = tf.Variable(tf.zeros([1, 10]),name='b')
        variable_summaries(b)
    with tf.name_scope('xw_plus_b'):
        wx_plus_b = tf.matmul(x,W) + b
    with tf.name_scope('softmax'):
        prediction = tf.nn.softmax(wx_plus_b)

# 代价函数
with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.square(y-prediction))
    tf.summary.scalar('loss', loss)
# 梯度下降法
with tf.name_scope('train'):
    train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)
    
# 初始化变量
init = tf.global_variables_initializer()

# 得到一个布尔型列表，存放结果是否正确
with tf.name_scope('accuracy'):
    with tf.name_scope('correct_prediction'):
        correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(prediction,1)) #argmax 返回一维张量中最大值索引
    # 求准确率
    with tf.name_scope('accuracy'):
        accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32)) # 把布尔值转换为浮点型求平均数
        tf.summary.scalar('accuracy', accuracy)
        
# 合并所有summary
merged = tf.summary.merge_all()
        
with tf.Session() as sess:
    sess.run(init)
    writer = tf.summary.FileWriter('logs/',sess.graph)
    for epoch in range(51):
        for batch in range(n_batch):
            # 获得批次数据
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            # 运行网络并记录log
            summary,_ = sess.run([merged, train_step], feed_dict={x:batch_xs, y:batch_ys})
        # 记录变量
        writer.add_summary(summary,epoch)
        acc = sess.run(accuracy, feed_dict={x:mnist.test.images,y:mnist.test.labels})
        print("Iter " + str(epoch) + " Testing Accuracy: " + str(acc))
    writer.close()
    writer.close()

