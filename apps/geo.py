from os import linesep
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd 
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# df = pd.read_pickle("data/master_usage.pkl")
# just_states = df[['SubjectId', 'formulation', 'state_cur', 'State_use']]

df = pd.read_feather("data/master_usage.ftr", columns=None).set_index(['SubjectId'])
try:
    df.drop(columns=['index'], inplace=True)
except:
    pass
df.reset_index(inplace=True)


from app import app

# app = dash.Dash(__name__)

all_formulations = ['All']
forms = list(set(df['formulation']))
form_lst = sorted(all_formulations + forms)
# form_lst.remove("Other")
# form_lst.append("Other")

#variables for the status dropdown
form_options = [{'label': i, 'value': i} for i in form_lst]

form_radio = dbc.FormGroup(
    [
        dbc.Label("Formulation"),
        dbc.RadioItems(
            options=form_options,
            value='All',
            id="form-radio",
            inline=True
        ), html.Br(),
            # html.P(id='form-text', children="", style={'margin-left': '5px'})
    ]
)
map_fig_card = dbc.Card(
                    dbc.CardBody(
                                [
                                    html.H5("Geographic Distribution - Current Residence State", className="card-title"),
                                    html.P(id='map-sub', children="", style={'text-align': 'center'}),
                                    dcc.Graph(id='map-fig', config={'displayModeBar':False}),
                                ]
                                ), className='float-box col-lg-11',
                    ), 

map_fig_card2 = dbc.Card(
                    dbc.CardBody(
                                [
                                    html.H5("Geographic Distribution - State of Use", className="card-title"),
                                    html.P(id='map-sub2', children="", style={'text-align': 'center'}),
                                    dcc.Graph(id='map-fig2', config={'displayModeBar':False}),
                                ]
                                ), className='float-box col-lg-11',
                    ), 

layout = dbc.Container([
                        # html.Br(),
                        dbc.Row([
                            dbc.Col(),
                            dbc.Col(dbc.Row(form_radio), className='col-lg-8'),
                                ]),
                        dbc.Row(map_fig_card, className='ml-5'),
                        html.Br(),
                        dbc.Row(map_fig_card2, className='ml-5'),
                        ], fluid=True)

@app.callback(
    Output("map-fig", "figure"), 
    Output("map-fig2", "figure"), 
    Output("map-sub", "children"), 
    Output("map-sub2", "children"), 
    Input("form-radio", "value"))
def update_map(form_choice):
    # print(f' this is form choice {form_choice}')
    if form_choice == 'All':
        state_grp = df.groupby(['state_cur_ab'])['SubjectId'].count().reset_index()
        state_grp = state_grp[(state_grp['state_cur_ab'] != 0) & (state_grp['SubjectId'] != 0)]
        state_grp = state_grp.rename(columns={'SubjectId':'Total'})
        map_fig = px.choropleth(state_grp, locations='state_cur_ab', locationmode = 'USA-states', scope="usa", hover_data=state_grp.columns, hover_name='Total', color='Total', height=700)
        #for the state of Use data
        state_grp2 = df.groupby(['state_use_ab'])['SubjectId'].count().reset_index()
        state_grp2 = state_grp2[(state_grp2['state_use_ab'] != 0) & (state_grp2['SubjectId'] != 0)]
        state_grp2 = state_grp2.rename(columns={'SubjectId':'Total'})
        map_fig2 = px.choropleth(state_grp2, locations='state_use_ab', locationmode = 'USA-states', scope="usa", hover_data=state_grp2.columns, hover_name='Total', color='Total', height=700)
    else:
        state_grp = df[df['formulation'] == form_choice]
        # print(state_grp.head())
        # print(f'form choice{form_choice} under selection option')
        state_grp = state_grp.groupby(['formulation','state_cur_ab'])['SubjectId'].count().reset_index()
        state_grp = state_grp[(state_grp['state_cur_ab'] != 0) & (state_grp['SubjectId'] != 0)]
        state_grp = state_grp.rename(columns={'SubjectId':'Total'})
        map_fig = px.choropleth(state_grp, locations='state_cur_ab', locationmode = 'USA-states', scope="usa", hover_data=state_grp.columns, hover_name='Total', color='Total', height=700)
        #for the state of Use data
        state_grp2 = df[df['formulation'] == form_choice]
        # print(state_grp.head())
        # print(f'form choice{form_choice} under selection option')
        state_grp2 = state_grp2.groupby(['formulation','state_use_ab'])['SubjectId'].count().reset_index()
        state_grp2 = state_grp2[(state_grp2['state_use_ab'] != 0) & (state_grp2['SubjectId'] != 0)]
        state_grp2 = state_grp2.rename(columns={'SubjectId':'Total'})
        map_fig2 = px.choropleth(state_grp2, locations='state_use_ab', locationmode = 'USA-states', scope="usa", hover_data=state_grp2.columns, hover_name='Total', color='Total', height=700)
    form_text = f'Formulation: {form_choice}'
    form_text2 = f'Formulation: {form_choice}'
    return map_fig, map_fig2, form_text, form_text2

# app.run_server(debug=True)