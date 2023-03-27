The bfsustanviz is a commandline and gui wrapper project of Standord Python NLP Library for Many Human Languages.

The running of the python script of bfsustanviz request: 

OS: Microsoft Windows 10 or Later

Python: Python 3.9 with stanza, charset, psutil, pyinstaller, wxpython installed.

The current version bfsustanviz 0.1 support the following lexical analyzing task. 

----[Chinese Simplified]----[ZH]

If you are using command prompt, please copy exactly the following command and make sure only alter the input and output directory.

Tag one *.txt file, use:

`python main.py --onefile --pos_tag --zh input d:\text.txt output d:\result.txt`

Tag all files located in the root of one directory, use:

`python main.py --dir --pos_tag --zh input d:\source output d:\target`

"--pos_tag" can be substituted with "--tokenize" for tokenize task.

Please be also noted that the algorithm is multicore optimized in directory mode. 

However, the original stanza running on "cpu" mode is rather slow. You may try to
enble "gpu" with cuda capabilities.

The gui version of bfsustanviz is named BFSU Stanza Tagger 1.0, you may obtain the software via:

Link: https://pan.baidu.com/s/1bXQiz-DJ1Oz3yW1iIZr4Ng?pwd=bfsu
