import tkinter
import tkinter.messagebox
from emoji import emojize
from back import import_saved_info, exists, CurTaskData, Sprites, ButtonStatus, customtkinter, PhotoImage
from os import remove


class App(customtkinter.CTk):
    WIDTH = 640
    HEIGHT = 600

    customtkinter.set_appearance_mode("Right")
    customtkinter.set_default_color_theme(Sprites.PATH + "/Custom themes/red.json")

    def __init__(self) -> None:
        super().__init__()

        # region Window settings
        self.title('TODO' + emojize(':sparkles:'))
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", lambda: AppExit.on_closing(self))
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # endregion

        # region Sprite downloading
        self.add_list_image_light = Sprites.download_sprites("/Sprites/Light/add-list.png")
        self.add_list_image_dark = Sprites.download_sprites("/Sprites/Dark/add-list.png")

        self.add_setting_image_light = Sprites.download_sprites("/Sprites/Light/settings.png")
        self.add_setting_image_dark = Sprites.download_sprites("/Sprites/Dark/settings.png")
        # endregion

        self.frame_left = LeftFrame.create_frame(root=self)
        self.switch_theme = LeftFrame.get_widget(self, self.frame_left)

        self.frame_right = RightFrames.RightFrameCurrentTasks.create_frame(root=self)
        self.task_button = RightFrames.RightFrameCurrentTasks.get_widgets(self, self.frame_right)

        self.switch_theme.select()

        self.popUp_menu = PopUpMenu.PopUpMenuForCurTasks.create_popup_menu(root=self)
        CurrentTasks.import_cur_tasks(self)

    # region Methods
    @staticmethod
    def get_error(error_type: str) -> None:
        """Create new window with error message"""
        window = customtkinter.CTkToplevel()
        window.title("Error message")
        window.geometry("500x100")

        def close_error_window(root: customtkinter.CTkToplevel) -> None:
            root.destroy()

        button_exit_error = customtkinter.CTkButton(master=window,
                                                    text=error_type, text_font=("Roboto Medium", -22),
                                                    text_color="white",
                                                    fg_color='red', hover_color='orange',
                                                    command=lambda: close_error_window(window))
        button_exit_error.pack(fill="both",
                               expand=True,
                               padx=40, pady=40,
                               side=tkinter.TOP)

    def change_appearance_mode(self) -> None:
        """Change theme"""

        def change_images_themes() -> None:
            """Function that changes all images' version depending on appearance_mode"""

            def change_color_widgets(icon_image: (PhotoImage, PhotoImage), color: str) -> None:
                self.task_button.configure(image=icon_image[0], compound="right")
                if CurrentTasks.cur_task_array:
                    for data in CurrentTasks.cur_task_array:
                        data.setting_widget_button.configure(fg_color=color, hover_color=color,
                                                             image=icon_image[1], compound="right")

            match customtkinter.get_appearance_mode():
                case 'Light':
                    change_color_widgets((self.add_list_image_dark, self.add_setting_image_dark), color='#EBEBEB')
                case 'Dark':
                    change_color_widgets((self.add_list_image_light, self.add_setting_image_light), color='#2B2929')

        if self.switch_theme.get() == ButtonStatus.pressed.value:
            customtkinter.set_appearance_mode('Dark')
        else:
            customtkinter.set_appearance_mode('Light')

        change_images_themes()

    def change_right_frame(self, prev_frame: customtkinter.CTkFrame, mode: str) -> customtkinter.CTkFrame:

        new_frame_right = customtkinter.CTkFrame(master=self)

        match mode:
            case 'Current Tasks':
                prev_frame.grid_remove()
                self.frame_right = RightFrames.RightFrameCurrentTasks.create_frame(root=self)
                self.task_button = RightFrames.RightFrameCurrentTasks.get_widgets(self, self.frame_right)
                self.popUp_menu = PopUpMenu.PopUpMenuForCurTasks.create_popup_menu(root=self)

                CurrentTasks.save_cur_tasks()
                CurrentTasks.import_cur_tasks(self)
            case 'Task Archive':
                prev_frame.grid_remove()
                self.frame_right = RightFrames.RightFrameTaskArchive.create_frame(root=self)
                self.popUp_menu = PopUpMenu.PopUpMenuForTaskArchive.create_popup_menu(root=self)
                RightFrames.RightFrameTaskArchive.get_widgets(self.frame_right)
            case 'Notebook':
                prev_frame.grid_remove()
                self.frame_right = RightFrames.RightFrameNotebook.create_frame(root=self)
            case 'Emotional Tracker':
                prev_frame.grid_remove()
                self.frame_right = RightFrames.RightFrameNotebook.create_frame(root=self)
            case 'Settings':
                prev_frame.grid_remove()
                self.frame_right = RightFrames.RightFrameNotebook.create_frame(root=self)

        return new_frame_right

    def get_screen_points(self, event) -> None:
        """Method that allow to use 'right button menu'"""
        self.popUp_menu.post(event.x_root, event.y_root)


