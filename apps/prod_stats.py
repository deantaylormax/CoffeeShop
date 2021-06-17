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

df = pd.read_csv("data/final_data.csv")
initial_lst = ['All']
cat_labels = ['Coffee', 'Smoothies', 'Tea', 'Espresso', 'Cocktails', 'Cold', 'Bottles-Cans', 'Wine-Glasses', 'Wine-Bottles', 'Pizza', 'Breakfast', 'Good Eats']
cat_list = ['cof', 'smt', 'tea', 'esp', 'ckt', 'col', 'can', 'wng', 'wnb', 'piz', 'bkf', 'goo']
cat_dict = dict(zip(cat_labels, cat_list))
cat_options = [{'label':k, 'value':v} for k,v in cat_dict.items()]

from app import app

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

cat_dropdown = dcc.Dropdown(id='cat', multi=False, value=cat_options[0]['value'],options=cat_options, style={'width':'75%', 'color':'#000000'}, clearable=False)

item_dropdown = dcc.Dropdown(id='item', multi=True, value=[], style={'width':'75%', 'color':'#000000'}, clearable=False)

weather_radio = dbc.FormGroup(
    [
        dbc.Label("Weather"),
        dbc.RadioItems(
            options=[],
            value=[],
            id="weather",
            inline=True
        ), html.Br(),
    ]
)

graph_type_radio = dbc.FormGroup(
    [
        dbc.Label("Graph Type"),
        dbc.RadioItems(
            options= [
                # {'label':'Bar', 'value':'Bar'},
                # {'label':'Line', 'value':'Line'},
                # {'label':'Bar Group', 'value':'Bar Group'},
                # {'label':'Extra', 'value':'Extra'},
                    ],
            value='Bar',
            id="graph-type",
            inline=True
        ), html.Br(),
    ]
)

stats_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P(id='stats-header', children = f"Daily Revenue", style={'textAlign':'center'}),
                html.Hr(style={'color':'#ff8300'}),
                html.P(id='data-max', children="", style={'textAlign':'center'}),
                html.P(id='data-mean', children="", style={'textAlign':'center'}),
                html.P(id='data-min', children="", style={'textAlign':'center'}),
            ], 
        ),
    ],
    style={"width": "15rem"}, className='float-box mr-2'
)

# dataset_stats = dbc.Card(
#     [
#         dbc.CardBody(
#             [
#                 html.P(f"Dataset Statistics", style={'textAlign':'center'}),
#                 html.Hr(style={'color':'#ff8300'}),
#                 html.P(id='9-dataset-avg-age', children="", style={'textAlign':'right'}),
#                 html.P(id='9-dataset-avg-dur', children="", style={'textAlign':'right'}),
#             ], 
#         ),
#     ],
#     style={"width": "15rem"}, className='float-box'
# )


graph_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(id='prod-header', children="PRODUCT DATA", className="card-title"),
            
            html.P(id='graph-sub', children=""
            ),
            dcc.Graph(id='bar-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9',
    
), 

my_image = 'assets/27_medium.png'

layout = dbc.Container([
                        dbc.Row([
                                dbc.Col(
                                    html.H1('Product Statistics'))
                                 ], className="row justify-content-center"),
                                html.Br(), 
                                # html.Br(),
                        dbc.Row([
                                dbc.Col([
                                    dbc.Row(cat_dropdown),
                                    dbc.Row(item_dropdown),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    dbc.Row(stats_card),
                                        ], xs=12, sm=3, md=3, lg=2, xl=2, className='mt-2 ml-3'), 
                                # dbc.Col(stats_card, xs=12, sm=12, md=12, lg=3, xl=3),
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col(graph_type_radio, xs=2, sm=2, md=2, lg=2, xl=2),
                                        dbc.Col(html.Img(src=my_image, id='weather-image'),xs=2, sm=2, md=2, lg=2, xl=2, className='mb-2'),
                                        dbc.Col(weather_radio),
                                            ]),
                                    dbc.Row(graph_card), 
                                        ], xs=12, sm=8, md=8, lg=8, xl=8, className='ml-4'),
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
    Output('weather', 'options'),
    Output('weather', 'value'),
    Input('cat', 'value'))
