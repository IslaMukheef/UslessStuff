## Anonybox - AES-256 Encrypted Mailbox

###  Python 3:

 #### Requirements 
 ~~~~
 pycrypto,socket,sys,shutil,os 
 ~~~~
> sudo pip3 install pycryptodome

### Running:
For server side:
> sudo python3 server.py


For client side:
> sudo python3 client.py

### Encryption info:

*AES-256 CBC PKCS#7
                                    ENCRYPTION
                                    ----------
Anonybox uses the [symmetric](https://en.wikipedia.org/wiki/Symmetric-key_algorithm) encription with AES -256 CBC PKCS 7
NOTE That this version does not use IV you can turn it on from
AES.py file also users should turn it on too
   
### HOW TO USE

For server side:
 ~~~~
> ip                  : ip address default 127.0.0.1 
 ~~~~
 ~~~~
> port                : use a specific port default is 3000
 ~~~~
 ~~~~
> key(optional)       : key is used as way to encrypt data it's not used in this version but 
                        the default is secret
 ~~~~
 ~~~~
> update              : shows the updates
 ~~~~
 ~~~~
> new user            : create new user(require Username, password and secret)
                        admin can create only 5 users
 ~~~~
 ~~~~
> admin cmd           : allows admin to send message or to pass commands to the server
 ~~~~
 ~~~~
> stop/start          : start or stop the server
  ~~~~
  ~~~~
                                     CMD COMMANDS
    --------------------------------------------------------------------------
--help              : shows the help message
--clear update      : clears the updates box
--clear message     : clears admin message box
--PDM               : send a private message to a specific person 
                        EXAMPLS:--PDM isla@hi isla how is everying :D
                               :--PDM stalin@trans rights :D
                      [NOTE] if wrong user or wronge spelling was passed server will send
                      the message to the public
--refresh           : refresh the online list to see if a user was loged in or went ofline
--stop user         : force a user to sleep for 60s from sending messages [NOTE] you 
                       can't mute your self examples:--stop isla
                                                     --stop Capitalism
--shutdown          : it will kill the whole server and destroy the app
 ~~~~
 ~~~~
 For client side:
 ~~~~
 ~~~~
> ip                  : ip address default 127.0.0.1 
 ~~~~
 ~~~~
> port                : use a specific port default is 3000
 ~~~~
 ~~~~
> key(require)       : key is used as way to encrypt data it's not used in this version but 
                        the default is secret
 ~~~~
 ~~~~
> UserName            : set this user name to login
 ~~~~
 ~~~~
> new user            : create new user(require Username, password and secret)
                        admin can create only 5 users
 ~~~~
 ~~~~
> Password            : use this password to login
 ~~~~
 ~~~~
 > Secret              : use this secret to encrypt my data while 
                        i'm talking to the server
 ~~~~
 ~~~~
> stop/start          : start or stop the server
 
                                     CMD COMMANDS
    --------------------------------------------------------------------------
--help              : shows the help message
--PDM               : send a private message to a specific person 
                        [NOTE] normally admin will not see the message
                        but he/she can change that so assume they do 
                        EXAMPLS:--PDM isla@hi isla how is everying :D
                               :--PDM admin@i hate everyone :D
--clear message     : clears message box
--shutdown          : it will kill the whole server and destroy the app
 ~~~~

   
