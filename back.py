from os.path import splitext, exists
from os import rename


def reformat_file(before: str, after: str) -> None:
    """Reformat file for reading"""
    saving_file = 'logs/save.' + before
    base = splitext(saving_file)[0]
    rename(saving_file, base + '.' + after)


def import_saved_info() -> (list, list):
    """Give an array with all current task info"""

    if not (exists('logs/save.tds')):
        return [], []

    reformat_file(before='tds', after='txt')

    task_array = []
    event_array = []

    with open('logs/save.txt', 'r') as saving_file:
        while True:
            line = saving_file.readline().replace('\n', '', 1)
            if not line:
                break
            task_array.append(line.split(" : ")[0])
            event_array.append(int(line.split(" : ")[1]))

    reformat_file(before='txt', after='tds')
    saving_file.close()

    return task_array, event_array
