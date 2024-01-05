
import jinja2
import os
import csv
import pandas as pd
import json
from DF_maker import dataframes_maker


def render_index(tpl_path, context):
    path, filename = os.path.split(tpl_path)

    environment = jinja2.Environment(undefined=jinja2.StrictUndefined,
        loader=jinja2.FileSystemLoader(path or '.')) #It means jinja will take templates of environment from file in the introduced path

    return environment.get_template(filename).render(context)


def render_template(template_path, output_path, context, file_path=None, column_names=None):
    # Load the template environment
    template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
    template_env = jinja2.Environment(loader=template_loader, autoescape=True)
    
    def load_csv_data(file_path):
        return pd.read_csv(file_path).to_dict(orient='list')
    template_env.filters['load_csv_data'] = load_csv_data
    
    # Function to modify the CSV data
    def modify_csv_data(file_path, column_names):
        # Read CSV into a DataFrame
        df = pd.read_csv(file_path)

        df['component1'] = df[column_names[file_path]['component1']]
        df['component2'] = df[column_names[file_path]['component2']]
        # You can perform other modifications as needed

        # Convert the DataFrame to a dictionary
        modified_data = df.to_dict(orient='list')

        return modified_data

# Register the function as a Jinja filter
    template_env.filters['modify_csv_data'] = modify_csv_data
    # Load the template
    template = template_env.get_template(os.path.basename(template_path))
    
    # Include the file_path in the context
    context['file_path'] = file_path
    context['column_names'] = column_names
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
    # Specify the filenames and associated column names
    dataframes_list = [
  #  {'filename': '/home/mandanas/1-CINECA-projects/benchmark/benchmark_10it/bench_7.2dev_gpua_iter/000000/result/result.dat', 'column_name': 'electrons', 'efficiency':'electrons', 'x_axis':'Nodes', 'time_unit':'second'},
 #   {'filename': '/home/mandanas/1-CINECA-projects/benchmark/benchmark_10it/bench_7.2dev_nogpua_iter/000000/result/result.dat', 'column_name': 'electrons', 'efficiency':'electrons', 'x_axis':'Nodes','time_unit':'second'},
    {'filename': 'results.dat', 'column_name': 'sth_kernel', 'efficiency':'sth_kernel', 'x_axis':'Nodes', 'time_unit':'second'}
    ]
    dataframes = dataframes_maker(dataframes_list)

    data_file_path = [#"./df_1.txt", "./df_2.txt",
     "./df_3.txt"]
    
    # Define the output path for the rendered HTML
    output_path = [#"./output_chart1.html", "./output_chart2.html", 
    "./output_chart3.html"]

    # Define the column names for each file
    column_names = {
        #"./df_1.txt": {'component1': 'electrons', 'component2': 'other components (df_1)'},
        #"./df_2.txt": {'component1': 'electrons', 'component2': 'other components (df_2)'},
        "./df_3.txt": {'component1': 'sth_kernel', 'component2': 'other components (df_3)'},
    }

    # Create the context to be used in the template
    context = {
        'page_title': page_title,
        'output_path': output_path,
    }
    # Render the template and save the output HTML
    filenames = []
    for file_path, output_file in list(zip(data_file_path, output_path)):
        render_template("chart_modify.tmpl", output_file, context, file_path=file_path, column_names = column_names)
        print(file_path)
        filenames.append(output_file)

    gen_index(filenames)

    
    print(f"Template has been rendered and saved to {output_path}")
#it works!
