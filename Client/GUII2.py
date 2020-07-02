import tkinter as tk
import threading
from tkinter import scrolledtext
from tkinter import messagebox

class Message_list:
    def __init__(self, frame):
        self.messages_list = scrolledtext.ScrolledText(frame, wrap='word', font=('Helvetica', 13))
        self.messages_list.insert(tk.END, 'Welcome to Python Chat\n')
        self.messages_list.configure(state='disabled')

    def write(self, text):
        print(text)
        self.messages_list.configure(state='normal')
        if text != '\n':
            self.messages_list.insert(tk.END, text)
        self.messages_list.configure(state='disabled')
        self.messages_list.see(tk.END)

    def show(self):
        self.messages_list.pack(fill=tk.BOTH, expand=tk.YES)

    def hide(self):
        print('okokok')
        self.messages_list.pack_forget()

class Window(object):
    def __init__(self, title, font, client):
        self.title = title
        self.font = font
        self.client = client
        self.root = tk.Tk()
        self.root.title(title)
        self.build_window()
        
class LoginWindow(Window):
    def __init__(self, client, font):
        super(LoginWindow, self).__init__('Login', font, client)
        self.build_window()

    def build_window(self):
        # username label and text entry box
        tk.Label(self.root, text="User Name").grid(row=0, column=0)
        #usernameLabel
        self.usernameEntry = tk.Entry(self.root, font=self.font)
        self.usernameEntry.grid(row=0, column=1)
        self.usernameEntry.focus_set()

        # password label and password entry box
        tk.Label(self.root,text="Password").grid(row=1, column=0)
        #passwordLabel
        self.passwordEntry = tk.Entry(self.root, font=self.font, show='*')
        self.passwordEntry.grid(row=1, column=1)

        tk.Button(self.root, text="Register", command=self.Register).grid(row=4, column=0)
        tk.Button(self.root, text="Login", command=self.Login).grid(row=4, column=1)

    def Register(self):
        self.client.Connect()
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        if not self.client.Register(username, password):
            self.client.close()
        else:
            self.client.Listen()
            self.root.quit()

    def Login(self):
        self.client.Connect()
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        if not self.client.Login(username, password):
            self.client.close()
        else:
            self.client.Listen()
            self.root.quit()

    def run(self):
        self.root.mainloop()
        self.root.destroy()


class ChatWindow(Window):
    def __init__(self, client, font):
        super(ChatWindow, self).__init__('ChatWindow', font, client)
        self.build_window()
        self.update()
        self.bool = True

    def build_window(self):
        """Build chat window, set widgets positioning and event bindings"""
        # Size config
        self.root.geometry('{}x{}'.format(800, 450))
        self.root.minsize(600, 400)

        # Frames config
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # List of messages
        self.frame00 = tk.Frame(main_frame)
        self.frame00.grid(column=0, row=0, rowspan=2, sticky=tk.N + tk.S + tk.W + tk.E)

        # List of logins
        frame01 = tk.Frame(main_frame)
        frame01.grid(column=1, row=0, rowspan=3, sticky=tk.N + tk.S + tk.W + tk.E)

        # Message entry
        frame02 = tk.Frame(main_frame)
        frame02.grid(column=0, row=2, columnspan=1, sticky=tk.N + tk.S + tk.W + tk.E)

        # Buttons
        frame03 = tk.Frame(main_frame)
        frame03.grid(column=0, row=3, columnspan=2, sticky=tk.N + tk.S + tk.W + tk.E)

        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=8)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # ScrolledText widget for displaying messages
        self.message_list = Message_list(self.frame00)
        #self.messages_list = scrolledtext.ScrolledText(self.frame00, wrap='word', font=self.font)
        #self.messages_list.insert(tk.END, 'Welcome to Python Chat\n')
        #self.messages_list.configure(state='disabled')

        # Listbox widget for displaying active users and selecting them
        self.logins_list = tk.Listbox(frame01, selectmode=tk.SINGLE, font=self.font,
                                      exportselection=False)
        self.logins_list.bind('<<ListboxSelect>>', self.selected_login_event)

        # Entry widget for typing messages in
        self.entry = tk.Text(frame02, font=self.font)
        self.entry.focus_set()
        self.entry.bind('<Return>', self.send_entry_event)

        # Button widget for sending messagesFriend_request_button_label
        self.send_button = tk.Button(frame03, text='Send', font=self.font)
        self.send_button.bind('<Button-1>', self.send_entry_event)

        # Button for exiting
        self.exit_button = tk.Button(frame03, text='Send file', font=self.font)
        self.exit_button.bind('<Button-1>', self.send_file_event)

        # Positioning widgets in frame
        #self.messages_list.pack(fill=tk.BOTH, expand=tk.YES)
        self.logins_list.pack(fill=tk.BOTH, expand=tk.YES)
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.send_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.exit_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        # Protocol for closing window using 'x' button
        #self.root.protocol("WM_DELETE_WINDOW", self.on_closing_event)

    def run(self):
        """Handle chat window actions"""
        self.root.mainloop()
        self.root.destroy()

    def update(self):
        friendlist = self.client.showFriend()
        for friend in friendlist:
            self.logins_list.insert(tk.END, friend)

    def selected_login_event(self, event):
        """Set as target currently selected login on login list"""
        target = self.logins_list.get(self.logins_list.curselection())
        self.client.target = target
        self.message_list.hide()
        
        
        if target not in self.client.message_list_dict:
            self.client.startChatTo(target)

        print('target')
        self.message_list = self.client.message_list_dict[target]
        self.message_list.show()

    def send_entry_event(self, event):
        #message = self.entry.get('1.0', tk.END)
        #self.client.chatTo(message=message)
        text = self.entry.get(1.0, tk.END)
        if text != '\n':
            #message = 'msg;' + self.login + ';' + self.target + ';' + text[:-1]
            print(text)
            self.client.chatTo(message=text[:-1])
            self.entry.mark_set(tk.INSERT, 1.0)
            self.entry.delete(1.0, tk.END)
            self.entry.focus_set()
            print('ok')
        else:
            messagebox.showinfo('Warning', 'You must enter non-empty message')

        """
        ""Send message from entry field to target""
        text = self.entry.get(1.0, tk.END)
        if text != '\n':
            #message = 'msg;' + self.login + ';' + self.target + ';' + text[:-1]
            #print(message)
            self.client.chatTo(message=text[:-1])
            self.entry.mark_set(tk.INSERT, 1.0)
            self.entry.delete(1.0, tk.END)
            self.entry.focus_set()
            print('ok')
        else:
            messagebox.showinfo('Warning', 'You must enter non-empty message')

        with self.lock:
            self.messages_list.configure(state='normal')
            if text != '\n':
                self.messages_list.insert(tk.END, text)
            self.messages_list.configure(state='disabled')
            self.messages_list.see(tk.END)
        return 'break'
        """

    def send_file_event(self, event):
        if self.bool:
            self.bool = False
            self.message_list.hide()
        else:
            self.bool = True
            self.message_list.show()

    def on_closing_event(self):
        pass