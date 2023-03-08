import os
import sys
import json
import time

ingame_user_name = ""
ingame_sequence = []
ingame_inventory = []
ingame_cases = []
ingame_health = 0

def SignIn():
    os.system('cls')
    user_name = input("Please enter your name: ")
    user_pass = input("Please enter your password: ")
    with open("player_status.json", "r") as read_file:
        data = json.load(read_file)
    for users in data:
        if( (users["user_name"]==user_name) & (users["user_pass"]==user_pass) ):
            global ingame_user_name
            ingame_user_name = user_name
            return 1
    return 0

def SignUp():
    os.system('cls')
    user_id = 0
    user_name = input("Please enter your name: ")
    user_pass = input("Please enter your password: ")
    with open("player_status.json", "r") as read_file:
        data = json.load(read_file or 'null')
    for users in data:
        user_id = users["user_id"]
        if(users["user_name"]==user_name):
            return 0
    global ingame_user_name
    user_id = user_id+1
    ingame_user_name = user_name
    data.append({
        "user_id":user_id,
        "user_name":user_name,
        "user_pass":user_pass,
        "inventory":[],
        "sequence":[],
        "health":100
    })
    with open("player_status.json", "w") as write_file:
        json.dump(data, write_file)
    return 1

def NewGame():
    global ingame_sequence
    ingame_sequence = [1]
    ChooseItems()
    if(ShowCase(ingame_cases[0])==0):
        print("Game Over\nPress any key to continue")
        with open("player_status.json", "r") as read_file:
            data = json.load(read_file)
        for user in data:
            if(user["user_name"]==ingame_user_name):
                user["inventory"] = ingame_inventory
                user["sequence"] = ingame_sequence
                user["health"] = ingame_health
        with open("player_status.json", "w") as write_file:
            json.dump(data, write_file)
        input()
    else:
        with open("player_status.json", "r") as read_file:
            data = json.load(read_file)
        for user in data:
            if(user["user_name"]==ingame_user_name):
                user["inventory"] = ingame_inventory
                user["sequence"] = ingame_sequence
                user["health"] = ingame_health
        with open("player_status.json", "w") as write_file:
            json.dump(data, write_file)
        

def ChooseItems():
    global ingame_inventory
    counter = 0
    while(counter<3):
        os.system("cls")
        print("Your current items: ",end='')
        for i in ingame_inventory:
            print(i+" , ",end='')
        print("\n")
        item = input("Choose Your Items\n1.emergency flare\n2.plier\n3.magic pills\n4.knife\n5.axe\n")
        while( (item!='1') & (item!='2') & (item!='3') & (item!='4') & (item!='5') ):
            item = input("Incorrect Input\nChoose Your Items\n1.emergency flare\n2.plier\n3.magic pills\n4.knife\n5.axe\n")
        match item:
            case '1':
                ingame_inventory.append("emergency flare")
            case '2':
                ingame_inventory.append("plier")
            case '3':
                ingame_inventory.append("magic pills")
            case '4':
                ingame_inventory.append("knife")
            case '5':
                ingame_inventory.append("axe")
        counter+=1

def ContinueGame():
    global ingame_health
    global ingame_sequence
    global ingame_inventory
    with open("player_status.json", "r") as read_file:
        data = json.load(read_file)
    for user in data:
        if(user["user_name"]==ingame_user_name):
            ingame_inventory = user["inventory"]
            ingame_sequence = user["sequence"]
            ingame_health = user["health"]
    print(ingame_health)
    time.sleep(20)
    if(ShowCase(ingame_cases[ingame_sequence[len(ingame_sequence)-1]-1])==0):
        print("Game Over\nPress any key to continue")
        with open("player_status.json", "r") as read_file:
            data = json.load(read_file)
        for user in data:
            if(user["user_name"]==ingame_user_name):
                user["inventory"] = ingame_inventory
                user["sequence"] = ingame_sequence
                user["health"] = ingame_health
        with open("player_status.json", "w") as write_file:
            json.dump(data, write_file)
        input()
    else:
        with open("player_status.json", "r") as read_file:
            data = json.load(read_file)
        for user in data:
            if(user["user_name"]==ingame_user_name):
                user["inventory"] = ingame_inventory
                user["sequence"] = ingame_sequence
                user["health"] = ingame_health
        with open("player_status.json", "w") as write_file:
            json.dump(data, write_file)

