import dash
import dash_core_components as dcc
import dash_html_components as html
from numpy.lib.function_base import select
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_core_components.RadioItems import RadioItems
import csv
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
from datetime import datetime
import time
from datetime import date
now = pd.to_datetime('now')
#Dash Stuff
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_table

""" DATA AND VARIABLES """
# df = pd.read_pickle("data/cancer.pkl")

df = pd.read_feather("data/cancer.ftr", columns=None).set_index(['SubjectId'])
try:
    df.drop(columns=['index'], inplace=True)
except:
    pass
df.reset_index(inplace=True)

df.sort_values(by=['Firm'], ascending=True, inplace=True)
firm_list = sorted(list(set(df['Firm'].to_list())))
# firm_list.remove("")
# print(firm_list[:10])
# firm_list = start_lst + initial_list
firm_options = [{'label':i, 'value':i} for i in firm_list]
# print(firm_options)
retailer_lst = ['AppleBees', 'theRestaurant','theCoffeeShop','theMechanic','HealthyVegan','SignalProcessing','Clover', 'MarigoldsInc', 'WorldProducts', 'Meryls','GreatBurger', 'Canelos', 'Jones_park', 'SuperStore','HealthyPharmacy', 'Mineal','theMainFoodandDrug', 'Tomotion', 'Fallint','MegaSuperStore', 'Hillmans']

from app import app

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

firm_dropdown = dcc.Dropdown(id='2-cancer-firm-dd', multi=False, value=firm_list[0], options=firm_options, style={'width':'100%', 'color':'black'}, clearable=False)
retailer_dropdown = dcc.Dropdown(id='2-retailer-dd', multi=False, value=['All'], options=[], style={'width':'100%', 'color':'black'}, clearable=False)
status_radio = dbc.RadioItems(id="2-ret-status-radio", options=[], value=[], style={"margin-left": "5px"})

total_cancer_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4(id='2-total-cancer-header', children="", className="card-title"),
                dcc.Graph(id='2-total-cancer-graph',config={'displayModeBar':False}),

                # dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],style={"width": "100%"}, className='float-box',
)

stats_card = dbc.Card(
    [
        # dbc.CardHeader("General Statistics", style={'textAlign':'center'}),
        dbc.CardBody(
            [
                # html.H4("Card title", className="card-title"),
                html.P(f"Statistics (Average in Years)", style={'textAlign':'center'}),
                html.Hr(style={'color':'#ff8300'}),
                html.P(id='2-ca-avg-age', children="", style={'textAlign':'right'}),
                html.P(id='2-ca-avg-use', children="", style={'textAlign':'right'}),
                html.P(id='2-ca-use-to-diag', children="", style={'textAlign':'right'}),
                html.P(id='2-ca-avg-age-first-use', children="", style={'textAlign':'right'}),
            ], 
        ),
        # dbc.CardFooter("This is the footer"),
    ], style={"width": "100%"}, className='float-box'
)

yrs_use_slider = dcc.RangeSlider(
        id='2-ca-years-use-slider',
        step=1,
        value=[],
        marks={},
        dots=True,
        tooltip = {'always_visible':False, 'placement':'bottom'}     
        )

yrs_use_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(id='2-ca-yrs-use-header', children="", className="card-title", style={'text-align': 'center'}),
            html.P("Use Years"),
            yrs_use_slider,
        ]
    ), className='float-box col-lg-12 mt-2'
)

duration_of_use_slider = dcc.RangeSlider(
        id='2-ca-dur-slider',
        # min=0,
        # max=40,
        step=1,
        value=[],
        marks={},
        dots=True,
        tooltip = {'always_visible':False, 'placement':'bottom'}     
        )

duration_of_use_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(id='2-ca-dur-use-header', children="", className="card-title", style={'text-align': 'center'}),
            html.P(
                "Total Years of Use"
            ),
            duration_of_use_slider,
        ]
    ), className='float-box col-lg-12 mt-3'
)

age_slider = dcc.RangeSlider(
        id='2-ca-age-slider',
        step=1,
        value=[],
        marks={},
        dots=True,
        tooltip = {'always_visible':True, 'placement':'bottom'}
        )

