# coding: utf-8
import json
import jinja2
import os, glob
from pprint import pformat
import numpy as np
import pandas as pd

# Some nice colors from https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
colors = ((230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 190), (0, 128, 128), (230, 190, 255), (170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180))

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)

    environment = jinja2.Environment(undefined=jinja2.StrictUndefined,
        loader=jinja2.FileSystemLoader(path or './')) #It means jinja will take templates of environment from file in the introduced path
        
    def sublist(x, y):
        return [x[i] - y[i] if isinstance(x[i], float) else 'NaN' for i in range(len(x))]
    environment.filters['sublist'] = sublist
    def addlist(x, y):
        return [x[i] + y[i] if isinstance(x[i], float) else 'NaN' for i in range(len(x))]
    environment.filters['addlist'] = addlist

    return environment.get_template(filename).render(context)

def add_to_plots(plots, key, value, accuracy):
    for k, plot in plots.items():
        if k == key:
            plot['data'].append(value)
            if accuracy:
                plot['accuracy'].append(accuracy)
        else:
            plot['data'].append('NaN')
            if accuracy:
                plot['accuracy'].append(0)
    
def gen_plots(filename):
    data = None
    data = copy.deepcopy(pd.read_csv(filename)) 
    #with open (filename, 'r') as f:
     #   data = json.load(f)

    labels = []
    datasets = {'efficiency': {'label': ''},
                'runtime_component': {'label': ''},
               }

    info = []
    descriptions = set()
    for run in data:
        code, description, results, inputs = run
        # there can be empty results. One should filter calculations at
        # dump stage but this is not always possible.
        if results == {}:
            continue
        descriptions.add(description)

    for run in data:
        code, description, results, inputs = run
        # there can be empty results. One should filter calculations at
        # dump stage but this is not always possible.
        if results == {}:
            continue

        # maybe do some validation here? Anyway this can be done much better
        info = [pformat(x) for x in inputs]

        labels.append(code)
        for k in list(datasets.keys()):
            if k in results:
              # create data if it does not exist
                if not datasets[k].get('plots', False):
                    datasets[k]['plots'] = {}
                    for i, init_desc in enumerate(descriptions):
                        datasets[k]['plots'][init_desc]  = { 'data':[], 'accuracy': [], 'color': 'rgba({}, {}, {}, 1)'.format(*colors[i]) }

              # Add to reference or test
              add_to_plots(datasets[k]['plots'], description, results[k], results.get(k+'_accuracy', None))

                datasets[k]['min'] = min(datasets[k].get('min', 1e12), results[k])
                
                
                datasets[k]['max'] = max(datasets[k].get('max', -1e12),results[k])
            else:
                datasets.pop(k)
                continue

            if not datasets[k]['label']:
                try:
                    datasets[k]['label'] = k+' ('+results[k+'_units']+')'
                except KeyError:
                print("Warning, no units for "+k)

    # Enlarge axis by 5%
    for k in datasets.keys():
        variation = (datasets[k]['max'] - datasets[k]['min'])
        # chartjs bug
        variation = 1e-5 if variation < 1e-5 else variation*0.05

        datasets[k]['min'] = datasets[k]['min'] - variation
        datasets[k]['max'] = datasets[k]['max'] + variation

    _, basename = os.path.split(filename)
    name, _ = os.path.splitext(basename)
    with open (name+'.html', 'w') as f:
        f.write(render('plot.tmpl', {'title': name, 'labels': labels, 'datasets': datasets, 'info':info}))

def gen_index(flist):
    entries = {}
    for filename in flist:
        _, basename = os.path.split(filename)
        name, _ = os.path.splitext(basename)
        entries[name+'.html'] = name

    with open ('index.html', 'w') as f:
        f.write(render('index.tmpl', {'entries': entries}))

if __name__ == "__main__":
    flist = []

    for filename in glob.glob('./data/*.json'):
        gen_plots(filename)
        flist.append(filename)

    gen_index(flist)
