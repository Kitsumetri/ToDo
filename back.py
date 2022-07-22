from os.path import splitext
from os import rename


def reformat_file(before: str, after: str) -> None:
    saving_file = 'save.' + before
    base = splitext(saving_file)[0]
    rename(saving_file, base + '.' + after)


def import_saved_info() -> list:
    reformat_file(before='tds', after='txt')
    task_array = []

    with open('save.txt', 'r') as saving_file:
        while True:
            line = saving_file.readline().replace('\n', '', 1)
            if not line:
                break
            task_array.append(line)
    saving_file.close()

    reformat_file(before='txt', after='tds')
    return task_array
