from tkinter import *
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

main_root = customtkinter.CTk()
main_root.title("Lectures")
main_root.geometry("950x550")

tab = customtkinter.CTkTabview(main_root)
tab.pack()

lecture_tab = tab.add("Home")

def add_lecture():
    text = entry.get("1.0", "end-1c")

    if len(text) < 250:
        message_label.configure(text="Text is too short to summarize", text_color="#d15e71")
        return
    
    print(text)

#Home
home_frame = customtkinter.CTkFrame(master=lecture_tab, width=500, height=350)
home_frame.pack()

home_label = customtkinter.CTkLabel(master=home_frame, text="Text Summarizer")
home_label.configure(font=("Roborto", 28))
home_label.pack(pady=(30, 10))

message_label = customtkinter.CTkLabel(master=home_frame, text="")
message_label.configure(font=("Roborto", 18))
message_label.pack(pady=10)

entry = customtkinter.CTkTextbox(master=home_frame, width=650, height=250)
entry.pack(pady=20, padx=30)

sumbit_button = customtkinter.CTkButton(master=home_frame, text="Summarize", command=add_lecture)
sumbit_button.configure(font=("Roborto", 18))
sumbit_button.pack(pady=12, padx=10)
