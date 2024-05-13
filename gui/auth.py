import customtkinter

class LoginFrame():
    
    def __init__(self):
        pass

    def create_frame(self, root):
        login_frame = customtkinter.CTkFrame(master = root)
        login_frame.pack(pady=20, padx=60, fill="both", expand=True)

        login_label = customtkinter.CTkLabel(master = login_frame, text="Login")
        login_label.configure(font=("Roborto", 24))
        login_label.pack(pady=12, padx=10)

        username_entry = customtkinter.CTkEntry(master=login_frame, placeholder_text="Username")
        password_entry = customtkinter.CTkEntry(master=login_frame, placeholder_text="Password", show="*")

        username_entry.pack(pady=12, padx=10)
        password_entry.pack(pady=12, padx=10)

        login_button = customtkinter.CTkButton(master=login_frame, text="Login")
        login_button.pack(pady=12, padx=10)

        return login_frame

    
class RegisterFrame():
    
    def __init__(self):
        pass

    def create_frame(self, root):
        register_frame = customtkinter.CTkFrame(master = root)
        register_frame.pack(pady=20, padx=60, fill="both", expand=True)

        register_label = customtkinter.CTkLabel(master = register_frame, text="Register")
        register_label.configure(font=("Roborto", 24))
        register_label.pack(pady=12, padx=10)

        username_entry = customtkinter.CTkEntry(master=register_frame, placeholder_text="Username")
        password_entry = customtkinter.CTkEntry(master=register_frame, placeholder_text="Password", show="*")

        username_entry.pack(pady=12, padx=10)
        password_entry.pack(pady=12, padx=10)

        register_button = customtkinter.CTkButton(master=register_frame, text="Register")
        register_button.pack(pady=12, padx=10)

        return register_frame