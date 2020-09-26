# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import os
import subprocess
import threading
import time

import ConnectionTracer
import barcode
import keyboard
import win32api
import win32con
import win32print
import win32ui
import wx
import wx.xrc
import qrcode
from PIL import ImageWin, Image, ImageDraw, ImageFont
from barcode.writer import ImageWriter
from pip._vendor import requests


class MyLabelPrint(wx.Frame):
    chinese = ['上海慧银信息科技有限公司', '型    号:', '数    量:', '箱    号:', '识 别 码:']
    english = ['Wizarpos International Co.,Ltd.', 'Model No:', 'Quantity:', 'Box   No:', 'Id    No:']
    choiceType = 'Q2'
    boxsize = '12'
    VERSION_IFNO = "1.0.1"

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"标签打印", pos=wx.DefaultPosition, size=wx.Size(1300, 660),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(1300, 660), wx.DefaultSize)

        self.m_menubar4 = wx.MenuBar(0)
        self.m_menu7 = wx.Menu()
        self.m_menubar4.Append(self.m_menu7, u"文件")

        self.m_menu8 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(self.m_menu8, wx.ID_ANY, u"简体中文", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu8.Append(self.m_menuItem1)

        self.m_menuItem2 = wx.MenuItem(self.m_menu8, wx.ID_ANY, u"English", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu8.Append(self.m_menuItem2)

        self.m_menuItem3 = wx.MenuItem(self.m_menu8, wx.ID_ANY, u"Japanes", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu8.Append(self.m_menuItem3)

        self.m_menubar4.Append(self.m_menu8, u"语言")

        self.m_menu9 = wx.Menu()
        self.m_menubar4.Append(self.m_menu9, u"关于")

        self.SetMenuBar(self.m_menubar4)

        gSizer2 = wx.GridSizer(1, 1, 0, 0)

        gSizer2.SetMinSize(wx.Size(170, 100))
        self.m_notebook29 = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.getSNAndPrintSNBtn = wx.ScrolledWindow(self.m_notebook29, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                    wx.HSCROLL | wx.VSCROLL)
        self.getSNAndPrintSNBtn.SetScrollRate(5, 5)
        gSizer3 = wx.GridSizer(4, 4, 0, 0)

        self.zhanwei1 = wx.StaticText(self.getSNAndPrintSNBtn, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.zhanwei1.Wrap(-1)
        gSizer3.Add(self.zhanwei1, 0, wx.ALL, 5)

        self.zhanwei2 = wx.StaticText(self.getSNAndPrintSNBtn, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.zhanwei2.Wrap(-1)
        gSizer3.Add(self.zhanwei2, 0, wx.ALL, 5)

        self.zhanwei3 = wx.StaticText(self.getSNAndPrintSNBtn, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.zhanwei3.Wrap(-1)
        gSizer3.Add(self.zhanwei3, 0, wx.ALL, 5)

        self.zhanwei4 = wx.StaticText(self.getSNAndPrintSNBtn, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.zhanwei4.Wrap(-1)
        gSizer3.Add(self.zhanwei4, 0, wx.ALL, 5)

        self.zhanwei5 = wx.StaticText(self.getSNAndPrintSNBtn, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.zhanwei5.Wrap(-1)
        gSizer3.Add(self.zhanwei5, 0, wx.ALL, 5)

        self.connectTips = wx.StaticText(self.getSNAndPrintSNBtn, wx.ID_ANY, u"连接设备后获取SN:", wx.Point(-1, -1),
                                         wx.DefaultSize, 0)
        self.connectTips.Wrap(-1)
        self.connectTips.SetFont(wx.Font(22, 75, 90, 90, False, "黑体"))

        gSizer3.Add(self.connectTips, 0, wx.ALL, 5)

        self.snShowInput = wx.TextCtrl(self.getSNAndPrintSNBtn, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                       wx.Size(300, 40), wx.TE_CENTRE | wx.TE_READONLY | wx.SIMPLE_BORDER)
        self.snShowInput.SetMaxLength(16)
        self.snShowInput.SetFont(wx.Font(22, 75, 90, 90, False, "黑体"))
        self.snShowInput.SetToolTip(u"连接设备后查看SN")

        gSizer3.Add(self.snShowInput, 0, wx.ALL, 5)

        # self.editSN = wx.CheckBox(self.getSNAndPrintSNBtn, wx.ID_ANY, u"编辑", wx.DefaultPosition, wx.Size(100, 40), 0)
        # self.editSN.SetFont(wx.Font(22, 75, 90, 90, False, "黑体"))
        #
        # gSizer3.Add(self.editSN, 0, wx.ALL, 5)

        self.zhanwei6 = wx.StaticText(self.getSNAndPrintSNBtn, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.zhanwei6.Wrap(-1)
        gSizer3.Add(self.zhanwei6, 0, wx.ALL, 5)

        self.zhanwei7 = wx.StaticText(self.getSNAndPrintSNBtn, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.zhanwei7.Wrap(-1)
        gSizer3.Add(self.zhanwei7, 0, wx.ALL, 5)

        self.getSNBtn = wx.Button(self.getSNAndPrintSNBtn, wx.ID_ANY, u"获取SN", wx.DefaultPosition, wx.Size(250, -1), 0)
        self.getSNBtn.SetFont(wx.Font(22, 75, 90, 90, False, "黑体"))

        gSizer3.Add(self.getSNBtn, 0, wx.ALL, 5)

        self.m_button4 = wx.Button(self.getSNAndPrintSNBtn, wx.ID_ANY, u"获取并打印SN", wx.DefaultPosition, wx.Size(250, -1),
                                   0)
        self.m_button4.SetFont(wx.Font(22, 75, 90, 90, False, "黑体"))

        gSizer3.Add(self.m_button4, 0, wx.ALL, 5)

        self.getSNAndPrintSNBtn.SetSizer(gSizer3)
        self.getSNAndPrintSNBtn.Layout()
        gSizer3.Fit(self.getSNAndPrintSNBtn)
        self.m_notebook29.AddPage(self.getSNAndPrintSNBtn, u"打印SN", True)
        self.m_panel1 = wx.Panel(self.m_notebook29, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        topgbs = wx.GridBagSizer(0, 0)
        topgbs.SetFlexibleDirection(wx.BOTH)
        topgbs.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.orderNoView = wx.StaticText(self.m_panel1, wx.ID_ANY, u"工单号:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.orderNoView.Wrap(-1)
        self.orderNoView.SetFont(wx.Font(16, 75, 90, 90, False, "黑体"))
        self.orderNoView.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))

        topgbs.Add(self.orderNoView, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.ALL, 5)

        self.orderNoInput = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1),
                                        wx.TE_CENTRE | wx.SIMPLE_BORDER)
        # self.orderNoInput.SetMaxLength(11)
        self.orderNoInput.SetFont(wx.Font(16, 75, 90, 90, False, "黑体"))

        topgbs.Add(self.orderNoInput, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.ALL, 5)

        self.boxNoView = wx.StaticText(self.m_panel1, wx.ID_ANY, u"箱号:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.boxNoView.Wrap(-1)
        self.boxNoView.SetFont(wx.Font(16, 75, 90, 90, False, "黑体"))
        self.boxNoView.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))

        topgbs.Add(self.boxNoView, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.ALL, 5)

        self.boxNoInput = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1),
                                      wx.TE_CENTRE | wx.TE_READONLY | wx.SIMPLE_BORDER)
        self.boxNoInput.SetFont(wx.Font(16, 75, 90, 90, False, "黑体"))

        topgbs.Add(self.boxNoInput, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.ALL, 5)

        self.terminalTypeView = wx.StaticText(self.m_panel1, wx.ID_ANY, u"型号:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.terminalTypeView.Wrap(-1)
        self.terminalTypeView.SetFont(wx.Font(16, 75, 90, 90, False, "黑体"))
        self.terminalTypeView.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))

        topgbs.Add(self.terminalTypeView, wx.GBPosition(0, 4), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.ALL, 5)

        self.terminalTypeInput = wx.TextCtrl(self.m_panel1, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size(80, -1),
                                             wx.TE_CENTRE | wx.TE_READONLY | wx.SIMPLE_BORDER)
        self.terminalTypeInput.SetFont(wx.Font(16, 75, 90, 90, False, "黑体"))

        topgbs.Add(self.terminalTypeInput, wx.GBPosition(0, 5), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer4.Add(topgbs, 1, wx.EXPAND, 5)

        sn1gbs = wx.GridBagSizer(0, 0)
        sn1gbs.SetFlexibleDirection(wx.BOTH)
        sn1gbs.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.sn1View = wx.StaticText(self.m_panel1, wx.ID_ANY, u" 1 ", wx.DefaultPosition, wx.Size(30, 30),
                                     0 | wx.SIMPLE_BORDER)
        self.sn1View.Wrap(-1)
        self.sn1View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn1View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn1View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn1gbs.Add(self.sn1View, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn1Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                    wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn1Input.SetMaxLength(16)
        self.sn1Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn1gbs.Add(self.sn1Input, wx.GBPosition(0, 1), wx.GBSpan(1, 1), 0, 5)

        self.sn2View = wx.StaticText(self.m_panel1, wx.ID_ANY, u" 2 ", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn2View.Wrap(-1)
        self.sn2View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn2View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn2View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn1gbs.Add(self.sn2View, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn2Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                    wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn2Input.SetMaxLength(16)
        self.sn2Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn1gbs.Add(self.sn2Input, wx.GBPosition(0, 3), wx.GBSpan(1, 1), 0, 5)

        self.sn3View = wx.StaticText(self.m_panel1, wx.ID_ANY, u" 3 ", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn3View.Wrap(-1)
        self.sn3View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn3View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn3View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn1gbs.Add(self.sn3View, wx.GBPosition(0, 4), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn3Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                    wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn3Input.SetMaxLength(16)
        self.sn3Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn1gbs.Add(self.sn3Input, wx.GBPosition(0, 5), wx.GBSpan(1, 1), 0, 5)

        self.sn4View = wx.StaticText(self.m_panel1, wx.ID_ANY, u" 4 ", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn4View.Wrap(-1)
        self.sn4View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn4View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn4View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn1gbs.Add(self.sn4View, wx.GBPosition(0, 6), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn4Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                    wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn4Input.SetMaxLength(16)
        self.sn4Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn1gbs.Add(self.sn4Input, wx.GBPosition(0, 7), wx.GBSpan(1, 1), 0, 5)

        self.sn5View = wx.StaticText(self.m_panel1, wx.ID_ANY, u" 5 ", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn5View.Wrap(-1)
        self.sn5View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn5View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn5View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn1gbs.Add(self.sn5View, wx.GBPosition(0, 8), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn5Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                    wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn5Input.SetMaxLength(16)

        self.sn5Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn1gbs.Add(self.sn5Input, wx.GBPosition(0, 9), wx.GBSpan(1, 1), 0, 5)

        self.sn6View = wx.StaticText(self.m_panel1, wx.ID_ANY, u" 6 ", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn6View.Wrap(-1)
        self.sn6View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn6View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn6View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn1gbs.Add(self.sn6View, wx.GBPosition(0, 10), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn6Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                    wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn6Input.SetMaxLength(16)

        self.sn6Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn1gbs.Add(self.sn6Input, wx.GBPosition(0, 11), wx.GBSpan(1, 1), 0, 5)

        bSizer4.Add(sn1gbs, 1, wx.ALIGN_CENTER, 5)

        sn2gbs = wx.GridBagSizer(0, 0)
        sn2gbs.SetFlexibleDirection(wx.BOTH)
        sn2gbs.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.sn7View = wx.StaticText(self.m_panel1, wx.ID_ANY, u" 7 ", wx.DefaultPosition, wx.Size(30, 30),
                                     0 | wx.SIMPLE_BORDER)
        self.sn7View.Wrap(-1)
        self.sn7View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn7View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn7View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn2gbs.Add(self.sn7View, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn7Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                    wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn7Input.SetMaxLength(16)

        self.sn7Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn2gbs.Add(self.sn7Input, wx.GBPosition(0, 1), wx.GBSpan(1, 1), 0, 5)

        self.sn8View = wx.StaticText(self.m_panel1, wx.ID_ANY, u" 8 ", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn8View.Wrap(-1)
        self.sn8View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn8View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn8View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn2gbs.Add(self.sn8View, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn8Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                    wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn8Input.SetMaxLength(16)

        self.sn8Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn2gbs.Add(self.sn8Input, wx.GBPosition(0, 3), wx.GBSpan(1, 1), 0, 5)

        self.sn9View = wx.StaticText(self.m_panel1, wx.ID_ANY, u" 9 ", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn9View.Wrap(-1)
        self.sn9View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn9View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn9View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn2gbs.Add(self.sn9View, wx.GBPosition(0, 4), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn9Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                    wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn9Input.SetMaxLength(16)

        self.sn9Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn2gbs.Add(self.sn9Input, wx.GBPosition(0, 5), wx.GBSpan(1, 1), 0, 5)

        self.sn10View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"10", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn10View.Wrap(-1)
        self.sn10View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn10View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn10View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn2gbs.Add(self.sn10View, wx.GBPosition(0, 6), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn10Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn10Input.SetMaxLength(16)

        self.sn10Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn2gbs.Add(self.sn10Input, wx.GBPosition(0, 7), wx.GBSpan(1, 1), 0, 5)

        self.sn11View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"11", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn11View.Wrap(-1)
        self.sn11View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn11View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn11View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn2gbs.Add(self.sn11View, wx.GBPosition(0, 8), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn11Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn11Input.SetMaxLength(16)

        self.sn11Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn2gbs.Add(self.sn11Input, wx.GBPosition(0, 9), wx.GBSpan(1, 1), 0, 5)

        self.sn12View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"12", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn12View.Wrap(-1)
        self.sn12View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn12View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn12View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn2gbs.Add(self.sn12View, wx.GBPosition(0, 10), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn12Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn12Input.SetMaxLength(16)

        self.sn12Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn2gbs.Add(self.sn12Input, wx.GBPosition(0, 11), wx.GBSpan(1, 1), 0, 5)

        bSizer4.Add(sn2gbs, 1, wx.ALIGN_CENTER, 5)

        sn3gbs = wx.GridBagSizer(0, 0)
        sn3gbs.SetFlexibleDirection(wx.BOTH)
        sn3gbs.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.sn13View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"13", wx.DefaultPosition, wx.Size(30, 30),
                                      0 | wx.SIMPLE_BORDER)
        self.sn13View.Wrap(-1)
        self.sn13View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn13View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn13View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn3gbs.Add(self.sn13View, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn13Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn13Input.SetMaxLength(16)

        self.sn13Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn3gbs.Add(self.sn13Input, wx.GBPosition(0, 1), wx.GBSpan(1, 1), 0, 5)

        self.sn14View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"14", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn14View.Wrap(-1)
        self.sn14View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn14View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn14View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn3gbs.Add(self.sn14View, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn14Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn14Input.SetMaxLength(16)

        self.sn14Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn3gbs.Add(self.sn14Input, wx.GBPosition(0, 3), wx.GBSpan(1, 1), 0, 5)

        self.sn15View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"15", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn15View.Wrap(-1)
        self.sn15View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn15View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn15View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn3gbs.Add(self.sn15View, wx.GBPosition(0, 4), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn15Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn15Input.SetMaxLength(16)

        self.sn15Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn3gbs.Add(self.sn15Input, wx.GBPosition(0, 5), wx.GBSpan(1, 1), 0, 5)

        self.sn16View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"16", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn16View.Wrap(-1)
        self.sn16View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn16View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn16View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn3gbs.Add(self.sn16View, wx.GBPosition(0, 6), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn16Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn16Input.SetMaxLength(16)

        self.sn16Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn3gbs.Add(self.sn16Input, wx.GBPosition(0, 7), wx.GBSpan(1, 1), 0, 5)

        self.sn17View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"17", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn17View.Wrap(-1)
        self.sn17View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn17View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn17View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn3gbs.Add(self.sn17View, wx.GBPosition(0, 8), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn17Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn17Input.SetMaxLength(16)

        self.sn17Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn3gbs.Add(self.sn17Input, wx.GBPosition(0, 9), wx.GBSpan(1, 1), 0, 5)

        self.sn18View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"18", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn18View.Wrap(-1)
        self.sn18View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn18View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn18View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn3gbs.Add(self.sn18View, wx.GBPosition(0, 10), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn18Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn18Input.SetMaxLength(16)

        self.sn18Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn3gbs.Add(self.sn18Input, wx.GBPosition(0, 11), wx.GBSpan(1, 1), 0, 5)

        bSizer4.Add(sn3gbs, 1, wx.ALIGN_CENTER, 5)

        sn4gbs = wx.GridBagSizer(0, 0)
        sn4gbs.SetFlexibleDirection(wx.BOTH)
        sn4gbs.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.sn19View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"19", wx.DefaultPosition, wx.Size(30, 30),
                                      0 | wx.SIMPLE_BORDER)
        self.sn19View.Wrap(-1)
        self.sn19View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn19View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn19View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn4gbs.Add(self.sn19View, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn19Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn19Input.SetMaxLength(16)

        self.sn19Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn4gbs.Add(self.sn19Input, wx.GBPosition(0, 1), wx.GBSpan(1, 1), 0, 5)

        self.sn20View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"20", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn20View.Wrap(-1)
        self.sn20View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn20View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn20View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn4gbs.Add(self.sn20View, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn20Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn20Input.SetMaxLength(16)

        self.sn20Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn4gbs.Add(self.sn20Input, wx.GBPosition(0, 3), wx.GBSpan(1, 1), 0, 5)

        self.sn21View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"21", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn21View.Wrap(-1)
        self.sn21View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn21View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn21View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn4gbs.Add(self.sn21View, wx.GBPosition(0, 4), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn21Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn21Input.SetMaxLength(16)

        self.sn21Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn4gbs.Add(self.sn21Input, wx.GBPosition(0, 5), wx.GBSpan(1, 1), 0, 5)

        self.sn22View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"22", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn22View.Wrap(-1)
        self.sn22View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn22View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn22View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn4gbs.Add(self.sn22View, wx.GBPosition(0, 6), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn22Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn22Input.SetMaxLength(16)

        self.sn22Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn4gbs.Add(self.sn22Input, wx.GBPosition(0, 7), wx.GBSpan(1, 1), 0, 5)

        self.sn23View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"23", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn23View.Wrap(-1)
        self.sn23View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn23View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn23View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn4gbs.Add(self.sn23View, wx.GBPosition(0, 8), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn23Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn23Input.SetMaxLength(16)

        self.sn23Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn4gbs.Add(self.sn23Input, wx.GBPosition(0, 9), wx.GBSpan(1, 1), 0, 5)

        self.sn24View = wx.StaticText(self.m_panel1, wx.ID_ANY, u"24", wx.DefaultPosition, wx.Size(30, 30), 0)
        self.sn24View.Wrap(-1)
        self.sn24View.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))
        self.sn24View.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.sn24View.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        sn4gbs.Add(self.sn24View, wx.GBPosition(0, 10), wx.GBSpan(1, 1), wx.LEFT | wx.RIGHT, 5)

        self.sn24Input = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(170, -1),
                                     wx.TE_CENTRE | wx.SIMPLE_BORDER)
        self.sn24Input.SetMaxLength(16)

        self.sn24Input.SetFont(wx.Font(15, 75, 90, 90, False, "黑体"))

        sn4gbs.Add(self.sn24Input, wx.GBPosition(0, 11), wx.GBSpan(1, 1), 0, 5)

        bSizer4.Add(sn4gbs, 1, wx.ALIGN_CENTER, 5)

        gSizer31 = wx.GridSizer(1, 3, 0, 0)

        self.boxingBtn = wx.Button(self.m_panel1, wx.ID_ANY, u"装箱", wx.DefaultPosition, wx.DefaultSize, 0)
        self.boxingBtn.SetFont(wx.Font(18, 75, 90, 90, False, "黑体"))

        gSizer31.Add(self.boxingBtn, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.reprintpage1Btn = wx.Button(self.m_panel1, wx.ID_ANY, u"打印第一页", wx.DefaultPosition, wx.DefaultSize, 0)
        self.reprintpage1Btn.SetFont(wx.Font(18, 75, 90, 90, False, "黑体"))

        gSizer31.Add(self.reprintpage1Btn, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.reprintpage2Btn = wx.Button(self.m_panel1, wx.ID_ANY, u"打印第二页", wx.DefaultPosition, wx.DefaultSize, 0)
        self.reprintpage2Btn.SetFont(wx.Font(18, 75, 90, 90, False, "黑体"))

        gSizer31.Add(self.reprintpage2Btn, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        bSizer4.Add(gSizer31, 1, wx.ALIGN_CENTER, 5)

        self.m_staticText89 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText89.Wrap(-1)
        bSizer4.Add(self.m_staticText89, 0, wx.ALL, 5)

        self.m_staticText91 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText91.Wrap(-1)
        bSizer4.Add(self.m_staticText91, 0, wx.ALL, 5)

        self.m_staticText92 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText92.Wrap(-1)
        bSizer4.Add(self.m_staticText92, 0, wx.ALL, 5)

        self.tipsInput = wx.TextCtrl(self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TE_READONLY)
        self.tipsInput.SetFont(wx.Font(16, 75, 90, 90, False, "黑体"))
        self.tipsInput.SetMinSize(wx.Size(1300, -1))

        bSizer4.Add(self.tipsInput, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_panel1.SetSizer(bSizer4)
        self.m_panel1.Layout()
        bSizer4.Fit(self.m_panel1)
        self.m_notebook29.AddPage(self.m_panel1, u"装箱", False)

        gSizer2.Add(self.m_notebook29, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(gSizer2)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.orderNoInput.Bind(wx.EVT_KEY_UP, self.toNextInput)
        # self.orderNoInput.Bind(wx.EVT_SET_FOCUS, self.selectAllString)
        self.getSNBtn.Bind(wx.EVT_BUTTON, self.getTerminalSN)
        self.getSNAndPrintSNBtn.Bind(wx.EVT_BUTTON, self.printSNCode)
        # self.editSN.Bind(wx.EVT_CHECKBOX, self.toogleEnabalTextCtrl)
        self.boxingBtn.Bind(wx.EVT_BUTTON, self.clickSubmitCheck)
        self.reprintpage1Btn.Bind(wx.EVT_BUTTON, self.printCodePage)
        self.reprintpage2Btn.Bind(wx.EVT_BUTTON, self.printCodePage)

        self.sn1Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn2Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn3Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn4Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn5Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn6Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn7Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn8Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn9Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn10Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn11Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn12Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn13Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn14Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn15Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn16Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn17Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn18Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn19Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn20Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn21Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn22Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn23Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.sn24Input.Bind(wx.EVT_KEY_UP, self.toNextInput)
        self.hide24label()

    # def toogleEnabalTextCtrl(self, event):
    #     s = self.editSN.IsChecked()
    #     if s:
    #         self.snShowInput.SetEditable(True)
    #     else:
    #         self.snShowInput.SetEditable(False)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def selectAllString(self, event):
        # test = wx.Window.FindWindowById(event.GetId(), frame)
        # print(test.GetValue() + "SELECT")
        event.Skip()

    show24 = False

    def setmode_and_size(self, qrstr):
        modelinfo_split = qrstr[qrstr.index("Model"):qrstr.index("Model") + 20].split("=")
        print(modelinfo_split)
        if len(modelinfo_split) == 2:
            terminal_info = modelinfo_split[1]
            terminal_info_split = terminal_info.split(",")
            if len(terminal_info_split) == 2:
                terminal_type = terminal_info_split[0]
                terminal_size = terminal_info_split[1]
                print(terminal_info_split)
                type = terminal_type.upper()[terminal_type.__len__() - 2:terminal_type.__len__()]
                self.choiceType = type
                self.terminalTypeInput.SetValue(type)
                if terminal_size == "24":
                    self.boxsize = "24"
                    self.show24label()
                else:
                    self.boxsize = "12"
                    self.hide24label()

    def set_orderno_info(self, qrstr):
        ordernoinfo_split = qrstr[qrstr.index("OrderNo"):qrstr.index("OrderNo") + 21].split("=")
        print(ordernoinfo_split)
        self.orderNoInput.SetValue(ordernoinfo_split[1])

    def parseOrderQRContent(self, qrvalue):
        qrstr = str(qrvalue)
        self.setmode_and_size(qrstr)
        self.set_orderno_info(qrstr)

    def toNextInput(self, event):
        if event.GetId() == self.orderNoInput.GetId():
            if str(self.orderNoInput.GetValue()).__len__() > 10:
                qrvalue = self.orderNoInput.GetValue()
                print("order value" + qrvalue)
                self.parseOrderQRContent(qrvalue)
        elif event.GetId() == self.sn1Input.GetId():
            if str(self.sn1Input.GetValue()).__len__() == 16:
                self.sn1Input.SetValue(str(self.sn1Input.GetValue()).upper())
                self.sn2Input.SetFocus()
        elif event.GetId() == self.sn2Input.GetId():
            if str(self.sn2Input.GetValue()).__len__() == 16:
                self.sn2Input.SetValue(str(self.sn2Input.GetValue()).upper())
                self.sn3Input.SetFocus()
        elif event.GetId() == self.sn3Input.GetId():
            if str(self.sn3Input.GetValue()).__len__() == 16:
                self.sn3Input.SetValue(str(self.sn3Input.GetValue()).upper())
                self.sn4Input.SetFocus()
        elif event.GetId() == self.sn4Input.GetId():
            if str(self.sn4Input.GetValue()).__len__() == 16:
                self.sn4Input.SetValue(str(self.sn4Input.GetValue()).upper())
                self.sn5Input.SetFocus()
        elif event.GetId() == self.sn5Input.GetId():
            if str(self.sn5Input.GetValue()).__len__() == 16:
                self.sn5Input.SetValue(str(self.sn5Input.GetValue()).upper())
                self.sn6Input.SetFocus()
        elif event.GetId() == self.sn6Input.GetId():
            if str(self.sn6Input.GetValue()).__len__() == 16:
                self.sn6Input.SetValue(str(self.sn6Input.GetValue()).upper())
                self.sn7Input.SetFocus()
        elif event.GetId() == self.sn7Input.GetId():
            if str(self.sn7Input.GetValue()).__len__() == 16:
                self.sn7Input.SetValue(str(self.sn7Input.GetValue()).upper())
                self.sn8Input.SetFocus()
        elif event.GetId() == self.sn8Input.GetId():
            if str(self.sn8Input.GetValue()).__len__() == 16:
                self.sn8Input.SetValue(str(self.sn8Input.GetValue()).upper())
                self.sn9Input.SetFocus()
        elif event.GetId() == self.sn9Input.GetId():
            if str(self.sn9Input.GetValue()).__len__() == 16:
                self.sn9Input.SetValue(str(self.sn9Input.GetValue()).upper())
                self.sn10Input.SetFocus()
        elif event.GetId() == self.sn10Input.GetId():
            if str(self.sn10Input.GetValue()).__len__() == 16:
                self.sn10Input.SetValue(str(self.sn10Input.GetValue()).upper())
                self.sn11Input.SetFocus()

        elif event.GetId() == self.sn11Input.GetId():
            if str(self.sn11Input.GetValue()).__len__() == 16:
                self.sn11Input.SetValue(str(self.sn11Input.GetValue()).upper())
                self.sn12Input.SetFocus()
        elif event.GetId() == self.sn12Input.GetId():
            if str(self.sn12Input.GetValue()).__len__() == 16:
                self.sn12Input.SetValue(str(self.sn12Input.GetValue()).upper())
                if self.show24:
                    self.sn13Input.SetFocus()
                else:
                    print("12 terminal end print boxcode")
                    self.submitTmsCheck(event)
                    event.Skip()
        elif event.GetId() == self.sn13Input.GetId():
            if str(self.sn13Input.GetValue()).__len__() == 16:
                self.sn13Input.SetValue(str(self.sn13Input.GetValue()).upper())
                self.sn14Input.SetFocus()
        elif event.GetId() == self.sn14Input.GetId():
            if str(self.sn14Input.GetValue()).__len__() == 16:
                self.sn14Input.SetValue(str(self.sn14Input.GetValue()).upper())
                self.sn15Input.SetFocus()
        elif event.GetId() == self.sn15Input.GetId():
            if str(self.sn15Input.GetValue()).__len__() == 16:
                self.sn15Input.SetValue(str(self.sn15Input.GetValue()).upper())
                self.sn16Input.SetFocus()
        elif event.GetId() == self.sn16Input.GetId():
            if str(self.sn16Input.GetValue()).__len__() == 16:
                self.sn16Input.SetValue(str(self.sn16Input.GetValue()).upper())
                self.sn17Input.SetFocus()
        elif event.GetId() == self.sn17Input.GetId():
            if str(self.sn17Input.GetValue()).__len__() == 16:
                self.sn17Input.SetValue(str(self.sn17Input.GetValue()).upper())
                self.sn18Input.SetFocus()
        elif event.GetId() == self.sn18Input.GetId():
            if str(self.sn18Input.GetValue()).__len__() == 16:
                self.sn18Input.SetValue(str(self.sn18Input.GetValue()).upper())
                self.sn19Input.SetFocus()
        elif event.GetId() == self.sn19Input.GetId():
            if str(self.sn19Input.GetValue()).__len__() == 16:
                self.sn19Input.SetValue(str(self.sn19Input.GetValue()).upper())
                self.sn20Input.SetFocus()
        elif event.GetId() == self.sn20Input.GetId():
            if str(self.sn20Input.GetValue()).__len__() == 16:
                self.sn20Input.SetValue(str(self.sn20Input.GetValue()).upper())
                self.sn21Input.SetFocus()
        elif event.GetId() == self.sn21Input.GetId():
            if str(self.sn21Input.GetValue()).__len__() == 16:
                self.sn21Input.SetValue(str(self.sn21Input.GetValue()).upper())
                self.sn22Input.SetFocus()
        elif event.GetId() == self.sn22Input.GetId():
            if str(self.sn22Input.GetValue()).__len__() == 16:
                self.sn22Input.SetValue(str(self.sn22Input.GetValue()).upper())
                self.sn23Input.SetFocus()
        elif event.GetId() == self.sn23Input.GetId():
            if str(self.sn23Input.GetValue()).__len__() == 16:
                self.sn23Input.SetValue(str(self.sn23Input.GetValue()).upper())
                self.sn24Input.SetFocus()
        elif event.GetId() == self.sn24Input.GetId():
            if str(self.sn24Input.GetValue()).__len__() == 16:
                self.sn24Input.SetValue(str(self.sn24Input.GetValue()).upper())
                self.submitTmsCheck(event)
                print("24 terminal end print boxcode")
        event.Skip()

    def hide24label(self):
        self.show24 = False

        self.sn13Input.Hide()
        self.sn14Input.Hide()
        self.sn15Input.Hide()
        self.sn16Input.Hide()
        self.sn17Input.Hide()
        self.sn18Input.Hide()
        self.sn19Input.Hide()
        self.sn20Input.Hide()
        self.sn21Input.Hide()
        self.sn22Input.Hide()
        self.sn23Input.Hide()
        self.sn24Input.Hide()

        self.sn13View.Hide()
        self.sn14View.Hide()
        self.sn15View.Hide()
        self.sn16View.Hide()
        self.sn17View.Hide()
        self.sn18View.Hide()
        self.sn19View.Hide()
        self.sn20View.Hide()
        self.sn21View.Hide()
        self.sn22View.Hide()
        self.sn23View.Hide()
        self.sn24View.Hide()

    def show24label(self):
        self.show24 = True

        self.sn13Input.Show()
        self.sn14Input.Show()
        self.sn15Input.Show()
        self.sn16Input.Show()
        self.sn17Input.Show()
        self.sn18Input.Show()
        self.sn19Input.Show()
        self.sn20Input.Show()
        self.sn21Input.Show()
        self.sn22Input.Show()
        self.sn23Input.Show()
        self.sn24Input.Show()

        self.sn13View.Show()
        self.sn14View.Show()
        self.sn15View.Show()
        self.sn16View.Show()
        self.sn17View.Show()
        self.sn18View.Show()
        self.sn19View.Show()
        self.sn20View.Show()
        self.sn21View.Show()
        self.sn22View.Show()
        self.sn23View.Show()
        self.sn24View.Show()

    snPath = ''
    boxPath = ''
    infoPath = ''

    def createSNCode(self, sn):
        if sn.__len__() < 16:
            print("createCode  len error")
            return
        snStr = str(sn)
        code = barcode.Code128(snStr, writer=ImageWriter())
        paths = "./sn/" + snStr[2:7] + "/"
        if not os.path.exists(paths):
            os.makedirs(paths)
        code.save(paths + "/" + snStr,
                  {'text_distance': 0.5, 'module_height': 6, 'module_width': 0.14, 'quiet_zone': 1, 'font_size': 10})
        self.snPath = paths + "/" + snStr + ".png"
        print("createSNCode   self.snn = " + self.snPath)

    def printSNCode(self, sn):
        self.getTerminalSN(sn)
        sn = str(self.snShowInput.GetValue()).replace("\n", "")
        print("printSNCode sn = ", sn)
        if len(sn) == 0:
            self.snShowInput.SetValue("SN未获取到")
        elif len(sn) < 16:
            self.snShowInput.SetLabelText("SN不是正确的WP***")
            return
        self.createSNCode(sn)
        try:
            # self.createCode(str(self.snShowInput.GetValue()))
            print("print sn code")
            printer_name = win32print.GetDefaultPrinter()
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)
            bmp = Image.open(self.snPath)
            if bmp.size[0] < bmp.size[1]:
                bmp = bmp.rotate(0)
            # ratios = [1.0 * printable_area[0] / bmp.size[1], 1.0 * printable_area[1] / bmp.size[0]]
            # scale = min(ratios)
            scale = 1
            hDC.StartDoc(self.snPath)
            hDC.StartPage()
            dib = ImageWin.Dib(bmp)
            scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
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
            print("print_sn_img " + (str)(e.args))
            return False

    isInsert = False

    def getTerminalSN(self, sn):
        print("getSN(self, event):")
        try:
            tempsn = subprocess.Popen("adb shell getprop persist.wp.generatesn.tempsn",
                                      shell=True,
                                      stdout=subprocess.PIPE,
                                      stdin=subprocess.PIPE)
            adbSnVal = str(tempsn.stdout.read().decode())
            print("tempsn",adbSnVal)
            if len(adbSnVal) < 16:
                pi = subprocess.Popen("adb shell getprop ro.boot.serialno",
                                      shell=True,
                                      stdout=subprocess.PIPE,
                                      stdin=subprocess.PIPE)
                adbSnVal = str(pi.stdout.read().decode())
            print("serialnosn",adbSnVal)

            if "WP" in adbSnVal:
                # sn = adbSnVal[adbSnVal.index("WP"):adbSnVal.index("WP") + 16]
                self.snShowInput.SetValue(str(adbSnVal))
            else:
                self.snShowInput.SetValue("不是WP的SN")

        except Exception as e:
            self.snShowInput.SetValue("ex: 未获取到SN")
            print(e.args)

    def checkOrderNo(self):
        orderNo = self.orderNoInput.GetValue()
        b = True
        if len(str(orderNo)) < 10:
            win32api.MessageBox(0, "工单输入错误，请检查", "提醒", win32con.MB_ICONWARNING)
            b = False
            return b
        # sns = self.getInputSn()
        # print("checkSNS sns",sns)
        # if len(str(sns)) == 0:
        #     win32api.MessageBox(0, "SN号码错误，请检查", "提醒", win32con.MB_ICONWARNING)
        #     b = False
        return b

    def clickSubmitCheck(self, event):
        if win32api.MessageBox(0, "箱未装满,确定要装箱吗?", "警告", win32con.MB_OKCANCEL) == 1:
            self.submitTmsCheck(event)
        else:
            pass

    def submitTmsCheck(self, event):
        # 检测数据合格性
        if not self.checkOrderNo():
            return
        sns = self.getInputSn()
        boxcode = self.orderNoInput.GetValue()
        print("第1关检测数据结束 sns=", sns)
        if (len(sns) < 16):
            win32api.MessageBox(0, "请检查SN!", "提醒", win32con.MB_ICONWARNING)
            return
        list_sns_split = sns.split(",")
        isValidSN = True
        for s in list_sns_split:
            if len(s) != 16:
                if len(s) != 0:
                    isValidSN = False
        if not isValidSN:
            win32api.MessageBox(0, "SN号码错误，请检查", "提醒", win32con.MB_ICONWARNING)
            return

        print("第2关检测数据结束")

        try:
            requrl = "http://192.168.200.17:8080/wizarView/manufacture/factory-order!boxing.action"
            reqdata = {"orderNo": boxcode, "sns": sns}
            data2 = json.dumps(reqdata)
            reqtimestamp = str(round(time.time() * 1000))
            reqsig = self.calcSig("V3rKG21ZgCNHYKBl6Fki40R1EM0ZgUC3", data2, reqtimestamp)
            print(reqsig.decode("utf8"))
            reqheaders = {"Timestamp": reqtimestamp, "Sig": reqsig, "Factory-Code": "0", }
            r0 = requests.post(requrl, timeout=3, data=data2, headers=reqheaders)
            self.tipsInput.SetValue('正在上传TMS，请稍等')
            responseresult = str(r0.content.decode("utf8"))
            print("response = " + responseresult)
            if responseresult.__contains__("DOCTYPE html"):
                self.tipsInput.SetValue('未获取到正确的返回结果,\n请联系服务器管理员')
                self.isCheckTMS = True
                self.printBoxCode(event)

                return
            repstatus = ""
            pyob = json.loads(responseresult)
            repstatus = pyob["status"]
            represult = ""
            repmsg = ""
            reperrorsn = ""
            if repstatus == 1:
                represult = pyob["result"]["boxCode"]
                self.boxNoInput.SetValue(represult)
                self.tipsInput.SetValue("状态:" + str(repstatus) + ",箱号:" + represult)
                self.isCheckTMS = True
            else:
                self.isCheckTMS = False
                repmsg = pyob["msg"]
                reperrorsn = pyob["result"]["errorSn"]
                switchs = {
                    1: "装箱成功",
                    1053: "工单未找到",
                    1054: "IMEI 耗尽",
                    1055: "MEID 耗尽",
                    1059: "没有足够的 MEID",
                    1060: "工单未找到PCBA号",
                    1061: "发现有终端二次装箱",
                    1062: "此工单已取消",
                    1063: "PCBA 存在",
                    1064: "未知 CODE",
                    1065: "未知 SN",
                    1066: "报废的SN",
                    1067: "此工单已完成",
                    1068: "工单SN溢出",
                    1069: "未知工单类型",
                    1070: "无生产记录",
                    1071: "工厂订单序列号型号不匹配",
                    1072: "工厂订单类型不匹配",
                    1073: "业主有工厂信息",
                    1074: "终端已经报废，不能报废",
                    1075: "终端已装箱，不能报废",
                    1076: "终端已装箱，不能还原",
                    1077: "终端序列号计数溢出，无法恢复",
                    1078: "工厂订单签名错误",
                    1079: "客户端代号与名字不匹配",
                    1080: "有终端未完成",
                }
                statusstr = ""
                try:
                    statusstr = switchs[repstatus]
                except KeyError as e:
                    self.isCheckTMS = False
                    statusstr = "服务器返回未知状态," + repmsg
                    pass
                self.tipsInput.SetValue("状态:" + statusstr + ",SN=" + reperrorsn)
                self.printBoxCode(event)
        except Exception as e:
            self.isCheckTMS = False
            self.tipsInput.SetValue("出错啦: " + str(e.args))
            print(e.args)
        event.Skip()

    def calcSig(self, token, msg, timestamp):
        preSigData = str(token) + str(msg) + str(timestamp)
        # print("preSigData  : " + preSigData)
        out1 = hashlib.sha256(preSigData.encode("utf8")).hexdigest()
        plain_data = base64.b64encode(bytes(out1, 'utf-8'), altchars=None)
        return plain_data

    def box_sn_to_png(self, text_str, filename):
        ean = barcode.Code128(text_str, writer=ImageWriter())

        if self.show24:
            ean.save(filename,
                     {'text_distance': 0.3, 'module_height': 1, 'module_width': 0.1, 'quiet_zone': 0.2, 'font_size': 6})
            # encoder = Code128Encoder(text_str, options={"ttf_font": "C:/Windows/Fonts/SimHei.ttf", "ttf_fontsize": 8,
            #                                             "bottom_border": 5, "height": 10, "label_border": 2})
            # encoder.save(filename, bar_width=1)
        else:
            ean.save(filename,
                     {'text_distance': 1, 'module_height': 3, 'module_width': 0.12, 'quiet_zone': 3, 'font_size': 10})

    isCheckTMS = False

    def printBoxCode(self, event):
        if not self.isCheckTMS:
            win32api.MessageBox(0, "TMS检查未通过!", "提醒", win32con.MB_ICONWARNING)
            return
        orderno = self.orderNoInput.GetValue()
        paths = "./order/" + orderno
        if not os.path.exists(paths):
            os.makedirs(paths)
        self.creatBoxCode(orderno, self.getInputSn())
        # self.orderNoInput.SetValue(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        event.Skip()

    def printCodePage(self, event):
        if len(str(self.orderNoInput.GetValue())) > 10 and len(str(self.boxNoInput.GetValue())) > 5:
            if event.GetId() == self.reprintpage1Btn.GetId():
                self.printerPrint(str(self.boxPath), str(self.orderNoInput.GetValue()), str(self.boxNoInput.GetValue()))
            elif event.GetId() == self.reprintpage2Btn.GetId():
                self.printerPrint(str(self.infoPath), str(self.orderNoInput.GetValue()),
                                  str(self.boxNoInput.GetValue()))
        else:
            win32api.MessageBox(0, "工单号不正确,不能打印", "提醒", win32con.MB_ICONWARNING)

    def getInputSn(self):
        list_sns_value = []
        if len(str(self.sn1Input.GetValue())) == 16:
            list_sns_value.append(str(self.sn1Input.GetValue()))
        elif len(str(self.sn1Input.GetValue())) != 0:
            win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn1Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
            return

        if len(str(self.sn2Input.GetValue())) == 16:
            list_sns_value.append(str(self.sn2Input.GetValue()))
        elif len(str(self.sn2Input.GetValue())) != 0:
            win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn2Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
            return
        if len(str(self.sn3Input.GetValue())) == 16:
            list_sns_value.append(str(self.sn3Input.GetValue()))
        elif len(str(self.sn3Input.GetValue())) != 0:
            win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn3Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
            return
        if len(str(self.sn4Input.GetValue())) == 16:
            list_sns_value.append(str(self.sn4Input.GetValue()))
        elif len(str(self.sn4Input.GetValue())) != 0:
            win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn4Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
            return
        if len(str(self.sn5Input.GetValue())) == 16:
            list_sns_value.append(str(self.sn5Input.GetValue()))
        elif len(str(self.sn5Input.GetValue())) != 0:
            win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn5Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
            return
        if len(str(self.sn6Input.GetValue())) == 16:
            list_sns_value.append(str(self.sn6Input.GetValue()))
        elif len(str(self.sn6Input.GetValue())) != 0:
            win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn6Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
            return
        if len(str(self.sn7Input.GetValue())) == 16:
            list_sns_value.append(str(self.sn7Input.GetValue()))
        elif len(str(self.sn7Input.GetValue())) != 0:
            win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn7Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
            return
        if len(str(self.sn8Input.GetValue())) == 16:
            list_sns_value.append(str(self.sn8Input.GetValue()))
        elif len(str(self.sn8Input.GetValue())) != 0:
            win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn8Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
            return
        if len(str(self.sn9Input.GetValue())) == 16:
            list_sns_value.append(str(self.sn9Input.GetValue()))
        elif len(str(self.sn9Input.GetValue())) != 0:
            win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn9Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
            return
        if len(str(self.sn10Input.GetValue())) == 16:
            list_sns_value.append(str(self.sn10Input.GetValue()))
        elif len(str(self.sn10Input.GetValue())) != 0:
            win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn10Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
            return
        if len(str(self.sn11Input.GetValue())) == 16:
            list_sns_value.append(str(self.sn11Input.GetValue()))
        elif len(str(self.sn11Input.GetValue())) != 0:
            win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn11Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
            return
        if len(str(self.sn12Input.GetValue())) == 16:
            list_sns_value.append(str(self.sn12Input.GetValue()))
        elif len(str(self.sn12Input.GetValue())) != 0:
            win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn12Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
            return
        if self.show24:
            if len(str(self.sn12Input.GetValue())) == 16:
                list_sns_value.append(str(self.sn12Input.GetValue()))
            elif len(str(self.sn12Input.GetValue())) != 0:
                win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn12Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
                return
            if len(str(self.sn13Input.GetValue())) == 16:
                list_sns_value.append(str(self.sn13Input.GetValue()))
            elif len(str(self.sn13Input.GetValue())) != 0:
                win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn13Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
                return
            if len(str(self.sn14Input.GetValue())) == 16:
                list_sns_value.append(str(self.sn14Input.GetValue()))
            elif len(str(self.sn14Input.GetValue())) != 0:
                win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn14Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
                return
            if len(str(self.sn15Input.GetValue())) == 16:
                list_sns_value.append(str(self.sn15Input.GetValue()))
            elif len(str(self.sn15Input.GetValue())) != 0:
                win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn15Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
                return
            if len(str(self.sn16Input.GetValue())) == 16:
                list_sns_value.append(str(self.sn16Input.GetValue()))
            elif len(str(self.sn16Input.GetValue())) != 0:
                win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn16Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
                return
            if len(str(self.sn17Input.GetValue())) == 16:
                list_sns_value.append(str(self.sn12Input.GetValue()))
            elif len(str(self.sn17Input.GetValue())) != 0:
                win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn17Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
                return
            if len(str(self.sn18Input.GetValue())) == 16:
                list_sns_value.append(str(self.sn18Input.GetValue()))
            elif len(str(self.sn18Input.GetValue())) != 0:
                win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn18Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
                return
            if len(str(self.sn19Input.GetValue())) == 16:
                list_sns_value.append(str(self.sn19Input.GetValue()))
            elif len(str(self.sn19Input.GetValue())) != 0:
                win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn19Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
                return
            if len(str(self.sn20Input.GetValue())) == 16:
                list_sns_value.append(str(self.sn20Input.GetValue()))
            elif len(str(self.sn20Input.GetValue())) != 0:
                win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn20Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
                return
            if len(str(self.sn21Input.GetValue())) == 16:
                list_sns_value.append(str(self.sn21Input.GetValue()))
            elif len(str(self.sn21Input.GetValue())) != 0:
                win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn21Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
                return
            if len(str(self.sn23Input.GetValue())) == 16:
                list_sns_value.append(str(self.sn23Input.GetValue()))
            elif len(str(self.sn23Input.GetValue())) != 0:
                win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn23Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
                return
            if len(str(self.sn24Input.GetValue())) == 16:
                list_sns_value.append(str(self.sn24Input.GetValue()))
            elif len(str(self.sn24Input.GetValue())) != 0:
                win32api.MessageBox(0, "SN号码错误，请检查: " + self.sn24Input.GetValue(), "提醒", win32con.MB_ICONWARNING)
                return
        return ','.join(list_sns_value)

    def creatBoxCode(self, orderno, sns):
        global boxsns, snx, sny, boxinfo
        boxcode = self.boxNoInput.GetLabelText()
        print("sns = " + sns + ",orderno= " + orderno + ",boxcode = " + boxcode)
        for sn in sns.split(","):
            print('barcode_fun ' + sn)
            self.box_sn_to_png(str(sn), './order/' + orderno + '/' + sn)

        if len(sns.split(",")) >= 1:
            base_img0 = Image.open('./order/' + orderno + '/' + sns.split(",")[0] + '.png')
            snx = base_img0.size[0]
            sny = base_img0.size[1]
            if self.show24:
                boxsns = Image.new('RGB', (2 * snx, 12 * sny), color="#FFFFFF")
                boxinfo = Image.new('RGB', (2 * snx, 12 * sny), color="#FFFFFF")
            else:
                boxsns = Image.new('RGB', (2 * snx, 6 * sny), color="#FFFFFF")
                boxinfo = Image.new('RGB', (2 * snx, 6 * sny), color="#FFFFFF")
            boxsns.paste(base_img0, (0 * snx, 0 * sny, 1 * snx, 1 * sny))
        if len(sns.split(",")) >= 2:
            base_img1 = Image.open('./order/' + orderno + '/' + sns.split(",")[1] + '.png')
            boxsns.paste(base_img1, (1 * snx, 0 * sny, 2 * snx, 1 * sny))
        if len(sns.split(",")) >= 3:
            base_img2 = Image.open('./order/' + orderno + '/' + sns.split(",")[2] + '.png')
            boxsns.paste(base_img2, (0 * snx, 1 * sny, 1 * snx, 2 * sny))
        if len(sns.split(",")) >= 4:
            base_img3 = Image.open('./order/' + orderno + '/' + sns.split(",")[3] + '.png')
            boxsns.paste(base_img3, (1 * snx, 1 * sny, 2 * snx, 2 * sny))
        if len(sns.split(",")) >= 5:
            base_img4 = Image.open('./order/' + orderno + '/' + sns.split(",")[4] + '.png')
            boxsns.paste(base_img4, (0 * snx, 2 * sny, 1 * snx, 3 * sny))
        if len(sns.split(",")) >= 6:
            base_img5 = Image.open('./order/' + orderno + '/' + sns.split(",")[5] + '.png')
            boxsns.paste(base_img5, (1 * snx, 2 * sny, 2 * snx, 3 * sny))
        if len(sns.split(",")) >= 7:
            base_img6 = Image.open('./order/' + orderno + '/' + sns.split(",")[6] + '.png')
            boxsns.paste(base_img6, (0 * snx, 3 * sny, 1 * snx, 4 * sny))
        if len(sns.split(",")) >= 8:
            base_img7 = Image.open('./order/' + orderno + '/' + sns.split(",")[7] + '.png')
            boxsns.paste(base_img7, (1 * snx, 3 * sny, 2 * snx, 4 * sny))
        if len(sns.split(",")) >= 9:
            base_img8 = Image.open('./order/' + orderno + '/' + sns.split(",")[8] + '.png')
            boxsns.paste(base_img8, (0 * snx, 4 * sny, 1 * snx, 5 * sny))
        if len(sns.split(",")) >= 10:
            base_img9 = Image.open('./order/' + orderno + '/' + sns.split(",")[9] + '.png')
            boxsns.paste(base_img9, (1 * snx, 4 * sny, 2 * snx, 5 * sny))
        if len(sns.split(",")) >= 11:
            base_img10 = Image.open('./order/' + orderno + '/' + sns.split(",")[10] + '.png')
            boxsns.paste(base_img10, (0 * snx, 5 * sny, 1 * snx, 6 * sny))
        if len(sns.split(",")) >= 12:
            base_img11 = Image.open('./order/' + orderno + '/' + sns.split(",")[11] + '.png')
            boxsns.paste(base_img11, (1 * snx, 5 * sny, 2 * snx, 6 * sny))
        if self.show24:
            if len(sns.split(",")) >= 13:
                base_img12 = Image.open('./order/' + orderno + '/' + sns.split(",")[12] + '.png')
                boxsns.paste(base_img12, (0 * snx, 6 * sny, 1 * snx, 7 * sny))
            if len(sns.split(",")) >= 14:
                base_img13 = Image.open('./order/' + orderno + '/' + sns.split(",")[13] + '.png')
                boxsns.paste(base_img13, (1 * snx, 6 * sny, 2 * snx, 7 * sny))
            if len(sns.split(",")) >= 15:
                base_img14 = Image.open('./order/' + orderno + '/' + sns.split(",")[14] + '.png')
                boxsns.paste(base_img14, (0 * snx, 7 * sny, 1 * snx, 8 * sny))
            if len(sns.split(",")) >= 16:
                base_img15 = Image.open('./order/' + orderno + '/' + sns.split(",")[15] + '.png')
                boxsns.paste(base_img15, (1 * snx, 7 * sny, 2 * snx, 8 * sny))
            if len(sns.split(",")) >= 17:
                base_img16 = Image.open('./order/' + orderno + '/' + sns.split(",")[16] + '.png')
                boxsns.paste(base_img16, (0 * snx, 8 * sny, 1 * snx, 9 * sny))
            if len(sns.split(",")) >= 18:
                base_img17 = Image.open('./order/' + orderno + '/' + sns.split(",")[17] + '.png')
                boxsns.paste(base_img17, (1 * snx, 8 * sny, 2 * snx, 9 * sny))
            if len(sns.split(",")) >= 19:
                base_img18 = Image.open('./order/' + orderno + '/' + sns.split(",")[18] + '.png')
                boxsns.paste(base_img18, (0 * snx, 9 * sny, 1 * snx, 10 * sny))
            if len(sns.split(",")) >= 20:
                base_img19 = Image.open('./order/' + orderno + '/' + sns.split(",")[19] + '.png')
                boxsns.paste(base_img19, (1 * snx, 9 * sny, 2 * snx, 10 * sny))
            if len(sns.split(",")) >= 21:
                base_img20 = Image.open('./order/' + orderno + '/' + sns.split(",")[20] + '.png')
                boxsns.paste(base_img20, (0 * snx, 10 * sny, 1 * snx, 11 * sny))
            if len(sns.split(",")) >= 22:
                base_img21 = Image.open('./order/' + orderno + '/' + sns.split(",")[21] + '.png')
                boxsns.paste(base_img21, (1 * snx, 10 * sny, 2 * snx, 11 * sny))
            if len(sns.split(",")) >= 23:
                base_img22 = Image.open('./order/' + orderno + '/' + sns.split(",")[22] + '.png')
                boxsns.paste(base_img22, (0 * snx, 11 * sny, 1 * snx, 12 * sny))
            if len(sns.split(",")) >= 24:
                base_img23 = Image.open('./order/' + orderno + '/' + sns.split(",")[23] + '.png')
                boxsns.paste(base_img23, (1 * snx, 11 * sny, 2 * snx, 12 * sny))

        boxsnsimgpath = './order/' + orderno + '/' + boxcode + '.png'
        self.boxPath = boxsnsimgpath
        boxsns.save(boxsnsimgpath)
        infoimgpath = './order/' + orderno + '/' + boxcode + '_info.png'
        self.infoPath = infoimgpath

        boxinfo.save(infoimgpath)
        self.printerPrint(boxsnsimgpath, orderno, boxcode)
        self.printerPrint(infoimgpath, orderno, boxcode)

    def printerPrint(self, imagePath, orderno, boxcode):
        try:
            printer_name = win32print.GetDefaultPrinter()
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)
            imageBmp = Image.open(imagePath)
            if imagePath.__contains__("info"):
                self.creatBoxInfo(imageBmp, orderno, boxcode)
            scale = 1
            hDC.StartDoc(imagePath)
            hDC.StartPage()
            dib = ImageWin.Dib(imageBmp)
            scaled_width, scaled_height = [int(scale * i) for i in imageBmp.size]
            x1 = 60  # 控制位置
            y1 = 20
            x2 = x1 + scaled_width
            y2 = y1 + scaled_height
            dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))
            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()
            return True
        except Exception as e:
            print("print_img " + (str)(e.args))
            return False

    def creatBoxInfo(self, boxbmp, orderno, boxcode):
        draw = ImageDraw.Draw(boxbmp)
        width, height = boxbmp.size
        color = "#000000"
        header_chinese_font = ImageFont.truetype("simsun.ttc", 44, encoding="unic")  # 设置字体
        header_english_font = ImageFont.truetype("simsun.ttc", 32, encoding="unic")  # 设置字体
        normal_chinese_font = ImageFont.truetype("simsun.ttc", 24, encoding="unic")  # 设置字体
        normal_english_font = ImageFont.truetype("simsun.ttc", 24, encoding="unic")  # 设置字体
        # header头
        draw.text((80, 10), u'%s' % self.chinese[0], color, header_chinese_font)
        draw.text((100, 50), u'%s' % self.english[0], color, header_english_font)

        draw.text((90, 110), u'%s' % self.chinese[1], color, normal_chinese_font)
        draw.text((90, 130), u'%s' % self.english[1], color, normal_english_font)
        draw.text((220, 120), 'WIZARPOS  ' + self.choiceType, color, header_english_font)

        draw.text((90, 170), u'%s' % self.chinese[2], color, normal_chinese_font)
        draw.text((90, 190), u'%s' % self.english[2], color, normal_english_font)
        draw.text((220, 180), self.boxsize, color, header_english_font)

        draw.text((90, 230), u'%s' % self.chinese[3], color, normal_chinese_font)
        draw.text((90, 250), u'%s' % self.english[3], color, normal_english_font)
        draw.text((220, 240), '____ OF ____', color, header_english_font)

        draw.text((90, 290), u'%s' % self.chinese[4], color, normal_chinese_font)
        draw.text((90, 310), u'%s' % self.english[4], color, normal_english_font)
        draw.text((220, 300), boxcode, color, header_english_font)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=6,
            border=4
        )
        # 传入数据
        qr.add_data(boxcode)
        qr.make(fit=True)
        # 生成二维码
        qrimg = qr.make_image()
        icon_w, icon_h = qrimg.size
        w = int((width - icon_w) / 2)
        h = int((height - icon_h))
        boxbmp.paste(qrimg, (w, h), mask=None)
        boxbmp.save('./order/' + orderno + '/' + boxcode + '_info.png', 'png')

    # also, you can custom port and host
    # ConnectionTracer.config.PORT = 5037
    #
    # bind hook function


def hook_function(devices: set):
    print(devices)
    if len(devices) > 0:
        frame.printSNCode("")
    else:
        print("devices unplugin")
        frame.snShowInput.SetValue("")
    #
    # # also you can directly run:
    # # ConnectionTracer.start(hook_function, port=8080)
    # #
    # print('tracer already started')
    #
    # # get connection status
    # print('now status: ', ConnectionTracer.get_status())

    # do something else you want
    # time.sleep(1)
    #
    # # stop it
    # ConnectionTracer.stop()
    # print('tracer stopped')


count = 0


def listen_device():
    global count
    while True:
        count = count + 1
        print("device get count ", count)
        frame.printSNCode("")
        time.sleep(2)


if __name__ == '__main__':
    app = wx.App()
    frame = MyLabelPrint(None)
    frame.Show()
    # listenThreading = threading.Thread(target=listen_device, args=())
    # listenThreading.start()
    ConnectionTracer.start(hook_function)
    app.MainLoop()
