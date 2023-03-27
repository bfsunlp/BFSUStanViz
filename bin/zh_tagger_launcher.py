# -*- coding:utf-8 -*-
"""
Copyright (c) 2022-2023, LIU Dingjia, BFSUNLP Group.
All rights reserved.
Email: 
dingjialiu@gmail.com
bfsunlp@gmail.com
"""
import bin.bfsu_stanza_tagger as bst
import os
import stanza
import wx
import wx.adv
import codecs
import time
import shutil
import threading
import resources.read_file as rf
import scripts.lexical_analyzer as la
import chardet
import psutil
import multiprocessing
from pubsub import pub
from wx.lib.wordwrap import wordwrap



class AppZh(wx.App):

    def OnInit(self):
        lang = "zh"
        language = "Chinese Simplified"
        frame = bst.MainFrame(parent=None, id=-1, lang=lang, language=language)
        cwd = os.getcwd()
        icon_path = os.path.join(os.path.join(cwd, 'resources/ico'), 'logo.ico')
        frame.SetIcon(wx.Icon(icon_path))
        frame.Show()
        self.SetTopWindow(frame)
        return True


if __name__ == "__main__":
    app = AppZh()
    app.MainLoop()
