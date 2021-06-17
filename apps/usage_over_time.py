from os import linesep
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd 
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


# df = pd.read_pickle("data/use_over_time.pkl")

df = pd.read_feather("data/use_over_time.ftr", columns=None)
# df.drop(columns=['index'], inplace=True)
# df.reset_index(inplace=True)


all_formulations = df.formulation.unique()
# main_usage = pd.read_pickle("data/master_usage.pkl")

main_usage = pd.read_feather("data/master_usage.ftr", columns=None).set_index(['SubjectId'])
try:
    df.drop(columns=['index'], inplace=True)
except:
    pass
main_usage.reset_index(inplace=True)

google = pd.read_csv("data/google_final.csv")

from app import app

# app = dash.Dash(__name__)


# id="checklist",
#         options=[{"label": x, "value": x} 
#                  for x in all_formulations],
#         value=all_formulations[0:1],
#         labelStyle={'display': 'inline-block'}

product_check = dbc.FormGroup(
    [
        dbc.Label("Product Type"),
        dbc.Checklist(
            options=[{"label": x, "value": x} 
                 for x in all_formulations],
            value=all_formulations[0:1],
            labelStyle={'display': 'inline-block'},
            id="usage-product-check",inline=True, 
        )
    ]
)

line_fig1_card = dbc.Card(
                    dbc.CardBody(
                                [
                                    html.H5("PRODUCT DATA", className="card-title"),
                                    # html.P(
                                    #     "Explain what this graph is "
                                    # ),
                                    # html.P(id='4-graph-sub', children=""
                                    #         ),
                                    #put the graph component here
                                    dcc.Graph(id='line-chart1', config={'displayModeBar':False}),
                                ]
                                ), className='float-box col-lg-11 mt-4, ml-4',
    
                    ), 

line_fig2_card = dbc.Card(
                    dbc.CardBody(
                                [
                                    html.H5("Google Search Data for ('zantac + cancer')", className="card-title"),
                                    # html.P(
                                    #     "Explain what this graph is "
                                    # ),
                                    # html.P(id='4-graph-sub', children=""
                                    #         ),
                                    #put the graph component here
                                    dcc.Graph(id='line-chart2', config={'displayModeBar':False}),
                                ]
                                ), className='float-box col-lg-11 mt-4, ml-4',
    
                    ), 

line_fig3_card = dbc.Card(
                    dbc.CardBody(
                                [
                                    html.H5("When Claimants Started Using any Product", className="card-title"),
                                    # html.P(
                                    #     "Explain what this graph is "
                                    # ),
                                    # html.P(id='4-graph-sub', children=""
                                    #         ),
                                    #put the graph component here
                                    dcc.Graph(id='line-chart3', config={'displayModeBar':False}),
                                ]
                                ), className='float-box col-lg-11 mt-4, ml-4',
    
                    ), 

line_fig4_card = dbc.Card(
                    dbc.CardBody(
                                [
                                    html.H5("When Claimants Stopped Using All Products", className="card-title"),
                                    # html.P(
                                    #     "Explain what this graph is "
                                    # ),
                                    # html.P(id='4-graph-sub', children=""
                                    #         ),
                                    #put the graph component here
                                    dcc.Graph(id='line-chart4', config={'displayModeBar':False}),
                                ]
                                ), className='float-box col-lg-11 mt-4, ml-4',
    
                    ), 


layout = dbc.Container([

                        dbc.Row(html.H1('Usage Over Time'), className = 'ml-5'),
                        html.Br(),
                        dbc.Row(product_check, className = 'ml-5 mt-3'),
                        dbc.Row(line_fig1_card, className = 'ml-3 mt-3'),
                        dbc.Row(line_fig2_card, className = 'ml-3 mt-3'),
                        dbc.Row(line_fig3_card, className = 'ml-3 mt-3'),
                        dbc.Row(line_fig4_card, className = 'ml-3 mt-3'),
], fluid=True)


@app.callback(
    Output("line-chart1", "figure"), 
    Output("line-chart2", "figure"), 
    Output("line-chart3", "figure"), 
    Output("line-chart4", "figure"), 
    Input("usage-product-check", "value"))
def update_line_chart(form_choice):
    filtered_form = df[df.formulation.isin(form_choice)]
    final_data = filtered_form.groupby(['formulation','use_years'])['SubjectId'].count().reset_index()
    final_data = final_data.rename(columns={'use_years':'Year', 'SubjectId':'Total'})
    final_data = final_data[final_data.Total >0]
    # print(f'final_data head {final_data.head()}')
    # print(form_choice)
    fig1 = px.scatter(final_data, 
        x="Year", y="Total", color='formulation').update_traces(mode='lines+markers')
    fig1.update_layout(
        title={
            'text': "<br><br><b>Total Products</b> in Use by Year",
            'y':1.0,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    final_google = google[(google['Year'].between(1980, 2020))]
    fig2 = px.scatter(final_google, x="Year", y="Total").update_traces(mode='lines+markers')
    fig2.update_layout(
        title={
            'text': "<br><br><b>Zantac + Cancer</b> Google Searches By Year",
            'y':1.0,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    main_usage['start_yr'] = main_usage['use_years'].str[0]
    start_yr_data = main_usage.groupby(['formulation', 'start_yr'])['SubjectId'].count().reset_index()  
    start_yr_data = start_yr_data.rename(columns={'start_yr':'Start Year', 'SubjectId':'Total'})
    # start_yr_data = start_yr_data[(start_yr_data['Start Year'] > 1980) & (start_yr_data['Total'] >0) & (start_yr_data['Start Year'] < 2021)]
    start_yr_data = start_yr_data[(start_yr_data['Start Year'].between(1980, 2020))]

    fig3 = px.scatter(start_yr_data, x="Start Year", y="Total", color='formulation').update_traces(mode='lines+markers')
    fig3.update_layout(
        title={
            'text': "<br><br><b>Total Claimants Starting</b> Any Drug by Year",
            'y':1.0,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    main_usage['end_yr'] = main_usage['use_years'].str[1]
    end_yr_data = main_usage.groupby(['formulation', 'end_yr'])['SubjectId'].count().reset_index()  
    end_yr_data = end_yr_data.rename(columns={'end_yr':'End Year', 'SubjectId':'Total'})
    # end_yr_data = end_yr_data[(end_yr_data['End Year'] > 1980) & (end_yr_data['Total'] >0)]
    end_yr_data = end_yr_data[(end_yr_data['End Year'].between(1980, 2020))]
    fig4 = px.scatter(end_yr_data, x="End Year", y="Total", color='formulation').update_traces(mode='lines+markers')
    fig4.update_layout(
        title={
            'text': "<br><br><b>Total Claimants Stopping</b> Any Drug by Year",
            'y':1.0,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig1, fig2, fig3, fig4

# app.run_server(debug=True)