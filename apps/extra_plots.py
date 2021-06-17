from os import linesep
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd 
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# df = pd.read_pickle('data/master_usage.pkl')
df = pd.read_feather("data/master_usage.ftr", columns=None).set_index(['SubjectId'])
try:
    df.drop(columns=['index'], inplace=True)
except:
    pass
df.reset_index(inplace=True)

# cancer = pd.read_pickle('data/cancer.pkl')
cancer = pd.read_feather("data/cancer.ftr", columns=None).set_index(['SubjectId'])
try:
    cancer.drop(columns=['index'], inplace=True)
except:
    pass
cancer.reset_index(inplace=True)

# just_states = df[['SubjectId', 'formulation', 'state_cur', 'State_use']]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

liv_dec = df[['SubjectId', 'deceased', 'total_use_years']]
liv_dec.deceased = liv_dec.deceased.astype('object')
liv_dec.fillna('no data', inplace=True)
liv_dec.drop_duplicates(subset=['SubjectId'], inplace=True)
final_liv = liv_dec[(liv_dec['deceased'] == "Deceased") | (liv_dec['deceased'] == "Living")]
final_liv = final_liv[(final_liv['total_use_years'] >= 1) & (final_liv['total_use_years'] <= 40)]
facet_df = final_liv.groupby(['total_use_years', 'deceased'])['SubjectId'].count().reset_index()
facet_df = facet_df.rename(columns={'SubjectId':'Total'})

#create firm list
plot_list = ['Years of Use', 'Products']
plot_options = [{'label':i, 'value':i} for i in plot_list]

from app import app

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

plot_dropdown = dcc.Dropdown(id='plot-dd', multi=False, value=plot_options[0]['value'] ,options=plot_options, style={'width':'50%', 'color':'#000000'}, clearable=False)

graph_card = dbc.Card(
    dbc.CardBody(
        [
            # html.H5("Additional Plot Options", className="card-title"),
            html.H5(id='plot-graph-header', children="", className="card-title"),
            
            # html.P(id='plot-graph-sub', children=""
            # ),
            dcc.Graph(id='plot-fig', config={'displayModeBar':False}),
        ]
    ), className='float-box col-lg-9 mt-4, ml-4',
    
), 

layout = dbc.Container([
                        html.Br(),
                        html.Br(),
                        dbc.Row(),
                        dbc.Row(plot_dropdown, className='ml-2'),
                        html.Br(),
                        html.Br(),
                        dbc.Row(graph_card),
                            ], fluid=True)


@app.callback(
    Output('plot-fig', 'figure'),
    # Output('plot-graph-sub', 'children'),
    Output('plot-graph-header', 'children'),
    Input('plot-dd', 'value'))
def select_plot(plot_choice):
    if plot_choice == 'Years of Use':
        fig = px.scatter(facet_df, x="total_use_years", y="Total", color="deceased", facet_col="deceased",
                                    labels={
                                                "total_use_years": "Total Years of Use",
                                                "Total": "Total Claimants",
                                            },)
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_layout(showlegend=False)
    else:
        admin_tot = df[['SubjectId', 'admin_method', 'formulation']]
        fig = admin_tot.groupby(['formulation', 'admin_method'])['SubjectId'].count().reset_index()
        fig = fig.rename(columns={'SubjectId':'Total'})
        #remove zero values
        fig = fig[fig['Total'] >= 1]
        fig.sort_values(by=['Total'], inplace=True, ascending=False)
        fig = px.bar(fig, x="formulation", y="Total", color="formulation", facet_row="admin_method", text="Total")
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_layout(showlegend=False)
    graph_sub = plot_choice
    return fig, graph_sub

if __name__ == '__main__':
    app.run_server(debug=True)