#!/user/bin/env python3
#coding=utf-8
from socket import *
import sys,os
import getpass
from tkinter import *
from time import strftime
import time
import datetime 
import signal
from threading import Lock
import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import showwarning, showinfo
from tkinter.colorchooser import askcolor
import turtle
import random
import pygame
from pachong import FindURL
import requests
from bs4 import BeautifulSoup

#网络连接
def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)

    s = socket()
    try:
        s.connect(ADDR)
    except:
        print("服务器连接失败")
        return
    # do_chat(s)
    login(s)


# 登录界面
def login(s):
    # 一级窗口
    root = tk.Tk()
    # # 图片，待抠图
    a = PhotoImage(file=r'./ss.gif')
    b = Label(root, image=a)  # 右侧分区中添加标签（绑定图片）
    b.image = a
    b.grid()
    # 标题
    root.title("登陆界面")
    # 限制
    root.resizable(width=False, height=False)
    # 设置窗口大小和窗口位置
    root.geometry("500x550+450+70")


    # 账号和输入框
    z = Label(root, text="账号：", font=("黑体", 15),
              fg="#000000", bg="#0cc9c9").place(x=142, y=250)
    m = Label(root, text="密码：", font=("黑体", 15),
              fg="#000000", bg="#0cc9c9").place(x=142, y=280)

    # 显示输入框
    # 账号
    zz = tk.StringVar(root, value="")
    # zz.set("1216757638")
    zhanghao = tk.Entry(root, textvariable=zz, font=("黑体", 16), width=12)
    zhanghao.place(x=197,y=251)
    # 密码
    mm = tk.StringVar(root, value="")
    mima = tk.Entry(root, textvariable=mm, font=("黑体", 16), width=12,show="*")
    mima.place(x=197, y=291)

    # 注册，登陆
    # zhuce = Button(root, text="注册", width=6, command=(lambda: registered(root)),bg='gray85')
    # denglu = Button(root, text="登陆", width=6, command=(lambda: do_login(root)),bd=2, bg='gray85')
    zhuce = Button(root, text="注册", width=6, command=lambda: registered(s,root))
    denglu = Button(root, text="登陆", width=6, command=lambda: do_login(s,zz,mm))
    zhuce.place(x=277, y=330)
    denglu.place(x=192, y=330)

    # 消息循环
    root.mainloop()

#按登录按钮运行登录函数
def do_login(s,zz,mm):
    msg = "L {} {}".format(zz.get(),mm.get())
    s.send(msg.encode())
    data = s.recv(128).decode()

    if data == "OK":
        tk.messagebox.showinfo(title="成功", message="登录成功")
        chat(s)
    else:
        tk.messagebox.showerror(title="错误", message="登录失败")

#按注册按钮进行注册页面
def registered(s,root):
    # 创建一个缩的界面
    s1 = Toplevel()
    s1.geometry("180x180")
    L1 = Label(s1, text="用户名")
    L1.pack()
    L2 = Label(s1, text="账号:")
    zhanghao = tk.StringVar()
    zh = Entry(s1, textvariable=zhanghao)
    zh.pack()

    L3 = Label(s1, text="密码")
    L3.pack()
    mima = tk.StringVar()
    mm = Entry(s1, textvariable=mima)
    mm.pack()

    L4 = Label(s1, text="再次输入")
    L4.pack()
    mima2 = tk.StringVar()
    mm2 = Entry(s1, textvariable=mima2)
    mm2.pack()

    def huoqu():
        name = zh.get()
        pwd = mm.get()
        pwd1 = mm2.get()
        # 调用处理窗口
        do_register(s,name, pwd, pwd1)
    Button(s1, text="提交", command=huoqu).pack()


# 提交注册信息      
def do_register(s,name, pwd, pwd1):
    if (" " in name) or (" " in pwd):
        showwarning('提示', '用户名及密码不能含有空格！')
        return
    if pwd != pwd1:
        showwarning('提示', '两次密码输入不一致！')
        return

    msg = "R {} {}".format(name,pwd)
    #发送请求
    s.send(msg.encode())
    #等待回复
    data = s.recv(128).decode()
    if data == "OK":
        tk.messagebox.showinfo(title="成功", message="注册成功")
        return
    else:
        tk.messagebox.showerror(title="失败", message="注册失败")
        return




