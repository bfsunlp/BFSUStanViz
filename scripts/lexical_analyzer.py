# -*- coding:utf-8 -*-
"""
Copyright (c) 2022-2023, LIU Dingjia, BFSUNLP Group.
Email: dingjialiu@gmail.com; bfsunlp@gmail.com
"""
import os
import stanza
import codecs
import psutil
import multiprocessing
import resources.read_file as rf


def sentence_seg(line, pipline):
    nlp = pipline
    doc = nlp(line)
    sentences = []
    for sentence in doc.sentences:
        sentence_tokens = [token.text for token in sentence.tokens]
        sentence = " ".join(sentence_tokens)
        sentences.append(sentence)
    return sentences


def tokenize(line, pipline):
    nlp = pipline
    doc = nlp(line)
    tokens = []
    for sentence in doc.sentences:
        for token in sentence.tokens:
            tokens.append(token.text)
    return tokens


def pos_tag(line, pipline, tagset="xpos"):
    nlp = pipline
    doc = nlp(line)
    tokens_with_pos = []
    if tagset == "xpos":
        tokens_with_pos = ["_".join((word.text, word.xpos))
                           for sent in doc.sentences
                           for word in sent.words]
    elif tagset == "upos":
        tokens_with_pos = ["_".join((word.text, word.upos))
                           for sent in doc.sentences
                           for word in sent.words]
    return tokens_with_pos


def process_file(input_path, output_path, job, mode="single", pipeline=None, lang=None, tagset="xpos"):
    if mode == "single":
        if job == "tokenize":
            nlp = stanza.Pipeline(lang=lang, dir="./resources/model/",
                                  processors="tokenize",
                                  download_method="none",
                                  use_gpu=False)
            process_func = tokenize
        elif job == "pos_tag":
            nlp = stanza.Pipeline(lang=lang, dir="./resources/model/",
                                  processors="tokenize,pos",
                                  download_method="none",
                                  use_gpu=False)
            process_func = pos_tag
        else:
            nlp = None
            process_func = None
            print("parameter \"job\" is not properly assigned! please either use \"tokenize\" "
                  "or use \"pos_tag\" as its value!")
    elif mode == "multi":
        nlp = pipeline
        if job == "tokenize":
            process_func = tokenize
        elif job == "pos_tag":
            process_func = pos_tag
        else:
            process_func = None
    else:
        print("parameter \"mode\" is not properly assigned! please either use \"single\" "
              "for one file or use \"multi\" for batch processing!")
        process_func = None
        nlp = None

    if process_func and nlp:
        encoding = rf.detect_encode(input_path)
        if encoding in rf.UTF8SET:
            with codecs.open(input_path, "r", "utf-8") as input_obj:
                with codecs.open(output_path, "w", "utf-8") as output_obj:
                    for each_line in input_obj.readlines():
                        if each_line:
                            result = " ".join(process_func(each_line, nlp, tagset))
                        else:
                            result = ""
                        output_obj.write(result + "\n")
        else:
            print("Encoding error! " + os.path.split(input_path)[-1],
                  "should be encoded with \"utf-8\" character set!")
        return True
    else:
        return False


def process_dir(input_path, output_path, job, lang):
    file_names = [name for name in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, name))]
    # print(file_names)
    cpu_count = psutil.cpu_count(logical=False)
    threads = int(cpu_count / 2)
    pool = multiprocessing.Pool(processes=threads)
    for each_name in file_names:
        input_p = os.path.join(input_path, each_name)
        output_p = os.path.join(output_path, each_name)
        # print(input_p)
        # process_file(input_p, output_p, job, "single")
        pool.apply_async(process_file, (input_p, output_p, job, "single", None, lang))
    pool.close()
    pool.join()
    print("processing Finished!")


def process_dir_single_thread(input_files, output_path, job, model_dir):
    nlp = None

    for each_file in input_files:
        print(output_path)
        print(os.path.split(each_file)[-1])
        output_file = os.path.join(output_path, os.path.split(each_file)[-1])
        process_file(each_file, output_file, job, mode="multi", pipeline=nlp)


if __name__ == "__main__":
    pass

