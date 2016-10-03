from flask import Flask, render_template, request
import hashlib

app = Flask(__name__) 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html", title = "Log in", text = "Log in, if you please.")

@app.route("/signup")
def signup():
    return render_template("signup.html", title = "Account Signup", text = "Create an account")

@app.route("/auth", methods=["POST"])
def authenticate():
    dictOfUsers = getDictOfUsers()
    user = request.form['username']
    passwd = request.form['password']
    if not user in dictOfUsers.keys():
        my_title = "Please register"
        my_text = "Username not recognized. Please go back and try again, or register a new account."
    else:
        if hashPW(passwd) == dictOfUsers[user]:
            my_title = "Success!"
            my_text = "Logged in!!! Yessss"
        else:
            my_title = "Failure!"
            my_text = "Authentification failed. Incorrect password. Please try again."
            
    return render_template("output.html", title = my_title, text = my_text)

@app.route("/register", methods=["POST"])
def register():
    dictOfUsers = getDictOfUsers()
    user = request.form['username']
    pass1 = request.form['password1']
    pass2 = request.form['password2']
    if (pass1 != pass2):
        my_title = "Registration Failure"
        my_text = "Passwords do not match. Please try again."
        my_template = "signup.html"
    else:
        if user in dictOfUsers.keys():
            my_title = "Registration Failure"
            my_text = "Sorry, username is taken! Please enter a different username."
            my_template = "signup.html"
        else:
            dictOfUsers[user] = hashPW(pass1)
            outputToUserCSV(dictOfUsers)
            my_title = "Registration Success!"
            my_text = "Account created! Please log in"
            my_template = "login.html"
    return render_template(my_template, title = my_title, text = my_text)

def getDictOfUsers():
    d = {}
    userFile = open("data/users.csv", "r")
    userList = userFile.readlines()
    for user in userList:
        userInfo = user.strip().split(",")
        username = userInfo[0]
        password = userInfo[1]
        d[username] = password
    return d

def outputToUserCSV(userDict):
    output = ""
    for user in userDict:
        output += user + "," + userDict[user] + "\n"
    output.strip()
    userFile = open("data/users.csv", "w")
    userFile.write(output)
    userFile.close()

def hashPW(pw):
    hashObj = hashlib.sha1()
    hashObj.update(pw)
    return hashObj.hexdigest()

if __name__ == "__main__":
    app.debug = True
    app.run()