# 进入聊天界面
def chat(s):
    #创建窗口
    root2=tk.Tk()
    #标题
    root2.title("简单智能回复机器人")
    #限制大小
    root2.resizable(width=False,height=False)
    #设置窗口大小和窗口位置
    root2.geometry("700x515+350+200")

    #创建容器Frame ,大小,白色
    a = Frame(root2,width = 450, height = 328,bg = 'white')#接收消息区
    b = Frame(root2,width =450, height = 120, bg = 'white')#发送消息区
    c = Frame(root2,width = 80,height = 470)#右边图片区
    #创建元素控件
    text_msglist = Text(a,font=("Times", "11", "bold italic"))
    text_msgsend = Text(b,font=("Times", "11", "bold italic"))
    #行，列
    #padx：设置控件周围水平方向空白区域保留大小； pady：设置控件周围垂直方向空白区域保留大小；
    a.grid(row = 0, column = 0, columnspan = 2, padx = 1, pady = 3)
    b.grid(row = 1, column = 0, columnspan = 2, padx = 1, pady = 3)
    c.grid(row = 0, column = 2, rowspan = 2, padx = 3, pady = 5)
    #d.grid(row = 0, column = 1, rowspan = 1, padx = 3, pady = 5)
    a.grid_propagate(0)
    b.grid_propagate(0)
    c.grid_propagate(0)

    #发送按钮
    fa = Button(root2, text = '发送', width = 8,command=lambda:msgsend(s))
    #下一步
    #发送按钮需要获取从b窗口的文本内容,然后发送给显示端，
    def msgsend(s):
        # # 在聊天内容上方加一行 显示发送人及发送时间
        msgcontent = \
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '+'我:'
        msgrobot = \
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n ' + '机器人:' 
        # 加锁，避免显示接收信息及自编辑信息显示混乱
        lock = Lock()
        with lock:
            text_msglist.insert(END, msgcontent, 'green')
            text_msglist.insert(END,text_msgsend.get('0.0', END))
        msg = text_msgsend.get('0.0',END)
        text_msgsend.delete('0.0', END)
        msg = 'C {}'.format(msg)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        text_msglist.insert(END, msgrobot, 'blue')
        text_msglist.insert(END, data + '\n')
        # print(data)

    #关闭按钮
    qu =Button(root2, text = '关闭',width = 8 , command=quit)
    gn1 =Button(root2, text = '功能1',height=2,width = 10 ,bg="green", command=lambda:gongneng1())
    gn2 =Button(root2, text = '功能2',height=2,width = 10 ,bg="green", command=lambda:gongneng2())

    # E为右对齐，W为左对.
    fa.grid(row=2,column=0)
    qu.grid(row=2,column=1,sticky=E)
    gn1.grid(row=0,column=3)
    gn2.grid(row=1,column=3)

    def gongneng1():
        def main():
            FL = FindURL()
            FL.gui_arrange()
            thinter.mainloop()
        if __name__ == "__main__":
            main()
        # q = turtle.Pen()
        # turtle.bgcolor("black")
        # sides = 7
        # colors = ["red","orange","yellow","green","cyan","blue","purple"]
        # for x in range(360):
        #     q.pencolor(colors[x%sides])
        #     q.forward(x*3/sides+x)
        #     q.left(360/sides+1)
        #     q.width(x*sides/200)

    def gongneng2():
        PANEL_width = 600
        PANEL_highly = 500
        FONT_PX = 15

        pygame.init()

        # 创建一个可是窗口
        winSur = pygame.display.set_mode((PANEL_width, PANEL_highly))

        font = pygame.font.SysFont("123.ttf", 25)

        bg_suface = pygame.Surface((PANEL_width, PANEL_highly), flags=pygame.SRCALPHA)

        pygame.Surface.convert(bg_suface)

        bg_suface.fill(pygame.Color(0, 0, 0, 28))

        winSur.fill((0, 0, 0))

        # 字母版
        letter = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c',
                  'v', 'b', 'n', 'm']
        texts = [
            font.render(str(letter[i]), True, (0, 255, 0)) for i in range(26)
        ]

        # 按屏幕的宽带计算可以在画板上放几列坐标并生成一个列表
        column = int(PANEL_width / FONT_PX)
        drops = [0 for i in range(column)]

        while True:
            # 从队列中获取事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    chang = pygame.key.get_pressed()
                    if(chang[32]):
                        exit()

            # 将暂停一段给定的毫秒数
            pygame.time.delay(30)

            # 重新编辑图像第二个参数是坐上角坐标
            winSur.blit(bg_suface, (0, 0))

            for i in range(len(drops)):
                text = random.choice(texts)

                # 重新编辑每个坐标点的图像
                winSur.blit(text, (i * FONT_PX, drops[i] * FONT_PX))

                drops[i] += 1
                if drops[i] * 10 > PANEL_highly or random.random() > 0.95:
                    drops[i] = 0

            pygame.display.flip()

    # 设置显示和发送文本框
    text_msglist.grid(row=0, column=0, sticky=NSEW)
    text_msgsend.grid(row=0, column=0, sticky=NSEW)

    text_msgsend.focus()
    text_msgsend.bind('<Return>', (lambda event: msgsend(s)))

    
    #消息循环，显示窗口
    root2.mainloop()



if __name__ == '__main__':
    main()
