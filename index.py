#!/user/bin/env python3
#coding=utf-8

'''
MODULES: python3.5
'''

from socket import *
from multiprocessing import *
import os,sys
import pymysql
import signal
from time import sleep,ctime
import random
import time
import re

#文件库路径
FILE_PATH = "/home/tarena/EasyRobot/"
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)


#创建子进程接收处理客户端请求
def do_child(c,addr):
    print("进入子进程")
    db = pymysql.connect("127.0.0.1","root","123456","jiqiren")
    while True:
        #收发信息
        data = c.recv(128).decode()
        # if (not data) or data[0] == "E":
        #     print(addr,"已退出")
        #     c.close()
        #     sys.exit(0)
        # elif data[0] == 'H':
        #     c.send('您好，我是小白！(quit退出聊天)'.encode())
        if data[0] == "C":
            do_chat(c,data)
        elif data == "":
            c.close()
            sys.exit(0)
        elif data[0] == "R":
            do_register(c,db,data)
        elif data[0] == "L":
            name = do_login(c,db,data)

#核对注册信息
def do_register(c,db,data):
    print("注册操作")
    l = data.split(" ")
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()

    #判断用户名是否存在
    sql = "select * from user where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchone()

    if r != None:
        c.send(b"EXISTS")
        return

    #用户不存在插入用户
    sql = "insert into user(name,passwd) values('%s','%s')"%(name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except:
        db.rollback()
        c.send(b'FALL')
    db.close()   
    
#核对登录信息
def do_login(c,db,data):
    print("登录操作")
    l = data.split(" ")
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()

    sql = "select * from user where name='%s' and passwd='%s'"%(name,passwd)

    cursor.execute(sql)
    r = cursor.fetchone()

    if r == None:
        c.send(b'FALL')
    else:
        c.send(b'OK')
        return name

def do_chat(c,data):
    print("开始聊天")
    l = data.split(" ")
    data0 = l[1].strip()
    #文本查询
    try:
        f = open("./ciku.txt")
    except:
        c.send(b'FALL')
        return

    for line in f:
        #用正则表达式切割空格
        lst = re.split(r"\s+",line)
        say = lst[0]
        root = lst[1]
        if data0 == say:
            c.send(root.encode())
            break
    else:
        say0 = ["我听不懂你在说什么",\
        "我还小，智慧不足，等我升级以后就理解你说的话了",\
        "没有人陪我聊天，我会感到寂寞的，幸好有你陪我聊天",\
        "怎么回答你好呢？...",\
        "你知道吗，我的主人是Eason,是他制造我的..."]
        say0 = say0[random.randint(0,4)]
        c.send(say0.encode())
    f.close()



#创建套接字，接收客户端连接，创建新进程
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    #处理子进程退出
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print("Listen the port 8888...")

    while True:
        try:
            #等待接受连接
            print("Waiting for connect...")
            c,addr = s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print("服务器异常:",e)
            continue 

        print("已连接客户端:",addr)
        #创建子进程
        pid = os.fork()

        if pid == 0:
            s.close()
            do_child(c,addr)
        else:
            c.close()
            continue


if __name__ == '__main__':
    main()