import os

import pandas as pd

from email_helper import Email


def build_full_dataframe(folder):
    """ Expects a directory containing a 'Clean' and a 'Spam' folder """
    data = list()

    for nt_f in os.scandir(os.path.join(folder, 'Clean')):
        e = Email(nt_f.path)
        data.append([e.title + " " + e.content, 0, nt_f.name])

    for nt_f in os.scandir(os.path.join(folder, 'Spam')):
        e = Email(nt_f.path)
        data.append([e.title + " " + e.content, 1, nt_f.name])

    return pd.DataFrame(data, columns=['text', 'label_num', 'filename'])


def build_eval_dataframe(folder):
    """ Expects a directory containing emails """
    data = list()

    for nt_f in os.scandir(folder):
        e = Email(nt_f.path)
        data.append([e.title + " " + e.content, nt_f.name])

    return pd.DataFrame(data, columns=['text', 'filename'])


def dump_res_file(eval_dataframe, results, file_path):
    """ Expects the 
        eval_dataframe that should contain a filename column, 
        a vector of binary results (0 - cln, 1 - inf). 
        The file_path is used to determine where the result 
            file will be written 
    """
    filenames = eval_dataframe.filename
    m = ['cln', 'inf']
    with open(file_path, 'w') as g:
        for i in range(len(results)):
            g.write(filenames.values[i] + '|' + m[results[i]] + "\n")
