from os.path import splitext, exists, dirname, realpath
from os import rename

PATH = dirname(realpath(__file__)).replace('/python files', '', 1)


def reformat_file(before: str, after: str) -> None:
    """Reformat file for reading"""
    saving_file = PATH + '/logs/save.' + before
    base = splitext(saving_file)[0]
    rename(saving_file, base + '.' + after)


def import_saved_info() -> (list, list):
    """Give an array №1 with all current task info and give array №2 with task events"""

    if not (exists(PATH + '/logs/save.tds')):
        return [], []

    reformat_file(before='tds', after='txt')

    task_array = []
    event_array = []

    with open(PATH + '/logs/save.txt', 'r') as saving_file:
        while True:
            line = saving_file.readline().replace('\n', '', 1)
            if not line:
                break
            task_array.append(line.split(" : ")[0])
            event_array.append(int(line.split(" : ")[1]))

    reformat_file(before='txt', after='tds')
    saving_file.close()

    return task_array, event_array
