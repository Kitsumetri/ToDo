import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.title("To-Do List")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ============FRAME_LEFT==============
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=200,
                                                 height=100,
                                                 corner_radius=0)

        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(5, weight=1)
        self.frame_left.grid_rowconfigure(8, minsize=20)
        self.frame_left.grid_rowconfigure(11, minsize=10)

        # ============FRAME_RIGHT=============
        # configure grid layout (3x7)
        self.frame_right.rowconfigure(0, weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure(1, weight=1)  # ?
        self.frame_right.columnconfigure(2, weight=0)

        # ========================================LEFT==========================================================

        # ===============Text_0_left===============
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
                                                text="Notebook",
                                                command=self.button_event)
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
        self.task_button.grid(row=0, column=1, pady=10, padx=10)

        # ============SET_DEFAULT_VALUES==============
        self.optionmenu_1.set("Dark")
        self.cur_task_numbers = 1
        self.glob_task_numbers = 1

    # =========================================Methods==========================================================

    @staticmethod
    def button_event():
        print("Button pressed")

    @staticmethod
    def create_top_level():
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

    @staticmethod
    def delete_task():
        pass

    @staticmethod
    def change_appearance_mode(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    cur_task_numbers = 1
    glob_task_numbers = 0

    def create_task(self):

        info = self.get_task_info()
        if len(info) > 50:
            self.get_error("Info must not contain more than 50 symbols")
            return

        if info and (info[0] != " ") and (info[0] != "\n"):
            check_box = customtkinter.CTkCheckBox(master=self.frame_right,
                                                  text=info)
            check_box.grid(row=App.cur_task_numbers, column=0, pady=10, padx=20)
            App.cur_task_numbers += 1

    @staticmethod
    def get_task_info():
        dialog = customtkinter.CTkInputDialog(master=None,
                                              text="Task info:",
                                              title="Create Task")
        info = dialog.get_input()
        print("Task info:", info)
        return info

    @staticmethod
    def get_error(error_type: str):
        window = customtkinter.CTkToplevel()
        window.title("Error message")
        window.geometry("500x100")
        label = customtkinter.CTkLabel(master=window,
                                       text=error_type,
                                       text_color="red")
        label.pack(fill="both", expand=True, padx=40, pady=40)

    def on_closing(self):
        self.destroy()


def application_ui():
    app = App()
    app.mainloop()
