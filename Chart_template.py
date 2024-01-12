import jinja2
import os
import csv
import pandas as pd
import json
#from DF_maker import dataframes_maker
import sys
import argparse
import copy

def render_index(tpl_path, context):
    path, filename = os.path.split(tpl_path)

    environment = jinja2.Environment(undefined=jinja2.StrictUndefined,
    loader=jinja2.FileSystemLoader(path or '.')) #It means jinja will take templates of environment from file in the introduced path
    # Include url_for_.... in the context
    context['url_for_index'] = 'index.html'
    context['url_for_qe'] = 'qe.html'
    context['url_for_yambo'] = 'yambo.html'
    
    return environment.get_template(filename).render(context)

def render_qe(tpl_path, context):
    path, filename = os.path.split(tpl_path)

    environment = jinja2.Environment(undefined=jinja2.StrictUndefined,
    loader=jinja2.FileSystemLoader(path or '.')) #
    # Include url_for_... in the context
    context['url_for_index'] = 'index.html'
    context['url_for_qe'] = 'qe.html'
    context['url_for_yambo'] = 'yambo.html'

    return environment.get_template(filename).render(context)

def render_yambo(tpl_path, context):
    path, filename = os.path.split(tpl_path)

    environment = jinja2.Environment(undefined=jinja2.StrictUndefined,
    loader=jinja2.FileSystemLoader(path or '.')) #
    # Include url_for_index in the context
    context['url_for_index'] = 'index.html'
    context['url_for_qe'] = 'qe.html'
    context['url_for_yambo'] = 'yambo.html'
    
    return environment.get_template(filename).render(context)

def render_template(template_path, entry, entry_info, context):
    # Load the template environment
    template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
    template_env = jinja2.Environment(loader=template_loader, autoescape=True)


    def load_csv_data(entry):
        return entry.to_dict(orient='list')

    template_env.filters['load_csv_data'] = load_csv_data

    def to_list(series):
        return series.tolist()
    
    template_env.filters['to_list'] = to_list

    context['Lx_axis'] = entry_info['x_axis']
    context['Lcolumn_name'] = entry_info['column_name']
    context['Lcomponent'] = entry_info['component']

    # Load the template
    template = template_env.get_template(os.path.basename(template_path))

    # Include the dataframe and column_names in the context
    context['dataframe'] = entry
    context['x'] = entry[entry_info['x_axis']]
    context['column_name'] = entry[entry_info['column_name']]
    context['output_path'] = entry_info['output_path']
    if entry_info['component'] != 'empty':
        context['component'] = entry[entry_info['component']]
        context['other_comp'] = entry[entry_info['column_name']] - entry[entry_info['component']]

    # Render the template with the provided context
    output_html = template.render(context)

    # Write the rendered HTML to the output file
    with open(entry_info['output_path'], 'w') as output_file:
        output_file.write(output_html)


def gen_index():
    entries = {}
    with open ('index.html', 'w') as f:
        f.write(render_index('templates/index.tmpl', {'entries': entries}))
        
def gen_qe(flist_qe):
    entries = {}
    #n=0
    for filename in flist_qe:
        _, basename = os.path.split(filename)
        name, _ = os.path.splitext(basename)
        entries[name+'.html'] = name
        #entries[name+f'{n}'+'.html'] = name+f'{n}'
        #n+=1
    with open ('qe.html', 'w') as f:
        f.write(render_qe('templates/qe.tmpl', {'entries': entries}))
        
def gen_yambo(flist_yambo):
    entries = {}
    #n=0
    for filename in flist_yambo:
        _, basename = os.path.split(filename)
        name, _ = os.path.splitext(basename)
        entries[name+'.html'] = name
        #entries[name+f'{n}'+'.html'] = name+f'{n}'
        #n+=1
    with open ('yambo.html', 'w') as f:
        f.write(render_yambo('templates/yambo.tmpl', {'entries': entries}))

def count_files(directory):
    """In order to count the numbers of data_files and get the files in the provided directory"""
    try:
        # List all files in the directory
        files = os.listdir(directory)
        # Count the number of files
        file_count = len(files)
        return file_count, files
    except OSError:
        # Handle the case where the directory doesn't exist or is not accessible
        return -1, []

def code_recogniser(file_path, keywords):
    # Extract the folder names from the file path
    folders = file_path.split(os.path.sep)

    # Find the folder with any of the specified keywords
    found_keywords = [folder for folder in folders if any(keyword.lower() in folder.lower() for keyword in keywords)]

    if found_keywords:
        #print(f"Found keywords {found_keywords} in the folder path.")
        return found_keywords[0]
    else:
        print(f"No specified keywords found in the file path.")
        return None

def dataframes_maker(dataframes_list, **kwargs):
    loaded_dataframes = {}
    for num, df_dict in enumerate(dataframes_list, start=1):
        df_name = f'df_{num}'
        dataframe = pd.read_csv(df_dict['filename'])
        code_name= code_recogniser(df_dict['filename'], keywords_to_search)
        # Add new information to the dataframe dictionary
        dataframe_info = {
            'dataframe': dataframe,
            'x_axis': df_dict['x_axis'],
            'column_name': df_dict['column_name'],
            'time_unit': df_dict['time_unit'],
            'component': df_dict['component'],
            'code': code_recogniser(df_dict['filename'], keywords_to_search),
            'output_path': kwargs.get('output_path', f'./output_chart{num}_{code_name}.html'),
            #'column_names': {df_dict['column_name']: ' '},  # Adjust as needed
        }
        
        loaded_dataframes[df_name] = copy.deepcopy(dataframe_info)

        # Add more items if needed
       # loaded_dataframes[df_name]['new_item'] = 'some_value'

    return loaded_dataframes


