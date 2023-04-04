import os
import codecs


def gui_gen(lan_list, template):
    cwd = os.getcwd()
    with codecs.open(template, "r", "utf-8") as temp_obj:
        temp_content = temp_obj.read()
    for acr, fn in lan_list:
        content = temp_content.replace("acronym", acr)
        content = content.replace("full_name", fn)
        target_path = os.path.join(cwd, "%s_tagger_launcher.py" % acr)
        with codecs.open(target_path, "w", "utf-8") as target_obj:
            target_obj.write(content)


def pyinspec_gen(lan_list, template):
    cwd = os.getcwd()
    with codecs.open(template, "r", "utf-8") as temp_obj:
        temp_content = temp_obj.read()
    for acr, fn in lan_list:
        content = temp_content.replace("acronym", acr)
        content = content.replace("upper_name", acr.upper())
        target_path = os.path.join(cwd, "%s_tagger_launcher.spec" % acr)
        with codecs.open(target_path, "w", "utf-8") as target_obj:
            target_obj.write(content)
        # print(target_path)
        # print(acr.upper())
        # print(content)


if __name__ == '__main__':
    gui_gen(lan_list=[("nl", "Dutch"),
                      ("de", "German"),
                      ("et", "Estonian"),
                      ("fr", "French"),
                      ("it", "Italian"),
                      ("ru", "Russian"), ],
            template="launcher_template.tmp")

    pyinspec_gen(lan_list=[("nl", "Dutch"),
                           ("de", "German"),
                           ("et", "Estonian"),
                           ("fr", "French"),
                           ("it", "Italian"),
                           ("ru", "Russian"), ],
                 template="specs_template.tmp")
