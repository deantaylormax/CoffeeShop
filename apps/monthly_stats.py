import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_core_components.RadioItems import RadioItems
import csv
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from datetime import datetime
import time
from datetime import date
now = pd.to_datetime('now')
#Dash Stuff
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table

""" DATA AND VARIABLES """

df = pd.read_csv("data/monthly_stats.csv")
initial_lst = ['All']
cat_labels = ['Coffee', 'Smoothies', 'Tea', 'Espresso', 'Cocktails', 'Cold', 'Bottles-Cans', 'Wine-Glasses', 'Wine-Bottles', 'Pizza', 'Breakfast', 'Good Eats']
cat_list = ['cof', 'smt', 'tea', 'esp', 'ckt', 'col', 'can', 'wng', 'wnb', 'piz', 'bkf', 'goo']
cat_dict = dict(zip(cat_labels, cat_list))
cat_options = [{'label':k, 'value':v} for k,v in cat_dict.items()]

month_cat_dropdown = dcc.Dropdown(id='monthly-cat', multi=False, value=cat_options[0]['value'],options=cat_options, style={'width':'75%', 'color':'#000000'}, clearable=False)
month_item_dropdown = dcc.Dropdown(id='monthly-item', multi=False, value=[], style={'width':'75%', 'color':'#000000'}, clearable=False)

from app import app

month_graph_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("MONTHLY DATA", className="card-title"),
            dcc.Graph(id='month-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9',
    
),

layout = dbc.Container([
                        dbc.Row([
                                dbc.Col(
                                    html.H1('Monthly Comparison'))
                                 ], className="row justify-content-center"),
                                html.Br(), 
                                # html.Br(),
                        dbc.Row([
                                dbc.Col([
                                    dbc.Row(month_cat_dropdown),
                                    dbc.Row(month_item_dropdown),
                                    # dbc.Row(weather_radio),
                                        ], xs=12, sm=3, md=3, lg=2, xl=2, className='mt-2 ml-3'), 
                                # dbc.Col(stats_card, xs=12, sm=12, md=12, lg=3, xl=3),
                                dbc.Col([
                                    dbc.Row([
                                        # dbc.Col(rev_graph_type_radio),
                                        # dbc.Col(html.Img(id='image-change', src='assets/27_medium.png')),
                                        # dbc.Col(weather_radio)
                                            ]),
                                    dbc.Row(month_graph_card), 
                                        ], xs=12, sm=8, md=8, lg=9, xl=9),
                                        # ], className='mt-2 col-lg-3'),
                                ]),
                        dbc.Row([
                            dbc.Col([
                                # dbc.Row(years_of_use_card), 
                                # dbc.Row(duration_of_use_card), 
                                # dbc.Row(age_card),
                                    ], xs=12, sm=12, md=12, lg=3, xl=3, className='mt-2 ml-2'), 
                            dbc.Col([
                                # dbc.Row(formulation_check, className='ml-5'), 
                                # dbc.Row(formulation_dose, className='ml-5'), 
                                # dbc.Row(delivery, className='ml-5'), 
                                # dbc.Row(emp_graph_card, className='ml-2'),
                                dbc.Row(),
                                    ]),
                                ]),
                        # dbc.Row(table_card),
                            ], fluid=True)

@app.callback(
    Output("monthly-item", 'options'),
    Output("monthly-item", 'value'),
    Input('monthly-cat', 'value')) 
    # Input('weather', 'value'))
def set_form_list_options(cat):
    # print(f' cat = {cat}')
    main_df = df[df['product'].str.startswith(cat)]
    item_lst = sorted(list(set(main_df['product'])))
    value = item_lst[0] #makes the default value the first option in the status_lst
    # print(f'value = {value}')
    return [{'label': i, 'value': i} for i in item_lst], value

@app.callback(
    Output('month-fig', 'figure'),
    Input('monthly-item', 'value'))
def update_graph(item):
    graph_data = df[df['product'] == item]
    monthly_stats=px.line(graph_data,
                        x='month', y='revenue')
    monthly_stats.update_layout(showlegend=False)
   
    return monthly_stats

if __name__ == '__main__':
    app.run_server(debug=True)