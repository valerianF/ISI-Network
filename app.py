import os
import re
import dash 
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
# import plotly.graph_objects as go

from apps.network import netObj
from apps.sunburst import appObj

""" App initialization """
app = dash.Dash(__name__)

""" Importing the datasheet into a pandas dataframe """
data = pd.read_csv(os.path.join(os.getcwd(), 'data', 'installationsList.csv'))

""" Defining the sunburst objects and label arrays."""
AI = appObj(data, 'Artistic Intention')
SD = appObj(data, 'System Design')
IN = appObj(data, 'Interaction')
FI = appObj(data, 'Field')

""" Initiate respective sunburst arrays."""
AI.initiate_arrays()
SD.initiate_arrays()
IN.initiate_arrays()
FI.initiate_arrays()

labellist = AI.labels[12:] + IN.labels[7:] + SD.labels[18:] + FI.labels[13:]
IDlist = AI.df['ids'][12:].tolist() + IN.df['ids'][7:].tolist() + SD.df['ids'][18:].tolist() + FI.labels[13:]
parentlist = AI.parentslabels[12:] + IN.parentslabels[7:] + SD.parentslabels[18:] + FI.parents[13:]

""" Create Network Elements """
net = netObj(data)

""" Application Layout """
app.layout = html.Div([
    html.Div([
        cyto.Cytoscape(
            id='main-network',
            layout={
                'name':'cose',
                'nodeDimensionsIncludeLabels': 'true'
                },
            style={'width': '100%', 'height': '800px'},
            elements = [],
            stylesheet = [],
            minZoom=0.3,
            maxZoom=1
        )
    ]),

    html.Div([
        dcc.Dropdown(
            id='dropdown_cat',
            options = [
                {
                'label': re.sub('<br>', ' ', parentlist[i]) + ' | ' + re.sub('<br>', ' ', labellist[i]),
                'value': labellist[i]
                } for i in range(0, len(labellist))
                ],
            multi=True, # Makes in sort that several categories can be selected
            placeholder="Select one or more categories to filter installations",
            style={
                    'height': '200%',
                    'width' : '500px'
                    }
        ),
        # html.Button('Take a Snapshot', id='snap-button', n_clicks=0, style={'marginLeft': '30px'}),
    ], style={'display': 'flex'}),

])

@app.callback([
    Output('main-network', 'elements'),
    Output('main-network', 'stylesheet')
    ], [Input('dropdown_cat', 'value')])
def update_elements(input_values):

    output_values = []

    if input_values is None or input_values == []:
        net.initiate_network([], parent="IA")
        elements = net.elements
        stylesheet = net.stylesheet
        return elements, stylesheet
    else:
        for input_value in input_values:
            output_values.append(IDlist[labellist.index(input_value)])
        net.initiate_network(output_values, parent="IA")

        elements = net.elements
        stylesheet = net.stylesheet

        return elements, stylesheet




if __name__ == '__main__':
    app.run_server(debug=True)