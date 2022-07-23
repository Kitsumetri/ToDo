from os.path import splitext
from os import rename
from typing import Union


def reformat_file(before: str, after: str) -> None:
    saving_file = 'save.' + before
    base = splitext(saving_file)[0]
    rename(saving_file, base + '.' + after)


def import_saved_info(mode: str) -> Union[int, list, list[str]]:

    if not open('save.tds', 'w'):
        print(123)
        if mode == 'only number':
            return len([])
        if mode == 'full information':
            return []

    reformat_file(before='tds', after='txt')
    task_array = []

    with open('save.txt', 'r') as saving_file:
        while True:
            line = saving_file.readline().replace('\n', '', 1)
            if not line:
                break
            task_array.append(line)

    reformat_file(before='txt', after='tds')
    saving_file.close()

    if mode == 'only number':
        return len(task_array) + 1
    if mode == 'full information':
        return task_array
