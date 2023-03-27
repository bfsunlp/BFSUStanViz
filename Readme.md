<div align="center">
<!-- Title: -->
  <a href="https://github.com/bfsunlp/BFSUStanViz">
    <img src="http://corpus.bfsu.edu.cn/images/bfsucorpuslogo_1.png" height="100" alt="Gitpod Ready-to-Code">
  </a>
  <h1><a href="https://github.com/bfsunlp/BFSUStanViz">BFSUStanViz</a> - Python</h1>
<!-- Short description: -->
  <h3>A Stanza Commandline & Graphic Wrapper - multicore optimized - for Education & Research Only</h3>
</div>

## Environment Setup

### Operating System

Microsoft Windows 10 or Later, MacOS (only commandline available)

### Python Version

Python 3.9

### pip

```bash
pip install stanza, wxpython, pyinstaller, chardet, psutil, pubsub
```

### conda

Anaconda3-2022.10-Windows-x86_64.exe

https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2022.10-Windows-x86_64.exe

https://repo.anaconda.com/archive/Anaconda3-2022.10-Windows-x86_64.exe

```bash
conda create  --name BFSUStanViz --file conda-spec-list.txt
```

## Running BFSUStanViz

The current version BFSUStanViz 1.0 support lexical analyzing task, the supported language is keeping updating.

Currently Supported Languages:

```bash
"zh" ------> [Chinese Simplified]
```

# Command Line

If you are using command prompt or Anaconda Prompt, please use the following command in Windows Terminal/Anaconda Prompt with administrator previlige and make sure the conda environment BFSUStanViz is activated.

To tag one file, use:

```bash
python main.py --onefile --pos_tag --zh input c:\text.txt output c:\result.txt
```

To tag all files located in the root of one directory, use:

```bash
python main.py --dir --pos_tag --zh input d:\source output d:\target
```

"--pos_tag" can be replaced with "--tokenize" for tokenization task, "--zh" can be replaced with other supported language acronym.

Please be also noted that the algorithm is multicore optimized in directory mode. 

However, the original stanza running on "cpu" mode is rather slow. You may try to
enble "gpu" with cuda capability.

# GUI Support

You may also obtain a windows graphic interface "BFSU Stanza Tagger 1.0" through the following link:

https://pan.baidu.com/s/1bXQiz-DJ1Oz3yW1iIZr4Ng?pwd=bfsu 
