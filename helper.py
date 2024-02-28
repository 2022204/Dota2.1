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
    new_password = ""
    for i in range(len(password)):
        if password[i].isupper():
            new_password += mapped[i].upper()
        else:
            new_password += mapped[i]

        
    return new_password
            


if __name__ == "__main__":
    main()