age_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(id='2-ca-age-header', children="", className="card-title", style={'text-align': 'center'}),
            html.P(
                "Current Age"
            ),
            age_slider,
        ]
    ), className='float-box col-lg-12 mt-3'
)

firm_ca_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("CANCER DATA", className="card-title"),
            dcc.Graph(id='2-cancer-graph', config={'displayModeBar':False, 'edits':{'colorbarTitleText':True}}),
        ]
    ), style={"width": "100%"}, className='float-box',
), 


table_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Dataset Reflected in the Chart Above", className="card-title"),
            html.P('Click the Export Button to Download Excel file of the data from the chart'),
            #put the graph component here
            html.Div(id='2-ca-table'),
        ]
    ), className='float-box mt-2',
), 

download_button = dcc.Input(id="input-filename", type="text", placeholder="Enter File name")

layout = dbc.Container([
                            dbc.Row(html.H1('Plaintiff Cancer Data')),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row(firm_dropdown),                                    
                                    dbc.Row(retailer_dropdown),
                                    dbc.Row([
                                        dbc.Col(status_radio, className='mt-2'),
                                        dbc.Col(html.P(id='2-status-header', children=""), className='mt-2'),
                                        ]),
                                    dbc.Row(stats_card, className='mt-2'),
                                        ],xs=10, sm=10, md=10, lg=4, xl=4, className='mt-0', align='start'),
                                dbc.Col([
                                    dbc.Row(yrs_use_card),
                                    dbc.Row(duration_of_use_card),
                                    dbc.Row(age_card),
                                        ], className='ml-5'),
                                    ],className='mt-5',justify ='around'),

                            dbc.Row(dbc.Col(total_cancer_card, xs=12, sm=12, md=12, lg=12, xl=12),className='mt-5'),
                            # dbc.Row(html.P('DATA TABLE HEADER ROW'),justify='center', className='mt-5'),
                            # dbc.Row(download_button,justify='center', className='mt-5'),
                            # dbc.Row(html.Button('Download', id='done', n_clicks=0)),
                            dbc.Row(table_card),
                            # dbc.Row(html.P('Insert Data Table Here')),
                            ])

"""       CALLBACKS         """
@app.callback(
    Output('2-retailer-dd', 'options'),
    Output('2-retailer-dd', 'value'),
    Input('2-cancer-firm-dd', 'value')) 
def set_retailer_dropdown(selected_firm):
    ret_choice = df[(df['Firm'] == selected_firm) & (df['retailer'].isin(retailer_lst))]
    ret_lst = sorted(list(set(ret_choice['retailer'])))
    start_lst = ['All']
    # first_ret_lst = list(sorted(ret_choice['Firm'].unique()))
    total_ret_lst = start_lst + ret_lst
    # firm_lst.remove("")
    value = total_ret_lst[0]  #makes the default value the first option in the list
    return [{'label': i, 'value': i} for i in total_ret_lst], value
@app.callback(
    Output('2-ret-status-radio', 'options'),
    Output('2-ret-status-radio', 'value'),
    Input('2-cancer-firm-dd', 'value'),
    Input('2-retailer-dd', 'value'))
def set_status_options(selected_firm, selected_retailer):
    if selected_retailer == 'All':
        firm_status = df[df['Firm'] == selected_firm]
    else:
        firm_status = df[(df['retailer'] == selected_retailer) &
                    (df["Firm"] == selected_firm)]
    # print(f'firm status rows = {firm_status.shape[0]}')
    initial_lst = ['All'] #to add an all option to the list
    df_lst = list(set(firm_status['deceased']))
    final_lst = [x for x in df_lst if x in ['All', 'Living', 'Deceased']]
    final_lst.sort(reverse=True) # to have Living appear before Deceased in the radio button order
    
    if len(final_lst) == 1: #if the dataset only has all deceased or all living clients
        status_lst = final_lst #the radio buttons will only show one option
    else:
        status_lst = initial_lst + final_lst #if there are living and deceased clients, then show three options, All, Living and Deceased
    # print(f'final list before return - {status_lst}')
    value = status_lst[0]  #makes the default value the first option in the status_lst
    # print(type(status_lst))
    return [{'label': i, 'value': i} for i in status_lst], value
@app.callback(
    Output('2-status-header', 'children'),
    Input('2-retailer-dd', 'value'),
    Input('2-cancer-firm-dd', 'value'),
    Input('2-ret-status-radio', 'value'))