class LeftFrame(App):
    """Class for creating left frame and add widgets on it"""
    def __int__(self, root):
        super().__init__()
        self.root = root

    @staticmethod
    def create_frame(root) -> customtkinter.CTkFrame:
        frame_left = customtkinter.CTkFrame(master=root,
                                            width=200, height=100,
                                            corner_radius=0)

        frame_left.grid(row=0, column=0,
                        sticky="nswe")

        frame_left.grid_rowconfigure(0, minsize=10)
        frame_left.grid_rowconfigure(5, weight=1)
        frame_left.grid_rowconfigure(8, minsize=20)
        frame_left.grid_rowconfigure(11, minsize=10)

        return frame_left

    @staticmethod
    def get_widget(root, frame_left: customtkinter.CTkFrame) -> customtkinter.CTkSwitch:

        label = customtkinter.CTkLabel(master=frame_left,
                                       text='To-Do List ' + emojize(':sparkles:'),
                                       text_font=("Roboto Medium", -28))  # font name and size in px
        label.grid(row=0, column=0,
                   pady=10, padx=10)

        button_cur_tasks = customtkinter.CTkButton(master=frame_left,
                                                   text="Current Tasks",
                                                   command=lambda: root.change_right_frame(
                                                       prev_frame=root.frame_right, mode='Current Tasks'))
        button_cur_tasks.grid(row=1, column=0,
                              pady=10, padx=20)

        button_task_archive = customtkinter.CTkButton(master=frame_left,
                                                      text="Task Archive",
                                                      command=lambda: root.change_right_frame(
                                                          prev_frame=root.frame_right, mode='Task Archive'))
        button_task_archive.grid(row=2, column=0,
                                 pady=10, padx=20)

        button_notebook = customtkinter.CTkButton(master=frame_left,
                                                  text="Notebook",
                                                  command=lambda: root.change_right_frame(
                                                      prev_frame=root.frame_right, mode='Notebook'))
        button_notebook.grid(row=3, column=0,
                             pady=10, padx=20)

        button_emotional_tracker = customtkinter.CTkButton(master=frame_left,
                                                           text="Emotional Tracker",
                                                           command=lambda: root.change_right_frame(
                                                               prev_frame=root.frame_right, mode='Emotional Tracker'))

        button_emotional_tracker.grid(row=4, column=0,
                                      pady=10, padx=20)

        button_app_settings = customtkinter.CTkButton(master=frame_left,
                                                      text='Settings',
                                                      command=lambda: root.change_right_frame(
                                                          prev_frame=root.frame_right, mode='Settings'))
        button_app_settings.grid(row=9, column=0,
                                 padx=10, pady='20')

        switch_theme = customtkinter.CTkSwitch(master=frame_left,
                                               text="Dark mode",
                                               command=root.change_appearance_mode)

        switch_theme.grid(row=10, column=0,
                          pady=10, padx=20,
                          sticky='w')
        return switch_theme


