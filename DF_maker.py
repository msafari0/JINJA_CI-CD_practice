import numpy as np
import pandas as pd
import glob
import copy

def dataframes_maker(dataframes_list, plot='runtime_components', colormap=None, **kwargs):
    """
    Load dataframes from a list of dictionaries.

    Args:
        dataframes_list (list): A list of dictionaries where each dictionary contains
        a dataframe and its associated column name. Also plot the result! it needs to
        specify the type of Plot, the options are: 'runtime_components' and efficiency. user can
        specify the desired colormap! or default one in the function.

    Returns:
        dict: A dictionary where keys are dataframe names and values are the corresponding dataframes and plot.

    Usage:
        dataframes_maker(dataframes_list, plot='runtime_components/efficiency')
            Where: dataframes_list = [{'filename':'dat_file1', 'x_axis':'any_column', 'column_name':'any_column', 'time_unit':'second', 'component':'any_column'},
                                      {'filename':'dat_file2', 'x_axis':'any_column', 'column_name':'any_column', 'time_unit':'second', 'component':'any_column'},
                                      {'filename':'dat_file3', 'x_axis':'any_column', 'column_name':'any_column', 'time_unit':'second', 'component':'any_column'},...]

    Author:
        Mandana Safari
    """

    loaded_dataframes = {}
    n = 0

    for num, df_dict in enumerate(dataframes_list, start=1):
        #df_name = f'df_{num}'
        df_name = f'df_{num}_{df_dict["code"][0]}'  # Include code in df_name

        filename = df_dict['filename']

        filename = df_dict['filename']
        time_unit = df_dict['time_unit']

        loaded_dataframes[df_name] = copy.deepcopy(pd.read_csv(filename))

        column_name = df_dict['column_name']
        if column_name not in loaded_dataframes[df_name].columns:
            raise ValueError(f"Error: Column '{column_name}' does not exist in DataFrame '{df_name}'.")

        component = df_dict.get('component', 'empty')

        x_axis = df_dict['x_axis']
        if x_axis not in loaded_dataframes[df_name].columns:
            raise ValueError(f"Error: Column '{x_axis}' does not exist in DataFrame '{df_name}'.")

        loaded_dataframes[df_name]['empty'] = loaded_dataframes[df_name][x_axis] - loaded_dataframes[df_name][x_axis]
        if component != 'empty':
            loaded_dataframes[df_name][f'other components of {column_name}'] = loaded_dataframes[df_name][column_name] - loaded_dataframes[df_name][component]


        if time_unit == 'second':
            loaded_dataframes[df_name].iloc[:, 3:] /= 1
        elif time_unit == 'minute':
            loaded_dataframes[df_name].iloc[:, 3:] /= 60
        elif time_unit == 'hour':
            loaded_dataframes[df_name].iloc[:, 3:] /= 3600
        else:
            print(f"Error: Invalid time unit '{time_unit}' specified.")

    return loaded_dataframes


