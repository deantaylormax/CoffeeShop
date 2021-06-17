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
# df = pd.read_pickle("data/prod_data.pkl")

df = pd.read_feather("data/prod_data.ftr", columns=None).set_index(['SubjectId'])
try:
    df.drop(columns=['index'], inplace=True)
except:
    pass
df.reset_index(inplace=True)


# print(df.head())
# freq = pd.read_csv(r"U:\Projects\Zantac\Code\aggregate_reports\agg_rpt_dash_dfs\freq_data.csv")
#change the Year column to integer for graphing
df.Year = df.Year.astype('int')
df.sort_values(by=['Firm'], inplace=True)
# all_firms = ['All Firms']
firm_list = sorted(list(set(df['Firm'].unique())))
# firm_list.remove("0")
firm_options = [{'label':i, 'value':i} for i in firm_list]
#variables for Year slider
year_min = df['Year'].min()
year_max = df['Year'].max()
#variables for Age slider
age_min = 0
age_max = 110
#variables for status dropdown (i.e. All, Living, Deceased)
all_status = ['All']
other_status = list(set(df['deceased']))
status_lst = all_status + other_status
#variables for the status dropdown
status_options = [{'label':'All Clients', 'value':"Living"}, {'label':'Living', 'value':"living"}, {'label':'Deceased', 'value':"deceased"}]
living = df[df['deceased'] == 'Living']
deceased = df[df['deceased'] == 'Deceased']
#options for the radio buttons, hard coded in 
data_options = [{'label':'All Clients', 'value': 'All'}, {'label':'Living', 'value':'Living'}, {'label':'Deceased', 'value':'Deceased'}]
tot_use_min = 0
tot_use_max = 40

from app import app

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

""" Put all the various components here and then below, place them in the layout """

firm_dropdown = dcc.Dropdown(id='4-firm-dd', multi=False, value=firm_options[0]['value'] ,options=firm_options, style={'width':'100%', 'color':'#000000'}, clearable=False)

status_radio = dbc.FormGroup(
    [
        dbc.Label("Client Status"),
        dbc.RadioItems(
            options=[],
            value=[],
            id="4-status-dd",
            inline=True
        ), html.Br(),
            html.P(id='status-text', children="", style={'margin-left': '5px'})
    ]
)

stats_card = dbc.Card(
    [
        # dbc.CardHeader("General Statistics", style={'textAlign':'center'}),
        dbc.CardBody(
            [
                # html.H4("Card title", className="card-title"),
                html.P(f"General Statistics", style={'textAlign':'center'}),
                html.Hr(style={'color':'#ff8300'}),
                html.P(id='4-avg-age', children="", style={'textAlign':'right'}),
                html.P(id='4-avg-use', children="", style={'textAlign':'right'}),
            ], 
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "15rem"}, className='float-box'
)

dataset_stats = dbc.Card(
    [
        # dbc.CardHeader("General Statistics", style={'textAlign':'center'}),
        dbc.CardBody(
            [
                # html.H4("Card title", className="card-title"),
                html.P(f"Dataset Statistics", style={'textAlign':'center'}),
                html.Hr(style={'color':'#ff8300'}),
                html.P(id='4-dataset-avg-age', children="", style={'textAlign':'right'}),
                html.P(id='4-dataset-avg-dur', children="", style={'textAlign':'right'}),
            ], 
        ),
        # dbc.CardFooter("This is the footer"),
    ],
    style={"width": "15rem"}, className='float-box'
)



graph_card = dbc.Card(
                    dbc.CardBody(
                                [
                                    html.H5("PRODUCT DATA", className="card-title"),
                                    # html.P(
                                    #     "Explain what this graph is "
                                    # ),
                                    html.P(id='4-graph-sub', children=""
                                            ),
                                    #put the graph component here
                                    dcc.Graph(id='4-bar-fig', config={'displayModeBar':False}),
                                ]
                                ), className='float-box col-lg-11 mt-4, ml-4',
    
                    ), 

table_card = dbc.Card(
    dbc.CardBody(
        [
            # html.H5("Graph Example", className="card-title"),
            html.H5(id='4-table-sub', children="", style={'text-align': 'center'}
            ),
            #put the graph component here
            html.Div(id='4-data-table'),
        ]
    ), className='float-box col-lg-11 mt-5',
    
), 

""" page components in order top to bottom """

years_of_use_slider = dcc.RangeSlider(
        id='4-years-use-slider',
        min=0,
        max=10,
        step=1,
        value=[],
        marks={},
        # dots=True,
        tooltip = {'always_visible':False, 'placement':'bottom'}     
        )

years_of_use_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(id='4-years-use-header', children="", className="card-title", style={'text-align': 'center'}),
            # html.P(
            #     "This card also has some text content and not much else, but "
            #     "it is twice as wide as the first card."
            # ),
            years_of_use_slider,
        ]
    ), className='float-box col-lg-12 mt-7'
)