def ShowCase(case):
    global ingame_health
    global ingame_sequence
    global ingame_inventory
    os.system("cls")
    print(case["text"]+"\n")
    match case["health"][0]:
        case '+':
            ingame_health = ingame_health + int(case["health"][1:])
        case '-':
            ingame_health = ingame_health - int(case["health"][1:])
        case _:
            ingame_health = int(case["health"])
    print("Your Health: "+str(ingame_health)+"\n")
    if(ingame_health<=0):
        ingame_sequence = []
        ingame_health = 100
        ingame_inventory = []
        return 0
    print("Your items are\n")
    for i , item in enumerate(ingame_inventory):
        print(str(i)+". "+item+"")
    print("\n")
    for i , option in enumerate(case["options"]):
        print(str(i+1)+". "+option["text"]+"")
        print("required tools are ",end ='')
        for item in case["require_inventory"][i]:
            print(item + " , ")
        print("\n")
    
    print("Enter 0 to exit\n")
    for i , option in enumerate(case["options"]):
        print("Enter "+str(i+1)+" to choose option "+str(i+1)+"")
    next_case = input()
    flag = True
    while(flag):
        if(next_case=='0'):
            print("Out")
            flag = False
            os.system("cls")
            return 1
        for i , option in enumerate(case["options"]):
            if(next_case==str(i+1)):
                print("index: "+str(i)+"\n")
                
                flag = False
                ingame_sequence.append(option["next_card_id"])
                print(ingame_sequence)
                print(ingame_cases[option["next_card_id"]-1])
                # time.sleep(30)
                return ShowCase(ingame_cases[option["next_card_id"]-1])
                break    

while(True):
    os.system('cls')
    user_input=input('Press 1 for Sign Up\nPress 2 for Login\nPress 3 to Exit\n')
    while( (user_input!='1') & (user_input!='2') & (user_input!='3') ):
        os.system('cls')
        user_input=input('Wrong Input\nPress 1 for Sign Up\nPress 2 for Login\n')
    match user_input:
        case '1':
            if(SignUp()==0):
                print("Account name already used\n")
                continue
        case '2':
            if(SignIn()==0):
                print("Wrong Input\n")
                continue
        case '3':
            # print("hola")
            sys.exit()
    os.system('cls')
    while(True):
        print("Hello "+ingame_user_name+"\n")
        match user_input:
            case '1':
                user_input=input("Press 1 for New Game\n\nPress 3 to Exit\n")
                while( (user_input!='1') & (user_input!='3') ):
                    os.system('cls')
                    user_input=input("Wrong Input\nPress 1 for New Game\n\nPress 3 to Exit\n")
            case '2':
                with open("player_status.json", "r") as read_file:
                    data = json.load(read_file)
                for users in data:
                    if((users["user_name"]==ingame_user_name) & (len(users["sequence"])>0 )):
                        
                        ingame_sequence = users["sequence"]
                        ingame_inventory = users["inventory"]
                        user_input=input("Press 1 for New Game\nPress 2 to continue Game\nPress 3 to Exit\n")
                        while( (user_input!='1') & (user_input!='2') & (user_input!='3') ):
                            os.system('cls')
                            user_input=input('Wrong Input\nPress 1 for Sign Up\nPress 2 to continue Game\nPress 2 for Login\n')
                        break
                    elif((users["user_name"]==ingame_user_name) & (len(users["sequence"])<=0 )):
                        user_input=input("Press 1 for New Game\n\nPress 3 to Exit\n")
                        while( (user_input!='1') & (user_input!='3') ):
                            os.system('cls')
                            user_input=input("Wrong Input\nPress 1 for New Game\n\nPress 3 to Exit\n")
                        break
        os.system("cls")
        match user_input:
            case '1':
                with open("cases.json", "r") as read_file:
                    ingame_cases = json.load(read_file)
                NewGame()
            case '2':
                with open("cases.json", "r") as read_file:
                    ingame_cases = json.load(read_file)
                ContinueGame()
            case '3':
                sys.exit()
    
    

with open("cases.json", "r") as read_file:
    data = json.load(read_file)

for case in data:
    print(case["card_id"])