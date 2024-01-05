import numpy as np
import pandas as pd
import glob
import copy


# Define a list of color tuples for each colormap
colors_list = [("#2EA6A6", "#F28F38"), ("#FF5733", "#33FF57"), ("#FF5733", "#3377FF")]


def dataframes_maker(dataframes_list, **kwargs):
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
            Where: dataframes_list = [{'filename':'dat_file1', 'column_name':'any_column', 'efficiency':'any_column', 'x_axis':'any_column', 'time_unit':'minute'},
                                      {'filename':'dat_file2', 'column_name':'any_column', 'efficiency':'any_column', 'x_axis':'any_column', 'time_unit':'minute'},
                                      {'filename':'dat_file3', 'column_name':'any_column', 'efficiency':'any_column', 'x_axis':'any_column', 'time_unit':'minute'}, ...]
        
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
            
        
        efficiency = df_dict['efficiency']
        if efficiency not in loaded_dataframes[df_name].columns:
            raise ValueError(f"Error: Column '{efficiency}' does not exist in DataFrame '{df_name}'.")
            
        x_axis = df_dict['x_axis']
        if x_axis not in loaded_dataframes[df_name].columns:
            raise ValueError(f"Error: Column '{x_axis}' does not exist in DataFrame '{df_name}'.")
            
     
        loaded_dataframes[df_name][f'other components ({df_name})'] = loaded_dataframes[df_name]['walltime'] - loaded_dataframes[df_name][column_name]
        loaded_dataframes[df_name][f'{column_name} of ({df_name})'] = loaded_dataframes[df_name][column_name]
        
                        
        T1 = loaded_dataframes[df_name][efficiency][loaded_dataframes[df_name][x_axis]== loaded_dataframes[df_name][x_axis].min()].values[0]
        Tp = loaded_dataframes[df_name][efficiency].values
        # Calculate speedup and efficiency
        loaded_dataframes[df_name]['speedup'] = T1 / Tp
        loaded_dataframes[df_name][f'efficiency of {efficiency}'] = (T1 / Tp) *( loaded_dataframes[df_name][x_axis].min()/loaded_dataframes[df_name][x_axis]) * 100


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



