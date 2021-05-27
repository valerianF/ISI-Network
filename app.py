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

""" Initiate arrays"""
AI.initiate_arrays()
SD.initiate_arrays()
IN.initiate_arrays()
FI.initiate_arrays()

labellist = AI.labels[12:] + IN.labels[7:] + SD.labels[18:] + FI.labels[13:]
IDlist = AI.df['ids'][12:].tolist() + IN.df['ids'][7:].tolist() + SD.df['ids'][18:].tolist() + FI.labels[13:]
parentlist = AI.parentslabels[12:] + IN.parentslabels[7:] + SD.parentslabels[18:] + FI.parents[13:]

linkIDlist = AI.df['ids'][1:12].tolist() + IN.df['ids'][1:7].tolist() + SD.df['ids'][1:18].tolist()
linkparentlist = AI.labels[1:12] + IN.labels[1:7] + SD.labels[1:18]

linkIDlist = [x for x in linkIDlist if x not in ['LS', 'SP', 'TS', 'IT', 'SD', 'SG']]
linkparentlist = [x for x in linkparentlist if x not in 
    ["Visitor\'s<br>Position", "Spatialization", "Type of<br>Input Device", 
    "Interaction<br>Type", "Sound<br>Design", "Sound<br>Generation"]]


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
            id='dropdown_link',
            options = [
                {
                'label': re.sub('<br>', ' ', linkparentlist[i]),
                'value': linkparentlist[i]
                } for i in range(0, len(linkparentlist))
                ],
            multi=False, # A single category to filter installations
            placeholder="Select a category to link installations",
            style={
                    'height': '200%',
                    'width' : '500px'
                    }
        ),
    ], style={'display': 'flex'}),

    html.P(style={'paddingBottom': '0px'}),  

    html.Div([
        dcc.Dropdown(
            id='dropdown_filter',
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
    ], style={'display': 'flex'}),

])

@app.callback([
    Output('main-network', 'elements'),
    Output('main-network', 'stylesheet')
    ], [Input('dropdown_filter', 'value'),
    Input('dropdown_link', 'value')])
def update_elements(input_cat, input_link):

    output_values = []
    output_link = ""

    if input_cat is None or input_cat == []:
        output_values = ['SG_Obj_Mecha']
    else:
        for input_value in input_cat:
            output_values.append(IDlist[labellist.index(input_value)])

    if input_link is None or input_link == []:
        output_link = "IA"
    else:
        output_link = linkIDlist[linkparentlist.index(input_link)]

    net.initiate_network(output_values, parent=output_link)
    elements = net.elements
    stylesheet = net.stylesheet

    return elements, stylesheet




if __name__ == '__main__':
    app.run_server(debug=True)