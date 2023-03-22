# -*- coding:utf-8 -*-
"""
Copyright (c) 2022-2023, LIU Dingjia, BFSUNLP Group.
Email: dingjialiu@gmail.com; bfsunlp@gmail.com
"""

import sys
import scripts.lexical_analyzer as cla

if __name__ == "__main__":
    # print(sys.argv)
    if sys.argv[1] == "--onefile":
        lang = sys.argv[3][2:]
        job = sys.argv[2][2:]
        input_path = sys.argv[5]
        output_path = sys.argv[7]
        cla.process_file(input_path=input_path,
                         output_path=output_path,
                         job=job,
                         mode="single",
                         pipeline=None,
                         lang=lang)
        print("Job is accomplished! Please check:\n" + output_path)

    elif sys.argv[1] == "--dir":
        lang = sys.argv[3][2:]
        job = sys.argv[2][2:]
        # print(job)
        input_path = sys.argv[5]
        output_path = sys.argv[7]
        cla.process_dir(input_path=input_path,
                        output_path=output_path,
                        job=job,
                        lang=lang)
    else:
        raise ValueError(sys.argv[1] + " can not be recognized!")

