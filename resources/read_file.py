# -*- coding:utf-8 -*-
"""
Copyright (c) 2022-2023, LIU Dingjia, BFSUNLP Group.
All rights reserved.
Email: 
dingjialiu@gmail.com
bfsunlp@gmail.com
"""

import os
import codecs
import chardet

UTF8SET = ["ascii", "utf-8"]


def load_dir_files(dir_path):
    file_names = os.listdir(dir_path)
    file_paths = [os.path.join(dir_path, each_name) for each_name in file_names
                  if os.path.isfile(os.path.join(dir_path, each_name))]
    return file_paths


def detect_encode(file_path):
    try:
        with codecs.open(file_path, "r", "utf-8") as file_obj:
            file_obj.read()
        return "utf-8"
    except UnicodeDecodeError:
        with open(file_path, "rb") as file_obj:
            data = file_obj.read()
            result = chardet.detect(data)["encoding"]
        return result


def group_file_by_size(file_set, num_group):
    group = {}
    group_list = []
    for each_group in range(num_group):
        group[each_group] = [[], 0]
        group_list.append(each_group)
    for each_file in file_set:
        group_list = sorted(group_list, key=lambda x: group[x][-1])
        group[group_list[0]][0].append(each_file)
        group[group_list[0]][1] = group[group_list[0]][1] + os.path.getsize(each_file)
    return group


if __name__ == "__main__":
    pass


