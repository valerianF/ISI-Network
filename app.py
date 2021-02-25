import os
import dash 
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
# from dash.dependencies import Input, Output
# import plotly.graph_objects as go

from apps.network import netObj

""" App initialization """
app = dash.Dash(__name__)

""" Importing the datasheet into a pandas dataframe """
data = pd.read_csv(os.path.join(os.getcwd(), 'data', 'installationsList.csv'))

net = netObj(data)
net.initiate_network(['IA_Many', 'IDof_One', 'CO_Exhibition'])
elements = net.elements

""" Application Layout """
app.layout = html.Div([
    cyto.Cytoscape(
        id='main-network',
        layout={
            'name': 'concentric',
            'padding': '0'
            },
        style={'width': '100%', 'height': '800px'},
        elements = elements
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)