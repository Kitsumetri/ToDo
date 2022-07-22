import tkinter
import customtkinter
import tkinter.messagebox
from back import import_saved_info

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.title("To-Do List")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ========configure grid layout========
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ============FRAME_LEFT==============
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=200,
                                                 height=100,
                                                 corner_radius=0)

        self.frame_left.grid(row=0,
                             column=0,
                             sticky="nswe")

        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(5, weight=1)
        self.frame_left.grid_rowconfigure(8, minsize=20)
        self.frame_left.grid_rowconfigure(11, minsize=10)

        # ============FRAME_RIGHT=============

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0,
                              column=1,
                              sticky="nswe",
                              padx=20, pady=20)

        self.frame_right.grid_rowconfigure(0, minsize=10)

        # ==========RIGHT_CLICK_MENU==========
        self.popupMenu = tkinter.Menu(self, tearoff=0)
        self.popupMenu.add_command(label="Create task",
                                   command=self.create_task)
        self.popupMenu.add_command(label="Two",
                                   command=self.check_cur_tasks)
        self.popupMenu.add_command(label="Three",
                                   command=self.check)
        self.bind("<Button-2>", self.popup)

        # ========================================LEFT==========================================================

        # ===============Text_0_left=================
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="To-Do",
                                              text_font=("Roboto Medium", -24))  # font name and size in px
        self.label_1.grid(row=0, column=0, pady=10, padx=10)

        # ===============Button_1_left===============
        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Global tasks",
                                                command=self.create_top_level)
        self.button_1.grid(row=1, column=0, pady=10, padx=20)

        # ===============Button_2_left===============
        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Notebook")
        self.button_2.grid(row=2, column=0, pady=10, padx=20)

        # ==================Themes===================
        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Themes:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=16, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")
        # ======================================================================================================

        # ========================================RIGHT=========================================================

        self.label_right = customtkinter.CTkLabel(master=self.frame_right,
                                                  text="Current Tasks",
                                                  text_font=("Roboto Medium", -22))
        self.label_right.grid(row=0, column=0, pady=10, padx=10)

        self.task_button = customtkinter.CTkButton(master=self.frame_right,
                                                   text="Create Task",
                                                   command=self.create_task)
        self.task_button.grid(row=0, column=1, pady=10, padx=10, sticky='w')

        # ======================================================================================================

        # ============SET_DEFAULT_VALUES==============
        self.optionmenu_1.set("Dark")

        self.cur_task_numbers = self.import_cur_tasks()
        self.cur_task_info = import_saved_info()
        self.cur_task_value = []
        self.cur_task_array = {}

        self.cur_check_tasks_array = []

    # =========================================Methods==========================================================

    def add_task(self, task: customtkinter.CTkCheckBox):
        self.cur_check_tasks_array.append(task)

    @staticmethod
    def create_top_level() -> None:
        window = customtkinter.CTkToplevel()
        window.title("TopLevel")
        window.geometry("400x300")
        label = customtkinter.CTkLabel(master=window,
                                       text="Add something")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

        def slider_event(value):
            print(value)

        slider = customtkinter.CTkSlider(master=window, from_=0, to=100, command=slider_event)
        slider.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def create_task(self, mode: str) -> None:
        info, is_okay = self.get_task_info()

        if is_okay:
            self.cur_task_info.append(info)
            check_task = customtkinter.CTkCheckBox(master=self.frame_right,
                                                   text=info,
                                                   textvariable=tkinter.StringVar)
            check_task.grid(row=self.cur_task_numbers,
                            column=0,
                            pady=10, padx=20,
                            sticky='w')
            self.add_task(task=check_task)
            self.cur_task_numbers += 1

    def get_task_info(self) -> (str, bool):
        dialog = customtkinter.CTkInputDialog(master=None,
                                              text="Task info:",
                                              title="Create Task")
        info = dialog.get_input()
        info_is_okay = False

        if info and (info[0] != " ") and (info[0] != "\n"):
            if len(info) > 50:
                self.get_error(error_type="Info must not contain more than 50 symbols")
                return info, info_is_okay

            info_is_okay = True
            return info, info_is_okay
        return info, info_is_okay

    def check_cur_tasks(self):
        print(self.cur_check_tasks_array)

    def import_cur_tasks(self) -> int:
        info_arr = import_saved_info()
        row = 1
        while row <= len(info_arr):
            check_task = customtkinter.CTkCheckBox(master=self.frame_right,
                                                   text=info_arr[row-1],
                                                   textvariable=tkinter.StringVar)
            check_task.grid(row=row, column=0, pady=10, padx=20, sticky='w')
            row += 1
        return row

    @staticmethod
    def get_error(error_type: str) -> None:
        window = customtkinter.CTkToplevel()
        window.title("Error message")
        window.geometry("500x100")
        label = customtkinter.CTkLabel(master=window,
                                       text=error_type,
                                       text_color="red")
        label.pack(fill="both", expand=True, padx=40, pady=40)

    @staticmethod
    def change_appearance_mode(new_appearance_mode) -> None:
        customtkinter.set_appearance_mode(new_appearance_mode)

    def save(self) -> None:

        with open('save.tds', 'w') as saving_file:
            for task in self.cur_task_info:
                saving_file.write(task + '\n')
        saving_file.close()

    def check(self) -> None:
        for task_checkbox in self.cur_check_tasks_array:
            task_checkbox.select()

    def popup(self, event):
        self.popupMenu.post(event.x_root, event.y_root)

    def on_closing(self) -> None:
        self.save()
        self.destroy()

    # ==========================================================================================================


def application_ui() -> None:
    App().mainloop()
