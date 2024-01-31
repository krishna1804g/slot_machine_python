import numpy as np
import random
import os, csv

MIN_BET = 10
MAX_BET= 100
MAX_LINES = 3

ROWS = 3
COLS = 3

spin_items = {
    "💕": 4,
    "💥": 9,
    "😜": 6,
    "🙃": 5
}

spin_value = {
    "❤️": 10,
    "💥": 5,
    "😎": 5,
    "🎶": 8
}


def write_player_data(name, balance):
    with open("ledger.csv", 'a') as file:
        writer = csv.DictWriter(file, fieldnames=["name","balance"])
        if os.stat("ledger.csv").st_size != 0:
            writer.writeheader
        writer.writerow({
            "name":name,
            "balance": balance
        })
        


def get_the_player():
    flag = 0
    name = input("Enter Your name: ")
    
    # check if name is there in the file
    if os.stat("ledger.csv").st_size != 0:
        with open("ledger.csv", 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["name"] == name:
                    flag = 1
                    player_balance = int(row["balance"])
                break
        if flag:
            print(f"Your current balance is {player_balance}")
            if player_balance < MIN_BET:
                print("You dont have enough balance, please add to continue")
                player_balance = deposite()
        else:
            print(f"Player not found. Creating new player with name {name}")
            player_balance = deposite()
            write_player_data(name, player_balance)
            
    else:
        write_player_data(name, player_balance)

    
    return player_balance, name

    
def deposite():
    while True:
        depo = input("Enter the total amount to deposite: rs ")
        if depo.isdigit():
            depo = int(depo)
            if depo > 100:
                break
            else:
                print("Enter amount greater than 100")
        else:
            print("Enter valid amount")

    return depo

def bet_amount():
    while True:
        bet = input("Enter the total amount to bet per line: rs ")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            else:
                print(f"Enter amount in range [{MIN_BET}-{MAX_BET}]")
        else:
            print("Enter valid amount")

    return bet


def lines_to_bet():
    while True:
        lines = input(f"Enter the number of lines 1-{MAX_LINES}: ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print(f"Not in range 1-{MAX_LINES}")
        else:
            print("Enter a valid value")

    return lines



def spin():
    spin_machine = []
    
    spin_item_list = []
    for key, value in spin_items.items():
        for _ in range(value):
            spin_item_list.append(key)
            
    temp_items = spin_item_list[:]
    
    for _ in range(ROWS):
        a = []
        for _ in range(COLS):
            item_chose = random.choice(temp_items)
            temp_items.remove(item_chose)
            a.append(item_chose)
        spin_machine.append(a)
        
    spin_machine = np.transpose(spin_machine)

    return spin_machine

def print_spin_wheels(spin_machine):
    for wheel in spin_machine:
        for i, item in enumerate(wheel):
            if len(wheel) - 1 != i:
                print(f"  {item}  ", end="|")
            else:
                print(f"  {item}  ", end="")
        print()


def check_winnings(lines, spinning_machine, bet):
    total_winnnings = 0
    
    for line in range(lines):
        if len(set(spinning_machine[line])) == 1:
            item = spinning_machine[line][0]
            total_winnnings += spin_value[item] * bet
            
    return total_winnnings
  
  
      
def play_game(balance):
    while True:
        lines = lines_to_bet()
        bet = bet_amount()
        if bet > balance:
            print(f"NOT enough balance, balance left: Rs {balance}")
            continue
        total_bet_amount = bet * lines
        break
    
    spin_machine = spin()
    print_spin_wheels(spin_machine)
    
    winnings = check_winnings(lines, spin_machine, bet)
    return winnings - total_bet_amount
    

def main():
    balance, player_name = get_the_player()
    
    while True:
        try:
            ans = input("Press enter to play, (q to quit)")
        except KeyboardInterrupt:
            return
        if ans == 'q':
            with open("ledger.csv", 'r+') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                data = list(reader)
                
                # find the entry eith specific name and update the balance
                for row in data:
                    if row["name"] == player_name:
                        if row["balance"] == balance:
                            break
                        row["balance"] = balance
                    break
                # move the file pointer to the beginning
                file.seek(0)
                
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)  
            break
        
        balance += play_game(balance)
        print(f"Current balance Rs {balance}")
        
    print(f"Balance left Rs {balance}")
    

if __name__ == "__main__":
    main()