if __name__ == "__main__":
    # Define the data for filling in the template
    page_title = "Benchmarking results"
    print('Welcome Message:')
    print('\t Flask code for visualizing benchmark results of the MAX project.')
    print('\tArguments: file_names or directores, x_axis, column_name, time_unit, component(any_column or empty)')
    print('\tAuthor: Mandana Safari \n')
    if len(sys.argv) < 2:
        print('Inserting all the parameters is mandetory (x_axis,column_name,time_unit,component)')
        print('USAGE with directories: python Chart_template.py --directories ./yambo=Nodes,walltime,second,electrons ./qe=Nodes,walltime,second,sth_kernel ...')
        print('USAGE with files: python Chart_templategen.py --files ./yambo/result0.dat=Nodes,walltime,second,sth_kernel ./yambo/result1.dat=Nodes,walltime,second,electrons ...')
        print('More information with: python Chart_template.py --help')
    
    # Modify the argument parsing logic
    parser = argparse.ArgumentParser(description='Flask code for visualizing benchmark results of the MAX project.')
    parser.add_argument('--files', nargs='+', type=str, help='List of file specifications with associated x_axis, column_name, time_unit, and component (use equal sign to separate file path and arguments)')
    parser.add_argument('--directories', '-dirs', nargs='+', type=str, help='List of directories specifications with associated x_axis, column_name, time_unit, and component (use equal sign to separate directory and arguments)')

    args = parser.parse_args()

    dataframes_list = []

    keywords_to_search = ['yambo', 'qe', 'othercode']

    if args.directories:
        for dir_spec in args.directories:
            dir_info = {}
            dir_parts = dir_spec.split('=')
            dir_info['directory'] = dir_parts[0]

            if len(dir_parts) > 1:
                properties = dir_parts[1].split(',')
                dir_info['x_axis'] = properties[0] or 'Nodes'
                dir_info['column_name'] = properties[1] or 'walltime'
                dir_info['time_unit'] = properties[2] or 'second'
                dir_info['component'] = properties[3] or 'empty'

            # Extract code from the folder structure
            code = None

            code = code_recogniser(dir_info['directory'], keywords_to_search)

            dir_info['code'] = code
                
            #dataframes_list.append(dir_info)


            file_count, files = count_files(dir_info['directory'])
            if file_count == -1:
                print(f"Error: Unable to access or find the directory {dir_info['directory']}.")
            else:
                print(f"The number of files in the directory {dir_info['directory']} is: {file_count}")
                for file_path in files:
                    print(f"Processing file: {file_path}")
                    x_axis = dir_info['x_axis'] or 'Nodes'
                    column_name = dir_info['column_name'] or 'walltime'
                    time_unit = dir_info['time_unit'] or 'second'
                    component = dir_info['component'] or 'empty'

                    # Extract code from the folder structure
                    code = code_recogniser(dir_info['directory'], keywords_to_search)
                    dataframes_list.append({'filename': os.path.join(dir_info['directory'], file_path), 'x_axis': x_axis, 'column_name': column_name, 'time_unit': time_unit, 'component': component, 'code': code})

    elif args.files:
        for file_spec in args.files:
            file_info = {}
            file_parts = file_spec.split('=')
            file_info['filename'] = file_parts[0]

            if len(file_parts) > 1:
                properties = file_parts[1].split(',')
                file_info['x_axis'] = properties[0] or 'Nodes'
                file_info['column_name'] = properties[1] or 'walltime'
                file_info['time_unit'] = properties[2] or 'second'
                file_info['component'] = properties[3] or 'empty'

            # Extract code from the folder structure
            code = None

            code = code_recogniser(file_info['filename'], keywords_to_search)

            file_info['code'] = code
                
            dataframes_list.append(file_info)
    else:
        print("Please provide either --directories or --files as arguments.")

    print(dataframes_list)

    loaded_dataframes = dataframes_maker(dataframes_list)

    # Create the context to be used in the template
    context = {
        'page_title': page_title,
    }
    # Render the template and save the output HTML
    filenames_qe = []
    filenames_yambo = []
    # Accessing the dataframes and associated information
    for df_name, df_info in loaded_dataframes.items():
        dataframe = df_info['dataframe']
        x_axis = df_info['x_axis']
        column_name = df_info['column_name']
        time_unit = df_info['time_unit']
        component = df_info['component']
        code = df_info['code']
        output_path = df_info['output_path']

        #print(f"Processing dataframe: {df_name}")
        #print(f"X-axis: {x_axis}, Column Name: {column_name}, Time Unit: {time_unit}, Component: {component}, Code: {code}")
        #print(dataframe)
        #render_template("templates/chart_modify.tmpl", output_path, context, dataframe=dataframe, column_name = column_name)
        render_template("templates/chart_modify.tmpl", dataframe, df_info, context)
        if code=='qe':
            filenames_qe.append(output_path)
        if code=='yambo':
            filenames_yambo.append(output_path)

    gen_index()
    gen_qe(filenames_qe)
    gen_yambo(filenames_yambo)
    
    print(f"Template has been rendered and saved to {filenames_yambo} and {filenames_qe}")
#it works!
    
    
