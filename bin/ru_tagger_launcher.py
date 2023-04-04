# -*- coding:utf-8 -*-
"""
Copyright (c) 2022-2023, LIU Dingjia, BFSU NLP Team, BFSU Corpus Research Group.
All rights reserved.
Email:
bfsunlp@gmail.com
dingjialiu@gmail.com
"""

import os
import wx
import wx.adv
import source.bfsu_stanza_tagger as bst

# Pseudo import for pyinstaller lib package
import chardet
import stanza
import stanza.resources.common as sc
from pubsub import pub
from wx.lib.wordwrap import wordwrap


class App(wx.App):

    def OnInit(self):
        lang = "ru"
        language = "Russian"
        cwd = os.getcwd()
        frame = bst.MainFrame(parent=None, id=-1, lang=lang, language=language, cwd=cwd)
        icon_path = os.path.join(os.path.join(cwd, 'resources/ico'), 'logo.ico')
        frame.SetIcon(wx.Icon(icon_path))
        frame.Show()
        self.SetTopWindow(frame)
        return True


if __name__ == "__main__":
    app = App()
    app.MainLoop()
