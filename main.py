import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


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

        # ============frame_right============
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

        # ============frame_right============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ===================================

        # ========================================LEFT==========================================================

        # ===============Text_0_left===============
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="To-Do",
                                              text_font=("Roboto Medium", -24))  # font name and size in px
        self.label_1.grid(row=0, column=0, pady=10, padx=10)

        # ===============Button_1_left===============
        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Button_1",
                                                command=self.create_top_level)
        self.button_1.grid(row=1, column=0, pady=10, padx=20)

        # ===============Button_2_left===============
        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Button_2",
                                                command=self.button_event)
        self.button_2.grid(row=2, column=0, pady=10, padx=20)

        # ===============Themes===============
        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Themes:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=16, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")
        # ======================================================================================================

        # ========================================RIGHT=========================================================

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="All_tasks",
                                                   height=400,
                                                   corner_radius=8,  # <- custom corner radius
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        # ============set default values==============
        self.optionmenu_1.set("Dark")

    # =========================================Methods====================================================

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
    def change_appearance_mode(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)



    def on_closing(self, event=0):
        self.destroy()


def main():
    app = App()
    app.mainloop()
    # tests()


def tests():
    customtkinter.set_appearance_mode("dark")

    app = customtkinter.CTk()
    app.geometry("400x300")

    def button_click_event():
        dialog = customtkinter.CTkInputDialog(master=None, text="Type in a number:", title="Test")
        print("Number:", dialog.get_input())

    button = customtkinter.CTkButton(app, text="Open Dialog", command=button_click_event)
    button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    app.mainloop()


if __name__ == "__main__":
    main()
