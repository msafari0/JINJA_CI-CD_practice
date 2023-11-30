from flask import Flask, render_template

#create a Flask instance
app = Flask(__name__)

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
