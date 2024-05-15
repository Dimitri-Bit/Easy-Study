import customtkinter
import requests

JWT_TOKEN = None
lecture_tabs = []

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title("Authentication")
root.geometry("550x450")

# Functions
def un_req_post(url, data):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br'}
    
    return requests.post(url, headers=headers, json=data)

def req_post(url, data):
    global JWT_TOKEN
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Authorization': 'Bearer ' + str(JWT_TOKEN)}
        
    return requests.post(url, headers=headers, json=data)

def req_get(url):
    global JWT_TOKEN
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Authorization': 'Bearer ' + str(JWT_TOKEN)}
        
    return requests.get(url, headers=headers)

def clear_auth():
    auth_tab.destroy()
    root.geometry("950x550")
    root.title("Lectures")


def create_lecture(name, text):
    lecture_tab = home_tab.add(name)

    lecture_frame = customtkinter.CTkScrollableFrame(master=lecture_tab, width=600, height=450)
    lecture_frame.pack()

    name_label = customtkinter.CTkLabel(master=lecture_frame, text=name)
    name_label.configure(font=("Roberto", 28))
    name_label.pack(pady=(30, 10))

    text_box = customtkinter.CTkTextbox(master=lecture_frame, width=650, height=250)
    text_box.configure(font=("Roborto", 16))
    text_box.pack(pady=20, padx=30)
    text_box.insert(0.0, text)


def refresh_lectures():
    global lecture_tabs

    response = req_get("http://localhost:8080/getlectures")
    json_response = response.json()

    if not response.status_code == 200:
        message_label.configure(text=json_response["message"], text_color="#d15e71")
        return

    lectures = json_response["lectures"]

    for lecture in lectures:
        if not lecture["name"] in lecture_tabs:
            create_lecture(lecture["name"], lecture["contents"])
            lecture_tabs.append(lecture["name"])


def login():
    global JWT_TOKEN
    username = login_username_entry.get()
    password = login_password_entry.get()

    data = {
        "username": username,
        "password": password
    }

    response = un_req_post("http://localhost:8080/login", data)
    json_response = response.json()
    
    if not response.status_code == 200:
        login_message_label.configure(text=json_response["message"], text_color="#d15e71")
        return
    
    if response.status_code == 200:
        login_message_label.configure(text=json_response["message"], text_color="#50c76d")
        JWT_TOKEN = json_response["access_token"]
        clear_auth()
        home_tab.pack()
        refresh_lectures()
        return
    
    login_message_label.configure(text="Something went wrong", text_color="#d15e71")


def register():
    username = register_username_entry.get()
    password = register_password_entry.get()

    data = {
        "username": username,
        "password": password
    }

    response = un_req_post("http://localhost:8080/register", data)
    json_response = response.json()

    if not response.status_code == 201:
        register_message_label.configure(text=json_response["message"], text_color="#d15e71")
        return

    if response.status_code == 201:
        register_message_label.configure(text=json_response["message"], text_color="#50c76d")
        return
    
    register_message_label.configure(text="Something went wrong", text_color="#d15e71")


def add_lecture():
    name = name_entry.get()
    text = text_entry.get("1.0", "end-1c")

    data = {
        "name": name,
        "text": text
    }

    response = req_post("http://localhost:8080/addlecture", data)
    json_response = response.json()

    if not response.status_code == 200:
        print(json_response)
        print(f"JWT: {JWT_TOKEN}")
        message_label.configure(text=json_response["message"], text_color="#d15e71")
        return
    
    if response.status_code == 200:
        message_label.configure(text=json_response["message"], text_color="#50c76d")
        refresh_lectures()
        return
        
    message_label.configure(text="Something went wrong", text_color="#d15e71")


# Auth Tab
auth_tab = customtkinter.CTkTabview(root)
auth_tab.pack(pady=10)

login_tab = auth_tab.add("Login")
register_tab = auth_tab.add("Register")

# Login Frame
login_frame = customtkinter.CTkFrame(master=login_tab)
login_frame.pack(pady=20, padx=60)

login_label = customtkinter.CTkLabel(master = login_frame, text="Login")
login_label.configure(font=("Roborto", 24))
login_label.pack(pady=12, padx=10)

login_message_label = customtkinter.CTkLabel(master=login_frame, text="")
login_message_label.configure(font=("Roborto", 18), text_color="#d15e71")
login_message_label.pack()

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

register_message_label = customtkinter.CTkLabel(master=register_frame, text="")
register_message_label.configure(font=("Roborto", 18))
register_message_label.pack()

register_username_entry = customtkinter.CTkEntry(master=register_frame, placeholder_text="Username")
register_password_entry = customtkinter.CTkEntry(master=register_frame, placeholder_text="Password", show="*")

register_username_entry.pack(pady=12, padx=10)
register_password_entry.pack(pady=12, padx=10)

register_button = customtkinter.CTkButton(master=register_frame, text="Register", command=register)
register_button.pack(pady=12, padx=10)

# Home Tab
home_tab = customtkinter.CTkTabview(root)

homepage_tab = home_tab.add("Home")

# Homepage
home_frame = customtkinter.CTkFrame(master=homepage_tab, width=500, height=350)
home_frame.pack()

home_label = customtkinter.CTkLabel(master=home_frame, text="AI Summarizer")
home_label.configure(font=("Roborto", 28))
home_label.pack(pady=(30, 10))

message_label = customtkinter.CTkLabel(master=home_frame, text="")
message_label.configure(font=("Roborto", 18))
message_label.pack(pady=10)

name_entry = customtkinter.CTkEntry(master=home_frame, width=650, placeholder_text="Lecture Name")
name_entry.configure(font=("Roborto", 16))
name_entry.pack()

text_entry = customtkinter.CTkTextbox(master=home_frame, width=650, height=250)
text_entry.pack(pady=20, padx=30)

sumbit_button = customtkinter.CTkButton(master=home_frame, text="Summarize", command=add_lecture)
sumbit_button.configure(font=("Roborto", 18))
sumbit_button.pack(pady=12, padx=10)


root.mainloop()