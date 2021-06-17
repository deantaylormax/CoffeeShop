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
# print(f' full df {df.head()}')
#getting list of employee
employee_lst = list(df["employee"].explode().unique())
emps_joined = ",".join(employee_lst)
emps_list = []
emps_list.append(emps_joined)
emps_split = emps_list[0].split(",")
employee_lst = list(set(emps_split))
try:
    employee_lst.remove('0')
except:
    pass
#create firm list
initial_lst = ['All']
# employee_lst = [x.replace(" ", "_") for x in employee_lst]
employee = initial_lst + employee_lst

# emp_options = [{'label':i.replace("_", " "), 'value':i} for i in employee]

dayWeekLabels = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dayWeekOptions = [{'label':i, 'value':i} for i in dayWeekLabels]

from app import app

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

dayWeekDropdown = dcc.Dropdown(id='dayWeek', multi=False, value=dayWeekOptions[0]['value'],options=dayWeekOptions, style={'width':'75%', 'color':'#000000'}, clearable=False)

# item_dropdown = dcc.Dropdown(id='item', multi=True, value=[], style={'width':'75%', 'color':'#000000'}, clearable=False)

# weather_lst = list(set(df['cond']))
# final_weath_lst = initial_lst + weather_lst

# print(f'final weat hlst {final_weath_lst}')

weather_radio = dbc.FormGroup(
    [
        dbc.Label("Weather Conditions"),
        dbc.RadioItems(
            options=[],
            value=[],
            id="rev-weather",
            inline=True
        ), html.Br(),
    ]
)


rev_graph_type_radio = dbc.FormGroup(
    [
        dbc.Label("Revenue Graph Type"),
        dbc.RadioItems(
            options= [
                {'label':'Total Revenue', 'value':'Total'},
                {'label':'Average Revenue', 'value':'Average'},
                {'label':'Highest Revenue Product', 'value':'Highest'},
                {'label':'Lowest Revenue Product', 'value':'Lowest'},
                # {'label':'Extra', 'value':'Extra'},
                    ],
            value='Total',
            id="rev-graph-type",
            inline=True
        ), html.Br(),
    ]
)




# stats_card = dbc.Card(
#     [
#         dbc.CardBody(
#             [
#                 html.P(f"General Statistics", style={'textAlign':'center'}),
#                 html.Hr(style={'color':'#ff8300'}),
#                 html.P(id='9-avg-age', children="", style={'textAlign':'right'}),
#                 html.P(id='9-avg-use', children="", style={'textAlign':'right'}),
#             ], 
#         ),
#     ],
#     style={"width": "15rem"}, className='float-box'
# )

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


rev_graph_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(id='rev-data-header', children="REVENUE DATA", className="card-title"),
            dcc.Graph(id='rev-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9',
    
),

my_image = 'assets/27_medium.png'

layout = dbc.Container([
                        dbc.Row([
                                dbc.Col(
                                    html.H1(id='rev-data-header', children='Revenue Data'))
                                 ], className="row justify-content-center"),
                                html.Br(), 
                                # html.Br(),
                        dbc.Row([
                                dbc.Col([
                                    dbc.Row(dbc.Label('Day of the Week')),
                                    dbc.Row(dayWeekDropdown),
                                    # dbc.Row(weather_radio),
                                        ], xs=12, sm=3, md=3, lg=2, xl=2, className='mt-2 ml-3'), 
                                # dbc.Col(stats_card, xs=12, sm=12, md=12, lg=3, xl=3),
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col(rev_graph_type_radio),
                                        # dbc.Col(html.Img(id='image-change', src='assets/27_medium.png')),
                                        # dbc.Col(weather_radio)
                                            ]),
                                    dbc.Row(rev_graph_card), 
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
                                # dbc.Row(rev_graph_card, className='ml-2'),
                                dbc.Row(),
                                    ]),
                                ]),
                        # dbc.Row(table_card),
                            ], fluid=True)

@app.callback(
    Output('rev-weather', 'options'),
    Output('rev-weather', 'value'),
    Input('rev-cat', 'value'))
def set_status_options(cat):
    if cat == 'All':
        data = df
    else:
        data = df[df['product'].str.startswith(cat)]    
    weather_lst = initial_lst + list(set(data['cond'].str.title()))
    # print(f'weather_lst {weather_lst}')
    value = weather_lst[0]  #makes the default value the first option in the status_lst
    return [{'label': i, 'value': i} for i in weather_lst], value

@app.callback(
    Output('rev-fig', 'figure'),
    Output('rev-data-header', 'children'),
    Input('dayWeek', 'value'),
    Input('rev-graph-type', 'value'))
def update_graph(dayWeek, graph_type):
    # print(f'graph type {graph_type}')
    month_lst = []
    if dayWeek == 'All':
        initial_df = df
    else:
        initial_df = df[df['dayname'] == dayWeek]
    if graph_type == 'Total':
        main_df = initial_df.groupby("date")["revenue"].sum().reset_index()
        main_df['revenue'] = main_df['revenue'].round(decimals=2)
        master_product_fig=px.bar(main_df,
                        x='date', y='revenue', text='revenue')
    elif graph_type == "Average":
        main_df = initial_df.groupby(["date"])["revenue"].mean().reset_index()
        main_df['revenue'] = main_df['revenue'].round(decimals=2)
        master_product_fig=px.bar(main_df,
                        x='date', y='revenue', text='revenue')
    elif graph_type == 'Lowest':
        prod_sales = initial_df.groupby("date")
        # prod_sales['revenue'] = prod_sales['revenue'].round(decimals=2)
        prod_sales = prod_sales[['date', 'product', 'revenue']]
        month_lst = []
        # prod_sales.get_group("2021-05-01")
        for date, date_df in prod_sales:
            initial_df = prod_sales.get_group(date)
            month_df = initial_df[initial_df['revenue'] == initial_df['revenue'].min()]
            month_df['revenue'] = month_df['revenue'].round(decimals=2)

            month_df.drop_duplicates(inplace=True)
            # month_df = month_df[month_df['revenue'] > 0]
            month_lst.append(month_df)
            low_prod_df = pd.concat(month_lst)
            master_product_fig=px.bar(low_prod_df, x='date', y='revenue', color="product", text='revenue')
    else:
        prod_sales = initial_df.groupby("date")
        # prod_sales['revenue'] = prod_sales['revenue'].round(decimals=2)
        prod_sales = prod_sales[['date', 'product', 'revenue']]
        month_lst = []
        # prod_sales.get_group("2021-05-01")
        for date, date_df in prod_sales:
            initial_df = prod_sales.get_group(date)
            month_df = initial_df[initial_df['revenue'] == initial_df['revenue'].max()]
            month_df.drop_duplicates(['date', 'revenue'], inplace=True)
            month_lst.append(month_df)
            high_prod_df = pd.concat(month_lst)
            master_product_fig=px.bar(high_prod_df, x='date', y='revenue', color="product", text='revenue')
    

    if dayWeek == 'All':
        rev_data_header = f'{graph_type} Revenue for the Entire Month'
    else:
        rev_data_header = f'{graph_type} Revenue for each {dayWeek} of the Month'




    master_product_fig.update_layout(showlegend=True)
   
    return master_product_fig, rev_data_header
    
if __name__ == '__main__':
    app.run_server(debug=True)