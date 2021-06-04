import pandas as pd
import numpy as np

class netObj:
    def __init__(self, data):
        self.data = data
        self.len = len(self.data)
        self.elements = []
        self.stylesheet = []
        self.colors = []
        self.parents = []

    def initiate_network(self, keys, parent=None):
        """ Create network parents and children nodes and edges. 

        Parameters
        ----------
        keys : list
            Specific taxa from which corresponding nodes are retrieved
        parent : str
            If assigned, groups nodes together in function of the taxon.

        """

        self.parents = []
        parents_f = []
        self.colors = ['red', 'blue', 'green','magenta', 'cyan', 'black', 'yellow', 'brown']
        self.elements = []
        self.stylesheet = []
        shared_parents = []
        is_compound = []

        # Initialize parents list
        for col in self.data:
            if parent in col:
                for i in range(self.len):
                    values_i = [self.data.loc[i, key] for key in keys]
                    if all(v == 1 for v in values_i):
                        if self.data.loc[i, col] == 1:
                            if col not in self.parents:
                                self.parents.append(col)
                                is_compound.append(False)

        # Prior evaluation of shared parents
        array = np.linspace(0, self.len-1, self.len, dtype=int)
        for i in range(self.len):
            values_i = [self.data.loc[i, key] for key in keys]
            if all(v == 1 for v in values_i):
                array = np.delete(array, np.where(array == i))
                node_parent_i = []

                # Evaluate Node's parent(s)
                for col in self.parents:
                    if self.data.loc[i, col] == 1:
                        node_parent_i.append(col)

                # Continue if node doesn't have any parent
                if node_parent_i == []:
                    continue
                
                # Evaluate remaining installations for siblings
                for j in array:
                    values_j = [self.data.loc[j, key] for key in keys]
                    if all(v == 1 for v in values_j):
                        node_parent_j = []

                        # Evaluate Node's parent(s)
                        for col in self.parents:
                            if self.data.loc[j, col] == 1:
                                node_parent_j.append(col)

                        if (any([p in node_parent_i for p in node_parent_j])):
                            n_p = 0
                            for p in node_parent_i:
                                if p in node_parent_j:
                                    n_p += 1
                                    shared_parents.append(p)
        
        # Node and Edge elements
        array = np.linspace(0, self.len-1, self.len, dtype=int)
        for i in range(self.len):
            values_i = [self.data.loc[i, key] for key in keys]
            if all(v == 1 for v in values_i):
                array = np.delete(array, np.where(array == i))
                node_parent_i = []

                # Evaluate Node's parent(s)
                for col in self.parents:
                    if self.data.loc[i, col] == 1:
                        node_parent_i.append(col)
               
                # Add Node
                self.elements.append(dict(
                    data=dict(
                        id=self.data.loc[i, 'ID'],
                        label=self.data.loc[i, 'Name'],
                        parent=node_parent_i
                    # grabbable=False
                    )
                ))

                # Continue if node doesn't have any parent
                if node_parent_i == []:
                    continue

                
                # Evaluate remaining installations for siblings
                for j in array:
                    values_j = [self.data.loc[j, key] for key in keys]
                    if all(v == 1 for v in values_j):
                        node_parent_j = []

                        # Evaluate Node's parent(s)
                        for col in self.parents:
                            if self.data.loc[j, col] == 1:
                                node_parent_j.append(col)

                        if (any([p in node_parent_i for p in node_parent_j])):
                            n_p = 0
                            for p in node_parent_j:
                                if p in node_parent_i:
                                    n_p += 1

                            if shared_parents.count(node_parent_i[0]) < 5:
                                # Add Edges for Nodes with same parent
                                self.elements.append(dict(
                                data=dict(
                                    source=self.data.loc[i, 'ID'],
                                    target=self.data.loc[j, 'ID'],
                                    label=node_parent_i[0]
                                ),
                                classes= self.colors[self.parents.index(node_parent_i[0])]
                                ))
                                if n_p == 2:
                                    if shared_parents.count(node_parent_i[1]) < 5:
                                        self.elements.append(dict(
                                        data=dict(
                                            source=self.data.loc[i, 'ID'],
                                            target=self.data.loc[j, 'ID'],
                                            label=node_parent_i[1]
                                        ),
                                        classes= self.colors[self.parents.index(node_parent_i[1])] +
                                            " " + 'bezier'
                                        ))
                                    else:
                                        is_compound[self.parents.index(node_parent_i[1])] = True

                                if n_p == 3:
                                    if shared_parents.count(node_parent_i[2]) < 5:
                                        self.elements.append(dict(
                                        data=dict(
                                            source=self.data.loc[i, 'ID'],
                                            target=self.data.loc[j, 'ID'],
                                            label=node_parent_i[2]
                                        ),
                                        classes= self.colors[self.parents.index(node_parent_i[2])] +
                                            " " + 'bezier1'
                                        ))
                                    else:
                                        is_compound[self.parents.index(node_parent_i[2])] = True
                            else:
                                is_compound[self.parents.index(node_parent_i[0])] = True

        for i in range(len(is_compound)):
            if is_compound[i]:
                self.elements.append(dict(
                                    data=dict(
                                        id=self.parents[i]
                                    ),
                                classes= self.colors[i]
                                ))
                self.stylesheet.append(dict(
                    selector = '$node > node' + self.colors[i],
                    style = {
                        'background-color': self.colors[i],
                        'background-opacity': '0.2',
                        'shape': 'roundrectangle',
                        'text-background-color': self.colors[i],
                        'text-background-opacity': '0.2',
                        'border-width': 0.2,
                    }
                ))
                                
        # Generate Stylesheets
        for i in range(len(self.elements)):
            try:
                for j in range(len(self.elements[i]['data']['parent'])):
                    if self.elements[i]['data']['parent'][j] is not [] and self.elements[i]['data']['parent'][j] not in shared_parents:
                        self.elements[i]['classes'] = "no_siblings_" + self.colors[self.parents.index(self.elements[i]['data']['parent'][j])]
                        self.stylesheet.append(dict(
                            selector = "node.no_siblings_" + self.colors[self.parents.index(self.elements[i]['data']['parent'][j])],
                            style = {
                                'background-color': self.colors[self.parents.index(self.elements[i]['data']['parent'][j])]
                            }
                        ))
            except KeyError:
                continue
                            
        for parent in self.parents:
            self.stylesheet.append(dict(
                selector = 'edge.' + self.colors[self.parents.index(parent)],
                style = {
                    'line-color': self.colors[self.parents.index(parent)]
                }
            ))
        
        self.stylesheet.append(dict(
            selector = 'node',
            style = {
                'label': 'data(label)',
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
                "control-point-distances": 8,
                "control-point-weights": 0.5              
            }
        ))

        self.stylesheet.append(dict(
            selector = 'edge.bezier1',
            style = {
                "curve-style": "unbundled-bezier",
                "control-point-distances": -8,
                "control-point-weights": 0.5             
            }
        ))

        self.stylesheet.append(dict(
            selector = ':selected',
            style = {
                "border-width": 4,
                "background-color": "black"
                }
        ))

