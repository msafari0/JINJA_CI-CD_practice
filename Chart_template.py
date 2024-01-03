
import jinja2
import os
import csv
import pandas as pd
from flask import Flask, render_template

def render_index(tpl_path, context):
    path, filename = os.path.split(tpl_path)

    environment = jinja2.Environment(undefined=jinja2.StrictUndefined,
        loader=jinja2.FileSystemLoader(path or '.')) #It means jinja will take templates of environment from file in the introduced path

    return environment.get_template(filename).render(context)


def render_template(template_path, output_path, context):
    # Load the template environment
    template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
    template_env = jinja2.Environment(loader=template_loader, autoescape=True)
    
    def load_csv_data(file_path):
        return pd.read_csv(file_path).to_dict(orient='list')
    template_env.filters['load_csv_data'] = load_csv_data
    # Load the template
    template = template_env.get_template(os.path.basename(template_path))
    
    
    # Render the template with the provided context
    output_html = template.render(context)

    # Write the rendered HTML to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(output_html)

def gen_index(flist):
    entries = {}
    #n=0
    for filename in flist:
        _, basename = os.path.split(filename)
        name, _ = os.path.splitext(basename)
        entries[name+'.html'] = name
        #entries[name+f'{n}'+'.html'] = name+f'{n}'
        #n+=1
    with open ('index.html', 'w') as f:
        f.write(render_index('index.tmpl', {'entries': entries}))

if __name__ == "__main__":
    # Define the data for filling in the template
    page_title = "Chart with Data from File"
    data_file_path = "./results.dat"
    
    datasets = [
        {'label': 'phqscf', 'name': 'phqscf', 'index': 3, 'backgroundColor': 'rgba(255, 0, 0, 0.7)'},
        {'label': 'dynmat0', 'name': 'dynmat0', 'index': 4, 'backgroundColor': 'rgba(0, 255, 0, 0.7)'},
        {'label': 'sth_kernel', 'name': 'sth_kernel', 'index': 5, 'backgroundColor': 'rgba(0, 0, 255, 0.7)'},
        {'label': 'h_psi', 'name': 'h_psi', 'index': 6, 'backgroundColor': 'rgba(255, 165, 0, 0.7)'},
    ]

    # Define the output path for the rendered HTML
    output_path = "./output_chart.html"

    # Create the context to be used in the template
    context = {
        'page_title': page_title,
        'data_file_path': data_file_path,
        'datasets': datasets,
    }

    # Render the template and save the output HTML
    #render_template("chart.tmpl", output_path, context)
    filenames = []
    filenames.append(output_path)
    #print(filenames)
    flist = []
    for filename in list(filenames):
        render_template("chart.tmpl", output_path, context)
        filenames.append(output_path)
        flist.append(filename)

    gen_index(flist)
    
    print(f"Template has been rendered and saved to {output_path}")




