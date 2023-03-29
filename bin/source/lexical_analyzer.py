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
import source.load_file as lf


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


def process_file(source_path, target_path, task, pipeline, tagset="xpos"):
    encoding = lf.detect_encode(source_path)
    if encoding == "utf-8":
        nlp = pipeline
        if task == "tokenize":
            with codecs.open(source_path, "r", "utf-8") as source_obj:
                with codecs.open(target_path, "w", "utf-8") as target_obj:
                    for each_line in source_obj.readlines():
                        if each_line:
                            result = " ".join(tokenize(each_line, nlp))
                        else:
                            result = ""
                        target_obj.write(result + "\n")
        elif task == "pos":
            with codecs.open(source_path, "r", "utf-8") as source_obj:
                with codecs.open(target_path, "w", "utf-8") as target_obj:
                    for each_line in source_obj.readlines():
                        if each_line:
                            result = " ".join(pos_tag(each_line, nlp, tagset))
                        else:
                            result = ""
                        target_obj.write(result + "\n")
        return True

    else:
        print("Encoding error! " + os.path.split(source_path)[-1],
              "must be \"utf-8\"")
        return False


def process_dir(source_paths, target_dir, task, pipeline, tagset):
    if pipeline:
        for each_source_path in source_paths:
            each_target_path = os.path.join(target_dir, os.path.split(each_source_path)[-1])
            print("processing...", each_source_path)
            process_file(each_source_path, each_target_path, task, pipeline=pipeline, tagset=tagset)
    else:
        print("Stanza pipeline is not correctly setup, check the task tag!")


if __name__ == "__main__":
    pass

