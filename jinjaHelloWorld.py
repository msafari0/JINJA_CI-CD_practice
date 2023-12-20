import jinja2

env = jinja2.Environment()
template = env.from_string('Hello {{ name }}!')

if __name__ == "__main__":
    results= template.render(name="World")
    print(results)

