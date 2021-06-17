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
#getting list of employees
employee_lst = list(df["employees"].explode().unique())
# emps_joined = ",".join(employees_lst)
# emps_list = []
# emps_list.append(emps_joined)
# emps_split = emps_list[0].split(",")
# employee_lst = list(set(emps_split))
# try:
#     employee_lst.remove('0')
# except:
#     pass
# #create firm list
initial_lst = ['All']
# employee_lst = [x.replace(" ", "_") for x in employee_lst]
employees = initial_lst + employee_lst

# print(f'employees {employees}')


# emp_options = [{'label':i.replace("_", " "), 'value':i} for i in employees]

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
            html.H5("REVENUE DATA", className="card-title"),
            dcc.Graph(id='rev-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9',
    
),

my_image = 'assets/27_medium.png'

layout = dbc.Container([
                        dbc.Row([
                                dbc.Col(
                                    html.H1('Revenue Data'))
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
    # Output('rev-image-change', 'src'),  
    # Output('graph-type', 'options'),  
    # Output('9-avg-use', 'children'),  
    # Output('9-years-use-header', 'children'),  
    # Output('9-dur-use-header', 'children'),  
    # Output('9-age-header', 'children'),
 
    # Input('cat', 'value'),
    # Input('rev-weather', 'value'),
    Input('dayWeek', 'value'),
    Input('rev-graph-type', 'value'))
    # Input('9-dur-slider', 'value'),
    # Input('9-age-slider', 'value'),
    # Input("9-dosage-check", 'value'),
    # Input("9-delivery-method", 'value'),
def update_graph(dayWeek, graph_type):
    # print(f'graph type {graph_type}')
    month_lst = []
    if dayWeek == 'All':
        initial_df = df
    else:
        initial_df = df[df['dayname'] == dayWeek]
    if graph_type == 'Total':
        main_df = initial_df.groupby("date")["revenue"].sum().reset_index()
        master_product_fig=px.bar(main_df,
                        x='date', y='revenue')
    elif graph_type == "Average":
        main_df = initial_df.groupby(["date"])["revenue"].mean().reset_index()
        master_product_fig=px.bar(main_df,
                        x='date', y='revenue')
    elif graph_type == 'Lowest':
        prod_sales = initial_df.groupby("date")
        prod_sales = prod_sales[['date', 'product', 'revenue']]
        month_lst = []
        # prod_sales.get_group("2021-05-01")
        for date, date_df in prod_sales:
            initial_df = prod_sales.get_group(date)
            month_df = initial_df[initial_df['revenue'] == initial_df['revenue'].min()]
            month_df.drop_duplicates(inplace=True)
            # month_df = month_df[month_df['revenue'] > 0]
            month_lst.append(month_df)
            low_prod_df = pd.concat(month_lst)
            master_product_fig=px.bar(low_prod_df, x='date', y='revenue', color="product")
    else:
        prod_sales = initial_df.groupby("date")
        prod_sales = prod_sales[['date', 'product', 'revenue']]
        month_lst = []
        # prod_sales.get_group("2021-05-01")
        for date, date_df in prod_sales:
            initial_df = prod_sales.get_group(date)
            month_df = initial_df[initial_df['revenue'] == initial_df['revenue'].max()]
            month_df.drop_duplicates(['date', 'revenue'], inplace=True)
            month_lst.append(month_df)
            high_prod_df = pd.concat(month_lst)
            master_product_fig=px.bar(high_prod_df, x='date', y='revenue', color="product")
    # print(f'main df head {main_df.head()}')
    # #setting the results with the use_years value
    # use_years_range = list(range(use_years[0], use_years[1] +1)) #create list of all values in the range to use to constrict the data
    # main_df = main_df[main_df.use_years_lst.apply(lambda x: set(x).intersection(use_years_range)).astype(bool)]
    # #duration used
    # final_df = main_df[(main_df['total_use_years'].between(duration[0], duration[1])) &
    #                     (main_df['age'].between(age[0], age[1])) & 
    #                     (main_df['formulation'].isin(formulation)) &
    #                     (main_df['dosage'].isin(dosage)) & 
    #                     (main_df['admin_method'].isin(delivery))
                        # ]    
    
    # final_df.drop_duplicates(subset=['SubjectId', 'formulation'], inplace=True) #to avoid double counting of subject IDs
    # final_data = main_df.groupby(['date', 'product'])['revenue'].sum().reset_inde
    # print(f'final data = {final_data.head()}')
    # final_data = final_data.rename(columns={'SubjectId':'Total'})
    # final_data = final_data[final_data['Total'] >0]
    # """ CONTENT FOR ALL THE TEXT FIELDS """
    # master_status_number = final_df.SubjectId.nunique()
    # if status == 'All':
    #     master_status_text = f'All {master_status_number} Clients' 
    # else:
    #     master_status_text = f'{master_status_number} {status} Clients'

    #average age stats
    # if selected_firm == 'All':
    #     master_firm = final_df
    # else:
    #     master_firm = final_df[final_df['Firm'] == selected_firm]
    # master_avg_age_retailer = round(master_firm['age'].mean(), 1)
    # master_avg_age_retailer_text = f'Average Age:  {master_avg_age_retailer}'
    # # #average duration text
    # master_avg_dur = round(master_firm['total_use_years'].mean(),1)
    # master_avg_dur_text = f'Average Years of Use:  {master_avg_dur}'
    # #Use years text
    # master_years_use_header = f"Years Used {use_years[0]} to {use_years[1]}"
    # #duration header text
    # master_dur_use_header = f'Duration Used {duration[0]} to {duration[1]} years'

    # # #age header text
    # master_age_header = f'Clients  {age[0]} to {age[1]} years old'
    # master_product_fig=px.bar(main_df,
    #                     x='date', y='revenue')


    master_product_fig.update_layout(showlegend=True)
   
    return master_product_fig
    
if __name__ == '__main__':
    app.run_server(debug=True)