duration_of_use_slider = dcc.RangeSlider(
        id='4-dur-slider',
        min=0,
        max=40,
        step=1,
        value=[0,40],
        marks={i:{'label': str(i),'style': {'color':'#ffffff'}} for i in range(0, 41, 10)},
        # dots=True,
        tooltip = {'always_visible':False, 'placement':'bottom'}     
        )

duration_of_use_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(id='4-dur-use-header', children="", className="card-title", style={'text-align': 'center'}),
            # html.P(
            #     "Total Years of Use from  [date] to [date]"
            # ),
            duration_of_use_slider,
        ]
    ), className='float-box col-lg-12 mt-3'
)

age_slider = dcc.RangeSlider(
        id='4-age-slider',
        min=age_min,
        max=age_max,
        step=2,
        value=[],
        marks={},
        # dots=True,
        tooltip = {'always_visible':False, 'placement':'bottom'}
        )

age_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(id='4-age-header', children="", className="card-title", style={'text-align': 'center'}),
            # html.P(
            #     "Current Age"
            # ),
            age_slider,
        ]
    ), className='float-box col-lg-12 mt-3'
)

product_check = dbc.FormGroup(
    [
        dbc.Label("Product Type"),
        dbc.Checklist(
            options=[],
            value=[],
            id="4-product-check",inline=True, 
        )
    ]
)

""" Setup the layout here with simple row and column lines"""

layout = dbc.Container([
                        dbc.Row(html.H1('Plaintiff Product Data'), className = 'ml-2'),
                            html.Br(), 
                            html.Br(),
                        # dbc.Row(html.P('this is it')),
                        dbc.Row(
                            [dbc.Col(
                                [dbc.Row(firm_dropdown),
                                html.Br(), 
                                dbc.Row(status_radio)], className='mt-2 col-lg-3, ml-3'), 
                            dbc.Col(stats_card, className='mt-2'),
                            dbc.Col(dataset_stats, className='mt-2'),
                            # dbc.Col(html.P('Where is fourth column?')),
                            ]),
                        # dbc.Row(html.P('Row above the graph data')),
                        dbc.Row([
                            dbc.Col([
                                # dbc.Row(html.P('Row above the sliders')), 
                                dbc.Row(years_of_use_card), 
                                dbc.Row(duration_of_use_card), 
                                dbc.Row(age_card)], xs=12, sm=12, md=12, lg=4, xl=4, className='mt-9, ml-4'), 
                            dbc.Col([
                                # dbc.Row(html.P('First Row above the graph data')), 
                                dbc.Row(product_check,className='ml-5'), 
                                dbc.Row(graph_card, className='ml-4')
                                    ]),
                                ]),
                        dbc.Row([dbc.Col(table_card)
                                ]
                    )], fluid=True)

""" Callback Functions """
""" for the status dropdown """
@app.callback(
    Output('4-status-dd', 'options'),
    Output('4-status-dd', 'value'),
    Input('4-firm-dd', 'value'))
def set_status_options(selected_firm):
    firm_choice = df[df['Firm'] == selected_firm]
    initial_lst = ['All'] #to add an all option to the list
    other_lst = list(set(firm_choice['deceased']))
    if 'nan' in other_lst:
        other_lst.remove('nan')
    if len(other_lst) == 1: #if the dataset only has all deceased or all living clients
        status_lst = other_lst #the radio buttons will only show one option
    else:
        status_lst = initial_lst + other_lst #if there are living and deceased clients, then show three options, All, Living and Deceased
    value = status_lst[0]  #makes the default value the first option in the status_lst
    # print(type(status_lst))
    return [{'label': i, 'value': i} for i in status_lst], value


