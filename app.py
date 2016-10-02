from flask import Flask, render_template, request
import hashlib

#this is a constructor call
#creating an instance of a class
app = Flask(__name__) 
print app
#tells apache what to do when browser requests access from root of flask app
@app.route("/")
def helloWorld():
    print "\n\n\n\n"
    print "::DIAG:: this flsk obj"
    print app
    print "::DIAG:: this request obj"
    print request
    print "::DIAG:: request.headers"
    print request.headers
    print "::DIAG:: request.method"
    print request.method
    print "::DIAG:: request.args"
    print request.args 
    print "::DIAG:: request.form"
    print request.form
    return render_template("form.html")


@app.route("/auth", methods=["POST"])
def authenticate():
    username = "arthur"
    password = "read"
    
    passHash = hashlib.sha1()
    passHash.update(password)
    hashedPassword = passHash.hexdigest()
    
    inputtedUser = request.form['username']
    inputtedPass = request.form['password']

    inputHash = hashlib.sha1()
    inputHash.update(inputtedPass)
    hashedInput = inputHash.hexdigest()

    if username == inputtedUser and hashedPassword == hashedInput:
        my_title = "Success!"
        my_text = "Logged in!!! Yessss"
    else:
        my_title = "Failure!"
        my_text = "Authentification failed...... c'mon man....."
    return render_template("output.html", title = my_title, text = my_text)

if __name__ == "__main__":
    app.debug = True
    app.run()
