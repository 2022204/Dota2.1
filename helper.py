def main():
    """This is helper function. It will assist the website for authentication etc"""
    print(hashed_password("abcABZ"))

def checkuser(users, username, password):
    for i in users:
        print(i["username"], type(i["username"]), i["password"], type(i["password"]), username, password)
        if i["username"] == username and hashed_password(i["password"]) == password:
            return None, i["value"]
    
    return "Invalid username/password", 0
def get_heroes(hero_list):
    heroes = []
    for item in hero_list:
        hero_dict = {
            'hero_id':item[0],
            'heroname': item[1],
            'description': item[3],
            'health': item[4],
            'armor': item[5],
            'attackspeed': item[6],
            'damage': item[7],
            'cost': item[2]
        }
        heroes.append(hero_dict)
    return heroes
def get_items(item_list):
    items = []
    for item in item_list:
        item_dict = {
            'item_id':item[0],
            'name': item[1],
            'description': item[3],
            'health': item[4],
            'armor': item[5],
            'attackspeed': item[6],
            'damage': item[7],
            'cost': item[2]
        }
        items.append(item_dict)
    return items

def get_history(history_list):
    duels = []
    for item in history_list:
        duel_dict = {
            'username': item[2],
            'opponent': item[3].capitalize(),  # Capitalize opponent's name
            'date': str(item[5]),  # Convert date to string
            'time': item[4].strftime('%H:%M'),  # Format time as 'HH:MM'
            'result': item[7],
            'exchange': item[6]
        }
        duels.append(duel_dict)
    return duels
def hashed_password(password):
    """This will encrypt user's password"""
    mapped = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
    alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    new_password = ""
    for i in password:
        if i.isalpha():
            if i.isupper():
                index = alphabets.index(i.lower())
                new_password += mapped[index].upper()
            elif i.lower():
                index = alphabets.index(i)
                new_password += mapped[index]
        
        else:
            new_password += i

    return new_password
            


if __name__ == "__main__":
    main()