"""for the product checklist """
@app.callback(
    Output("4-product-check", 'options'),
    Output("4-product-check", 'value'),
    Input('4-firm-dd', 'value'))
def set_checklist_options(selected_firm):
    firm_choice = df[df['Firm'] == selected_firm]
    prod_lst = list(set(firm_choice['Product_Type']))
    # print(f'prod lst {prod_lst}')
    value = prod_lst  #makes the default value the first option in the status_lst
    # print(f'product value {value}')
    return [{'label': i, 'value': i} for i in prod_lst], value

# """ Setting the Use Years Slider """
@app.callback(
    Output('4-years-use-slider', 'value'), #sets starting value for the slider
    Output('4-years-use-slider', 'marks'), #sets the marks for the length of the slider
    Output('4-years-use-slider', 'min'), #sets the marks for the length of the slider
    Output('4-years-use-slider', 'max'), #sets the marks for the length of the slider
    # Output('year-header', 'children'),  
    Input('4-firm-dd', 'value'))
def set_year_options(selected_firm):
    firm_choice = df[df['Firm'] == selected_firm]
    # initial_lst = ['All']
    year_lst = list(set(firm_choice['Year']))
    min=year_lst[0]
    max=year_lst[-1]
    years_use_value = [min, max]
    # marks = {i:str(i) for i in range(year_lst[0], year_lst[-1]+1, 5)}
    years_use_marks = {i:{'label': str(i),'style': {'color':'#ffffff'}} for i in range(year_lst[0], year_lst[-1]+1, 10)}
    # year_header = f'Use during the years {min} - {max}'
    return years_use_value, years_use_marks, min, max

# """ Setting the client age slider  """
@app.callback(
    Output('4-age-slider', 'value'), #sets starting value for the slider
    Output('4-age-slider', 'marks'), #sets the marks for the length of the slider
    Output('4-age-slider', 'min'), #sets the marks for the length of the slider
    Output('4-age-slider', 'max'), #sets the marks for the length of the slider
    # Output('year-header', 'children'),  
    Input('4-firm-dd', 'value'))
def set_age_options(selected_firm):
    firm_choice = df[df['Firm'] == selected_firm]
    # initial_lst = ['All']
    # age_lst = list(set(firm_choice['age']))
    age_lst = sorted(firm_choice['age'].to_list())
    # print(f'age list in age slider callback is {age_lst}')
    age_min=age_lst[0]
    try:
        age_max=age_lst[-1]
    except:
        age_max=age_lst[0]
    age_value = [age_min, age_max]
    # print(f'age value in the age callback function {age_value}')
    # marks = {i:str(i) for i in range(year_lst[0], year_lst[-1]+1, 5)}
    age_marks = {i:{'label': str(i),'style': {'color':'#ffffff'}} for i in range(age_lst[0], age_lst[-1]+1, 10)}
    # year_header = f'Use during the years {min} - {max}'
    return age_value, age_marks, age_min, age_max

# """ Main callbacks """
@app.callback(
    Output('4-bar-fig', 'figure'),
    Output('4-avg-age', 'children'),  
    Output('4-avg-use', 'children'),  
    Output('status-text', 'children'),  
    Output('4-years-use-header', 'children'),  
    Output('4-dur-use-header', 'children'),  
    Output('4-age-header', 'children'),  
    Output('4-data-table', 'children'),
    Output('4-graph-sub', 'children'), 
    Output('4-table-sub', 'children'),
    Output('4-dataset-avg-age', 'children'),
    Output('4-dataset-avg-dur', 'children'),
    # Output('page-title', 'children'),

    Input('4-firm-dd', 'value'),
    Input('4-status-dd', 'value'),
    Input('4-years-use-slider', 'value'),
    Input('4-dur-slider', 'value'),
    Input('4-age-slider', 'value'),
    Input("4-product-check", 'value'),

)

