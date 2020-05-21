from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, StringVar
import socket
import threading
from tkinter import messagebox
from functools import partial
import Client

class GUI:
    client_socket = None

    def __init__(self, master, client):
        self.root = master
        self.client = client
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.client.Connect()
        self.initialize_gui()

    def initialize_gui(self):
        self.root.title("Socket Chat")
        # self.root.resizable(0, 0)
        self.display_log_in()

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.client.destroy()
            self.client_socket.close()
            exit(0)

    def validateLogin(self, username, password):
        username = username.get()
        password = password.get()
        print("username entered :", username)
        print("password entered :", password)
        self.client.Login(username, password)
        return

    def validateRegister(self, username, password):
        username = username.get()
        password = password.get()
        print("username entered :", username)
        print("password entered :", password)
        self.client.Register(username, password)
        return

    def display_log_in(self):
        # username label and text entry box
        usernameLabel = Label(self.root, text="User Name").grid(row=0, column=0)
        username = StringVar()
        usernameEntry = Entry(self.root, textvariable=username).grid(row=0, column=1)

        # password label and password entry box
        passwordLabel = Label(self.root,text="Password").grid(row=1, column=0)  
        password = StringVar()
        passwordEntry = Entry(self.root, textvariable=password, show='*').grid(row=1, column=1)

        validateRegister = partial(self.validateRegister, username, password)
        validateLogin = partial(self.validateLogin, username, password)

        registerButton  = Button(self.root, text="Register", command=validateRegister).grid(row=4, column=0)
        loginButton = Button(self.root, text="Login", command=validateLogin).grid(row=4, column=1)  


if __name__ == '__main__':
    root = Tk()
    client = Client.Client()
    gui = GUI(root, client)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()