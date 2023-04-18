# -*- coding:utf-8 -*-
"""
Copyright (c) 2022-2023, LIU Dingjia, BFSU NLP Team, BFSU Corpus Research Group.
All rights reserved.
Email: 
bfsunlp@gmail.com
dingjialiu@gmail.com
"""

import os
import codecs
import shutil

if __name__ == "__main__":
    languages = [("nl", "Dutch"),
                 ("de", "German"),
                 ("et", "Estonian"),
                 ("fr", "French"),
                 ("it", "Italian"),
                 ("ru", "Russian"),
                 ("ro", "Romanian"),
                 ("ja", "Japanese"),
                 ("zh", "Chinese"),
                 ("ko", "Korean"),
                 ("es", "Spanish"), ]
    cwd = os.getcwd()
    with codecs.open("pack.bat", "w", "utf-8") as BAT:
        for lang in languages:
            BAT.write(r"cd dist" + "\n")
            tool_path = (r'"BFSU Stanza Tagger 1.2 [%s]"' % lang[0].upper())
            exe_name = tool_path + ".exe"
            BAT.write(r"md %s" % tool_path + "\n")
            BAT.write(r"cd.." + "\n")
            BAT.write(r"xcopy resources dist\\%s\\resources /e/y/i" % tool_path + "\n")
            BAT.write(r"xcopy license dist\\%s\\ /e/y/i" % tool_path + "\n")
            BAT.write(r"xcopy Stanza\\%s dist\\%s\\resources\\model\\%s /e/y/i" % (lang[0], tool_path, lang[0]) + "\n")
            BAT.write(r"pyinstaller %s_tagger_launcher.spec" % lang[0] + "\n")
            BAT.write(r"xcopy dist\\%s dist\\%s /e/y/i" % (exe_name, tool_path) + "\n")
