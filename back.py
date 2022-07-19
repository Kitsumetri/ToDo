from front import *
import os


def save():
    task_array = App.get_all_tasks()

    with open('save.tds', 'w') as saving_file:
        for task in task_array:
            if task == 'END':
                break
            saving_file.write(task + '\n')
    saving_file.close()


def reformat_file(before: str, after: str):
    saving_file = 'save.' + before
    base = os.path.splitext(saving_file)[0]
    os.rename(saving_file, base + '.' + after)


def import_saved_info():
    reformat_file('tds', 'txt')
    task_array = []

    with open('save.txt', 'r') as saving_file:
        while True:
            line = saving_file.readline().replace('\n', '', 1)
            if not line:
                break
            task_array.append(line)
    saving_file.close()

    reformat_file('txt', 'tds')
    return task_array


def application_back():
    save()
    import_saved_info()
