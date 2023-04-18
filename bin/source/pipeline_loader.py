# -*- coding:utf-8 -*-
"""
Copyright (c) 2022-2023, LIU Dingjia, BFSU NLP Team, BFSU Corpus Research Group.
All rights reserved.
Email: 
bfsunlp@gmail.com
dingjialiu@gmail.com
"""

import stanza


def load_pipline(lang, task, model_dir, use_gpu=False):
    l_type1 = ["en", "et", "ja", "ko", "nl", "ru", "ro", "zh", ]
    l_type2 = ["de", "fr", "it", ]

    if lang in l_type1:
        task_processors = {"lemmatize": "tokenize, pos, lemma",
                           "tokenize": "tokenize",
                           "pos": "tokenize, pos"}
    elif lang in l_type2:
        task_processors = {"lemmatize": "tokenize, mwt, pos, lemma",
                           "tokenize": "tokenize",
                           "pos": "tokenize, mwt, pos",
                           "mwt": "tokenize, mwt"}
    else:
        task_processors = {}

    try:
        nlp = stanza.Pipeline(lang=lang,
                              dir=model_dir,
                              processors=task_processors[task],
                              download_method="none",
                              use_gpu=use_gpu)
    except KeyError:
        nlp = False
    return nlp


if __name__ == "__main__":
    pass
