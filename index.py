import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
pd.set_option('mode.chained_assignment', None)
import dash_auth

# must add this line in order for the app to be deployed successfully on Heroku
from app import server

from app import app
from apps import prod_stats, rev_stats, employee_stats, monthly_stats

app.layout = html.Div([
                dbc.Row(
                    dbc.NavbarSimple(
                    children=[
                        dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem("Product Stats", href="/apps/prod_stats"),
                                dbc.DropdownMenuItem("Revenue", href="/apps/rev_stats"),
                                dbc.DropdownMenuItem("Employees", href="/apps/employee_stats"),
                                dbc.DropdownMenuItem("Monthly Statistics", href="/apps/monthly_stats"),
                                    ],
                            nav=True,
                            in_navbar=True,
                            label="Analytics",
                            # className='navbar-nav ml-auto'
                                        ),
                        # dbc.DropdownMenu(
                        #     children=[
                        #         # dbc.DropdownMenuItem("More pages", header=True),
                        #         # dbc.DropdownMenuItem("Cancer Data", href="/apps/ca_def"),
                        #         # dbc.DropdownMenuItem("Master Usage", href="/apps/master_use_def"),
                        #         # dbc.DropdownMenuItem("Usage Over Time", href="/apps/usage_over_time"),

                        #             ],
                        #     nav=True,
                        #     in_navbar=True,
                        #     label="Defense",
                        #                 ),
                            # dbc.DropdownMenu(
                            # children=[
                            #     # dbc.DropdownMenuItem("More pages", header=True),
                            #     # dbc.DropdownMenuItem("Comparisons", href="/apps/extra_plots"),
                            #     # dbc.DropdownMenuItem("Colors Change", href="/apps/four_prod_stats_white"),
                            #     # dbc.DropdownMenuItem("Master Usage", href="/apps/master_usage_def_V2"),
                            #     # dbc.DropdownMenuItem("Usage Over Time", href="/apps/usage_over_time"),
                            #     # dbc.DropdownMenuItem("Geo Alternative", href="/apps/geo_distribution_toggle"),

                            #         ],
                            # nav=True,
                            # in_navbar=True,
                            # label="Additional",
                            #             ),
                            
                            
                            ], 
                    className = "sticky-top",
                    brand="27 Club Coffee",
                    brand_href="https://www.27clubcoffee.com",
                    color="primary",
                    dark=True,
                    # className='navbar-nav mr-auto',
                    # sticky='top'
                                        )),
                dbc.Row([
                        dbc.Col(),
                        dbc.Col(),
                        dbc.Col(),
                        ]),
                html.Br(),  #puts space between nav bar and content
                dcc.Location(id='url', refresh=False),
                html.Div(id='page-content'),
                    ], style={
                                'position': 'relative',
                                'zIndex': '2',
                            })
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/main_stats':
        return prod_stats.layout
    elif pathname == '/apps/rev_stats':
        return rev_stats.layout
    elif pathname == '/apps/employee_stats':
        return employee_stats.layout
    elif pathname == '/apps/monthly_stats':
        return monthly_stats.layout
    else:
        return prod_stats.layout

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)