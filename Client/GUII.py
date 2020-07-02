import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
import threading
from tkinter import filedialog
from tkinter import messagebox

class Message_list:
    def __init__(self, frame):
        #self.messages_list = scrolledtext.ScrolledText(frame, wrap='word', font=('Helvetica', 13))
        #self.messages_list.insert(tk.END, 'Welcome to Python Chat\n')
        #self.messages_list.configure(state='disabled')
        #frame.grid_rowconfigure(0, weight=1)
        #frame.grid_columnconfigure(0, weight=1)
        self.messages_list = scrolledtext.ScrolledText(frame, wrap='word')
        #self.Message_box.grid(row=0,column=0,sticky='nswe')
        self.messages_list.insert(END, 'Welcome to Python Chat\n')
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

        tk.Label(self.root,text="IP").grid(row=2, column=0)
        self.IPEntry = tk.Entry(self.root, font=self.font)
        self.IPEntry.grid(row=2, column=1)

        tk.Button(self.root, text="Register", command=self.Register).grid(row=4, column=0)
        tk.Button(self.root, text="Login", command=self.Login).grid(row=4, column=1)

    def Register(self):
        self.client.Connect()
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        IP = self.IPEntry.get()
        self.client.configIP(IP)
        if not self.client.Register(username, password):
            self.client.close()
        else:
            self.client.Listen()
            self.root.quit()

    def Login(self):
        self.client.Connect()
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        IP = self.IPEntry.get()
        self.client.configIP(IP)
        if not self.client.Login(username, password):
            print('failed')
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

    def show_event(self, event):
        self.Show_button.pack_forget()
        self.Show_button_label.pack(side=LEFT, fill=BOTH, expand=YES)
        self.Friend_request_button_label.pack_forget()
        self.Friend_request_button.pack(side=LEFT, fill=BOTH, expand=YES)
        self.update()
        self.friend_request_list.pack_forget()
        self.logins_list.pack(side=LEFT, fill=BOTH, expand=YES)

    def Friend_request_event(self, event):
        self.Show_button_label.pack_forget()
        self.Show_button.pack(side=LEFT, fill=BOTH, expand=YES)
        self.Friend_request_button.pack_forget()
        self.Friend_request_button_label.pack(side=LEFT, fill=BOTH, expand=YES)
        self.update()
        self.logins_list.pack_forget()
        self.friend_request_list.pack(side=LEFT, fill=BOTH, expand=YES)


    def build_window(self):
        """Build chat window, set widgets positioning and event bindings"""
        # Size config
        self.root.geometry('{}x{}'.format(800, 450))
        self.root.minsize(600, 400)

        # create all of the main containers
        self.left_frame = Frame(self.root, bg='red', width=150, height=450, pady=3)
        self.right_frame = Frame(self.root, bg='blue', width=650, height=450, pady=3)

        # layout all of the main containers
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.left_frame.grid(row=0,column=0,sticky='ns')
        self.right_frame.grid(row=0,column=1,sticky='nswe')

        # create all of the left containers
        self.Username_Search_Frame = Frame(self.left_frame, bg='yellow', pady=3)
        self.Username_Search_Frame.grid_rowconfigure(0, weight=1)
        self.Username_Search_Frame.grid_columnconfigure(0, weight=1)
        self.Username_label = Label(self.Username_Search_Frame, text=self.client.username)
        self.Search_entry = Entry(self.Username_Search_Frame, text='Add people')
        self.Search_entry.bind('<Return>', self.add_event)
        self.Username_label.grid(row=0,column=0,sticky='nswe')
        self.Search_entry.grid(row=1,column=0,sticky='nswe')

        self.Show_Friend_request_Frame = Frame(self.left_frame, bg='red', pady=3)
        self.Show_button = Button(self.Show_Friend_request_Frame, text='Chats')
        self.Show_button.bind('<Button-1>', self.show_event)
        self.Show_button_label = Label(self.Show_Friend_request_Frame, text='Chats')

        self.Friend_request_button = Button(self.Show_Friend_request_Frame, text='Friend_request')
        self.Friend_request_button.bind('<Button-1>', self.Friend_request_event)
        self.Friend_request_button_label = Label(self.Show_Friend_request_Frame, text='Friend_request')

        self.Show_button_label.pack(side=LEFT, fill=BOTH, expand=YES)
        self.Friend_request_button.pack(side=LEFT, fill=BOTH, expand=YES)

        self.logins_list_Frame = Frame(self.left_frame, bg='green', pady=3)
        self.logins_list_Frame.grid_rowconfigure(0, weight=1)
        self.logins_list_Frame.grid_columnconfigure(0, weight=1)
        self.logins_list = Listbox(self.logins_list_Frame, selectmode=SINGLE, exportselection=False)
        self.logins_list.bind('<<ListboxSelect>>', self.selected_login_event)
        self.logins_list.pack(side=LEFT, fill=BOTH, expand=YES)

        self.friend_request_list = Listbox(self.logins_list_Frame, selectmode=SINGLE, exportselection=False)
        self.friend_request_list.bind('<<ListboxSelect>>', self.select_friend_request)
        #self.friend_request_list.pack(side=LEFT, fill=BOTH, expand=YES)

        self.Username_Search_Frame.grid(row=0,column=0,sticky='nswe')
        self.Show_Friend_request_Frame.grid(row=1,column=0,sticky='nswe')
        self.logins_list_Frame.grid(row=2,column=0,sticky='nswe')

        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)


        # create all of the right containers
        self.Target_name_frame = Frame(self.right_frame, bg='yellow', pady=3)
        self.Target_name_frame.grid_rowconfigure(0, weight=1)
        self.Target_name_frame.grid_columnconfigure(0, weight=1)
        self.Target = Label(self.Target_name_frame, text='Target_name')
        self.Target.grid(row=0,column=0,sticky='nswe')

        self.Message_box_frame = Frame(self.right_frame, bg='black', pady=3)
        self.message_list = Message_list(self.Message_box_frame)
        self.message_list.show()

        self.Entry_frame = Frame(self.right_frame, bg='grey', height=100, pady=3)
        self.Entry_frame.grid_rowconfigure(0, weight=1)
        self.Entry_frame.grid_columnconfigure(0, weight=1)
        self.Entry = Text(self.Entry_frame)
        self.Entry.bind('<Return>', self.send_entry_event)
        self.Entry.grid(row=0,column=0,sticky='nswe')

        self.Send_file_button = Button(self.right_frame, text='Send file')
        self.Send_file_button.bind('<Button-1>', self.send_file_event)
        self.Send_file_button.grid(row=3,column=0,sticky='nswe')

        self.Target_name_frame.grid(row=0,column=0,sticky='nswe')
        self.Message_box_frame.grid(row=1,column=0,sticky='nswe')
        self.Entry_frame.grid(row=2,column=0,sticky='nswe')
        

        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(2, weight=4)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing_event)

    def run(self):
        """Handle chat window actions"""
        self.root.mainloop()
        #self.root.destroy()

    def update(self):
        friendlist = self.client.showFriend()
        self.logins_list.delete(0,'end')
        self.friend_request_list.delete(0,'end')
        print('nice')
        for friend in friendlist:
            #if friendlist[friend] == 'Online':
            #    print(friend)
            self.logins_list.insert(tk.END, friend + ': ' + friendlist[friend])

        friendlist = self.client.showFriendRequest()
        print('nice')
        for friend in friendlist:
            self.friend_request_list.insert(tk.END, friend)

    def on_closing_event(self):
        self.client.close()
        print('ok')
        self.root.destroy()

    def selected_login_event(self, event):
        """Set as target currently selected login on login list"""
        cursor = self.logins_list.get(self.logins_list.curselection())
        target = cursor.split(':')[0]
        status = cursor.split(':')[1][1:]

        if target == None:
            return 

        self.Target.config(text=target)
        self.client.target = target
        self.message_list.hide()
        if target == None:
            return 

        if status == 'Online':
            if target not in self.client.buff_dict:
                self.client.startChatTo(target)
            elif self.client.buff_dict[target].status == False:
                self.client.startChatTo(target)

            print(target)
            self.message_list = self.client.message_list_dict[target]
            self.message_list.show()

        else:
            if target not in self.client.message_list_dict:
                self.client.message_list_dict[target] = Message_list(self.Message_box_frame)
            self.message_list = self.client.message_list_dict[target]
            self.message_list.show()

    def select_friend_request(self, event):
        """Set as target currently selected login on login list"""
        print('selected')
        target = self.friend_request_list.get(self.friend_request_list.curselection())
        print(target)
        if messagebox.askyesno('Add friend', 'Accept ' + target + '?'):
            self.client.acceptFriendRequest(target)
        else:
            self.client.rejectFriendRequest(target)
        self.update()

    def send_entry_event(self, event):
        #message = self.entry.get('1.0', tk.END)
        #self.client.chatTo(message=message)
        text = self.Entry.get(1.0, tk.END)
        if text != '\n':
            #message = 'msg;' + self.login + ';' + self.target + ';' + text[:-1]
            print(text)
            self.client.chatTo(message=text[:-1])
            self.Entry.mark_set(tk.INSERT, 1.0)
            self.Entry.focus_set()
            self.Entry.delete(1.0, tk.END)
            return 'break'
        else:
            messagebox.showinfo('Warning', 'You must enter non-empty message')

    def add_event(self, event):
        text = self.Search_entry.get()
        self.Search_entry.delete(0, END)
        if messagebox.askyesno('Add friend', 'Do you want to add ' + text):
            if self.client.addFriend(text):
                messagebox.showinfo('Add friend', 'Sent')
            else:
                messagebox.showwarning('Add friend', 'Failed!')

    def send_file_event(self, event):
        filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file")
        print(filename)
        if filename is not None:
            try:
                self.client.sendFileTo(filename) 
            except:
                return
