# import tkinter
# import customtkinter
# from pytubefix import YouTube

# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()

#         self.title("My app")
#         self.geometry("400x300")
#         self.columnconfigure(0, weight=1)
#         self.rowconfigure((0, 1), weight=1)


#         self.button = customtkinter.CTkButton(self, text="Press mee", command=self.button_pressed)
#         self.button.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan="2")
#         self.checkbox1 = customtkinter.CTkCheckBox(self, text="One")
#         self.checkbox1.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsw")
#         self.checkbox2 = customtkinter.CTkCheckBox(self, text="Two")
#         self.checkbox2.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsw")
#         self.checkbox3 = customtkinter.CTkCheckBox(self, text="Three")
#         self.checkbox3.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsw")

#     def button_pressed(self):
#         print("Pressed_button")


# app = App()

# app.mainloop()