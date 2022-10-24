import tkinter
from os.path import splitext, exists, dirname, realpath
from os import rename
from dataclasses import dataclass
import customtkinter
from PIL.Image import open as openIm, ANTIALIAS
from PIL.ImageTk import PhotoImage
from enum import Enum, unique
from typing import Any


PATH = dirname(realpath(__file__)).replace('/python files', '', 1)


def reformat_file(before: str, after: str, file_name: str) -> None:
    """Reformat file for reading"""
    saving_file = PATH + '/logs/' + file_name + '.' + before
    base = splitext(saving_file)[0]
    rename(saving_file, base + '.' + after)


def import_saved_info(mode: str) -> Any:

    match mode:
        case 'Current Tasks':
            """Give an array №1 with all current task info and give array №2 with task events"""

            if not (exists(PATH + '/logs/cur_tasks_save.tds')):
                return [], []

            reformat_file(before='tds', after='txt', file_name='cur_tasks_save')

            task_array = []
            event_array = []

            with open(PATH + '/logs/cur_tasks_save.txt', 'r') as saving_file:
                while True:
                    line = saving_file.readline().replace('\n', '', 1)
                    if not line:
                        break
                    task_array.append(line.split(" : ")[0])
                    event_array.append(int(line.split(" : ")[1]))

            reformat_file(before='txt', after='tds', file_name='cur_tasks_save')
            saving_file.close()

            return task_array, event_array

        case 'Global Tasks':
            task_array = []
            if not (exists(PATH + '/logs/global_tasks_save.tds')):
                return []

            reformat_file(before='tds', after='txt', file_name='global_tasks_save')
            with open(PATH + '/logs/global_tasks_save.txt', 'r') as saving_file:
                while True:
                    line = saving_file.readline().replace('\n', '', 1)
                    if not line:
                        break
                    task_array.append(line)

            reformat_file(before='txt', after='tds', file_name='global_tasks_save')
            saving_file.close()

            return task_array


@dataclass
class CheckBoxTaskInfo:
    """Dataclass for keeping info about task_check_box"""
    task_name: str
    task_widget: customtkinter.CTkCheckBox
    task_widget_event: bool


@dataclass
class SettingButtonTaskInfo:
    """Dataclass for keeping info about task_setting_button"""
    setting_widget_button: customtkinter.CTkButton
    setting_widget_button_menu: tkinter.Menu


@dataclass
class CurTaskData(CheckBoxTaskInfo, SettingButtonTaskInfo):
    """Child dataclass that keep all info about current tasks"""
    widget_row: int


class Sprites:
    """Class for sprite's info and downloading"""
    PATH = dirname(realpath(__file__)).replace('/python files', '', 1)
    image_size = 25

    @staticmethod
    def download_sprites(path_in_sprite_folder: str) -> PhotoImage:
        return PhotoImage(openIm(Sprites.PATH + path_in_sprite_folder).resize((25, 25), ANTIALIAS))\



@dataclass
class AppSettingsInfo:
    theme_color: str
    appearance_mode: str


@unique
class ButtonStatus(Enum):
    not_pressed = 0
    pressed = 1
