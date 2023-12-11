from flask import Flask, render_template
#The modules needed to add the field of data in the webpage with submit botton
####################################
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
####################################
#create a Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "My secret key which is supposed to be hidden"

####################################
#Ingridiantes for creating a field and submit!       1.Create a Form Class 
class NameForm(FlaskForm):
    name = StringField("What is your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")
#More about fields and different types of it: https://flask-wtf.readthedocs.io/en/1.2.x/
#                           and https://wtforms.readthedocs.io/en/3.1.x/fields/#basic-fields
####################################

#create a route decorator
@app.route('/')

#def index():
    #return "<h1>Hello world!</h1>"
#We can use filters to extra control:
#upper
#lower
#capitalize
#trim
#strptags
#more filters on JINJA webpage

def index():
    first_name = "John"
    stuff = "This is <strong>Bold</strong> Text"
    favorite_pizza = ['Margerita','cheese','pineapple',41]
    return render_template('index.html', first_name=first_name, 
                           stuff=stuff,
                           favorite_pizza=favorite_pizza)

#localhost:5000/user/John or any name! 
@app.route('/user/<name>')
def user(name):
    #return "<h1>Hello {}!!!</h1>".format(name) 
    return render_template('user.html', name=name)

#Create Costum Error pages
#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
    
########################################
##Ingridiantes for creating a field and submit! 2.make a name.html   3.Create a Name page (route and function)
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    #validate form
    if form.validate_on_submit():
    	name = form.name.data
    	form.name.data = ''
    	
    return render_template('name.html',
    	name = name,
    	form = form)
 #then you should go to the navbar and make a link for new page ...   	
#########################################