def set_status_text(selected_retailer, selected_firm, status):
    # print(selected_firm, status)
    if selected_retailer == 'All' and status == 'All':
        status_df = df[df['Firm'] == selected_firm]
        # status_num = status_df.shape[0]
        status_num = status_df['SubjectId'].nunique()

        # status_text = f'{status} {status_num} claimants'
        status_text = f'{status_num} claimants'
    elif selected_retailer != 'All' and status == 'All':
        status_df = df[(df['Firm'] == selected_firm) &
                    (df['retailer'] == selected_retailer)]
        # status_num = status_df.shape[0]
        status_num = status_df['SubjectId'].nunique()

        status_text = f'{status} {status_num}'
    elif selected_retailer == 'All' and status != 'All':
        status_df = df[(df['Firm'] == selected_firm) &
                    (df['deceased'] == status)]
        # status_num = status_df.shape[0]
        status_num = status_df['SubjectId'].nunique()
        status_text = f'{status_num} {status}'
    else: 
        status_df = df[(df['retailer'] == selected_retailer) &
                (df['Firm'] == selected_firm) & (df['deceased'] == status)]
        # status_num = status_df.shape[0]
        status_num = status_df['SubjectId'].nunique()

        # print(status_num)
        status_text = f'{status_num} {status}'
    # print(status_text)
    return status_text
@app.callback(
    Output('2-ca-years-use-slider', 'value'),
    Output('2-ca-years-use-slider', 'marks'), 
    Output('2-ca-years-use-slider', 'min'), 
    Output('2-ca-years-use-slider', 'max'),
    Input('2-retailer-dd', 'value'),
    Input('2-cancer-firm-dd', 'value'),
    Input('2-ret-status-radio', 'value'))
def set_use_years_options(selected_retailer, selected_firm, status):
    if selected_retailer == 'All' and status == 'All':
        years_df = df[df['Firm'] == selected_firm]
    elif selected_retailer != 'All' and status == 'All':
        years_df = df[(df['retailer'] == selected_retailer) &
        (df['Firm'] == selected_firm)]
    elif selected_retailer == 'All' and status != 'All':
        years_df = df[(df['Firm'] == selected_firm) &
        (df['deceased'] == status)]
    else:
        years_df = df[(df['retailer'] == selected_retailer) &
        (df['Firm'] == selected_firm) & (df['deceased'] == status)]
    total_start_years = years_df['first_use_year'].unique()
    total_end_years = years_df['last_use_year'].unique()
    start_yr = min([i for i in total_start_years if i > 1979])
    end_yr = max([i for i in total_end_years if i < 2021])
    mark_vals = [start_yr, end_yr]
    years_use_marks = {i:{'label': str(i),'style': {'color':'#ffffff'}} for i in range(start_yr, end_yr+1, 5)}
    # print(years_use_marks)
    return mark_vals, years_use_marks, start_yr, end_yr
@app.callback(
    Output('2-ca-dur-slider', 'value'), #sets starting value for the slider
    Output('2-ca-dur-slider', 'marks'), #sets the marks for the length of the slider
    Output('2-ca-dur-slider', 'min'), #sets the marks for the length of the slider
    Output('2-ca-dur-slider', 'max'), #sets the marks for the length of the slider
    # Output('year-header', 'children'),  
    Input('2-retailer-dd', 'value'),
    Input('2-cancer-firm-dd', 'value'),
    Input('2-ret-status-radio', 'value'))
def set_age_options(selected_retailer, selected_firm, status):
    if selected_retailer == 'All' and status == 'All':
        years_df = df[df['Firm'] == selected_firm]
    elif selected_retailer != 'All' and status == 'All':
        years_df = df[(df['retailer'] == selected_retailer) &
        (df['Firm'] == selected_firm)]
    elif selected_retailer == 'All' and status != 'All':
        years_df = df[(df['Firm'] == selected_firm) &
        (df['deceased'] == status)]
    else:
        years_df = df[(df['retailer'] == selected_retailer) &
        (df['Firm'] == selected_firm) & (df['deceased'] == status)]
    tot_yrs_lst = years_df['total_use_years'].unique()
    start_yr = min([i for i in tot_yrs_lst if i > 0])
    end_yr = max([i for i in tot_yrs_lst if i < 41])

    dur_mark_vals = [start_yr, end_yr]
    dur_yrs_marks = {i:{'label': str(i),'style': {'color':'#ffffff'}} for i in range(start_yr, end_yr+1, 2)}


    return dur_mark_vals, dur_yrs_marks, start_yr, end_yr