def set_status_options(cat):
    # print(f'cat value is {cat}')
    if cat == 'All':
        data = df
    else:
        data = df[df['product'].str.startswith(cat)]    
    weather_lst = initial_lst + list(set(data['cond'].str.title()))
    #print(f'weather_lst {weather_lst}')
    value = weather_lst[0]  #makes the default value the first option in the status_lst
    return [{'label': i, 'value': i} for i in weather_lst], value

# Formulation options dictated by inputs from retailer, status, 
@app.callback(
    Output("item", 'options'),
    Output("item", 'value'),
    Input('cat', 'value')) 
    # Input('weather', 'value'))
def set_form_list_options(cat):
    # print(f' cat = {cat}')
    main_df = df[df['product'].str.startswith(cat)]
    item_lst = sorted(list(set(main_df['product'])))
    value = item_lst[0] #makes the default value the first option in the status_lst
    # print(f'value = {value}')
    return [{'label': i, 'value': i} for i in item_lst], value

#this only shows barmode graph option if more than one item is displayed
@app.callback(
    Output("graph-type", "options"),
    Input("item", "value"))
def set_graph_type_options(item):
    if isinstance(item, str):
        check_item = [item]
    else:
        check_item = item
    if len(check_item) > 1:
        return [{'label':'Bar', 'value':'Bar'},
                {'label':'Line', 'value':'Line'},
                {'label':'Bar Group', 'value':'Bar Group'}]
    else:
        return [{'label':'Bar', 'value':'Bar'},
                {'label':'Line', 'value':'Line'}]

@app.callback(
    Output('bar-fig', 'figure'),
    Output('data-max', 'children'),
    Output('data-min', 'children'),
    Output('data-mean', 'children'),
    Output('prod-header', 'children'),
    # Output('weather-image', 'src'),
    Input('weather', 'value'),
    Input("item", 'value'),
    Input('graph-type', 'value'))
def update_graph(weather, items, graph_type):
    if weather == 'All':
        weather_image = my_image
    elif weather == 'Sunny':
        weather_image = 'assets/day.svg'
    elif weather == 'Rainy':
        weather_image = 'assets/rainy-1.svg'
    else:
        weather_image = 'assets/cloudy-day-1.svg'
    if isinstance(items, str):
        check_item = [items]
    else:
        check_item = items
    # print(f'check_item = {check_item}')
    if weather == 'All':
        main_df = df[df['product'].isin(check_item)]
    else:
        main_df = df[(df['product'].isin(check_item)) & (df['cond'] == weather.lower())]
    
    final_data = main_df.groupby(['date', 'product'])['revenue'].sum().reset_index()
    final_data['revenue'] = final_data['revenue'].round(decimals=2)

    #create the max, min, mean stats for the card next to the graph
    tot_max = round(final_data.revenue.max(), 2)
    data_max = f'Highest: ${tot_max}'
    tot_min = round(final_data.revenue.min(), 2)
    data_min = f'Lowest: ${tot_min}'
    tot_mean = round(final_data.revenue.mean(), 2)
    data_mean = f'Average: ${tot_mean}'

    if graph_type == 'Bar':
        master_product_fig=px.bar(final_data,
                        x='date', y='revenue', color="product", text='revenue')
    elif graph_type == 'Line':
        master_product_fig=px.line(final_data,
                        x='date', y='revenue', color="product")
    else: 
        master_product_fig=px.bar(final_data,
                        x='date', y='revenue', color="product", text='revenue', barmode='group')

    master_product_fig.update_layout(showlegend=True)

    if weather == 'All':
        prod_header = f'Daily Revenue for {items}'
    else:
        prod_header = f'Daily Revenue for {items} on {weather} days'
   
    return master_product_fig, data_max, data_min, data_mean, prod_header

if __name__ == '__main__':
    app.run_server(debug=True)