class RightFrames:
    """All right frames and widgets in a one class"""
    class RightFrameCurrentTasks(App):
        def __int__(self, root) -> None:
            super().__init__()
            self.root = root

        @staticmethod
        def create_frame(root) -> customtkinter.CTkFrame:
            """Create and place right frame on a screen"""
            frame_right = customtkinter.CTkFrame(master=root)
            frame_right.grid(row=0, column=1,
                             padx=20, pady=20,
                             sticky="nswe")

            frame_right.grid_rowconfigure(index=0, minsize=10)

            return frame_right

        @staticmethod
        def get_widgets(root, frame_right: customtkinter.CTkFrame) -> customtkinter.CTkButton:
            label_right = customtkinter.CTkLabel(master=frame_right,
                                                 text="Current Tasks " + emojize(':check_mark_button:'),
                                                 text_font=("Roboto Medium", -22))
            label_right.grid(row=0, column=0,
                             pady=10, padx=10)

            task_button = customtkinter.CTkButton(master=frame_right,
                                                  text="Create Task", text_font=("Roboto Medium", -19),
                                                  width=190, height=40,
                                                  image=root.add_list_image_light, compound='right',
                                                  command=lambda: CurrentTasks.create_task(root))
            task_button.grid(row=0, column=1, columnspan=2,
                             padx=20, pady=10,
                             sticky='s')

            return task_button

    class RightFrameTaskArchive(App):
        def __int__(self, root) -> None:
            super().__init__()
            self.root = root

        @staticmethod
        def create_frame(root) -> customtkinter.CTkFrame:
            """Create and place right frame on a screen"""
            frame_right = customtkinter.CTkFrame(master=root)
            frame_right.grid(row=0, column=1,
                             padx=20, pady=20,
                             sticky="nswe")

            frame_right.grid_rowconfigure(index=0, minsize=10)
            return frame_right

        @staticmethod
        def get_widgets(frame_right: customtkinter.CTkFrame) -> None:
            label_right = customtkinter.CTkLabel(master=frame_right,
                                                 text="Task Archive" + emojize(':check_mark_button:'),
                                                 text_font=("Roboto Medium", -22))
            label_right.grid(row=1, column=1,
                             pady=10, padx=10,
                             sticky='nswe')

    class RightFrameNotebook(App):
        def __int__(self, root) -> None:
            super().__init__()
            self.root = root

        @staticmethod
        def create_frame(root) -> customtkinter.CTkFrame:
            """Create and place right frame on a screen"""
            frame_right = customtkinter.CTkFrame(master=root)
            frame_right.grid(row=0, column=1,
                             padx=20, pady=20,
                             sticky="nswe")

            frame_right.grid_rowconfigure(index=0, minsize=10)
            return frame_right

    class RightFrameEmotionalTracker(App):
        def __int__(self, root) -> None:
            super().__init__()
            self.root = root

        @staticmethod
        def create_frame(root) -> customtkinter.CTkFrame:
            """Create and place right frame on a screen"""
            frame_right = customtkinter.CTkFrame(master=root)
            frame_right.grid(row=0, column=1,
                             padx=20, pady=20,
                             sticky="nswe")

            frame_right.grid_rowconfigure(index=0, minsize=10)
            return frame_right

    class RightFrameSettings(App):
        def __int__(self, root) -> None:
            super().__init__()
            self.root = root

        @staticmethod
        def create_frame(root) -> customtkinter.CTkFrame:
            """Create and place right frame on a screen"""
            frame_right = customtkinter.CTkFrame(master=root)
            frame_right.grid(row=0, column=1,
                             padx=20, pady=20,
                             sticky="nswe")

            frame_right.grid_rowconfigure(index=0, minsize=10)
            return frame_right


class AppSettings(App):
    pass


