import tensorflow as tf
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

def Init():  
    pass





#function to be called when mouse is clicked
def printcoords():
    global root
    root = Toplevel()
    frame1 = Frame(root, bd=2, relief=SUNKEN,height=50,width=50)
    frame = Frame(root, bd=2, relief=SUNKEN,height=50,width=50)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    yscroll = Scrollbar(frame)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    t1=Text(frame1,width = 10,height = 5)  
    #setting up a tkinter canvas with scrollbars
    frame1.grid_rowconfigure(100, weight=1)
    frame1.grid_columnconfigure(100, weight=1)    
    frame.grid_rowconfigure(100, weight=1)
    frame.grid_columnconfigure(100, weight=1)    
    xscroll.grid(row=1, column=0, sticky=E+W)    
    yscroll.grid(row=0, column=1, sticky=N+S)    
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)    
    frame1.pack(fill=BOTH,expand=1)
    tf.reset_default_graph()
    t1.delete(0.0,END)
    File = filedialog.askopenfilename(parent=root, initialdir="./MnistImage",title='Choose an image.')
    filename = ImageTk.PhotoImage(Image.open(File))
    canvas.image = filename  # <--- keep reference of your image
    canvas.create_image(0,0,anchor='nw',image=filename)
    
    im = Image.open(File)
    im = im.resize((28, 28))
    im = im.convert('L')
    ImageResult = list(im.getdata())

    x = tf.placeholder(tf.float32, [None,784])
    y = tf.placeholder(tf.float32, [None, 10])
    keep_prob = tf.placeholder(tf.float32)

    # 创建神经网络
    W1 = tf.Variable(tf.truncated_normal([784,2000],stddev=0.1))
    b1 = tf.Variable(tf.zeros([1, 2000]))
    # 激活层
    layer1 = tf.nn.tanh(tf.matmul(x,W1) + b1)
    # drop层
    layer1 = tf.nn.dropout(layer1,keep_prob=1.0)

    # 第二层
    W2 = tf.Variable(tf.truncated_normal([2000,500],stddev=0.1))
    b2 = tf.Variable(tf.zeros([1, 500]))
    layer2 = tf.nn.tanh(tf.matmul(layer1,W2) + b2)
    layer2 = tf.nn.dropout(layer2,keep_prob=1.0)

    # 第三层
    W3 = tf.Variable(tf.truncated_normal([500,10],stddev=0.1))
    b3 = tf.Variable(tf.zeros([1,10]))
    prediction = tf.matmul(layer2,W3) + b3

    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=prediction))

    # 梯度下降法
    train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)#得到98.3的正确率
    # train_step = tf.train.AdadeltaOptimizer(0.1).minimize(loss)  #97.34的准确率
    # train_step = tf.train.AdamOptimizer().minimize(loss)  # 97.8
    # train_step = tf.train.RMSPropOptimizer(learning_rate=0.001).minimize(loss) #98.06
    # train_step = tf.train.AdagradOptimizer(learning_rate=0.1).minimize(loss) # 98.29


    # 初始化变量
    init = tf.global_variables_initializer()

    prediction_2 = tf.nn.softmax(prediction)
    # 得到一个布尔型列表，存放结果是否正确
    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(prediction_2,1)) #argmax 返回一维张量中最大值索引

    # 求准确率
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32)) # 把布尔值转换为浮点型求平均数

    saver = tf.train.Saver(max_to_keep=1)

    with tf.Session() as sess:
        sess.run(init)
        saver.restore(sess, './ckpt/mnist.ckpt')  # 使用模型
        predicte = tf.argmax(prediction, 1)
        result = predicte.eval(feed_dict={x: [ImageResult]}, session=sess)
        t1.insert(INSERT,'识别结果：'+str(result[0]))
        t1.pack()

    def destroy_win():
        root.destroy()
        printcoords()

    Button(root,text='choose',command=destroy_win).pack()
    root.mainloop()


