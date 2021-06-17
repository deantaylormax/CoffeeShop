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

df = pd.read_csv("data/final_data.csv")
initial_lst = ['All']
cat_labels = ['Coffee', 'Smoothies', 'Tea', 'Espresso', 'Cocktails', 'Cold', 'Bottles-Cans', 'Wine-Glasses', 'Wine-Bottles', 'Pizza', 'Breakfast', 'Good Eats']
cat_list = ['cof', 'smt', 'tea', 'esp', 'ckt', 'col', 'can', 'wng', 'wnb', 'piz', 'bkf', 'goo']
cat_dict = dict(zip(cat_labels, cat_list))
cat_options = [{'label':k, 'value':v} for k,v in cat_dict.items()]

emp_cat_dropdown = dcc.Dropdown(id='emp-cat', multi=False, value=cat_options[0]['value'],options=cat_options, style={'width':'75%', 'color':'#000000'}, clearable=False)
emp_item_dropdown = dcc.Dropdown(id='emp-item', multi=False, value=[], style={'width':'75%', 'color':'#000000'}, clearable=False)

df = df[df['employee'] != '0']
# employee revenue data
emp_rev_tot= df.groupby(["product", "employee"])["revenue"].sum().reset_index().sort_values(['product','revenue'], ascending=False)
# employee unit data
emp_unit_tot = df.groupby(["product", "employee"])["units_sold"].sum().reset_index().sort_values(['product','units_sold'], ascending=False)
emp_unit_tot = emp_unit_tot[emp_unit_tot['employee'] != '0']

from app import app

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

emp_graph_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(id='rev-header', children = "Total Revenue", className="card-title"),
            dcc.Graph(id='emp-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9',
    
),

emp_unit_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(id='unit-header', children="Units Sold", className="card-title"),
            dcc.Graph(id='emp-unit-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9',
    
),

layout = dbc.Container([
                        dbc.Row([
                                dbc.Col(
                                    html.H1('Employee Data'))
                                 ], className="row justify-content-center"),
                                html.Br(), 
                                # html.Br(),
                        dbc.Row([
                                dbc.Col([
                                    dbc.Row(emp_cat_dropdown, className='mt-2'),
                                    dbc.Row(emp_item_dropdown),
                                    # dbc.Row(weather_radio),
                                        ], xs=12, sm=3, md=3, lg=2, xl=2, className='mt-2 ml-3'), 
                                # dbc.Col(stats_card, xs=12, sm=12, md=12, lg=3, xl=3),
                                dbc.Col([
                                    dbc.Row([
                                        # dbc.Col(graph_type_radio),
                                        # dbc.Col(weather_radio)
                                        # dbc.Col(html.Img(id='weather-image', src='assets/27_medium.png')),
                                            ]),
                                    dbc.Row(emp_graph_card),
                                    dbc.Row(emp_unit_card, className='mt-2'), 
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
                                # dbc.Row(graph_card, className='ml-2'),
                                dbc.Row(),
                                    ]),
                                ]),
                        # dbc.Row(table_card),


                            ], fluid=True)

@app.callback(
    Output("emp-item", 'options'),
    Output("emp-item", 'value'),
    Input('emp-cat', 'value')) 
    # Input('weather', 'value'))
def set_form_list_options(cat):
    main_df = df[df['product'].str.startswith(cat)]
    item_lst = sorted(list(set(main_df['product'])))
    value = item_lst[0] #makes the default value the first option in the status_lst
    return [{'label': i, 'value': i} for i in item_lst], value

@app.callback(
    Output('emp-fig', 'figure'),
    Output('emp-unit-fig', 'figure'),
    Output('rev-header', 'children'),
    Output('unit-header', 'children'),
    Input('emp-item', 'value'))
def update_graph(item):
    graph_data = emp_rev_tot[emp_rev_tot['product'] == item]
    unit_data = emp_unit_tot[emp_unit_tot['product'] == item]
    unit_data['employee'] = unit_data['employee'].str.replace("_", " ")
    #round out the revenue figures
    graph_data['revenue'] = graph_data['revenue'].round(decimals=2)
    #remove the underscrore between employee's fname and lname
    graph_data['employee'] = graph_data['employee'].str.replace("_", " ")

    emp_prod_data=px.bar(graph_data,
                        x='employee', y='revenue', text='revenue')
    emp_prod_data.update_layout(showlegend=False)
    emp_rev_max = graph_data[graph_data['revenue'] == graph_data['revenue'].max()].iloc[0,1]

    emp_unit_data=px.bar(unit_data,
                        x='employee', y='units_sold', text='units_sold')
    emp_unit_data.update_layout(showlegend=False)
    emp_unit_max =unit_data[unit_data['units_sold'] == unit_data['units_sold'].max()].iloc[0,1]

    rev_header = f"{emp_rev_max} generated the most revenue selling {item.title()}"
    unit_header = f"{emp_unit_max} sold the most units of {item.title()}"

    return emp_prod_data, emp_unit_data, rev_header, unit_header
    
if __name__ == '__main__':
    app.run_server(debug=True) 