def update_graph(selected_firm, status, years, duration, age, product):
    # print(selected_firm)
    if selected_firm == 'All Firms' and status == 'All':
        filtered_firm = df
    elif selected_firm != 'All Firms' and status == 'All':
        filtered_firm = df[df['Firm'] == selected_firm]
    elif selected_firm == 'All Firms' and status != 'All':
        filtered_firm = df[df['deceased'] == status]
    elif selected_firm != 'All Firms' and status != 'All':
        filtered_firm = df[(df['deceased'] == status) & 
                        (df['Firm'] == selected_firm)]
    filtered_firm = filtered_firm[(filtered_firm['Year'] >=years[0]) & 
                        (filtered_firm['Year'] <= years[1]) &
                        (filtered_firm['total_use_years'] >= duration[0]) &
                        (filtered_firm['total_use_years']<= duration[1]) & 
                        (filtered_firm['age'] >= age[0]) & 
                        (filtered_firm['age'] <= age[1]) &
                        filtered_firm['Product_Type'].isin(product)]
    
    # print(filtered_firm.head())


    """ CONTENT FOR ALL THE TEXT FIELDS """
    firm_avg = df[df['Firm'] == selected_firm]
    #Average Age Stats
    avg_age = round(firm_avg['age'].mean(), 1)
    avg_age_text = f'Average Age:  {avg_age}'
    #average duration text
    avg_dur = round(firm_avg['total_use_years'].mean(),1)
    avg_dur_text = f'Average Years of Use:  {avg_dur}'
    #dataset averages
    dataset_avg_age = round(filtered_firm['age'].mean(),1)
    dataset_avg_age_text = f'Average Age:  {dataset_avg_age}'
    dataset_avg_dur = round(filtered_firm['total_use_years'].mean(),1)
    dataset_avg_dur_text = f'Average Years of Use:  {dataset_avg_dur}'
    #totals for status chosen
    status_number = filtered_firm.SubjectId.nunique()
    if status == 'All':
        status_text = f'All {status_number} Clients' 
    else:
        status_text = f'{status_number} {status} Clients'
    #Use years text
    years_use_header = f"Product Used From {years[0]} to {years[1]}"
    #duration header text
    dur_use_header = f'Product Use Duration {duration[0]} to {duration[1]} years'
    #age header text
    age_header = f'Claimants between {age[0]} and {age[1]} years old'

    #the graph header
    graph_header = f'{status_text} using any Product {years[0]} - {years[1]}, from {duration[0]} - {duration[1]} years duration, ages {age[0]} - {age[1]}'
    table_header = f'{status_text} using any Product {years[0]} - {years[1]}, from {duration[0]} - {duration[1]} years duration, ages {age[0]} - {age[1]}'

    final_data = filtered_firm.groupby(['Product_Type', 'Year'])['SubjectId'].count().reset_index()
    final_data = final_data.rename(columns={'SubjectId':'Total'})
    final_data = final_data[final_data['Total'] >0]
    #now we define the actual figure, data for it and the x and y axis
    product_fig=px.bar(final_data,
                    text='Total',  #puts direct label on bar graph
                    x='Year', y='Total', color="Product_Type", labels=dict(Year="Year of Product Use", Total="Clients Using Each Product", Product_Type="Product Type", hover_data=["SubjectID", "Product_Type"]),
                    title='')
    table_fig =html.Div([dash_table.DataTable
                (id='table',
                style_header={'backgroundColor': '#df691a', 'color': '#ffffff'},
				columns=[{"name": i, "id": i} for i in filtered_firm.   columns if i != 'Firm'],
				page_size=10,
                style_as_list_view=True,
				data=filtered_firm.to_dict("records"),
                # export_format="csv",
                export_format="xlsx",
                filter_action="native",
                sort_action="native",
				style_cell={'width': '300px',
                            'height': '20px',
                            'textAlign': 'left', 
                            'backgroundColor': 'rgb(43, 62, 80)',
                            'color': 'white'}
                ),
                        ])
    # page_title = 'Plaintiff Firms Product Data'
    return product_fig, avg_age_text, avg_dur_text, status_text, years_use_header, dur_use_header, age_header, table_fig, graph_header, table_header, dataset_avg_age_text, dataset_avg_dur_text

if __name__ == '__main__':
    app.run_server(debug=True)