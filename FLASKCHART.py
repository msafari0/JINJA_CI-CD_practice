import jinja2
import os
import csv
import pandas as pd
from flask import Flask, render_template

# Assuming load_csv_data is the function you use to load CSV data
def load_csv_data(file_path):
    return pd.read_csv(file_path).to_dict(orient='list')

# Example Flask app setup
app = Flask(__name__)
app.jinja_env.filters['load_csv_data'] = load_csv_data

# Example route
@app.route('/')
def chart():
    data_file_path = '/home/mandanas/1-CINECA-projects/benchmark/benchmark_10it/bench_7.2dev_gpua_iter/000000/result/result.dat'
    page_title = 'Chart with Data from File'

    return render_template('chart3.html', page_title=page_title, data_file_path=data_file_path)

