from threading import Thread
from time import sleep
from tkinter import *
from tkinter import ttk,messagebox
import socket
from Utils.AES import *

UserHELP = """

ip(require)         : ip address default 127.0.0.1 
port(require)       : use a specific port default is 3000
key(require)        : key is used as way to encrypt data it's 
                      not used in this version but 
                      the default is secret
chat                : shows the messages also allow user to pass
                      command to the client
UserName            : se this user name to login 
Password            : use this password to login
Secret              : use this secret to encrypt my data while 
                        i'm talking to the server
    __________________________________________________________________________
                                    CMD COMMANDS
    --------------------------------------------------------------------------
--help              : shows this message
--PDM               : send a private message to a specific person 
                        [NOTE] normally admin will not see the message
                        but he/she can change that so assume they do 
                        EXAMPLS:--PDM isla@hi isla how is everying :D
                               :--PDM admin@i hate everyone :D
--clear message     : clears admin message box
--shutdown          : it will kill the whole server and destroy the app

    --------------------------------------------------------------------------
                                    ENCRYPTION
                                    ----------
Anonybox uses the symmetric encription with AES -256 CBC PKCS 7
NOTE That this version does not use IV you can turn it on from
AES.py file also users should turn it on too
    --------------------------------------------------------------------------
"""
Gkey = None
class master:
    def __init__(self,master):
        self.master = master
        master.geometry("600x500")
        master.configure(bg="gray20")
        master.title('Anonybox')
        master.resizable(width=FALSE, height=FALSE)
        frame1=Frame(master)
        frame1.pack()
        conn_label =Label(frame1,bg="gray24",width=300,height=2,)
        conn_label.pack()
        self.ip_entry= Entry(width=17)
        self.ip_entry.place(x=4,y=7)
        self.ip_entry.insert(0,"127.0.0.1")
        self.port_entry= Entry(width=6)
        self.port_entry.place(x=150,y=7)
        self.port_entry.insert(0,3000)
        self.key_entry=Entry(width=18)
        self.key_entry.insert(0,"secret")
        self.key_entry.place(x=210,y=7)
        self.start_button= Button(text="start",command=self.connection)
        self.start_button.place(x=370,y=3)
        info_lable = Label(frame1,bg="gray24",width=300,height=2)
        info_lable.pack()
        self.user_entry= Entry(width=17)
        self.user_entry.place(x=4,y=45)
        self.user_entry.insert(0,"UserName")
        self.secret_entry= Entry(width=17)
        self.secret_entry.place(x=150,y=45)
        self.secret_entry.insert(0,"Secret")
        self.password_entry=Entry(width=17)
        self.password_entry.insert(0,"Password")
        self.password_entry.place(x=295,y=45)
        self.login_button= Button(text="Login",command=self.Account)
        self.login_button.configure(state=DISABLED)
        self.login_button.place(x=445,y=41)
        self.chatlable = Text(bg="black",fg="green",width=62,height=20)
        update_scrollb = Scrollbar(self.chatlable,orient=VERTICAL, command=self.chatlable.yview)
        self.chatlable['yscrollcommand'] = update_scrollb.set
        update_scrollb.place(x=483,y=0,relheight=1, height=2)
       # self.chatlable.configure(state=DISABLED)
        self.chatlable.place(x=50,y=100)
        self.send_entry =Entry(width=62,bg="green",fg="black")
        self.send_entry.place(x=50,y=445)
        self.send_button=Button(text="SEND",width=59,command=self.commands)
        self.send_button.configure(state=DISABLED)
        self.send_button.place(x=50,y=469)
    def sendmsg(self,mesg):
            key = self.secret_entry.get()
            msg = encrypt(mesg,key)
            self.s.send(msg)
            self.send_entry.delete(0, 'end')
    def recvmsg(self,key):
        while True:
            msg = self.s.recv(1024)
            mesg = decrypt(msg,key)
            if mesg == "server asks if you still there":
                mesg = encrypt('YEP',key)
                self.s.send(mesg)
            else:
                self.chatlable.insert(INSERT,"{}\n".format(mesg))  
    def connection(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        key = str(self.key_entry.get())
        self.start_button["state"] = DISABLED
        self.start_button["text"]="stop"
        self.login_button["state"] =NORMAL
        msg= ("Client started with {}:{} using {} As a Secret".format(ip,port,key))
        self.chatlable.insert(INSERT,"{}\n".format(msg))
        self.cts(ip,port)
    def cts(self,host,port):#connect to the server
        try:
            self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.s.connect((host,int(port)))
        except:
           msg= ("Server  is refusing to connect [-]")
           self.chatlable.insert(INSERT,"{}\n".format(msg)) 
           self.start_button["state"] = NORMAL
           self.start_button["text"]="start"
           self.login_button["state"] =DISABLED
        wlc_msg = self.s.recv(1024).decode()
        wlc_msg = (f"{wlc_msg}\n Please login")
        self.chatlable.insert(INSERT,"{}".format(wlc_msg)) 
        self.login_button["state"] = NORMAL
    def authentication(self,user,password,key):
        self.s.send(user)
        respon = self.s.recv(1024).decode()
        if respon == 'OK':
            night_secret = encrypt(key,key)
            self.s.send(night_secret)
            respon = self.s.recv(1024)
            print(respon)
            respon = decrypt(respon,key)
            print(respon)
            if respon == 'OK':
                passd = encrypt(password,key)
                self.s.send(passd)
                respon = self.s.recv(1024).decode()
                msg = decrypt(respon,key)
                self.send_button["state"] = NORMAL
                self.chatlable.insert(INSERT,"{}\n".format(msg))
                self.send_entry.bind("<Return>",self.commands)
                Thread(target = self.recvmsg,args = (key,)).start()
            else:
                msg= ("Server  is refusing the connection [-]")
                self.chatlable.insert(INSERT,"{}\n".format(msg)) 
        else:
            msg= ("Server  is refusing the connection  [-]")
            self.chatlable.insert(INSERT,"{}\n".format(msg))               
    def Account(self):
        user = (self.user_entry.get()).encode()
        password = self.password_entry.get()
        key = self.secret_entry.get()
        self.authentication(user,password,key)
    def commands(self,event=None):
        global UserHELP
        key = self.secret_entry.get()
        cmd = self.send_entry.get()
        self.send_entry.delete(0, 'end')
        if cmd =='--clear message':
            self.chatlable.delete(1.0,END)
        elif cmd == '--help':
            self.chatlable.insert(END,UserHELP+'\n')
        elif cmd == '--shutdown':
            self.s.close()
            self.master.destroy()
        elif cmd[:5] == "--PDM":# PDM isla@hi isla how is everying :D
            mesg=cmd[6:];who=mesg.find('@');user=mesg[:who];data= mesg[who+1:]
            message = (f'PrivateDM:{user}:{data}')
            mes =encrypt(message,key)
            self.s.send(mes)
        else:
            self.sendmsg(cmd)
root = Tk()
mygui = master(root)
root.mainloop()
