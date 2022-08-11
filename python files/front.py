import tkinter
import tkinter.messagebox
from emoji import emojize
from back import import_saved_info, exists, TaskData, Sprites, ButtonStatus, customtkinter, PhotoImage
from os import remove


class App(customtkinter.CTk):
    WIDTH = 640
    HEIGHT = 600

    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme(Sprites.PATH + "/Custom themes/purple.json")

    def __init__(self) -> None:
        super().__init__()

        self.title('TODO' + emojize(':sparkles:'))
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(False, False)

        # region Sprite downloading
        self.add_list_image_light = Sprites.download_sprites("/Sprites/Light/add-list.png")
        self.add_list_image_dark = Sprites.download_sprites("/Sprites/Dark/add-list.png")

        self.add_setting_image_light = Sprites.download_sprites("/Sprites/Light/settings.png")
        self.add_setting_image_dark = Sprites.download_sprites("/Sprites/Dark/settings.png")
        # endregion

        # region Layout configuring
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # endregion

        # region Frame left init
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=200, height=100,
                                                 corner_radius=0)

        self.frame_left.grid(row=0, column=0,
                             sticky="nswe")

        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(5, weight=1)
        self.frame_left.grid_rowconfigure(8, minsize=20)
        self.frame_left.grid_rowconfigure(11, minsize=10)
        # endregion ш

        # region Frame right init
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1,
                              padx=20, pady=20,
                              sticky="nswe")

        self.frame_right.grid_rowconfigure(index=0, minsize=10)
        # endregion

        # region Popup_menu frame right

        self.popupMenu = tkinter.Menu(master=self.frame_right, tearoff=0)

        self.popupMenu.add_command(label="Create task",
                                   command=self.create_task)
        self.popupMenu.add_command(label="Delete all tasks",
                                   command=self.delete_all_cur_tasks)
        self.popupMenu.add_separator()
        self.popupMenu.add_command(label="Exit",
                                   command=self.on_closing)

        self.bind("<Button-2>", self.popup)

        # endregion_f

        # region Frame left widgets
        # ===============Text_0_left=================
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text='To-Do List ' + emojize(':sparkles:'),
                                              text_font=("Roboto Medium", -28))  # font name and size in px
        self.label_1.grid(row=0, column=0,
                          pady=10, padx=10)

        # ===============Button_1_left===============
        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Global tasks")
        self.button_1.grid(row=1, column=0,
                           pady=10, padx=20)

        # ===============Button_2_left===============
        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Notebook")
        self.button_2.grid(row=2, column=0,
                           pady=10, padx=20)

        # ==================Themes===================
        self.switch_theme = customtkinter.CTkSwitch(master=self.frame_left,
                                                    text='Dark mode',
                                                    command=self.change_appearance_mode)

        self.switch_theme.grid(row=10, column=0,
                               pady=10, padx=20,
                               sticky='w')
        # endregion

        # region Frame right widgets
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

        # endregion

        # region Default values
        self.cur_task_array = []
        self.import_cur_tasks()
        self.switch_theme.select()
        # endregion

    # =========================================Methods==========================================================
    def place_task_widget(self, info: str, row: int, event: int) -> None:
        """Place widget on a screen and add widget in a task array"""

        if len(self.cur_task_array) > 11:
            return

        check_task = customtkinter.CTkCheckBox(master=self.frame_right,
                                               text=info, textvariable=tkinter.StringVar)
        check_task.grid(row=row, column=0,
                        pady=10, padx=20,
                        sticky='w')

        task_setting_button = customtkinter.CTkButton(master=self.frame_right,
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
                change_image_theme(icon_image=self.add_setting_image_dark, color='#EBEBEB')
            case 'Dark':
                change_image_theme(icon_image=self.add_setting_image_light, color='#2B2929')

        match event:
            case ButtonStatus.not_pressed.value:
                check_task.deselect()
            case ButtonStatus.pressed.value:
                check_task.select()

        self.cur_task_array.append(TaskData(task_name=info, task_widget=check_task,
                                            widget_row=row, task_widget_event=bool(event),
                                            setting_widget_button=task_setting_button,
                                            setting_widget_button_menu=tkinter.Menu()))

        def popup_menu_create(button: customtkinter.CTkButton) -> None:
            """Would create a menu with options if button was clicked"""
            def delete_task(widget_row: int) -> None:  # NOTE: this need to be fixed, rows in other Objects don't change!
                """Delete task depending on current widget's row"""
                for data in self.cur_task_array:
                    if data.widget_row == widget_row:
                        data.task_widget.destroy()
                        data.setting_widget_button.destroy()
                        data.setting_widget_button_menu.destroy()
                        self.cur_task_array.remove(data)

            popup_to_button = tkinter.Menu(self, tearoff=0)
            popup_to_button.add_command(label="Delete task",
                                        command=lambda: delete_task(row))
            popup_to_button.add_command(label="Import to Archive")

            try:
                x = button.winfo_rootx()
                y = button.winfo_rooty()
                popup_to_button.tk_popup(x, y, 0)
            finally:
                setattr(self.cur_task_array[-1], 'setting_widget_button_menu', popup_to_button)
                popup_to_button.grab_release()

        task_setting_button.configure(command=lambda: popup_menu_create(task_setting_button))

        setattr(self.cur_task_array[-1], 'setting_widget_button', task_setting_button)

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

        if not self.cur_task_array:
            row = 1
        else:
            row = self.cur_task_array[-1].widget_row + 1

        if is_okay:
            self.place_task_widget(info=info, row=row, event=0)

    def import_cur_tasks(self) -> None:
        """Import current task info from save.tds"""

        info_arr, event_arr = import_saved_info()
        row = 1
        while row <= len(info_arr):
            self.place_task_widget(info=info_arr[row - 1], row=row, event=event_arr[row - 1])
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

    def change_appearance_mode(self) -> None:
        """Change theme"""

        def change_images_themes() -> None:
            """Function that changes all images' version depending on appearance_mode"""

            def change_color_widgets(icon_image: (PhotoImage, PhotoImage), color: str) -> None:
                self.task_button.configure(image=icon_image[0], compound="right")
                if self.cur_task_array:
                    for data in self.cur_task_array:
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

    def on_closing(self) -> None:
        """Method for closing app and saving information"""

        def save() -> None:
            """Save current tasks' info in save.tds;
               If no tasks exist then save.tds will be removed"""

            def get_check_box_values() -> None:
                """Update task array with widget.get() in values"""

                for t_data in self.cur_task_array:
                    t_data.task_widget_event = bool(t_data.task_widget.get())

            if not self.cur_task_array:
                if exists(Sprites.PATH + '/logs/save.tds'):
                    remove(Sprites.PATH + '/logs/save.tds')
                return
            else:
                get_check_box_values()

            with open(Sprites.PATH + '/logs/save.tds', 'w') as saving_file:
                for data in self.cur_task_array:
                    saving_file.write(data.task_name + ' : ' + str(int(data.task_widget_event)) + '\n')
            saving_file.close()

        save()
        self.destroy()

    # ============POPUP_MENU_METHODS==============
    def delete_all_cur_tasks(self) -> None:
        """Delete all tasks' widgets and info"""

        for data in self.cur_task_array:
            data.task_widget.destroy()
            data.setting_widget_button.destroy()

        self.cur_task_array.clear()

    def popup(self, event) -> None:
        """Method that allow to use 'right button menu'"""
        self.popupMenu.post(event.x_root, event.y_root)


def application() -> None:
    """Start loop for an App"""
    App().mainloop()