@app.callback(
    Output('2-ca-age-slider', 'value'), #sets starting value for the slider
    Output('2-ca-age-slider', 'marks'), #sets the marks for the length of the slider
    Output('2-ca-age-slider', 'min'), #sets the marks for the length of the slider
    Output('2-ca-age-slider', 'max'), #sets the marks for the length of the slider
    # Output('year-header', 'children'),  
    Input('2-retailer-dd', 'value'),
    Input('2-cancer-firm-dd', 'value'),
    Input('2-ret-status-radio', 'value'))
def set_tot_yrs_use_options(selected_retailer, selected_firm, status):
    if selected_retailer == 'All' and status == 'All':
        years_df = df[df['Firm'] == selected_firm]
    elif selected_retailer != 'All' and status == 'All':
        years_df = df[(df['retailer'] == selected_retailer) &
        (df['Firm'] == selected_firm)]
    elif selected_retailer == 'All' and status != 'All':
        years_df = df[(df['Firm'] == selected_firm) &
        (df['deceased'] == status)]
    else:
        years_df = df[(df['retailer'] == selected_retailer) &
        (df['Firm'] == selected_firm) & (df['deceased'] == status)]

    tot_age_lst = years_df['age'].unique()
    start_age = min([i for i in tot_age_lst if i > 0])
    end_age = max([i for i in tot_age_lst if i < 111])

    age_mark_vals = [start_age, end_age]
    age_yrs_marks = {i:{'label': str(i),'style': {'color':'#ffffff'}} for i in range(start_age, end_age+1, 5)}


    return age_mark_vals, age_yrs_marks, start_age, end_age

# #Updating the Graph and table with all the various inputs
@app.callback(
    # Output('cancer-graph', 'figure'),
    Output('2-total-cancer-graph', 'figure'),
    Output('2-ca-avg-age', 'children'),
    Output('2-ca-avg-use', 'children'),
    Output('2-ca-use-to-diag', 'children'),
    Output('2-ca-avg-age-first-use', 'children'),
    Output('2-ca-table', 'children'),
    # Output('total-cancer-header', 'children'),
    Input('2-retailer-dd', 'value'),
    Input('2-cancer-firm-dd', 'value'),
    Input('2-ret-status-radio', 'value'),
    Input('2-ca-years-use-slider', 'value'),
    Input('2-ca-dur-slider', 'value'),
    Input('2-ca-age-slider', 'value'))
