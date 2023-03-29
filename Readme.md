<div align="center">
<!-- Title: -->
  <a href="https://github.com/bfsunlp/BFSUStanViz">
    <img src="http://corpus.bfsu.edu.cn/images/bfsucorpuslogo_1.png" height="100" alt="Gitpod Ready-to-Code">
  </a>
  <h1><a href="https://github.com/bfsunlp/BFSUStanViz">BFSUStanViz</a> - Python</h1>
<!-- Short description: -->
  <h3>A Stanza Python Commandline & Graphic Wrapper</h3>
</div>

## Environment Setup

### Operating System

Microsoft Windows 10 or Later, MacOS (only command line available)

### Python Version

Python 3.9 (Python 3.7.x or later is available, but the full compatibility is not guaranteed.)

### pip

```bash
pip install stanza, wxpython, pyinstaller, chardet, psutil, pypubsub
```

### conda

Anaconda3-2022.10-Windows-x86_64.exe

https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2022.10-Windows-x86_64.exe

https://repo.anaconda.com/archive/Anaconda3-2022.10-Windows-x86_64.exe

```bash
conda create  --name BFSUStanViz --file conda-spec-list.txt
```

### Download Stanza Model

```bash
python download_model.py --model ko
```

stanza models will not come with BFSUStanViz, you should download a supported model before using either Prompt or GUI. 
Please be noted that the model downloading option is enabled in "settings" menu of the GUI version BFSU Stanza Tagger.

## Running BFSUStanViz

The current version BFSUStanViz 1.1 support lexical analyzing task, the supported language is keeping updating.

Currently Supported Languages:

```bash
"zh" ------> [Chinese Simplified]
"ko" ------> [Korean]
```

### Command Line

If you are using command prompt or Anaconda Prompt, please use the following command in Windows
Terminal/Anaconda Prompt with administrator privilege and make sure the conda environment BFSUStanViz is activated.

To tag one file, use:

```bash
python main.py --onefile --pos --zh --xpos D:\Demo\source.txt D:\Demo\target.txt
```

To tag all files located in the root of one directory, use:

```bash
python main.py --directory --tokenize --zh --xpos D:\source_dir D:\target_dir
```

"--pos" can be replaced with "--tokenize" for tokenization task;

"--zh" can be replaced with other supported language acronym;

"--xpos" can be replaced with "--upos" to switch the tagset from treebank tagset to universal dependency tagset,
for more information, please refer to https://universaldependencies.org/


However, the original stanza running on "cpu" mode is rather slow. You may try to
enable "gpu" with cuda capability.

### Wxpython GUI

The author of BFSUStanViz also developed a windows graphic interface named as BFSU Stanza Tagger, you may launch a gui
under the Python Environment by execute the following command in administrator approved terminal:

```bash
python .\bin\zh_tagger_launcher.py
```

"zh" can be replaced with other supported language acronym.

### Executable GUI Support

You may also obtain a windows graphic interface "BFSU Stanza Tagger 1.0" through the following link:

https://pan.baidu.com/s/1bXQiz-DJ1Oz3yW1iIZr4Ng?pwd=bfsu 

## Updates
```bash
2023-03-26 BFSUStanViz v1.0, BFSU Stanza Tagger 1.0. First issue
2023-03-26 BFSUStanViz v1.1, BFSU Stanza Tagger 1.1. Fix compatability issues, rewrite lexical_analyzer.
```

## References

BFSU Stanza Tagger 1.1 is a Windows GUI wrapper of "stanza" package. This GUI of BFSU Stanza Tagger 1.1 is developed 
by BFSU NLP team of Beijing Foreign Studies University Corpus Research Group and licensed under MIT Licence. 

Copyright © 2022-2023, LIU Dingjia, BFSU NLP Team, BFSU Corpus Group.

Stanza is a Python natural language analysis package. It contains tools to convert a string containing human language
text into lists of sentences and words, to generate base forms of those words, their parts of speech and morphological
features, to give a syntactic structure dependency parse, and to recognize named entities. The toolkit is designed to
be parallel among more than 70 languages, using the Universal Dependencies formalism. Stanza is created by the Stanford
NLP Group. The stanza package is licensed under the Apache License, Version 2.0.

Copyright © 2020 Stanford NLP Group.

If you use either BFSUStanViz or BFSU Stanza Tagger 1.1 in your work, please cite both of the following items:

Dingjia LIU. BFSU Stanza Tagger 1.1. BFSU Corpus Research Group. 2023.

Peng Qi, Yuhao Zhang, Yuhui Zhang, Jason Bolton and Christopher D. Manning. 2020. Stanza: A Python Natural Language
Processing Toolkit for Many Human Languages. In Association for Computational Linguistics (ACL) System Demonstrations. 2020.

Stanza: https://stanfordnlp.github.io/stanza/
BFSU Corpus Research Group: http://corpus.bfsu.edu.cn/
BFSUNLP Github: https://github.com/bfsunlp

