##############################################
# Program Name: BibleShare
# File Name: routes.py
# Purpose of File: The main driver file
# providing logic to the website
#
# Author: Jessie Ray
##############################################

from flask import Flask, render_template, url_for, session, request, redirect
import json
import random

######################################
# initial variable setup
######################################

# loads the Bible from KJV.json into a dictionary
with open('static/js/KJV.json') as b:
    bible = json.load(b)
# loads users.json into a dictionary
with open('static/js/users.json') as u:
    users = json.load(u)

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = str(random.randrange(1000000))

########################################
# end of variable setup
#######################################

@app.route('/', methods = ['GET', 'POST'])
def index():
    #Controller function for the login page
    session.pop('user', None)

    return render_template('index.html')

@app.route('/checkLogin', methods = ['GET', 'POST'])
def checkLogin():
	#Checks the login information against what is stored
	#in users.json and takes the appropriate action
	#depending on what is given.

	#param: none
	#return: redirect to home or back to index

    # Variable to hold the error

    error = None

    if request.method == 'POST':
        for user in range(len(users)):
            if request.form['username'] == users[user]['username']:
                if request.form['password'] == users[user]['password']:
                    session['user'] = request.form['username']
                    return redirect(url_for('home'))
                else:
                    error = "Invalid login credentials. Please try again."
                    return render_template("index.html", error = error)
            else:
                error = "Invalid login credentials. Please try again."
                return render_template("index.html", error = error)
    return render_template('checkLogin.html')

@app.route('/signUp', methods = ['GET', 'POST'])
def signUp():
	#Controller function for the sign up page
	#param: none
	#return: the template for signUp.html

    return render_template('signUp.html')

@app.route('/checkSignup', methods = ['GET', 'POST'])
def checkSignup():
	#Checks the information given against users.json and
	#a set of rules to determine if the sign up is valid,
	#then adds the information to users.json

	#param: none
	#return: either home.html or redirects back to signUp with an error.

    error = None
    if request.form['username'] != None:
        for user in range(len(users)):
            if request.form['username'] == users[user]['username']:
                error = "This user already exists. Please pick another username."
                return render_template('signUp.html', error =  error)
            # TODO: edit the JSON file to have the new information
    else:
        error = "Please enter a username"
        return render_template('signUp.html', error = error)
    return render_template('checkSignup.html')

def bibleSelection(B, CH, VS, VE):
    #This function uses the user inputs taken from forms to select the portion
    #of the Bible to display.

    #param: B (book), CHS (Chapters Start), CHE (Chapters End), VS (Verses Start), VE (Verses End)
    #return: result (an array containing the appropriate verses)

    result = []

    B = int(B)
    CH = int(CH)
    if VS != 'all':
        VS = int(VS)
    if VE != 'all':
        VE = int(VE)

    if VS == 'all':
        #for chap in range(len(bible[B]['chapters'])):
        for ver in range(len(bible[B]['chapters'][CH])):
            result.append(bible[B]['chapters'][CH][ver])

    #TODO MAKE THIS WORK!! (selecting a range of verses to display)
    else:
        rng = VE - VS
        for ver in range(len(bible[B]['chapters'][VS + rng])):
            result.append(bible[B]['chapters'][CH][ver])
    return result


@app.route('/home', methods = ['GET', 'POST'])
def home():
    #Controller function for the home page
    
    #checks to see if the user exists before it renders the page
    if "user" in session:
        if request.method == 'POST':
            B = request.form['bookSelect']
            CH = request.form['chapter']
            VS = request.form['versesStart']
            VE = request.form['versesEnd']
            desiredContent = bibleSelection(B, CH, VS, VE)
            return render_template('home.html', bible = bible, desiredContent = desiredContent)
        else:
            return render_template('home.html', bible = bible)
    else:
        error = "Please log in"
        return render_template("index.html", error = error)

if __name__ == '__main__':
    app.run(debug = True)
