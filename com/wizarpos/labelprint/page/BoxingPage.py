#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import os


class BoxingPage():
    new_sn_list_submit = []

    def __init__(self, master):
        self.master = master
        self.master.bind_all("<Control-r>", self.exit)
        self.master.bind_all("<Control-R>", self.exit)

        self.frame_order_qr = Frame(self.master)
        self.input_order_qr_variable = StringVar()
        Label(self.frame_order_qr, text='工单二维码', font=('楷体', 20)).grid(row=0, column=0, padx=5, sticky='w')
        self.order_qr_input = Entry(self.frame_order_qr, borderwidth=1, textvariable=self.input_order_qr_variable, justify=CENTER, font=('楷体', 15), width=100)
        # self.order_qr_input.bind("<Return>", func=self.handler_adaptor(self.parse_order_qr_content, qr_content=self.input_order_qr_variable.get()))
        self.order_qr_input.bind("<Return>", func=self.handler_adaptor(self.parse_order_qr_content, qr_content=self.order_qr_input))

        self.order_qr_input.focus_force()  # 设置焦点
        self.order_qr_input.grid(row=0, column=1)
        self.frame_order_qr.pack(side=TOP, pady=10)

        self.box_info = Frame(self.master)
        # 工单号
        self.order_id_variable = StringVar()
        Label(self.box_info, text='工单号', font=('楷体', 20)).grid(row=0, column=0, padx=5, sticky='w')
        self.order_id_input = Entry(self.box_info, borderwidth=1, textvariable=self.order_id_variable, justify=CENTER, state='readonly',takefocus=False, font=('楷体', 20), width=15)
        self.order_id_input.grid(row=0, column=1)

        # 终端型号
        self.model = StringVar()
        Label(self.box_info, text='终端型号', font=('楷体', 20)).grid(row=0, column=2, padx=5, sticky='w')
        Entry(self.box_info, borderwidth=1, textvariable=self.model, justify=CENTER,  state='readonly',takefocus=False, font=('楷体', 20), width=5).grid(row=0, column=3)
        # self.model.set("Q2")
        # 装箱数量
        self.sn_num = StringVar()
        Label(self.box_info, text='装箱数量', font=('楷体', 20)).grid(row=0, column=4, padx=5, sticky='w')
        self.num = Entry(self.box_info, borderwidth=1, textvariable=self.sn_num, justify=CENTER,  state='readonly',takefocus=False, foreground='red', font=('楷体', 20), width=5)
        self.sn_num.set("24")
        self.num.bind_all("<F5>", self.reset_all_ui)
        self.num.grid(row=0, column=5)
        self.box_info.pack(side=TOP, pady=10)

        self.box_id_frm = Frame(self.master)
        # 箱号
        self.box_id = StringVar()
        box_no = Entry(self.box_id_frm, borderwidth=1, textvariable=self.box_id, justify=CENTER,  state='readonly',takefocus=False, font=('楷体', 20), width=12)
        box_no.pack(side=RIGHT)
        box_no_label = Label(self.box_id_frm, text='箱号', font=('楷体', 20))
        box_no_label.pack(side=RIGHT)
        self.box_id_frm.pack(side=TOP, fill=X, pady=10)

        # 默认加载SN框12个
        self.sn_info = Frame(self.master)
        self.create_entry_variable = locals()  # 为了生成多个变量
        self.create_entry = locals()  # 为了生成多个变量

        self.create_sn_ui(self.sn_num.get(), self.sn_info)
        self.sn_info.pack(side=TOP, padx='5', pady='5')

        # log框
        self.changelog_text = scrolledtext.ScrolledText(self.master, borderwidth=1, height=5)
        self.changelog_text.pack(side=BOTTOM, padx=10, pady=10, fill=X)

        # 按钮
        self.buttons = Frame(self.master)
        self.btn_check = Button(self.buttons, text='装箱检查\n(F1)', bg='#C1CDC1', font=('楷体', 20), width=12, height=5, command=self.box_check_fun)
        self.btn_print_one = Button(self.buttons, text='打印第1页\n(F2)', bg='#C1CDC1', font=('楷体', 20), width=12, height=5, command=self.print_one_fun)
        self.btn_print_two = Button(self.buttons, text='打印第2页\n(F3)', bg='#C1CDC1', font=('楷体', 20), width=12, height=5, command=self.print_two_fun)
        self.btn_check.bind_all("<F1>", self.box_check_fun)
        self.btn_print_one.bind_all("<F2>", self.print_one_fun)
        self.btn_print_two.bind_all("<F3>", self.print_two_fun)
        self.btn_check.pack(side=LEFT, padx='50')
        self.btn_print_one.pack(side=LEFT, padx='50')
        self.btn_print_two.pack(side=LEFT, padx='50')

        self.buttons.pack(side=BOTTOM, padx=10, pady=10)

    def exit(self, *event):
        # root.bind("<Control-q>", self.handler_adaptor(self.handler, a=1, b=2, c=3))
        os._exit(0)

    # 根据装箱数量动态添加SN控件
    def create_sn_ui(self, num, frame):
        x, y = 0, 0
        for i in range(int(num)):
            sn = 'sn' + str(i + 1)
            self.create_entry_variable[sn] = StringVar()
            # 循环多个变量
            Label(frame, width=3, bg='#4169E1', text=i + 1, font=('楷体', 15)).grid(row=y, column=x * 2, padx=6, pady=10, sticky='w')
            self.create_entry[sn] = Entry(frame, textvariable=self.create_entry_variable[sn], justify=CENTER, highlightcolor='green', highlightthickness=1, relief=SUNKEN, font=('楷体', 20), width=16)
            self.create_entry[sn].grid(row=y, column=x * 2 + 1, pady=10)
            self.create_entry[sn].bind("<KeyRelease>", func=self.handler_adaptor(self.handler, create_entry=self.create_entry, create_entry_sn=i))
            print("self.create_entry[sn]   ", self.create_entry[sn], sn)
            x += 1
            if x == 4:
                x = 0
                y += 1

    def parse_order_qr_content(self, event, qr_content):
        print("qr_content", qr_content.get())
        pass

    def handler(self, event, create_entry, create_entry_sn):
        """事件处理函数"""
        sn = 'sn' + str(create_entry_sn + 1)
        print("len(create_entry[sn].get())", len(create_entry[sn].get()), create_entry[sn].get())
        if len(create_entry[sn].get()) >= 16:
            sn = 'sn' + str(create_entry_sn + 2)
            if create_entry_sn + 2 > int(self.num.get()):
                print("已经是最后一个了")
            else:
                create_entry[sn].focus_force()
            pass

        # return messagebox.showinfo(title="Hey, you got me!", message=create_entry_sn + "---"  , parent=self.master)

    def handler_adaptor(self, fun, **kwds):
        """事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧"""
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

    # 重置装箱数量
    def reset_sn_ui(self, *events):
        if 0 < int(self.sn_num.get()) <= 24:
            self.sn_info.destroy()
            self.sn_info = Frame(self.master)
            self.create_sn_ui(self.sn_num.get(), self.sn_info)
            self.sn_info.pack(side=TOP, padx='5', pady='5')
        else:
            messagebox.showwarning(title='装箱数量', message='数量太多', parent=self.master)

    def reset_info_ui(self, *event):
        self.input_order_qr_variable.set("")
        self.order_id_variable.set("")

    def reset_all_ui(self, *event):
        self.reset_sn_ui()

    def box_check_fun(self, *event):

        check_ok = self.sn_check()
        global new_sn_list_submit

        if check_ok:
            print("box_check_fun new_sn_list_submit", new_sn_list_submit, len(new_sn_list_submit))
            self.submitTMS(self.order_id_input.get(), new_sn_list_submit)

            # self.box_id.set('12345678910000')
            # messagebox.showinfo(title='装箱检查~', message='检查成功！', parent=self.master)

    def submitTMS(self, order_no, sn_list):
        str_sns = ''
        for i in sn_list:
            if len(i) == 16:
                str_sns += i + ","
                pass
            else:
                messagebox.showwarning("SN警告", "发现SN位数不够" + i)
        print("str_sns", str_sns)
        pass

    def print_one_fun(self, *event):
        messagebox.showwarning(title='打印第一页~', message='打印失败！', parent=self.master)

    def print_two_fun(self, *event):
        messagebox.showwarning(title='打印第二页~', message='打印失败！', parent=self.master)

    def sn_check(self, *event):
        print(event)
        # 检查终端型号
        # 检查重复
        # 循环获取输入框SN号
        sn_list = []
        for i in range(int(self.sn_num.get())):
            sn = 'sn' + str(i + 1)
            sn_list.append(self.create_entry_variable[sn].get())
        print(sn_list)
        new_sn_list = []
        for i in sn_list:
            if len(i) > 0:
                if i not in new_sn_list:
                    new_sn_list.append(i)
                else:
                    messagebox.showwarning("重复终端", "发现重复SN:" + i)
                    for x in range(int(self.sn_num.get())):
                        sn = 'sn' + str(x + 1)
                        print("self.create_entry_variable[sn]  aa ", self.create_entry_variable[sn].get(), i)
                        if self.create_entry_variable[sn].get() == i:
                            self.create_entry_variable[sn].focus_force()
                            self.create_entry_variable[sn].configure(highlightcolor='red', highlightthickness=1, )
                            self.create_entry_variable[sn].selection_range(0, END)
                            print("self.create_entry_variable[sn]  bb ", sn)
                            return False
                    return False
        print("new_sn_list", new_sn_list, len(new_sn_list))
        global new_sn_list_submit
        new_sn_list_submit = new_sn_list
        return True


if __name__ == '__main__':
    root = Tk()
    app = BoxingPage(root),
    scnWidth, scnHeight = root.maxsize()  # 获取屏幕的大小
    x, y = (scnWidth - 1300) / 2, (scnHeight - 660) / 2  # 定位窗口居中显示的坐标
    root.geometry("1300x660+%d+%d" % (x, y))  # +50+20
    # root.resizable(False, False)
    root.wm_minsize(1300, 660)
    root.title('装箱')
    root.mainloop()
