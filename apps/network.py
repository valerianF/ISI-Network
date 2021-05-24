import pandas as pd
import numpy as np

class netObj:
    def __init__(self, data):
        self.data = data
        self.IDs = []
        self.net = {}
        self.len = len(self.data)
        self.elements = []
        self.stylesheet = []

    def initiate_network(self, keys, parent=None):
        """ Create network parents and children nodes and edges. 

        Parameters
        ----------
        keys : list
            Specific taxa from which corresponding nodes are retrieved
        parent : str
            If assigned, groups nodes together in function of the taxon.

        """

        parents = []
        parents_f = []
        colors = ['red', 'blue', 'green','magenta', 'cyan']

        # Initialize parents list
        for col in self.data:
            if parent in col:
                for i in range(self.len):
                    values_i = [self.data.loc[i, key] for key in keys]
                    if all(v == 1 for v in values_i):
                        if self.data.loc[i, col] == 1:
                            if col not in parents:
                                parents.append(col)

        # Node and Edge elements
        array = np.linspace(0, self.len-1, self.len, dtype=int)
        for i in range(self.len):
            values_i = [self.data.loc[i, key] for key in keys]
            if all(v == 1 for v in values_i):
                array = np.delete(array, np.where(array == i))
                n_pi = 0

                # Evaluate Node's parent(s)
                for col in parents:
                    try:
                        if self.data.loc[i, col] == 1:
                            if n_pi == 0:
                                node_parent_i = [col]
                                n_pi += 1
                            else:
                                node_parent_i.append(col)
                    except KeyError:
                        continue

                # Add Node
                self.elements.append(dict(
                    data=dict(
                        id=self.data.loc[i, 'ID'],
                        label=self.data.loc[i, 'Name'],
                        parent=node_parent_i
                    # grabbable=False
                    )
                ))
                for j in array:
                    values_j = [self.data.loc[j, key] for key in keys]
                    if all(v == 1 for v in values_j):
                        # Evaluate Node's parent(s)
                        n_pj = 0
                        for col in parents:
                            try:
                                if self.data.loc[j, col] == 1:
                                    if n_pj == 0:
                                        node_parent_j = [col]
                                        n_pj += 1
                                    else:
                                        node_parent_j.append(col) 
                            except KeyError:
                                continue

                        if (any([p in node_parent_i for p in node_parent_j])):
                            n_p = 0
                            ind = []
                            for p in node_parent_j:
                                if p in node_parent_i:
                                    n_p += 1
                                    ind.append(node_parent_i.index(p))

                            # Add Edges for Nodes with same parent
                            self.elements.append(dict(
                            data=dict(
                                source=self.data.loc[i, 'ID'],
                                target=self.data.loc[j, 'ID'],
                                label=node_parent_i
                            ),
                            classes= colors[parents.index(node_parent_i[ind[0]])]
                            ))
                            if n_p == 2:
                                self.elements.append(dict(
                                data=dict(
                                    source=self.data.loc[i, 'ID'],
                                    target=self.data.loc[j, 'ID'],
                                    label=node_parent_i
                                ),
                                classes= colors[parents.index(node_parent_i[ind[1]])] +
                                    " " + 'bezier'
                                ))
                            if n_p == 3:
                                self.elements.append(dict(
                                data=dict(
                                    source=self.data.loc[i, 'ID'],
                                    target=self.data.loc[j, 'ID'],
                                    label=node_parent_i
                                ),
                                classes= colors[parents.index(node_parent_i[ind[2]])] +
                                    " " + 'bezier1'
                                ))

        # Generate Stylesheets
        for parent in parents:
            self.stylesheet.append(dict(
                selector = '.' + colors[parents.index(parent)],
                style = {
                    'line-color': colors[parents.index(parent)]
                }
            ))
        
        self.stylesheet.append(dict(
            selector = 'node',
            style = {
                'label': 'data(label)',
                'background-color':  '#BABABA',
                'border-width': '3',
                'border-style': 'solid',
                'border-color': 'black',
                'color': 'black',
                'text-background-color': 'white',
                'text-background-opacity': '1',
                'text-backgroun-shape': 'round-rectangle',
                'text-margin-y': '-5px',
                'font-family': 'FontBold, sans-serif'
            }
        ))

        self.stylesheet.append(dict(
            selector = 'edge.bezier',
            style = {
                "curve-style": "unbundled-bezier",
                "control-point-distances": 120,
                "control-point-weights": 0.1              
            }
        ))

        self.stylesheet.append(dict(
            selector = 'edge.bezier1',
            style = {
                "curve-style": "unbundled-bezier",
                "control-point-distances": 150,
                "control-point-weights": 0.4              
            }
        ))

