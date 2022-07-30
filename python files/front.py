import tkinter
import tkinter.messagebox
import customtkinter
from emoji import emojize
from back import import_saved_info, exists
from os.path import dirname, realpath
from os import remove
from PIL.Image import open as openIm, ANTIALIAS
from PIL.ImageTk import PhotoImage


class App(customtkinter.CTk):

    WIDTH = 640
    HEIGHT = 580
    PATH = dirname(realpath(__file__)).replace('/python files', '', 1)
    image_size = 25

    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme(PATH + "/Custom themes/purple.json")

    def __init__(self) -> None:
        super().__init__()

        self.title('Soft Caramel Table' + emojize(':sparkles:'))
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(True, True)

        self.add_list_image_light = PhotoImage(openIm(App.PATH + "/Sprites/Light/add-list.png").resize((App.image_size, App.image_size), ANTIALIAS))
        self.add_list_image_dark = PhotoImage(openIm(App.PATH + "/Sprites/Dark/add-list.png").resize((App.image_size, App.image_size), ANTIALIAS))

        self.add_setting_image_light = PhotoImage(openIm(App.PATH + "/Sprites/Light/settings.png").resize((App.image_size, App.image_size), ANTIALIAS))
        self.add_setting_image_dark = PhotoImage(openIm(App.PATH + "/Sprites/Dark/settings.png").resize((App.image_size, App.image_size), ANTIALIAS))

        # ========configure grid layout========
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ============FRAME_LEFT==============
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=200, height=100,
                                                 corner_radius=0)

        self.frame_left.grid(row=0, column=0,
                             sticky="nswe")

        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(5, weight=1)
        self.frame_left.grid_rowconfigure(8, minsize=20)
        self.frame_left.grid_rowconfigure(11, minsize=10)

        # ============FRAME_RIGHT=============

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1,
                              padx=20, pady=20,
                              sticky="nswe")

        self.frame_right.grid_rowconfigure(index=0, minsize=10)

        # ==========RIGHT_CLICK_MENU==========
        self.popupMenu = tkinter.Menu(master=self.frame_right, tearoff=0)
        self.popupMenu.add_command(label="Create task",
                                   command=self.create_task)
        self.popupMenu.add_command(label="Delete all tasks",
                                   command=self.delete_all_cur_tasks)

        self.bind("<Button-2>", self.popup)

        # ========================================LEFT==========================================================

        # ===============Text_0_left=================
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text='To-Do List ' + emojize(':sparkles:'),
                                              text_font=("Roboto Medium", -28))  # font name and size in px
        self.label_1.grid(row=0, column=0,
                          pady=10, padx=10)

        # ===============Button_1_left===============
        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Global tasks",
                                                command=self.create_top_level)
        self.button_1.grid(row=1, column=0,
                           pady=10, padx=20)

        # ===============Button_2_left===============
        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Notebook")
        self.button_2.grid(row=2, column=0,
                           pady=10, padx=20)

        # ==================Themes===================
        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Themes:")
        self.label_mode.grid(row=9, column=0,
                             pady=0, padx=16,
                             sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Dark", "Light"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0,
                               pady=10, padx=20,
                               sticky="w")
        # ======================================================================================================

        # ========================================RIGHT=========================================================

        self.label_right = customtkinter.CTkLabel(master=self.frame_right,
                                                  text="Current Tasks " + emojize(':check_mark_button:'),
                                                  text_font=("Roboto Medium", -22))
        self.label_right.grid(row=0, column=0,
                              pady=10, padx=10)

        self.task_button = customtkinter.CTkButton(master=self.frame_right,
                                                   text="Create Task", text_font=("Roboto Medium", -19),
                                                   width=190, height=40,
                                                   image=self.add_list_image_light, compound='right',
                                                   command=self.create_task)
        self.task_button.grid(row=0, column=1, columnspan=2,
                              padx=20, pady=10,
                              sticky='s')

        # ======================================================================================================

        # ============SET_DEFAULT_VALUES==============
        self.cur_task_dict = {}  # dict = { Task name: [widget, row, widget.get(), setting_button_widget] }
        self.import_cur_tasks()

    # =========================================Methods==========================================================

    @staticmethod
    def create_top_level() -> None:
        """Create top_level"""
        window = customtkinter.CTkToplevel()
        window.title("TopLevel")
        window.geometry("400x300")
        label = customtkinter.CTkLabel(master=window,
                                       text="Add something")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

        def slider_event(value):
            """Check slider value from 0 to 100"""
            print(value)

        slider = customtkinter.CTkSlider(master=window, from_=0, to=100, command=slider_event)
        slider.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    @staticmethod
    def button_event() -> None:
        print('Button pressed')

    def place_task_widget(self, info: str, row: int, event: int) -> None:
        """Place widget on a screen and add widget in a task dict"""

        check_task = customtkinter.CTkCheckBox(master=self.frame_right,
                                               text=info, textvariable=tkinter.StringVar)
        check_task.grid(row=row, column=0,
                        pady=10, padx=20,
                        sticky='w')

        task_settings_button = customtkinter.CTkButton(master=self.frame_right,
                                                       text='',
                                                       height=25, width=25,
                                                       command=self.button_event)
        task_settings_button.grid(row=row, column=2,
                                  pady=10, padx=20,
                                  sticky='e')

        match customtkinter.get_appearance_mode():
            case 'Light':
                task_settings_button.configure(fg_color='#EBEBEB', hover_color='#EBEBEB',
                                               image=self.add_setting_image_dark, compound="right")
            case 'Dark':
                task_settings_button.configure(fg_color='#2B2929', hover_color='#2B2929',
                                               image=self.add_setting_image_light, compound="right")

        match event:
            case 0:
                check_task.deselect()
            case 1:
                check_task.select()

        self.cur_task_dict.update({info: [check_task, row, event, task_settings_button]})

    def create_task(self) -> None:
        """Create task with its info in TaskBox"""
        def get_task_info() -> (str, bool):
            """Create a window for reading info and check if info in a correct form """
            dialog = customtkinter.CTkInputDialog(master=None,
                                                  text="Task info:",
                                                  title="Create Task")
            dialog_info = dialog.get_input()
            info_is_okay = False

            if dialog_info and (dialog_info[0] != " ") and (dialog_info[0] != "\n"):
                if len(dialog_info) > 50:
                    self.get_error(error_type="Info mustn't contain more than 50 symbols")
                    return dialog_info, info_is_okay

                info_is_okay = True
                return dialog_info, info_is_okay
            return dialog_info, info_is_okay

        info, is_okay = get_task_info()

        if self.cur_task_dict == {}:
            row = 1
        else:
            row = list(self.cur_task_dict.values())[-1][1] + 1  # take last num in a dict.values[row] + 1

        if is_okay:
            self.place_task_widget(info=info, row=row, event=0)

    def import_cur_tasks(self) -> None:
        """Import current task info from save.tds"""

        info_arr, event_arr = import_saved_info()
        row = 1
        while row <= len(info_arr):
            self.place_task_widget(info=info_arr[row-1], row=row, event=event_arr[row-1])
            row += 1

    @staticmethod
    def get_error(error_type: str) -> None:
        """Create new window with error message"""
        window = customtkinter.CTkToplevel()
        window.title("Error message")
        window.geometry("500x100")

        label = customtkinter.CTkLabel(master=window,
                                       text=error_type,
                                       text_color="red")
        label.pack(fill="both",
                   expand=True,
                   padx=40, pady=40,
                   side=tkinter.TOP)

    def change_appearance_mode(self, new_appearance_mode: str) -> None:
        """Change theme"""
        def change_images_themes() -> None:
            match customtkinter.get_appearance_mode():
                case 'Light':
                    self.task_button.configure(image=self.add_list_image_dark, compound="right")

                    for value in self.cur_task_dict.values():
                        value[3].configure(fg_color='#EBEBEB', hover_color='#EBEBEB',
                                           image=self.add_setting_image_dark, compound="right")
                case 'Dark':
                    self.task_button.configure(image=self.add_list_image_light, compound="right")

                    for value in self.cur_task_dict.values():
                        value[3].configure(fg_color='#2B2929', hover_color='#2B2929',
                                           image=self.add_setting_image_light, compound="right")

        customtkinter.set_appearance_mode(new_appearance_mode)
        change_images_themes()

    def on_closing(self) -> None:
        """Method for closing app and saving information"""
        def save() -> None:
            """Save current tasks' info in save.tds;
               If no tasks exist then save.tds will be removed"""
            def get_check_box_values() -> None:
                """Update cur_task_dict with widget.get() in values"""

                for info, values in self.cur_task_dict.items():
                    values[2] = values[0].get()
                    self.cur_task_dict.update({info: [value for value in values]})

            get_check_box_values()
            if self.cur_task_dict == {}:
                if exists(App.PATH + '/logs/save.tds'):
                    remove(App.PATH + '/logs/save.tds')
                return

            with open(App.PATH + '/logs/save.tds', 'w') as saving_file:
                for task in self.cur_task_dict.keys():
                    saving_file.write(task + ' : ' + str(self.cur_task_dict[task][2]) + '\n')
            saving_file.close()
        save()
        self.destroy()

    # ============POPUP_MENU_METHODS==============
    def delete_all_cur_tasks(self) -> None:
        """Delete all tasks' widgets and info in a dict"""
        copy_dict = self.cur_task_dict.copy()

        for key, values in copy_dict.items():
            values[0].destroy()
            values[3].destroy()
            self.cur_task_dict.pop(key)

    def popup(self, event) -> None:
        """Method that allow to use 'right button menu'"""
        self.popupMenu.post(event.x_root, event.y_root)

    # ==========================================================================================================


def application_ui() -> None:
    """Start loop for an App"""
    App().mainloop()
