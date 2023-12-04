# Here is a simple wesite interface with Python!
[sourse of the course](https://www.youtube.com/@Codemycom)
## Flask and Jinja is needed to use this!

First we need a instance of Flask!<br/>
 `python3 -m venv JINJAenv`<br/>
 `pip install flask`<br/>
 `pip freeze`<br/>  ---> to check which packages are installed and can be saved into another file to use later! or make the same virtual invironment <br/>
 `touch hello.py`<br/>
 
Second we need to introduce a route of website! with python decorator
Third we need to have index (what should be done in the webpage we want)
Forth the user can be introduced
Fifth export some invironments! otherwise for any changes we need to rerun the server! 

`export FLASK_ENV=development`<br/>
`export FLASK_APP=hello.py`<br/>

Then we can use html templates! in templates folder and make everything more general! or use already exist templates.<br/>

## Jinja: another python library which comes up with flask, and it is powerful for python interfaces with web. (similar to jango !)

This library is very powerful for template makers!<br/>
can pass variables to templates and use ligical and python scripts with some modulations:<br/>
 ```
 {% logical sentences like if or for %}
   {% endif or endfor %}

 for variables {{ variables  }}
```
The required variable can pass to the system in render_template(   , variable=variable)<br/>
this is the power of Jinja <br/>
