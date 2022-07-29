import tkinter
import tkinter.messagebox
import customtkinter
from emoji import emojize
from back import import_saved_info, exists
from PIL import Image, ImageTk
from os.path import dirname, realpath
from os import remove

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 640
    HEIGHT = 580
    PATH = dirname(realpath(__file__))
    image_size = 22

    def __init__(self):
        super().__init__()

        self.title('To-Do List' + emojize(':sparkles:'))
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(True, True)

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
                                              text='To-Do List' + ' ' + emojize(':sparkles:'),
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
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0,
                               pady=10, padx=20,
                               sticky="w")
        # ======================================================================================================

        # ========================================RIGHT=========================================================

        self.label_right = customtkinter.CTkLabel(master=self.frame_right,
                                                  text="Current Tasks",
                                                  text_font=("Roboto Medium", -22))
        self.label_right.grid(row=0, column=0,
                              pady=10, padx=10)

        self.add_list_image = ImageTk.PhotoImage(
            Image.open(App.PATH + "/Sprites/add-list.png").resize((App.image_size, App.image_size), Image.LANCZOS))

        self.task_button = customtkinter.CTkButton(master=self.frame_right,
                                                   text="Create Task",
                                                   text_font=("Roboto Medium", -19),
                                                   text_color='white',
                                                   image=self.add_list_image, compound="right",
                                                   width=190, height=40,
                                                   command=self.create_task)
        self.task_button.grid(row=0, column=1, columnspan=2,
                              padx=20, pady=10,
                              sticky='s')

        # ======================================================================================================

        # ============SET_DEFAULT_VALUES==============
        self.cur_task_dict = {}  # dict = { Task name: [widget, row, widget.get()] }
        self.cur_task_numbers = self.import_cur_tasks()  # just a row

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

    def create_task(self) -> None:
        """Create task with its info in TaskBox"""

        def get_task_info() -> (str, bool):
            dialog = customtkinter.CTkInputDialog(master=None,
                                                  text="Task info:",
                                                  title="Create Task")
            dialog_info = dialog.get_input()
            info_is_okay = False

            if dialog_info and (dialog_info[0] != " ") and (dialog_info[0] != "\n"):
                if len(dialog_info) > 50:
                    self.get_error(error_type="Info must not contain more than 50 symbols")
                    return dialog_info, info_is_okay

                info_is_okay = True
                return dialog_info, info_is_okay
            return dialog_info, info_is_okay

        info, is_okay = get_task_info()

        if is_okay:
            check_task = customtkinter.CTkCheckBox(master=self.frame_right,
                                                   text=info,
                                                   textvariable=tkinter.StringVar)
            check_task.grid(row=self.cur_task_numbers, column=0,
                            pady=10, padx=20,
                            sticky='w')
            self.cur_task_dict.update({info: [check_task, self.cur_task_numbers]})
            self.cur_task_numbers += 1

    def import_cur_tasks(self) -> int:
        """Import current task info from save.tds"""
        info_arr = import_saved_info()
        row = 1
        while row <= len(info_arr):
            check_task = customtkinter.CTkCheckBox(master=self.frame_right,
                                                   text=info_arr[row-1],
                                                   textvariable=tkinter.StringVar)
            check_task.grid(row=row, column=0,
                            pady=10, padx=20,
                            sticky='w')
            self.cur_task_dict.update({info_arr[row-1]: [check_task, row]})
            row += 1
        return len(info_arr) + 1

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
                   padx=40, pady=40)

    @staticmethod
    def change_appearance_mode(new_appearance_mode: str) -> None:
        """Change theme"""
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self) -> None:
        """Method for closing app and save information"""
        def save() -> None:
            """Save current tasks' info in save.tds;
               If no tasks exist then save.tds will be removed"""
            if self.cur_task_dict == {}:
                if exists('logs/save.tds'):
                    remove('logs/save.tds')
                return

            with open('logs/save.tds', 'w') as saving_file:
                for task in self.cur_task_dict.keys():
                    saving_file.write(task + '\n')
            saving_file.close()
        save()
        self.destroy()

    # ============POPUP_MENU_METHODS==============

    def delete_all_cur_tasks(self) -> None:
        """Delete all tasks' widgets and info in dict"""
        copy_dict = self.cur_task_dict.copy()

        for key, values in copy_dict.items():
            for value in values:
                if str(type(value)) == "<class 'customtkinter.widgets.ctk_checkbox.CTkCheckBox'>":
                    value.destroy()
                    self.cur_task_dict.pop(key)

    def popup(self, event) -> None:
        """Method that allow to use 'right button menu'"""
        self.popupMenu.post(event.x_root, event.y_root)

    # ==========================================================================================================


def application_ui() -> None:
    """Start loop for an App"""
    App().mainloop()
