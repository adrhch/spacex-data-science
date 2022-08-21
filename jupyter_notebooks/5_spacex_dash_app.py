# Import required libraries
import pandas as pd
import dash
#import dash_html_components as html
#import dash_core_components as dcc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc



# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create an app layout
app.layout = html.Div([
    dbc.Row([
    html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
            # TASK 1: Add a dropdown list to enable Launch Site selection
            html.Div(dcc.Dropdown(['CCAFS LC-40',
                                'CCAFS SLC-40',
                                'KSC LC-39A',
                                'VAFB SLC-4E',
                                'All sites'], 'All sites',
                                id='dropdown-site')),
            # The default select value is for ALL sites
            # dcc.Dropdown(id='site-dropdown',...)
            html.Br(),
            html.Div(dcc.Graph(id='success-pie-chart')),
            html.Br()
            ])
        ),
        dbc.Col(
            html.Div([
            # TASK 2: Add a pie chart to show the total successful launches count for all sites
            # If a specific launch site was selected, show the Success vs. Failed counts for the site
            

            html.P("Payload range (Kg):"),
            # TASK 3: Add a slider to select payload range
            dcc.RangeSlider(0, 9600, 1000, value=[0, 1000], id='payload-slider'),

            # TASK 4: Add a scatter chart to show the correlation between payload and launch success
            html.Div(dcc.Graph(id='success-payload-scatter-chart'))
            ])
    )])
])
                        
                                



# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

def compute_info(spacex_df,entered_site):
    if entered_site == 'All sites':
        df =  spacex_df
        graph_df =  df.groupby(['class']).count().reset_index()
    else:
        df =  spacex_df[spacex_df['Launch Site']==str(entered_site)]
        graph_df =  df.groupby(['class']).count().reset_index()
    return graph_df


@app.callback( [
               Output(component_id='success-pie-chart', component_property='figure'),
               ],
               Input(component_id='dropdown-site', component_property='value'))
def get_graph(entered_site):
    graph_df = compute_info(spacex_df,entered_site)
    fig = px.pie(graph_df, values='Launch Site', names='class', title='Success vs. Failed counts')
    return [fig]

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# TASK 4: Add a scatter chart to show the correlation between payload and launch success
@app.callback(
    Output("success-payload-scatter-chart", "figure"), 
    Input("payload-slider", "value"))
def update_bar_chart(slider_range):
    df = spacex_df
    low, high = slider_range
    mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
    fig = px.scatter(
        df[mask], x="Payload Mass (kg)", y="class", 
        color="class",
        template="plotly_white"
        )
    fig.update_yaxes(tickvals=[0,1])
    fig.update_traces(marker_size=30)    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
