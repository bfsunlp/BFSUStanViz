# -*- coding:utf-8 -*-
"""
Copyright (c) 2022-2023, LIU Dingjia, BFSUNLP Group.
Email: dingjialiu@gmail.com; bfsunlp@gmail.com
"""

import os
import sys
import source.lexical_analyzer as la
import source.pipeline_loader as pl
import source.load_file as lf

if __name__ == "__main__":
    task = sys.argv[2][2:]
    lang = sys.argv[3][2:]
    model_dir = os.path.join(os.getcwd(), r"resources\model")
    tagset = sys.argv[4][2:]
    nlp = pl.load_pipline(lang=lang,
                          task=task,
                          model_dir=model_dir)

    if sys.argv[1] == "--onefile":
        input_path = sys.argv[5]
        output_path = sys.argv[6]
        result = la.process_file(source_path=input_path,
                                 target_path=output_path,
                                 task=task,
                                 pipeline=nlp,
                                 tagset=tagset)
        if result:
            print("Job is accomplished! Please check:\n" + output_path)
        else:
            print("Job is not accomplished!")

    elif sys.argv[1] == "--directory":
        source_dir = sys.argv[5]
        target_dir = sys.argv[6]
        source_paths = lf.load_dir_files(source_dir)
        la.process_dir(source_paths=source_paths,
                       target_dir=target_dir,
                       task=task,
                       pipeline=nlp,
                       tagset=tagset)
    else:
        raise ValueError(sys.argv[1] + " can not be recognized!")

# python main.py --onefile --pos --zh --xpos D:\Demo\Chinese\E_LFS5K_F0016_ZH_.txt D:\output\result.txt
# python main.py --directory --tokenize --zh --xpos D:\Demo\Chinese D:\output
# process_file(source_path, target_path, task, pipeline, tagset="xpos")
