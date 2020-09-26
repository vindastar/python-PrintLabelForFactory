#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from mttkinter import mtTkinter as mttk
from tkinter import *
from tkinter import messagebox
import ConnectionTracer
import threading
import time
import subprocess
import os
from pip._vendor import requests
from pystrich.code128 import Code128Encoder
from pystrich.qrcode import QRCodeEncoder
import win32api
import win32con
import win32print
import win32ui
from PIL import ImageWin, Image, ImageDraw, ImageFont

is_connected_device = False
sn_code_path = ''


class GetSNPage():

    def __init__(self, master):
        self.master = master
        self.master.bind("<Control-c>", self.exit)
        self.master.bind("<Control-C>", self.exit)
        self.box_info = mttk.Frame(self.master)
        # SN号
        self.sn_input = mttk.StringVar()
        mttk.Label(self.box_info, text='连接设备后查看SN', font=('楷体', 20)).grid(row=0, column=0, padx=5, sticky='w')
        self.order_id_input = mttk.Entry(self.box_info, borderwidth=2, textvariable=self.sn_input, justify=mttk.CENTER, font=('楷体', 15), width=15)
        self.order_id_input.focus_force()  # 设置焦点
        self.order_id_input.grid(row=0, column=1)
        self.box_info.pack(side=mttk.TOP, pady=80)

        # 按钮
        global sn_code_path
        self.buttons = mttk.Frame(self.master)
        self.btn_get_sn = mttk.Button(self.buttons, text='获取SN\n\n(Ctrl+G)', bg='#C1CDC1', font=('楷体', 15), width=12, height=5, command=self.get_sn)
        self.btn_get_sn_print = mttk.Button(self.buttons, text='获取并打印SN\n\n(Ctrl+F)', bg='#C1CDC1', font=('楷体', 15), width=12, height=5, command=self.get_sn_print)
        self.btn_get_sn.bind_all("<Control-G>", self.get_sn)
        self.btn_get_sn.bind_all("<Control-g>", self.get_sn)
        self.btn_get_sn_print.bind_all("<Control-F>", self.get_sn_print)
        self.btn_get_sn_print.bind_all("<Control-f>", self.get_sn_print)
        self.btn_get_sn.pack(side=mttk.LEFT, padx='50')
        self.btn_get_sn_print.pack(side=mttk.LEFT, padx='50')
        self.buttons.pack(side=mttk.TOP, padx=10, pady=10)

        ConnectionTracer.start(hook_function)
        while_get_sn_thread = threading.Thread(target=self.listen_device(), args=())
        while_get_sn_thread.start()

    def exit(self, event):
        os._exit(0)
        # root.bind("<Control-q>", self.handler_adaptor(self.handler, a=1, b=2, c=3))
        # root.bind("<Control-q>", exit(0))

    def get_sn(self, *event):
        terminal_sn = self.get_terminal_sn()
        if len(terminal_sn) == 0:
            self.sn_input.set("未获取到SN")
            messagebox.showwarning(title='获取SN', message='未获取到SN!', parent=self.master)

    def get_sn_print(self, *event):
        self.start_print_sn_path()

    def handler(self, event, a, b, c):
        print(event)
        print("handler", a, b, c)

    def handler_adaptor(self, fun, **kwds):
        if kwds is None:
            kwds = kwds
        return lambda event, fun=fun, kwds=None: fun(event, **kwds)

    def get_terminal_sn(self):
        # global isConnectDevice
        # if isConnectDevice:
        #     pass
        # else:
        #     return print("isConnectDevice", isConnectDevice)
        try:
            print("getTerminalSN isConnectDevice", is_connected_device)
            pi = subprocess.Popen("adb shell getprop ro.boot.serialno", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            self.sn = str(pi.stdout.read().decode())
            print("getTerminalSN =" + self.sn)

            if "WP" in self.sn:
                self.sn = self.sn[self.sn.index("WP"):self.sn.index("WP") + 16]
                self.sn_input.set(str(self.sn))
                # self.createSNCode(self.sn)
            else:
                self.sn_input.set(str(self.sn))
                # self.sn_input.set("SN非慧银终端")
        except Exception as e:
            messagebox.showwarning(title='获取SN', message='ex: 未获取到SN!', parent=self.master)
            print(e.args)
        return self.sn

    def create_sn_code(self, sn):
        # if len(sn) < 16:
        #     print("createCode  len less 16 error")
        #     messagebox.showwarning(title='len less 16', message='SN长度不够,无法生成条码', parent=self.master)
        #     return

        encoder = Code128Encoder(sn, options={'label_border': 0, 'bottom_border': 6, 'height': 150, 'ttf_fontsize': 30, 'ttf_font': 'msyh'})
        if sn.__contains__("adb server is out"):
            messagebox.showwarning(title='restart app ', message='restart!', parent=self.master)

            return
        paths = "./sn/" + sn[2:7]
        if not os.path.exists(paths):
            os.makedirs(paths)
        encoder.save(paths + "/" + sn + ".png")
        qrcoder = QRCodeEncoder("BOX NO : 123987000")
        qrcoder.save(paths + "/" + sn + "_qr.png")
        # code.save(paths + "/" + snStr, {'text_distance': 0.5, 'module_height': 6, 'module_width': 0.14, 'quiet_zone': 1, 'font_size': 10})
        self.snPath = paths + "/" + sn + ".png"
        print("createSNCode   self.snPath = " + self.snPath)
        return self.snPath

    def get_create_print_sn(self):

        self.terminal_sn = self.get_terminal_sn().replace("\r\n", "")
        print("get_create_print_sn = ", self.terminal_sn)

        if len(self.terminal_sn) == 0 or len(self.terminal_sn) < 16:
            self.sn_input.set("未获取到SN")
            return

        global sn_code_path
        global is_connected_device
        if not is_connected_device:
            print("printSNCode but isConnectDevice", is_connected_device)
            return
        sn_code_path = self.create_sn_code(self.terminal_sn)
        is_connected_device = False

        self.start_print_sn_path()

    def start_print_sn_path(self):
        global sn_code_path
        if sn_code_path.startswith("WP"):
            pass
        else:
            messagebox.showwarning("重新获取", "非慧银生产SN,无法打印:\n" + self.terminal_sn)
            return
        try:
            print("print sn code")
            printer_name = win32print.GetDefaultPrinter()
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)
            sn_img = Image.open(sn_code_path)
            # if sn_img.size[0] < sn_img.size[1]:
            #     sn_img = sn_img.rotate(0)
            # ratios = [1.0 * printable_area[0] / bmp.size[1], 1.0 * printable_area[1] / bmp.size[0]]
            # scale = min(ratios)
            scale = 1
            hDC.StartDoc(sn_code_path)
            hDC.StartPage()
            dib = ImageWin.Dib(sn_img)
            scaled_width, scaled_height = [int(scale * i) for i in sn_img.size]
            x1 = 40  # 控制位置
            y1 = 0
            x2 = x1 + scaled_width
            y2 = y1 + scaled_height
            dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))
            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()
            return True
        except Exception as e:
            print("print_sn_img exception, snpath= " + sn_code_path)
            print(e.args)
            return False

    def timer_run(self):
        t = RepeatingTimer(2.0, self.get_create_print_sn)
        t.start()

    def listen_device(self):
        msg_handle = threading.Thread(target=self.timer_run, args=())
        msg_handle.daemon = True
        msg_handle.start()


class RepeatingTimer(threading.Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)

def hook_function(devices: set):
    global is_connected_device
    print(devices)
    if len(devices) > 0:
        is_connected_device = True
    else:
        is_connected_device = False


if __name__ == '__main__':
    root = Tk()
    app = GetSNPage(root),

    scnWidth, scnHeight = root.maxsize()  # 获取屏幕的大小
    x, y = (scnWidth - 1300) / 2, (scnHeight - 660) / 2  # 定位窗口居中显示的坐标
    root.geometry("1300x660+%d+%d" % (x, y))  # +50+20
    # root.resizable(False, False)
    root.wm_minsize(1300, 660)
    root.title('获取SN')
    root.mainloop()
