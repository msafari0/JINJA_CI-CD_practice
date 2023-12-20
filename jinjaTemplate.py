from jinja2 import Environment, FileSystemLoader

MAX_SCORE=100
TEST_NAME= "Python Test"

STUDENTS=[{"name":"Will","score":100},
	  {"name":"Tom","score":85},
	  {"name":"Bob","score":95},
	  {"name":"Dan","score":64},
	  {"name":"Ros","score":70}]

env = Environment(loader=FileSystemLoader("templates/"))
template = env.get_template("good.txt")

    	
if __name__ == "__main__":
    for student in STUDENTS:
        name = student["name"]
        filename = f"output/message_{name.lower()}.txt"
        content = template.render(student, 
    		max_score=MAX_SCORE,
    		test_name=TEST_NAME)
        with open(filename, mode="w", encoding="utf-8") as output:
            output.write(content)
            print("... wrote", filename)

