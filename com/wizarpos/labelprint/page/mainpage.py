#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from tkinter import *
from tkinter import ttk
from com.wizarpos.labelprint.page.BoxingPage import BoxingPage
from com.wizarpos.labelprint.page.GetSNPage import GetSNPage
import os


class MainDesk(object):
    def __init__(self, master):
        # 使用self会告诉所有的方法，这个变量是我们共有的，可以随便用
        self.root = master
        self.root.config()
        scnWidth, scnHeight = root.maxsize()  # 获取屏幕的大小
        x, y = (scnWidth - 1300) / 2, (scnHeight - 660) / 2  # 定位窗口居中显示的坐标
        root.geometry("1300x660+%d+%d" % (x, y))  # +50+20
        root.wm_minsize(1300, 660)
        self.root.title('标签打印及装箱工具 v1.0')
        # self.root.resizable(False, False)

        self.notebook = ttk.Notebook(self.root, width=1300, height=660)
        ttk.Style().configure(".", font=("楷体", 30))

        self.frame_get_sn = Frame(root)
        self.sn_page = GetSNPage(self.frame_get_sn)
        self.notebook.add(self.frame_get_sn, text=" 获取SN ")

        self.frame_boxing_page = Frame(root)
        self.boxing_page = BoxingPage(self.frame_boxing_page)
        self.notebook.add(self.frame_boxing_page, text=" 装箱页面 ")
        self.notebook.pack()

def exit():
    os._exit(0)

if __name__ == '__main__':
    root = Tk()
    desk = MainDesk(root)
    root.protocol('WM_DELETE_WINDOW', exit)
    root.mainloop()
