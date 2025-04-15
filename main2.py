import tkinter
import customtkinter
from pytubefix import YouTube

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("My app")
        self.geometry("400x150")
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1), weight=1)

        self.checkboxfrane = customtkinter.CTkFrame(self)
        self.checkboxfrane.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")
        self.checkbox2 = customtkinter.CTkCheckBox(self, text="two")
        self.checkbox2.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox3 = customtkinter.CTkCheckBox(self, text="Three")
        self.checkbox3.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        self.button = customtkinter.CTkButton(self, text="Press me", command=self.button_pressed)
        self.button.grid(row = 3, column=0, padx=10, pady=(0, 10), sticky="ew")

    def button_pressed(self):
        return "press button"



app = App()
app.mainloop()