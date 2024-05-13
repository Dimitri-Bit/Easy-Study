from tkinter import *
import customtkinter
import requests

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

root.title("Authentication")
root.geometry("550x450")

tab = customtkinter.CTkTabview(root)
tab.pack(pady=10)

login_tab = tab.add("Login")
register_tab = tab.add("Register")

def login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Accept-Language': 'en-US,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate, br'}
    
    data = {
        "username": username,
        "password": password
    }
    
    response = requests.post("http://localhost:8080/login", headers=headers, json=data)

    print(response)
    json_response = response.json()
    
    if not response.status_code == 200:
        message_label.configure(text=json_response["message"], text_color="#d15e71")
        return

    if response.status_code == 200:
        message_label.configure(text=json_response["message"], text_color="#50c76d")
        return
    
    message_label.configure(text="Something went wrong", text_color="#d15e71")

# Login Frame
login_frame = customtkinter.CTkFrame(master = login_tab)
login_frame.pack(pady=20, padx=60, fill="both", expand=True)

login_label = customtkinter.CTkLabel(master = login_frame, text="Login")
login_label.configure(font=("Roborto", 24))
login_label.pack(pady=12, padx=10)

message_label = customtkinter.CTkLabel(master=login_frame, text="")
message_label.configure(font=("Roborto", 18), text_color="#d15e71")
message_label.pack()

login_username_entry = customtkinter.CTkEntry(master=login_frame, placeholder_text="Username")
login_password_entry = customtkinter.CTkEntry(master=login_frame, placeholder_text="Password", show="*")

login_username_entry.pack(pady=12, padx=10)
login_password_entry.pack(pady=12, padx=10)

login_button = customtkinter.CTkButton(master=login_frame, text="Login", command=login)
login_button.pack(pady=12, padx=10)

# Register Frame
register_frame = customtkinter.CTkFrame(master = register_tab)
register_frame.pack(pady=20, padx=60, fill="both", expand=True)

register_label = customtkinter.CTkLabel(master = register_frame, text="Register")
register_label.configure(font=("Roborto", 24))
register_label.pack(pady=12, padx=10)

register_username_entry = customtkinter.CTkEntry(master=register_frame, placeholder_text="Username")
register_password_entry = customtkinter.CTkEntry(master=register_frame, placeholder_text="Password", show="*")

register_username_entry.pack(pady=12, padx=10)
register_password_entry.pack(pady=12, padx=10)

register_button = customtkinter.CTkButton(master=register_frame, text="Register")
register_button.pack(pady=12, padx=10)

root.mainloop()