"bfsustanviz" is a command and gui wrapper of Stanford NLP Python package "stanza".

The running of the python script of bfsustanviz require: 

Microsoft Windows 10 or Later

Python 3.9 with stanza, charset, psutil installed.

The current version bfsustanviz 1.0 support lexical analyzing task in limited languages. 

If you are using command prompt, please use exactly the following command.

If you tag only one *.txt file, use:

`python main.py --onefile --pos_tag --zh input d:\text.txt output d:\result.txt`

Tag all files located in the root of one directory, use:

`python main.py --dir --pos_tag --zh input d:\source output d:\target`

"--pos_tag" can be substituted with "--tokenize" for tokenize task.

The currently available languages are listed as follows:

Chinese simplified: --zh

Please be also noted that the algorithm is multicore optimized in directory mode. 

However, the original stanza running on "cpu" mode is rather slow. You may try to
enble "gpu" with cuda capabilities.
