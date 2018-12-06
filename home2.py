import time
import json
import os
import shutil


def info(fn):
    """
    Decorator that prints name of function and its processing time
    :param fn: function to decorate
    :return: fn
    """
    def wrapper(n):
        start = time.clock()
        result = fn(n)
        end = time.clock()
        print(fn.__name__)
        print(end-start)
        return result
    return wrapper


@info
def process(file):
    """
    Calculates sum of list elements
    :param file: file that contain list
    :return: sum of list elements
    """
    lst = json.loads(file.read())
    if isinstance(lst, list):
        return sum(lst)
    else:
        raise ValueError

def check_dir(s, r, e):
    """
    Check if all folders, using by monitoring function exist
    :param s: folder with files to process
    :param r: folder with result files
    :param e: folder with files, leads to exceptions during processing
    :return: True if all folders exist
    """
    return os.path.isdir(s) and os.path.isdir(r) and os.path.isdir(e)


def monitor(source, results, errors):
    """
    Function monitor source folder, and process .txt files
    :param source: folder with input data files which is under monitoring
    :param results: folder which contain processing results
    :param errors: folder with files which lead to errors during processing
    :return: None
    """
    if check_dir(source, results, errors):
        txt_filenames = [f for f in os.listdir(source) if f[-3:] == 'txt']
        txt_files = list(map(lambda x: open(os.path.join(source, x), 'r'),
                             txt_filenames))
        kv_files = dict(zip(txt_filenames, txt_files))

        for filename, file in kv_files.items():
            try:
                result = process(file)
                if not isinstance(result, Exception):
                    with open(os.path.join(results, filename), 'w') as \
                            result_file:
                        result_file.write(str(result))
            except Exception:
                shutil.copy(os.path.join(source, filename), errors)
            finally:
                file.close()
                if os.path.exists(os.path.join(source, filename)):
                    os.remove(os.path.join(source, filename))

with open('Bad_file3.txt', 'r') as file:
    process(file)