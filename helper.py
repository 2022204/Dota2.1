def main():
    """This is helper function. It will assist the website for authentication etc"""
    print(hashed_password("abcABZ"))

def checkuser(users, username, password):
    for i in users:
        if i["username"] == username and i["password"] == password:
            return None
    
    return "Invalid username/password"

def hashed_password(password):
    """This will encrypt user's password"""
    mapped = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
    alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    new_password = ""
    for i in password:
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
