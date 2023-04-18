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
import codecs
import time
import shutil
import threading
import source.load_file as lf
import source.lexical_analyzer as la
import source.pipeline_loader as pl
from pubsub import pub
from wx.lib.wordwrap import wordwrap


# pubsub workers
class OpenFilesThread(threading.Thread):
    def __init__(self, path_list):
        threading.Thread.__init__(self)
        self.breakflag = False
        self.path_list = path_list
        self.start()

    def stop(self):
        self.breakflag = True

    def workproc(self):
        for each_path in self.path_list:
            encoding = lf.detect_encode(each_path)
            pub.sendMessage("open_files", mstatus=[each_path, encoding])

    def run(self):
        self.workproc()


class DownloadModelThread(threading.Thread):
    def __init__(self, model_path, lang):
        threading.Thread.__init__(self)
        self.breakflag = False
        self.model_path = model_path
        self.lang = lang
        self.start()

    def stop(self):
        self.breakflag = True

    def workproc(self):
        try:
            import stanza
            stanza.download(self.lang, model_dir=self.model_path)
            pub.sendMessage("download", mstatus="Download Finished!")
        except:
            pub.sendMessage("download", mstatus="Download Failed!")

    def run(self):
        self.workproc()


class ProcessingThread(threading.Thread):
    def __init__(self, model_path, lang, input_files, output_path, task, tagset, nlp):
        threading.Thread.__init__(self)
        self.num_of_file = 0
        self.breakflag = False
        self.model_path = model_path
        self.lang = lang
        self.input_files = input_files
        self.output_path = output_path
        self.task = task
        self.tagset = tagset
        self.nlp = nlp
        self.start()

    def stop(self):
        self.breakflag = True

    def workproc(self):
        current_file_num = 0
        self.num_of_file = len(self.input_files)
        for each_file in self.input_files:
            current_file_num += 1
            output_file = os.path.join(self.output_path, os.path.split(each_file)[-1])
            pub.sendMessage("process", mstatus=["process", output_file, current_file_num, self.num_of_file])
            la.process_file(source_path=each_file,
                            target_path=output_file,
                            task=self.task,
                            pipeline=self.nlp,
                            tagset=self.tagset)

            # time.sleep(2)
            # process_file(each_file, output_file, job, mode="multi", pipeline=nlp)

    def run(self):
        self.workproc()
        pub.sendMessage("process", mstatus=["finished", self.num_of_file])


# model download frame
class ModelDownloadFrame(wx.MiniFrame):
    def __init__(self, parent, title, pos=wx.DefaultPosition, size=(500, 150),
                 style=wx.DEFAULT_FRAME_STYLE, model_path=None, lang=None):
        wx.MiniFrame.__init__(self, parent, -1, title, pos, size, style)
        self.lang = lang
        self.panel = wx.Panel(self, -1)
        self.panel.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.parent = parent
        self.model_path = model_path
        self.FontCtrls = []
        # self.sys_font = wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.sys_font = self.panel.GetFont()
        self.sys_font.PointSize += 2
        self.frame_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.status_ctrl_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.status_title = wx.StaticText(self.panel, -1, "Download model:")
        self.FontCtrls.append(self.status_title)
        self.status_ctrl_sizer.Add(self.status_title, 0, wx.ALIGN_CENTER_VERTICAL)
        self.ai = wx.ActivityIndicator(self.panel)
        # self.ai.Start()
        self.status_ctrl_sizer.Add(self.ai, 0, wx.LEFT, 40)
        self.startButton = wx.Button(self.panel, label='Start Download')
        self.Bind(wx.EVT_BUTTON, self.OnStartDownload, self.startButton)
        self.FontCtrls.append(self.startButton)
        self.status_ctrl_sizer.Add(self.startButton, 0, wx.LEFT, 50)

        self.frame_sizer.Add(self.status_ctrl_sizer, 1, wx.LEFT | wx.TOP | wx.BOTTOM, 30)

        for ctrl in self.FontCtrls:
            ctrl.SetFont(self.sys_font)
        self.panel.SetSizer(self.frame_sizer)
        self.panel.Fit()
        pub.subscribe(self.startDownloadDisplay, "download")

    def OnCloseWindow(self, event):
        self.Destroy()
        self.parent.Enable()

    def OnStartDownload(self, event):
        self.startButton.Disable()
        download_model_work = DownloadModelThread(model_path=self.model_path, lang=self.lang)
        self.status_title.SetLabel("Downloading...")
        self.ai.Start()
        # time.sleep(3)
        # self.Destroy()

    def startDownloadDisplay(self, mstatus):
        self.status_title.SetLabel(mstatus)
        if mstatus == "Download Finished!":
            model_ids = [i for i in self.parent.model_list.keys()]
            for each_model_id in model_ids:
                self.parent.settings_menu.Remove(self.parent.model_list[each_model_id][2])
                self.parent.model_list.pop(each_model_id)
            for each_model_name in os.listdir(self.model_path):
                each_model_path = os.path.join(self.model_path, each_model_name)
                if os.path.isdir(each_model_path):
                    model_id = self.parent.model_start_id + 1
                    self.parent.model_start_id += 1
                    model_item = wx.MenuItem(self.parent.settings_menu, model_id, each_model_name,
                                             "Select model: " + each_model_name, wx.ITEM_RADIO)
                    self.parent.settings_menu.Append(model_item)
                    self.parent.model_list[model_id] = (each_model_name, each_model_path, model_item)
        self.ai.Stop()
        time.sleep(3)
        self.Destroy()
        self.parent.Enable()


