from threading import Thread
from time import sleep
from tkinter import *
from tkinter import ttk,messagebox
import socket
from Utils.AES import *
from Utils.nightSec import night_sec
import os
import shutil

new_connections = {}  
blocked_addresses = [] #( ip + thier port)
NightSecretCheck = {} # [user,secret]
PasswordCheck = {} #[user,password]
Offline = {}        #[user userid]
Online = {}         #[user,userid]
Me     = {}         #[user,thier conn]
sleeping = []       # user
AdminHELP ="""

ip                  : ip address default 127.0.0.1 
port                : use a specific port default is 3000
key(optional)       : key is used as way to encrypt data it's not used in this version but 
                      the default is secret
update              : shows the updates
new user            : create new user(require Username, password and secret)
                        admin can create only 5 users
admin cmd           : allows admin to send message or to pass commands to the server
stop/start          : start or stop the server
    __________________________________________________________________________
                                    CMD COMMANDS
    --------------------------------------------------------------------------
--help              : shows this message
--clear update      : clears the updates box
--clear message     : clears admin message box
--PDM               : send a private message to a specific person 
                        EXAMPLS:--PDM isla@hi isla how is everying :D
                               :--PDM stalin@trans rights :D
--refresh           : refresh the online list to see if a user was loged in or went ofline
--stop user         : force a user to sleep for 60s from sending messages [NOTE] you 
                       can't mute your self examples:--stop isla
                                                     --stop Capitalism
--shutdown          : it will kill the whole server and destroy the app

    --------------------------------------------------------------------------
                                    ENCRYPTION
                                    ----------
Anonybox uses the symmetric encription with AES -256 CBC PKCS 7
NOTE That this version does not use IV you can turn it on from
AES.py file also users should turn it on too
    --------------------------------------------------------------------------
"""
class mas:
    def __init__(self,window):
        self.max = []
        self.window = window
        self.window.geometry("800x600")
        self.window.configure(bg="cyan3")
        self.window.title('Anonybox')
        self.window.resizable(width=FALSE, height=FALSE)
        f1 = Frame(window)
        f1.pack()
        conn_label =Label(f1,bg="gray24",width=300,height=2)
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
        self.start_button= Button(text="start",command=self.Freezing)
        self.close_button= Button(text="STOP",command=self.shutdown)
        self.start_button.place(x=370,y=3)
        l = Label(f1,bg="gray23",width=300,height=19,borderwidth=2, relief="raised")
        l.pack()
        self.admin_cmd = Text(l,bg="black",width=99,height=17,fg="green")
        self.admin_cmd.insert(INSERT,'Use command --help to see how i work :D\n')
        self.admin_cmd.place(x=1,y=1)
        admin_scrollb = Scrollbar(self.admin_cmd,orient=VERTICAL, command=self.admin_cmd.yview)
        self.admin_cmd['yscrollcommand'] = admin_scrollb.set
        admin_scrollb.place(x=779,y=1,relheight=1, height=1)
        self.adminEntry = Entry(l,width=97,bg='green')
        self.adminEntry.insert(0,"--help")
        self.adminEntry.place(x=6,y=300)
        self.adminEntry.bind("<Return>",self.command)
        f = Label(f1,text = "",bg="gray23",width=300,height=400,borderwidth=2, relief="raised")
        f.pack()
        self.Nuser_button= Button(text="New User",command=self.Create_acc)
        self.Nuser_button.place(x=410,y=563)
        self.UserEntry = Entry(width=10)
        self.UserEntry.insert(0,"UserName")
        self.PassEntry = Entry(width=10)
        self.PassEntry.insert(0,"Password")
        self.NightEntry = Entry(width=10)
        self.NightEntry.insert(0,"Secret")
        self.UserEntry.place(x=510,y=566)
        self.PassEntry.place(x=600,y=566)
        self.NightEntry.place(x=690,y=566)
        self.userslable = Label(f,text="",bg="gray23",width=40,height=10)
        self.userslable.place(x=450,y=10)
        self.live_update = Text(f,bg="black",width=45,height=13,fg='red')
        self.live_update.place(x=1,y=1)
        update_scrollb = Scrollbar(f,orient=VERTICAL, command=self.live_update.yview)
        self.live_update['yscrollcommand'] = update_scrollb.set
        update_scrollb.place(x=370,y=1,relheight=1, height=1)
        self.one=Label(self.userslable,text="",bg="gray",width=20)
        self.two=Label(self.userslable,text="",bg="gray",width=20)
        self.three=Label(self.userslable,text="",bg="gray",width=20)
        self.four=Label(self.userslable,text="",bg="gray",width=20)
        self.five=Label(self.userslable,text="",bg="gray",width=20)
    def Create_acc(self):
        global NightSecretCheck
        global PasswordCheck
        global Offline
        if len(self.max) == 0:
            max = ["one","two","three","four","five"]
        else:
            max = self.max
        #self.two.pack_forget()
        name,password,night = self.UserEntry.get(),self.PassEntry.get(),self.NightEntry.get()
        userID = max[0]
        max.pop(0) 
        self.max = max
        mesg = ("New User [{}] was added".format(name))
        try:
            if userID == "one": 
                self.one.config(text="{}{} [OFFLINE]".format(name,userID))
                self.one.pack()
            elif userID == "two": 
                self.two.config(text="{}{} [OFFLINE]".format(name,userID))
                self.two.pack()
            elif userID == "three": 
                self.three.config(text="{}{} [OFFLINE]".format(name,userID))
                self.three.pack()
            elif userID == "four": 
                self.four.config(text="{}{} [OFFLINE]".format(name,userID))
                self.four.pack()
            elif userID == "five": 
                self.five.config(text="{}{} [OFFLINE]".format(name,userID))
                self.five.pack()
            Thread(target = self.updates,args = (mesg,)).start()
            if not name in Offline:
                Offline[name] =userID
            NightSecretCheck[name]=night
            PasswordCheck[name]=password
            try:
                if len(self.max) == 0 and len(max) ==0:
                    self.Nuser_button["state"] = DISABLED
            except:
                pass
        except:
            messagebox.showerror("Users","There was an Error while adding new user")
    def set_var(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        key = str(self.key_entry.get())
        self.start_button.place_forget()
        self.close_button.place(x=370,y=3)
        msg= ("Server started with {}:{} using {} As a Secret".format(ip,port,key))
        self.updates(msg)
        return ip,port
    def connection(self):
        global new_connections
        global blocked_addresses
        ip,port = self.set_var()
        try:
            self.s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((ip,int(port)))
            self.s.listen(5)
            while True:
                conn,addr = self.s.accept()
                address = (f'{addr[0]}:{addr[1]}')
                mesg = (f"InComing connection from {address}") #infrom the server of new incoming connection
                self.updates(mesg)
                #conn.settimeout(20)  #if user did not send anything in 30s, server will close the connection
                if not address in blocked_addresses:
                    new_connections[address] = conn
                    Thread(target = self.authentication,args = (conn,address,)).start()
                else:
                    self.updates((f"Incoming connection from {address} was blocked"))
                    conn.close()
        except:
            messagebox.showerror("Connection","there was an error while trying to make the connection")
            self.s.close()
    def updates(self,mesg):
        self.live_update.insert(INSERT,"{}\n".format(mesg))
    def authentication(self,conn,addr):#talk to client
        global NightSecretCheck
        global blocked_addresses
        global PasswordCheck
        global Online
        global Offline
        global Me
        conn.send(b'Hello Guest, The connection is not encrypted yet...\nYou only got one chance good luck:)')
        user = conn.recv(1024).decode() #recv the user
        if len(user) > 0:
                    if user in NightSecretCheck:
                        conn.send(b'OK')
                        try:
                            night_secret = conn.recv(1024).decode() # recv the night secret
                            check= night_sec(NightSecretCheck[user],night_secret)
                        except:
                            blocked_addresses.append(addr)
                            conn.close()
                            self.updates((f"{addr} has been added to the blocked list"))
                            check = 404
                        if check == 1:
                            Thread(target = self.updates,args = ((f'{user} is trying to login'),)).start()
                            msg = encrypt('OK',NightSecretCheck[user])
                            conn.send(msg)
                            secure_passd = conn.recv(1024)
                            passd = decrypt(secure_passd,NightSecretCheck[user])
                            passd = passd
                            if PasswordCheck[user] == passd: 
                                Thread(target = self.updates,args = ((f"{user} has logged in"),)).start()
                                #self.updates(f"{user} Has successfully logged in")
                                if user in Offline:
                                    userID = Offline[user]
                                    del Offline[user]
                                    Online[user] = userID #Update the user to be on the online dic
                                msg = ('Welcome {}'.format(user))
                                Online[user] = userID
                                self.online(userID,user)
                                mesg = encrypt(msg,NightSecretCheck[user])
                                print(mesg)
                                conn.send(mesg)
                                Me[user] = conn
                                try:
                                    self.ttc(conn,user,NightSecretCheck[user])
                                    del Online[user]
                                    Offline[users] = userID
                                    self.offline(userID,user)
                                except:
                                    print('exit')
                            else:
                                blocked_addresses.append(addr)
                                conn.close()
                                self.updates((f"{addr} has been added to the blocked list"))
                                print("Couldn't check the password also the ip was blocked")
                        elif check == 2:
                            blocked_addresses.append(addr)
                            conn.close()
                            self.updates((f"{addr} has been added to the blocked list"))
                        else:
                            messagebox.showerror("ACCOUNS",f"there was an error while trying decrypting or while encrypting {user}")
                    else:
                        self.updates(f"{addr} has been added to the blocked list") 
                        blocked_addresses.append(addr)
                        conn.close()
                        blocked_addresses.append(addr)
        else:
            mesh = (f"user was not vaild {addr} has been added to the blocked list")
            Thread(target = self.updates,args = (mesg,)).start()
            blocked_addresses.append(addr)# block user from entrying
            conn.close()
    def ttc(self,conn,user,key):
        global NightSecretCheck
        global Online
        global Me
        while True:
            try:
                stuff = conn.recv(1024)
                print('stuff',stuff)
                if not stuff:
                    print('from here 2')
                    conn.close()
                    break
                else:
                    Usermesg = decrypt(stuff,key)
                    print('yeoo user message',Usermesg)
                    if Usermesg.startswith("PrivateDM"):
                        towho,mesg= Usermesg[10:].split(':')
                        if towho != "admin":
                            if towho in Online:
                                TOsecret = NightSecretCheck[towho]
                                TOconn = Me[towho]
                                self.PrivateDM(mesg,TOsecret,TOconn,user,key,conn)
                            else:
                                mesg = encrypt('[404] PrivateDM',key)
                                conn.send(mesg)
                        else:
                            self.admin_cmd.insert(END,f'PEEP POOOOP A private message from{user}:<\n'+mesg+':>\n')
                    elif Usermesg == '404':
                        stuff = 'Server Ignored your message'
                        mesg = encrypt(stuff,key)
                        conn.send(mesg)
                    else:
                        self.Public(user,Usermesg,key)
            except:
                print('from here 1')
                conn.close()
                break
    def Public(self,user,mesg,key,admin=False):
        global NightSecretCheck
        global Online
        global Me
        global sleeping
        mesg = (f'{user}:{mesg}\n')
        self.admin_cmd.insert(END,mesg)
        if not user in sleeping:
            if len(Online) > 0:
                for users in list(Online):
                    print(f"who is online {users}")
                    try:
                        night = NightSecretCheck[users]
                        NewMesg = encrypt(mesg,night)
                        conn = Me[users]
                        conn.send(NewMesg)
                    except socket.timeout:
                        self.updates((f"{users} didn't recv a message\n"))
            else:
                if admin:
                    self.admin_cmd.insert(END,'no one online yet!\n')
                if not admin:
                    NewMesg=("no one online yet!")
                    NewMesg = encrypt(mesg,key)
                    conn = Me[user]
                    conn.send(NewMesg)
    def PrivateDM(self,TheSecretMesg,TOsecret,TOconn,user,key,conn):
        global NightSecretCheck
        global Online 
        TheSecretMesg = (f"PEEEEP POOOOOOOOOOP PRIVATE MESSAGE[{user}]:{TheSecretMesg}")
        try:
            data = encrypt(TheSecretMesg,TOsecret)
            TOconn.send(data)
            notiy= 'A privet message has been sent\n'
            self.admin_cmd.insert(INSERT,notiy)
            data = encrypt("Private message have been delivered",key)
            conn.send(data)
        except socket.timeout:
            print("there was an error while delivering a private message\n")
    def Freezing(self):
        '''this method keeps the gui on loop while waiting for other users to join without 
            freezing the gui waiting for them '''
        Thread(target=self.connection,).start()
    def refresh(self):
        global Online
        global Me
        global Offline
        global NightSecretCheck
        Copy_Online = Online  #dictionary changed size during iteration
        print(Online)
        while True:
            for users in list(Copy_Online):
                conn = Me[users]
                night = NightSecretCheck[users]
                userid = Copy_Online[users]
                print(night)
                mesg = encrypt('server asks if you still there',night)
                try:
                    print(mesg)
                    conn.send(mesg)
                    data = conn.recv(1024)
                    if data:
                        self.online(userid,users)
                except:
                    print('user went offline',users)
                    del Online[users]
                    Offline[users] = userid
                    self.offline(userid,users)
            Copy_Online = Online
            print(Online,'after')
            print("Updates after 5")
            sleep(5)
    def online(self,userID,name):
            if userID == 'one':
                self.one.config(text="{}{} [ONLINE]".format(name,userID),fg ='green')
            elif userID == "two": 
                self.two.config(text="{}{} [ONLINE]".format(name,userID),fg ='green')
            elif userID == "three": 
                 self.two.config(text="{}{} [ONLINE]".format(name,userID),fg ='green')
            elif userID == "four": 
                 self.two.config(text="{}{} [ONLINE]".format(name,userID),fg ='green')
            elif userID == "five": 
                 self.two.config(text="{}{} [ONLINE]".format(name,userID),fg ='green')
    def offline(self,userID,name):
            print('inside offflinessefsdf',userID,name)
            if userID == 'one':
                self.one.config(text="{}{} [OFFLINE]".format(name,userID),fg ='black')
            elif userID == "two": 
                self.two.config(text="{}{} [OFFLINE]".format(name,userID),fg ='black')
            elif userID == "three": 
                 self.two.config(text="{}{} [OFFLINE]".format(name,userID),fg ='black')
            elif userID == "four": 
                 self.two.config(text="{}{} [OFFLINE]".format(name,userID),fg ='black')
            elif userID == "five": 
                 self.two.config(text="{}{} [OFFLINE]".format(name,userID),fg ='black')      
    def shutdown(self):
            self.s.close()
            self.window.destroy()
    def STFU(self,user):
        global sleeping
        sleeping.append(user)
        sleep(60)
        sleeping.remove(user)
        self.admin_cmd.insert(END,f'User {user} is out form sleeping for 60s'+'\n')
    def command(self,event=None): #admin commands
        global AdminHELP
        global NightSecretCheck
        global Online
        global Me
        global sleeping
        admin = True
        cmd = self.adminEntry.get()
        self.adminEntry.delete(0, 'end')
        key = None
        if cmd:
            if cmd[:5].startswith("--PDM"):
                mesg=cmd[6:];who=mesg.find('@');user=mesg[:who];data = 'admin:'+mesg[who+1:]
                conn= Me[user]
                TOsecret=NightSecretCheck[user]
                PDM = encrypt(data,TOsecret)
                conn.send(PDM)
                self.admin_cmd.insert(INSERT,'Privert message sent !')
            elif cmd[:2].startswith('--'):# PDM isla@hi isla how is everying :D
                if cmd == '--help':
                    self.admin_cmd.insert(END,AdminHELP+'\n')
                elif cmd == '--clear message':
                   self.admin_cmd.delete(1.0,END)
                elif cmd == '--clear update':
                    self.live_update.delete(1.0,END)
                elif cmd[:6] == '--stop': # --stop user
                    user = cmd[7:]
                    Thread(target = self.STFU,args = (user,)).start() 
                    self.admin_cmd.insert(END,f'User {user} is stopped for 60s'+'\n')
                elif cmd =='--shutdown server':
                    self.shutdown()
                elif cmd == '--refresh':
                    Thread(target=self.refresh,).start()
                else:
                    self.admin_cmd.insert(END,f"Server couldn't understand the command:{cmd}\n")
            else:
                self.Public('admin',cmd,key,admin)
         
root = Tk()
mygui = mas(root)
root.mainloop()
