Here is a simple wesite interface with Python!

Flask and Jinja is needed to use this!

First we need a instance of Flask!
 python3 -m venv JINJAenv
 pip install flask
 pip freeze  --->to check which packages are installed and can be saved into another file to use later! or make the same virtual invironment
 touch hello.py
Second we need to introduce a route of website! with python decorator
Third we need to have index (what should be done in the webpage we want)
Forth the user can be introduced
Fifth export some invironments! otherwise for any changes we need to rerun the server! 

"export FLASK_ENV=development"
"export FLASK_APP=hello.py"

Then we can use html templates! in templates folder and make everything more general! or use already exist templates

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Jinja: another python library which comes up with flask, and it is powerful for python interfaces with web. (similar to jango !)

This library is very powerful for template makers!
can pass variables to templates and use ligical and python scripts with some modulations:
   {% logical sentences like if or for %}
   {% endif or endfor %}

 for variables {{ variables  }}

The required variable can pass to the system in render_template(   , variable=variable)
this is the power of Jinja 