# main frame
class MainFrame(wx.Frame):

    def __init__(self, parent, id, lang, language, cwd):
        self.lang = lang
        self.language = language
        self.cwd = cwd
        self.model_dir = os.path.join(self.cwd, "resources\\model")
        self.readme_path = os.path.join(self.cwd, "Readme.md")
        print("model_dir", self.model_dir)
        self.model_list = {}
        # print(os.listdir(self.model_dir))
        wx.Frame.__init__(self, parent, id, title="BFSU Stanza Tagger - [%s] v1.1" % self.language, size=(900, 700))
        self.CenterOnScreen()
        self.panel = wx.Panel(self, -1)
        self.CreateStatusBar()

        # Setting up the menu
        self.FontCtrls = []
        # self.sys_font = wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.sys_font = self.panel.GetFont()
        self.sys_font.PointSize += 2
        self.run_font = wx.Font(16, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_MAX, wx.FONTWEIGHT_BOLD)
        self.menuBar = wx.MenuBar()

        self.file_menu = wx.Menu()
        self.open_file = wx.MenuItem(self.file_menu, 101, "Open &File(s)", "Open text files...")
        self.Bind(wx.EVT_MENU, self.OnOpenFile, id=101)
        self.file_menu.Append(self.open_file)
        self.open_directory = wx.MenuItem(self.file_menu, 102, "&Open Folder",
                                          "Open a folder that contain multiple text files...")
        self.Bind(wx.EVT_MENU, self.OnOpenDir, id=102)
        self.file_menu.Append(self.open_directory)
        self.file_menu.AppendSeparator()
        self.clear = wx.MenuItem(self.file_menu, 103, "&Clear Files", "Clear the appended Files...")
        self.Bind(wx.EVT_MENU, self.OnClearFile, id=103)
        self.file_menu.Append(self.clear)
        self.file_menu.AppendSeparator()
        self.exit = wx.MenuItem(self.file_menu, 104, "&Exit", "Quit BFSUStanzaTagger - [Simplified Chinese] ...")
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, id=104)
        self.file_menu.Append(self.exit)

        self.menuBar.Append(self.file_menu, "&File")  # Adding the "file_menu" to the MenuBar

        self.settings_menu = wx.Menu()
        self.download_model = wx.MenuItem(self.settings_menu, 201, "Download Model",
                                          "Download trained neural model...")
        self.Bind(wx.EVT_MENU, self.MenuDownloadModel, id=201)
        # self.Bind(wx.EVT_MENU, self.Menu301To303, id=301)
        self.settings_menu.Append(self.download_model)
        self.clear_model = wx.MenuItem(self.settings_menu, 202, "&Clear Models (Not recommended)",
                                       "Delete the downloaded models...")
        self.Bind(wx.EVT_MENU, self.MenuClearModel, id=202)
        self.settings_menu.Append(self.clear_model)
        self.settings_menu.AppendSeparator()
        self.model_start_id = 300
        for each_model_name in os.listdir(self.model_dir):
            each_model_path = os.path.join(self.model_dir, each_model_name)
            if os.path.isdir(each_model_path):
                model_id = self.model_start_id + 1
                self.model_start_id += 1
                model_item = wx.MenuItem(self.settings_menu, model_id, each_model_name,
                                         "Select model: " + each_model_name, wx.ITEM_RADIO)
                self.settings_menu.Append(model_item)
                self.model_list[model_id] = (each_model_name, each_model_path, model_item)

        self.menuBar.Append(self.settings_menu, "&Settings")

        self.help_menu = wx.Menu()
        self.about = wx.MenuItem(self.help_menu, 401, "About",
                                 "Information about BFSUStanzaTagger - [Simplified Chinese] ...")
        self.help_menu.Append(self.about)
        self.Bind(wx.EVT_MENU, self.MenuAbout, id=401)

        # self.licence = wx.MenuItem(self.help_menu, 402, "Licence",
        # "Check BFSUStanza Licence...")
        # self.help_menu.Append(self.licence)

        self.menuBar.Append(self.help_menu, "&Help")

        self.SetMenuBar(self.menuBar)  # Adding the MenuBar to the Frame content.
        self.Show(True)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.mode_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.task_names = ["POS Tagging", "Tokenization", "Lemmatization"]
        self.choose_task = wx.RadioBox(self.panel, label="Choose a task:", choices=self.task_names)
        self.FontCtrls.append(self.choose_task)
        self.mode_sizer.Add(self.choose_task, 1, wx.EXPAND | wx.ALL, 5)

        self.tag_set = ["Treebank POS", "Universal POS"]
        self.choose_tagset = wx.RadioBox(self.panel, label="Choose a tagset:", choices=self.tag_set)
        self.FontCtrls.append(self.choose_tagset)
        self.mode_sizer.Add(self.choose_tagset, 1, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.mode_sizer, 0, wx.EXPAND)

        self.target_path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.target_path_text = wx.StaticText(self.panel, -1, "Output path: ")
        self.FontCtrls.append(self.target_path_text)
        self.target_path_sizer.Add(self.target_path_text, 0, wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.target_path_ctrl = wx.TextCtrl(self.panel)
        self.FontCtrls.append(self.target_path_ctrl)
        self.target_path_sizer.Add(self.target_path_ctrl, 5, wx.EXPAND | wx.ALL, 5)
        self.target_path_open = wx.Button(self.panel, 401, "Choose")
        self.Bind(wx.EVT_BUTTON, self.OnChooseTargetPath, self.target_path_open)
        self.FontCtrls.append(self.target_path_open)
        self.target_path_sizer.Add(self.target_path_open, 1, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.target_path_sizer, 1, wx.EXPAND)

        self.function_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.open_file_button = wx.Button(self.panel, 501, "Open File(s)")
        self.Bind(wx.EVT_BUTTON, self.OnOpenFile, self.open_file_button)
        self.open_directory_button = wx.Button(self.panel, 502, "Open Folder")
        self.Bind(wx.EVT_BUTTON, self.OnOpenDir, self.open_directory_button)
        self.clear_file_button = wx.Button(self.panel, 503, "Clear All")
        self.Bind(wx.EVT_BUTTON, self.OnClearFile, self.clear_file_button)
        self.run_button = wx.Button(self.panel, 504, "RUN!")
        self.Bind(wx.EVT_BUTTON, self.OnRun, self.run_button)
        self.run_button.SetFont(self.run_font)
        self.FontCtrls.append(self.open_file_button)
        self.FontCtrls.append(self.open_directory_button)
        self.FontCtrls.append(self.clear_file_button)

        self.function_button_sizer.Add(self.open_file_button, 1, wx.EXPAND | wx.ALL, 5)
        self.function_button_sizer.Add(self.open_directory_button, 1, wx.EXPAND | wx.ALL, 5)
        self.function_button_sizer.Add(self.clear_file_button, 1, wx.EXPAND | wx.ALL, 5)
        self.function_button_sizer.Add(self.run_button, 1, wx.EXPAND | wx.ALL, 5)

        self.main_sizer.Add(self.function_button_sizer, 1, wx.EXPAND)

        self.file_list_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.input_file_list_sizer = wx.BoxSizer(wx.VERTICAL)
        self.input_file_Title = wx.StaticText(self.panel, -1, "Input files:")
        self.FontCtrls.append(self.input_file_Title)
        self.input_file_list_sizer.Add(self.input_file_Title, 0, wx.EXPAND | wx.ALL, 5)
        self.input_file_list_ctrl = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT)
        self.input_file_list_ctrl.InsertColumn(0, "File", width=320)
        self.input_file_list_ctrl.InsertColumn(1, "Encoding", width=80)
        self.FontCtrls.append(self.input_file_list_ctrl)
        self.input_file_list_sizer.Add(self.input_file_list_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        self.output_file_list_sizer = wx.BoxSizer(wx.VERTICAL)
        self.output_file_Title = wx.StaticText(self.panel, -1, "Output files:")
        self.FontCtrls.append(self.output_file_Title)
        self.output_file_list_sizer.Add(self.output_file_Title, 0, wx.EXPAND | wx.ALL, 5)
        self.output_file_list_ctrl = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT)
        self.output_file_list_ctrl.InsertColumn(0, "File", width=320)
        self.output_file_list_ctrl.InsertColumn(1, "Status", width=80)
        self.FontCtrls.append(self.output_file_list_ctrl)
        self.output_file_list_sizer.Add(self.output_file_list_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        self.file_list_sizer.Add(self.input_file_list_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.file_list_sizer.Add(self.output_file_list_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.main_sizer.Add(self.file_list_sizer, 10, wx.EXPAND)

        self.gauge_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.process_gauge = wx.Gauge(self.panel, -1, range=100)
        self.gauge_sizer.Add(self.process_gauge, 1, wx.EXPAND | wx.ALL, 5)

        self.main_sizer.Add(self.gauge_sizer, 1, wx.EXPAND)

        for ctrl in self.FontCtrls:
            ctrl.SetFont(self.sys_font)

        self.panel.SetSizer(self.main_sizer)
        self.panel.Fit()
        pub.subscribe(self.openFilesDisplay, "open_files")
        pub.subscribe(self.runDisplay, "process")

    def MenuDownloadModel(self, event):
        model_download_window = ModelDownloadFrame(self, "Download Stanza Model", model_path=self.model_dir,
                                                   lang=self.lang)
        model_download_window.CenterOnParent(wx.BOTH)
        model_download_window.Show(True)
        self.Disable()

    def MenuClearModel(self, event):
        model_ids = [i for i in self.model_list.keys()]
        for each_model_id in model_ids:
            self.settings_menu.Remove(self.model_list[each_model_id][2])
            shutil.rmtree(self.model_list[each_model_id][1], ignore_errors=True)
            self.model_list.pop(each_model_id)

    def MenuAbout(self, event):
        info = wx.adv.AboutDialogInfo()
        info.Name = "BFSU Stanza Tagger"
        info.Version = "1.1"
        info.Copyright = "(c) 2022-2023 LIU Dingjia, BFSUNLP Team, BFSU Corpus Research Group."
        with codecs.open(self.readme_path, "r", "utf-8") as f:
            about_info = f.read()
        info.Description = wordwrap(about_info, 350, wx.ClientDC(self))
        info.WebSite = (r"https://github.com/bfsunlp/BFSUStanViz", r"BFSUStanViz GITHUB")
        info.Developers = ["LIU Dingjia", ]
        wx.adv.AboutBox(info)

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnChooseTargetPath(self, event):
        dlg = wx.DirDialog(self, "Open the output folder:",
                           style=wx.DD_DEFAULT_STYLE
                                 | wx.DD_DIR_MUST_EXIST
                           # | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            dir_path = dlg.GetPath()
            self.target_path_ctrl.WriteText(dir_path)

    def OnOpenFile(self, event):
        wildcard = "All files(*.*)|*.*"
        dlg = wx.FileDialog(
            self,
            message="Open files...",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)  # | wx.FD_CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            file_paths = dlg.GetPaths()
            self.Disable()
            open_files_work = OpenFilesThread(file_paths)
            self.Enable()

    def openFilesDisplay(self, mstatus):
        file_path, encoding = mstatus
        if encoding == "utf-8":
            index = self.input_file_list_ctrl.InsertItem(self.input_file_list_ctrl.GetItemCount(),
                                                         file_path)
            self.input_file_list_ctrl.SetItem(index, 1, encoding)
        else:
            error_tag = " (encoding error, only support utf-8)"
            index = self.input_file_list_ctrl.InsertItem(self.input_file_list_ctrl.GetItemCount(),
                                                         "!" + file_path + error_tag)
            self.input_file_list_ctrl.SetItem(index, 1, encoding)
            self.input_file_list_ctrl.SetItemTextColour(index, wx.RED)

    def OnOpenDir(self, event):
        dlg = wx.DirDialog(self, "Open a folder:",
                           style=wx.DD_DEFAULT_STYLE
                                 | wx.DD_DIR_MUST_EXIST
                                 | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            dir_path = dlg.GetPath()
            file_paths = lf.load_dir_files(dir_path)
            self.Disable()
            open_files_work = OpenFilesThread(file_paths)
            self.Enable()

    def OnClearFile(self, event):
        self.input_file_list_ctrl.DeleteAllItems()
        self.output_file_list_ctrl.DeleteAllItems()

    def OnRun(self, event):
        output_dir = self.target_path_ctrl.GetValue().strip()
        dir_tag = False
        job = None
        nlp = None
        if output_dir:
            # print(output_dir)
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir)
                    dir_tag = True
                except OSError:
                    dlg = wx.MessageDialog(self, 'The output path is not correct!',
                                           'Warning',
                                           wx.OK | wx.ICON_INFORMATION
                                           # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                           )
                    dlg.ShowModal()
                    dlg.Destroy()
            else:
                if os.path.isdir(output_dir):
                    dir_tag = True
        else:
            dlg = wx.MessageDialog(self, 'Choose a folder as output path first!',
                                   'Warning',
                                   wx.OK | wx.ICON_INFORMATION
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
            dlg.Destroy()

        if dir_tag:
            file_paths = []
            num_of_rows = self.input_file_list_ctrl.GetItemCount()
            for each_item_idx in range(num_of_rows):
                file_path = self.input_file_list_ctrl.GetItemText(each_item_idx, 0)
                encoding = self.input_file_list_ctrl.GetItemText(each_item_idx, 1)
                if encoding == "utf-8":
                    file_paths.append(file_path)
            if file_paths:
                if self.model_list:
                    task = self.choose_task.GetStringSelection()
                    tag_set = self.choose_tagset.GetStringSelection()
                    if task == "POS Tagging":
                        task = "pos"
                    elif task == "Tokenization":
                        task = "tokenize"
                    elif task == "Lemmatization":
                        task = "lemmatize"
                    else:
                        task = None
                    if tag_set == "Treebank POS":
                        tagset = "xpos"
                    elif tag_set == "Universal POS":
                        tagset = "upos"
                    else:
                        tagset = None
                    try:
                        nlp = pl.load_pipline(lang=self.lang,
                                              task=task,
                                              model_dir=self.model_dir)
                    except:
                        dlg = wx.MessageDialog(self, 'Model is not correctly loaded!',
                                               'Warning',
                                               wx.OK | wx.ICON_INFORMATION
                                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                               )
                        dlg.ShowModal()
                        dlg.Destroy()

                    if nlp:
                        num_of_files = len(file_paths)
                        self.process_gauge.SetRange(num_of_files + 1)
                        ProcessingThread(model_path=self.model_dir,
                                         lang=self.lang,
                                         input_files=file_paths,
                                         output_path=output_dir,
                                         task=task,
                                         tagset=tagset,
                                         nlp=nlp)
                        self.run_button.Disable()
                else:
                    dlg = wx.MessageDialog(self, 'Please download a model first!',
                                           'Warning',
                                           wx.OK | wx.ICON_INFORMATION
                                           # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                           )
                    dlg.ShowModal()
                    dlg.Destroy()
            else:
                dlg = wx.MessageDialog(self, 'Please open file(s) or open a folder first!',
                                       'Warning',
                                       wx.OK | wx.ICON_INFORMATION
                                       # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                       )
                dlg.ShowModal()
                dlg.Destroy()

    def runDisplay(self, mstatus):
        if mstatus[0] == "process":
            self.SetStatusText("processing " + mstatus[1] + " (%d/%d)" % (mstatus[2], mstatus[3]))
            self.process_gauge.SetValue(mstatus[2])
            index = self.output_file_list_ctrl.InsertItem(self.output_file_list_ctrl.GetItemCount(), mstatus[1])
            self.output_file_list_ctrl.SetItem(index, 1, "success")
        elif mstatus[0] == "finished":
            self.process_gauge.SetValue(mstatus[1] + 1)
            dlg = wx.MessageDialog(self, 'Tasked is finished, %d file(s) was(were) processed!' % mstatus[1],
                                   'Info',
                                   wx.OK | wx.ICON_INFORMATION
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
            dlg.Destroy()
            self.run_button.Enable()


if __name__ == "__main__":
    pass
