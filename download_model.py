# -*- coding:utf-8 -*-
"""
Copyright (c) 2022-2023, LIU Dingjia, BFSUNLP Group.
All rights reserved.
Email: 
dingjialiu@gmail.com
bfsunlp@gmail.com
"""

import sys
import stanza
import stanza.resources.common as sc

if __name__ == "__main__":
    model_dir = "./resources/model"
    lang = sys.argv[2]
    print(lang)
    try:
        model_dir = sys.argv[4]
    except IndexError:
        pass
    try:
        stanza.download(lang=lang, model_dir=model_dir)
    except sc.UnknownLanguageError:
        print("Unknown Language Code, please refer to https://github.com/bfsunlp/BFSUStanViz")