class CurrentTasks(App):

    cur_task_array = []

    def __init__(self, root) -> None:
        super().__init__()
        self.root = root

    @staticmethod
    def place_task_widget(root, info: str, row: int, event: int) -> None:
        """Place widget on a screen and add widget in a task array"""

        if len(CurrentTasks.cur_task_array) > 9:
            root.get_error(error_type='Current tasks are full')
            return

        check_task = customtkinter.CTkCheckBox(master=root.frame_right,
                                               text=info, textvariable=tkinter.StringVar)
        check_task.grid(row=row, column=0,
                        pady=10, padx=20,
                        sticky='w')

        task_setting_button = customtkinter.CTkButton(master=root.frame_right,
                                                      text='',
                                                      height=25, width=25)

        task_setting_button.grid(row=row, column=2,
                                 pady=10, padx=20,
                                 sticky='e')

        def change_image_theme(icon_image: PhotoImage, color: str) -> None:
            task_setting_button.configure(fg_color=color, hover_color=color,
                                          image=icon_image, compound="right")

        match customtkinter.get_appearance_mode():
            case 'Light':
                change_image_theme(icon_image=root.add_setting_image_dark, color='#EBEBEB')
            case 'Dark':
                change_image_theme(icon_image=root.add_setting_image_light, color='#2B2929')

        match event:
            case ButtonStatus.not_pressed.value:
                check_task.deselect()
            case ButtonStatus.pressed.value:
                check_task.select()

        CurrentTasks.cur_task_array.append(CurTaskData(task_name=info, task_widget=check_task,
                                                       widget_row=row, task_widget_event=bool(event),
                                                       setting_widget_button=task_setting_button,
                                                       setting_widget_button_menu=tkinter.Menu()))

        task_setting_button.configure(command=lambda: PopUpMenu.PopUpMenuTaskSettings.create_popup_menu(button=task_setting_button,
                                                                                                        root=root,
                                                                                                        row=row))

        setattr(CurrentTasks.cur_task_array[-1], 'setting_widget_button', task_setting_button)

    @staticmethod
    def create_task(root) -> None:
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
                    root.get_error(error_type="Info mustn't contain more than 50 symbols")
                    return dialog_info, info_is_okay

                info_is_okay = True
                return dialog_info, info_is_okay
            return dialog_info, info_is_okay

        info, is_okay = get_task_info()

        if not CurrentTasks.cur_task_array:
            row = 1
        else:
            row = CurrentTasks.cur_task_array[-1].widget_row + 1

        if is_okay:
            CurrentTasks.place_task_widget(root=root, info=info, row=row, event=0)

    @staticmethod
    def import_cur_tasks(root) -> None:
        """Import current task info from cur_tasks_save.tds"""

        info_arr, event_arr = import_saved_info()
        row = 1
        while row <= len(info_arr):
            CurrentTasks.place_task_widget(root, info=info_arr[row - 1], row=row, event=event_arr[row - 1])
            row += 1

    @staticmethod
    def save_cur_tasks() -> None:
        """Save current tasks' info in cur_tasks_save.tds;
           If no tasks exist then cur_tasks_save.tds will be removed"""

        def get_check_box_values() -> None:
            """Update task array with widget.get() in values"""

            for t_data in CurrentTasks.cur_task_array:
                t_data.task_widget_event = bool(t_data.task_widget.get())

        get_check_box_values()

        if not CurrentTasks.cur_task_array:
            if exists(Sprites.PATH + '/logs/cur_tasks_save.tds'):
                remove(Sprites.PATH + '/logs/cur_tasks_save.tds')
            return
        else:
            get_check_box_values()

        with open(Sprites.PATH + '/logs/cur_tasks_save.tds', 'w') as saving_file:
            for data in CurrentTasks.cur_task_array:
                saving_file.write(data.task_name + ' : ' + str(int(data.task_widget_event)) + '\n')
        saving_file.close()

        CurrentTasks.cur_task_array.clear()


