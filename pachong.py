# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import tkinter
from bs4 import BeautifulSoup


class FindURL(object):

    def __init__(self):
        # 创建主窗口
        self.root0 = tkinter.Tk()
        self.root0.minsize = (600, 400)
        self.frame = tkinter.Frame(self.root0)
        self.frame.pack()
        # 设置标题
        self.root0.title("URL查找")
        # 创建一个输入框
        self.url_input = tkinter.Entry(self.frame, width=30)

        self.display_info = tkinter.Listbox(self.root0, width=50)

        # 创建一个查询按钮
        self.result_button = tkinter.Button(
            self.frame, command=self.find_URL_a, text="查询")
        self.url_input.focus()

    def gui_arrange(self):
        self.url_input.pack(side=tkinter.LEFT)
        self.display_info.pack()
        self.result_button.pack(side=tkinter.RIGHT)

    def find_URL_a(self):
        self.url = self.url_input.get()
        self.url_input.delete(0, tkinter.END)
        self.display_info.delete(0, tkinter.END)
        if len(self.url) <= 7:
            return
        self.res = requests.get('http://www.baidu.com')  # 设置default值
        if ('.cn'in self.url or '.com' in self.url) and self.url[0:6] != 'http:/':
            if self.url[0:7] != 'https:/':
                res2 = requests.get('http://' + self.url)
                if res2.status_code == 200:
                    self.res = res2
                else:
                    res2 = requests.get('https://' + self.url)
                    if res2.status_code == 200:
                        self.res = res2
        self.res.encoding = 'utf-8'
        self.soup = BeautifulSoup(self.res.text, 'html.parser')
        MESSAGE = []
        for line in self.soup.find_all('a'):
            if line.find(text=True) and line.has_attr('href'):
                self.display_info.insert(tkinter.END, line.find(
                    text=True) + " : " + line['href'])
                MESSAGE.append(line['href'])
            elif line.has_attr('href'):
                self.display_info.insert(tkinter.END, line['href'])
                MESSAGE.append(line['href'])
            else:
                self.display_info.insert(tkinter.END, "No Expect Message!!!")
        return MESSAGE


def main():
    FL = FindURL()
    FL.gui_arrange()
    tkinter.mainloop()

if __name__ == "__main__":
    main()
