import argparse
import subprocess
import os
parser = argparse.ArgumentParser()
parser.parse_args()

databases = {"bypass":None,"exploits":None,"shell":None} # files name
def database():# it will only return the numbers not the names
    available = {}
    for file in databases:
        path = f'modules/{file}/info.txt'
        if os.path.exists(path):
            lines = subprocess.Popen(['wc',f'{path}'],stdout=subprocess.PIPE) # geting file lines
            text = (lines.stdout.read()).split()
            line = text[0].decode()
            available[file]=line 
        else:
            print(f"couldn't locate the {file}:{path}") #if path doesn't exists print that
    return available
def main():
    print('\nchecking the database...\n')
    show_database=database()
    for vul in show_database:
        print(f"{vul}({show_database[vul]})")
    print('\n\nfor options use help\n')
    while True:
        cmd = input('?>')
        if cmd == 'help':
            print(help())
        elif cmd.startswith('show'):
            try:
                cmd = cmd.split()
                if len(cmd) >2:
                    cmd.remove('show')
                    new = ' '
                    new = new.join(cmd)
                    cmd = ['show',new]
                try:
                    update_database(cmd[1])
                    for vul in databases[cmd[1]]:
                        #print(f"\n{vul}\t\t:{databases[cmd[1][vul]]}\n")
                        print(f'\n{vul}\t\t:{databases[cmd[1]][vul]}\n')
                except:
                    print("[-] Couldn't update the database")
            except:
                print('please select something')
            
        elif cmd.startswith('search'):
            try:
                cmd = cmd.split()
                if len(cmd) >2:
                    cmd.remove('search')
                    new = ' '
                    new = new.join(cmd)
                    cmd = ['search',new]
                search_database(cmd[1])
            except:
                print('please use a word to search for')
            

            
def search_database(word):
    found= {}
    try:
        for available_module in databases:
            #if databases[available_module] ==None:
            try:
                update_database(available_module)
                #if cmd[1] in databases[available_module]:
                with open(f'modules/{available_module}/info.txt','r') as data:
                    for line in data:
                        if word in line:
                            name,description =line.split('<?>')
                            name = f'modules/{available_module}/{name}'
                            found[name]=description
            except:
                print("[-]couldn't look into the database")
        
    except:
        print("[-] couldn't finish the search")
    if not found == {}:
        for vul in found:
            print(f'{vul}\t\t:{found[vul]}')
    else:
        print('[-] no results')

def update_database(module):#geting module available vul
    if os.path.exists(f'modules/{module}') and module in databases:
            for file in os.listdir(f'modules/{module}'):
               # found=[] # list all the .py files that was found
               # if file.endswith('.py'):
               #    file = file.replace('.py','')
               #    found.append(file)
                with open(f'modules/{module}/info.txt','r') as data_info:
                    found = {}
                    for line in data_info:
                        try:
                            name,description = line.split('<?>') #<?> for splitting the name and the description
                        except:
                            print(f'[-]{line} has a bad description to fix it try this:\nexploit<?> a stupid description')
                        found[name]=description
                    databases.update({module:found})
    else:
        print(f"[-]couldn't find {module}")
    return

def help():
    return ('hello im help lmao')

main()
    