class ArchiveTasks(App):

    archive_tasks_array = []

    def __init__(self, root) -> None:
        super().__init__()
        self.root = root


class PopUpMenu:
    """All classes that are related to PopUpMenu"""
    class PopUpMenuForCurTasks(App):
        def __init__(self, root):
            super().__init__()
            self.root = root

        @staticmethod
        def delete_all_cur_tasks() -> None:
            """Delete all tasks' widgets and info"""

            for data in CurrentTasks.cur_task_array:
                data.task_widget.destroy()
                data.setting_widget_button.destroy()

            CurrentTasks.cur_task_array.clear()

        @staticmethod
        def create_popup_menu(root) -> tkinter.Menu:
            """Create a right click menu on a right_frame"""
            popupMenu = tkinter.Menu(master=root.frame_right, tearoff=0)

            popupMenu.add_command(label="Create task",
                                  command=lambda: CurrentTasks.create_task(root))
            popupMenu.add_command(label="Delete all tasks",
                                  command=PopUpMenu.PopUpMenuForCurTasks.delete_all_cur_tasks)
            popupMenu.add_separator()
            popupMenu.add_command(label="Exit",
                                  command=lambda: AppExit.on_closing(root))

            root.bind("<Button-2>", root.get_screen_points)

            return popupMenu

    class PopUpMenuForTaskArchive(App):
        def __init__(self, root):
            super().__init__()
            self.root = root

        @staticmethod
        def create_popup_menu(root) -> tkinter.Menu:
            """Create a right click menu on a right_frame"""
            popupMenu = tkinter.Menu(master=root.frame_right, tearoff=0)

            popupMenu.add_command(label="Create task")
            popupMenu.add_command(label="Delete all tasks")
            popupMenu.add_command(label="Import all tasks to current")
            popupMenu.add_separator()
            popupMenu.add_command(label="Exit",
                                  command=lambda: AppExit.on_closing(root))

            root.bind("<Button-2>", root.get_screen_points)

            return popupMenu

    class PopUpMenuTaskSettings(CurrentTasks):
        """Menu for task_settings_button"""

        @staticmethod
        def delete_task(widget_row: int) -> None:  # NOTE: this need to be fixed, rows in other Objects don't change!
            """Delete task depending on current widget's row"""
            for data in CurrentTasks.cur_task_array:
                if data.widget_row == widget_row:
                    data.task_widget.destroy()
                    data.setting_widget_button.destroy()
                    data.setting_widget_button_menu.destroy()
                    CurrentTasks.cur_task_array.remove(data)

        @staticmethod
        def import_to_archive() -> None:
            """Import task info to Archive container"""
            pass

        @staticmethod
        def create_popup_menu(root, button: customtkinter.CTkButton, row: int) -> None:
            """Will create a menu when button is pressed"""
            popup_to_button = tkinter.Menu(root, tearoff=0)
            popup_to_button.add_command(label="Delete task",
                                        command=lambda: PopUpMenu.PopUpMenuTaskSettings.delete_task(row))
            popup_to_button.add_command(label="Import to Archive",
                                        command=lambda: PopUpMenu.PopUpMenuTaskSettings.import_to_archive)

            try:
                x = button.winfo_rootx()
                y = button.winfo_rooty()
                popup_to_button.tk_popup(x, y, 0)
            finally:
                if len(CurrentTasks.cur_task_array) > 1:
                    setattr(CurrentTasks.cur_task_array[-1], 'setting_widget_button_menu', popup_to_button)
                popup_to_button.grab_release()


class AppExit(App):
    """Class for auto-saving current tasks and closing the app"""
    def __init__(self, root) -> None:
        super().__init__()
        self.root = root

    @staticmethod
    def on_closing(root) -> None:
        """Method for closing app and saving information"""
        CurrentTasks.save_cur_tasks()
        root.destroy()


def application() -> None:
    """Start loop for an App"""
    App().mainloop()