def dataframes_maker0(dataframes_list, **kwargs):
    """
    Load dataframes from a list of dictionaries.
    
    Args:
        dataframes_list (list): A list of dictionaries where each dictionary containsa dataframe and 
        its associated column name. Also plot the result! it needs to  spesify the type of Plot, the 
        options are: 'runtime_components' and efficiency. user can  spesify the desired colormap! or
        default one in the function.
    
    Returns:
        dict: A dictionary where keys are dataframe names and values are the corresponding dataframes and plot.
        
    Usage:
        dataframes_maker(dataframes_list, plot='runtime_components/efficiency')
            Where: dataframes_list = [{'filename':'dat_file1', 'x_axis':'any_column', 'column_name':'any_column', 'time_unit':'second', 'component':'any_column'},
                                      {'filename':'dat_file2', 'x_axis':'any_column', 'column_name':'any_column', 'time_unit':'second', 'component':'any_column'},
                                      {'filename':'dat_file3', 'x_axis':'any_column', 'column_name':'any_column', 'time_unit':'second', 'component':'any_column'},...]
        
    Author:
        Mandana Safari
    """
        
    loaded_dataframes = {}
    n=0
    for num, df_dict in enumerate(dataframes_list, start=1):

        df_name = f'df_{num}'
        dataframe = df_dict
        filename = df_dict['filename']
        time_unit = df_dict['time_unit']
        loaded_dataframes[df_name] = copy.deepcopy(pd.read_csv(filename))  
        
        column_name = df_dict['column_name']
        if column_name not in loaded_dataframes[df_name].columns:
            raise ValueError(f"Error: Column '{column_name}' does not exist in DataFrame '{df_name}'.")
        
        component = df_dict['component']
   
        #efficiency = df_dict['efficiency']
        #if efficiency not in loaded_dataframes[df_name].columns:
            #raise ValueError(f"Error: Column '{efficiency}' does not exist in DataFrame '{df_name}'.")
            
        x_axis = df_dict['x_axis']
        if x_axis not in loaded_dataframes[df_name].columns:
            raise ValueError(f"Error: Column '{x_axis}' does not exist in DataFrame '{df_name}'.")
        
        loaded_dataframes[df_name]['empty'] = loaded_dataframes[df_name][x_axis] - loaded_dataframes[df_name][x_axis]
        if df_dict['component'] != 'empty':
            loaded_dataframes[df_name][f'other components of {column_name}'] = loaded_dataframes[df_name][column_name] - loaded_dataframes[df_name][df_dict['component']]


                        
       # T1 = loaded_dataframes[df_name][efficiency][loaded_dataframes[df_name][x_axis]== loaded_dataframes[df_name][x_axis].min()].values[0]
       # Tp = loaded_dataframes[df_name][efficiency].values
        # Calculate speedup and efficiency
       # loaded_dataframes[df_name]['speedup'] = T1 / Tp
       # loaded_dataframes[df_name][f'efficiency of {efficiency}'] = (T1 / Tp) *( loaded_dataframes[df_name][x_axis].min()/loaded_dataframes[df_name][x_axis]) * 100


        if time_unit == 'second':
            loaded_dataframes[df_name].iloc[:, 3:] /= 1
        elif time_unit == 'minute':
            loaded_dataframes[df_name].iloc[:, 3:] /= 60
        elif time_unit == 'hour':
            loaded_dataframes[df_name].iloc[:, 3:] /= 3600
        else:
            print(f"Error: Invalid time unit '{time_unit}' specified.")
        

        
        # Save DataFrame to text file (tab-separated, change separator if needed)
        txt_filename = f'{df_name}.txt'
        loaded_dataframes[df_name].to_csv(txt_filename, sep=',', index=False)

            
    return loaded_dataframes



def render_template(template_path, output_path, context, dataframe=None, column_names=None):
    # Load the template environment
    template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
    template_env = jinja2.Environment(loader=template_loader, autoescape=True)
    
    def load_csv_data(dataframe):
        return pd.read_csv(dataframe).to_dict(orient='list')
    template_env.filters['load_csv_data'] = load_csv_data
    
    # Function to modify the CSV data
    def modify_csv_data(dataframe, column_names):
        # Read CSV into a DataFrame
        #df = pd.read_csv(file_path)

        df['column_name'] = df[column_names[dataframe]['column_name']]
        df['column_name'] = df[column_names[dataframe]['component']]
        # You can perform other modifications as needed

        # Convert the DataFrame to a dictionary
        modified_data = df.to_dict(orient='list')

        return modified_data

# Register the function as a Jinja filter
    template_env.filters['modify_csv_data'] = modify_csv_data
    # Load the template
    template = template_env.get_template(os.path.basename(template_path))
    
    # Include the file_path in the context
    context['dataframe'] = dataframe
    context['column_names'] = column_names
    context['output_path'] = output_path
    # Render the template with the provided context
    output_html = template.render(context)

    # Write the rendered HTML to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(output_html)