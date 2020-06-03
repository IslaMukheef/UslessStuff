
from .AES import *
def night_sec(secret,user_secret):#check if the user passed a valid secret
    try:
        hmm = decrypt(user_secret,secret).decode()
        if hmm == 0:
            return 2
        else:
            return 1
    except:
        return 3
        # 1 for valid : 2 for wrong: 3 error