def update_graph(selected_retailer, selected_firm, status, use_yrs, dur_yrs, age):
    if selected_retailer == 'All' and status == 'All':
        figure_df = df[df['Firm'] == selected_firm]
    elif selected_retailer != 'All' and status == 'All':
        figure_df = df[(df['retailer'] == selected_retailer) &
                    (df['Firm'] == selected_firm)]
    elif selected_retailer == 'All' and status != 'All':
        figure_df = df[(df['Firm'] == selected_firm) &
                (df['deceased'] == status)]
    else:
        figure_df = df[(df['retailer'] == selected_retailer) &
                (df['Firm'] == selected_firm) & (df['deceased'] == status)]
    # ca_use_yrs = figure_df[(figure_df['first_use_year'] >= use_yrs[0]) & (figure_df['last_use_year'] <= use_yrs[1])]
    ca_use_yrs = figure_df[(figure_df['first_use_year'].between(use_yrs[0], use_yrs[1]))]

    # ca_dur_yrs = ca_use_yrs[(ca_use_yrs['total_use_years'] >= dur_yrs[0]) & (ca_use_yrs['total_use_years'] <= dur_yrs[1])]
    ca_dur_yrs = ca_use_yrs[(ca_use_yrs['total_use_years'].between(dur_yrs[0], dur_yrs[1]))]

    # ca_age_yrs = ca_dur_yrs[(ca_dur_yrs['age'] >= age[0]) & (ca_dur_yrs['age'] <= age[1])]
    ca_age_yrs = ca_dur_yrs[(ca_dur_yrs['age'].between(age[0], age[1]))]
    ca_age_yrs.drop_duplicates(subset=['SubjectId', 'Cancer_Type'], inplace=True)
    ca_age_yrs.sort_values(by=['SubjectId'], inplace=True)


    #calculate stats for the stats card
    from statistics import mean
    # total_records = ca_age_yrs.shape[0]
    tot_age_lst = ca_age_yrs['age'].to_list()
    tot_dur_lst = ca_age_yrs['total_use_years'].to_list()
    first_use_to_diag = ca_age_yrs['first_use_to_diag_years'].to_list()
    age_first_use = ca_age_yrs['age_first_use'].to_list()
    age_lst = [i for i in tot_age_lst if i > 0 and i <110]
    dur_lst = [i for i in tot_dur_lst if i > 0 and i <41]
    first_use_to_diag_lst = [i for i in first_use_to_diag if i > 0 and i <41]
    age_first_use_lst = [i for i in age_first_use if i > 0 and i <110]

    avg_age = mean(age_lst)
    avg_dur = mean(dur_lst)
    avg_first_use_to_diag = mean(first_use_to_diag_lst)
    avg_age_first_use = mean(age_first_use_lst)
    # print(f'average age is {round((avg_age), 2)}')
    # print(f'average duration is {round((avg_dur),2)}')
    # print(f'average years from first use to diag is {round((avg_first_use_to_diag),2)}')

    avg_age_text = f'Age: {round((avg_age),2)}'
    avg_dur_text = f'Years of Use: {round((avg_dur),2)}'
    avg_first_use_to_diag_text = f'First Use to Diag: {round((avg_first_use_to_diag),2)}'
    avg_age_first_use_text = f'Age at First Use: {round((avg_age_first_use),2)}'

    final_data = ca_age_yrs.groupby(['Cancer_Type'])['SubjectId'].count().reset_index()
    final_data = final_data.rename(columns={'SubjectId':'Total'})
    #remove the word Cancer from each value
    final_data = final_data[final_data['Total'] >0]
    final_data = final_data.sort_values(by=['Total'], ascending=False)
    total_cancer=px.bar(final_data, text='Total', x='Cancer_Type', y='Total', color='Total', color_discrete_sequence=px.colors.qualitative.Pastel,labels=dict(Total="Total Claimants", Cancer_Type="Cancer Type", hover_data=["SubjectID", "Cancer_Type"]))
    total_cancer.update_layout(showlegend=False)

    table_df = ca_age_yrs[['SubjectId', 'deceased','age', 'total_use_years', 'Cancer_Type','diagnosis_date', 'retailer']]
    table_df['diagnosis_date'] = table_df['diagnosis_date'].dt.date
    table_df = table_df.rename(columns={'deceased':'Deceased', 'age':'Age','total_use_years':'Years of Use','Cancer_Type':'Cancer Type', 'diagnosis_date':'Diagnosis Date'})
    table_df.drop_duplicates(inplace=True)

    #design table here
    table_fig =html.Div([dash_table.DataTable(
				id='table',
                style_header={'backgroundColor': '#df691a', 'color': '#ffffff'},
				columns=[{"name": i, "id": i} for i in table_df.columns],
				page_size=10,
                style_as_list_view=True,
				data=table_df.to_dict("records"),
                # export_format="csv",
                export_format="xlsx",
                filter_action="native",
                sort_action="native",
				style_cell={'width': '300px',
				'height': '20px',
				'textAlign': 'left', 
                'backgroundColor': 'rgb(43, 62, 80)',
                'color': 'white'}),
                            ],
                )


    return total_cancer, avg_age_text, avg_dur_text, avg_first_use_to_diag_text, avg_age_first_use_text, table_fig


#attempting to get a file download button working
# @app.callback(
#     Input('done','n_clicks'),
#     State('2-ca-table','data'),
#     State('input-filename','value'))
# def updateout(_,tab_data,filename):
#     dl_file = pd.DataFrame.from_records(tab_data).to_csv(filename+'.csv',index=False)
#     return dl_file

if __name__ == '__main__':
    app.run_server(debug=True)