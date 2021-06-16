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

""" Local functions """
def doi_to_url(link):
    """ Converts the doi into a proper url.
    If the input is a link, returns it unchanged.
    Parameters
    ----------
    link : str
        Doi number.
    """
    if re.match('10.', link):
        return 'https://doi.org/' + link
    elif re.match('DOI:', link):
        return re.sub('DOI:', 'https://doi.org/', link)
    elif re.match('doi:', link):
        return re.sub('doi:', 'https://doi.org/', link)
    else:
        return link

""" External Stylesheet """
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

""" App initialization """
app = dash.Dash(__name__, 
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
    title='ISI Database',
    update_title='Loading...')

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

""" Define categories for composite links """
multi_cats = ["TS_", "LS_", "SD_"]

""" Setting lists. Hard to automatize..."""
labellist = AI.labels[12:] + IN.labels[7:] + SD.labels[18:] + FI.labels[13:]
IDlist = AI.df['ids'][12:].tolist() + IN.df['ids'][7:].tolist() + SD.df['ids'][18:].tolist() + FI.labels[13:]
parentlist = AI.parentslabels[12:] + IN.parentslabels[7:] + SD.parentslabels[18:] + FI.parents[13:]

linkIDlist0 = AI.df['ids'][1:12].tolist() + IN.df['ids'][1:7].tolist() + SD.df['ids'][1:18].tolist()
linkparentlist = AI.labels[1:12] + IN.labels[1:7] + SD.labels[1:18]

linkIDlist = [x for x in linkIDlist0 if (x not in ['IT', 'SP', 'IDof', 'ODof'] and not x.startswith(tuple(multi_cats)))]
linkparentlist = [x for x in linkparentlist if linkparentlist.index(x) in [linkIDlist0.index(n) for n in linkIDlist]]

compIDlist = ['TS_Ima', 'TS_Con', 'TS_Det', 'TS_Ide', 'TS_Ser', 'TS_Mic', 'TS_Mec', 'TS_Env', 'TS_Bio', 'TS_Ele']
complabellist = ['Image Sensors', 'Controllers', 'Detectors', 'Identification', 'Server-Client', 'Microphones',
    'Force and Pressure Sensors', 'Environment Sensors', 'Bio-Signals Sensors', 'Electric, Magnetic Sensors']


""" Application Layout """
app.layout = html.Div([

    html.H2('Interactive Sound Installations Database | Network Visualization Prototype'),

    html.Div([
        cyto.Cytoscape(
            id='main_network',
            layout={
                'name':'cose',
                'nodeDimensionsIncludeLabels': 'true'
                },
            style={'font-family': 'FontBold, sans-serif'},
            elements = [],
            stylesheet = [],
            minZoom=0.3,
            maxZoom=1
        )
    ]),

    html.Div(
        id='network_legend',
        className = 'legend'
    ),

    html.P(style={'paddingBottom': '0cm'}), 

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown_link',
                options = [
                    {
                    'label': re.sub('<br>', ' ', linkparentlist[i]),
                    'value': linkparentlist[i]
                    } for i in range(0, len(linkparentlist))
                    ],
                multi=True, # A single category to filter installations
                placeholder="Select one or more categories to link installations",
                style={
                        'height': '200%'
                        }
            ),
        ], style={'width': '49%', 'display': 'inline-block'}),

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
                        'height': '200%'
                        }
            ),
        ], style={'width': '49%', 'display': 'inline-block', 'margin-left': '2%'}),
    ]),
    
    html.P(style={'paddingBottom': '0cm'}),

    html.Div(id='tap_node')

])

@app.callback([
    Output('main_network', 'elements'),
    Output('main_network', 'stylesheet'),
    Output('network_legend', 'children'),
    Output('main_network', 'style')
    ], [Input('dropdown_filter', 'value'),
    Input('dropdown_link', 'value')])
def update_elements(input_cat, input_link):

    output_values = []
    output_link = []
    legend = ""
    content = []

    if (input_cat is not None and input_cat != []) and (input_link is not None and input_link != []):
        
        for input_value in input_cat:
            output_values.append(IDlist[labellist.index(input_value)]) 

        for link in input_link:
            output_link.append(linkIDlist[linkparentlist.index(link)])    
        
        net = netObj(data)
        net.create_network(output_values, parent=output_link)

        if not net.cat_check:
            return [], [], [html.H4("""You have chosen too many categories to link installations. Try to remove one or more categories.""")], {'width': '100%', 'height': '0vh'}

        elements = net.elements
        stylesheet = net.stylesheet

        for link in output_link:
            if output_link == 'TS':
                legend += ' | Type of Input Device'
            else:
                legend += ' | ' + re.sub('<br>', ' ', linkparentlist[linkIDlist.index(link)])

        legend = legend[2:]

        children = [
            html.Legend(html.H4(html.B(legend)))
        ]

        for parent in net.parents:
            if 'TS' in parent:
                children.extend([
                    html.Span(className=net.colors[net.parents.index(parent)]),
                    html.Li(re.sub('<br>', ' ', complabellist[compIDlist.index(parent)]))
                ])
            else:
                children.extend([
                    html.Span(className=net.colors[net.parents.index(parent)]),
                    html.Li(re.sub('<br>', ' ', labellist[IDlist.index(parent)]))
                ])

        return elements, stylesheet, [html.Fieldset(children)], {'width': '100%', 'height': '70vh'}
    else:
        return [], [], [html.H4("""Please select at least a category on each the dropdown lists below.""")], {'width': '100%', 'height': '0vh'}

@app.callback(
    Output('tap_node', 'children'),
    [Input('main_network', 'tapNodeData')])
def tap_node_data(tapdata):

    if tapdata is not None and tapdata != []:
        for i in range(0, len(data)):
            if data.iloc[i]['Name'] == tapdata['label']:
                break

        row = []
        for col in data.columns[[1, 2, 6, 5, 3]]:
            value = data.iloc[i][col]
            if col == 'Hyperlink':
                cell = html.Td(html.A(href=doi_to_url(value), children='Click Here', target='_blank'))                    
            else:
                cell = html.Td(value)
            row.append(cell)
        return [
            html.H5("You recently tapped this installation:"),
            html.Table(
                [html.Th(col) for col in data.columns[[1, 2, 6, 5, 3]]]
                + [html.Tr(row)]
            )
        ]

if __name__ == '__main__':
    app.run_server(debug=True)