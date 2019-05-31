import tkinter as tk

window=tk.Tk()
window.title('my window')
window.geometry('300x200')

#这里是窗口内容



l=tk.Label(window,
    text='OMG! this is TK!',    #标签文字
    bg='red',       #背景颜色
    font=('Arial',12),  #字体和字体大小
    width=15,height=2)  #标签长宽
l.pack()    #固定窗口位置


var = tk.StringVar() #这时文字变量储存器
l = tk.Label(window,textvariable=var, bg='green',font=('Arial',12),width=15,height=2)
l.pack()


on_hit=False  #初始状态为 false
def hit_me():
    global on_hit
    if on_hit == False: #从False状态到True状态
        on_hit = True
        var.set('you hit me') #设置标签的文字为‘you hit me’
    else: #从True 状态变为False状态
        on_hit=False
        var.set('') #设置文字为空

    
b=tk.Button(window, 
    text='hit me',  #显示再按钮上的文字
    width=15,height=2,
    command=hit_me) #点击按钮式执行命令

b.pack() #按钮位置

e=tk.Entry(window,show=None)
e.pack()


def insert_point():
    var=e.get()
    t.insert('insert',var)

def insert_end():
    var=e.get()
    t.insert('end',var)

b1=tk.Button(window,text='insert point',width=15,height=2,command=insert_point)
b1.pack()
b2=tk.Button(window,text='insert end',command=insert_end)
b2.pack()
t=tk.Text(window,height=2)
t.pack()


window.mainloop()