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

    def create_network(self, keys, parent=None):
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
        # compound_parents = []
        nodes_ind = []

        # Initialize parents list
        for col in self.data:
            if parent in col:
                for i in range(self.len):
                    values_i = [self.data.loc[i, key] for key in keys]
                    if all(v == 1 for v in values_i):
                        if self.data.loc[i, col] == 1:
                            if col not in self.parents:
                                self.parents.append(col)

        # Determine filtered installations' position in list
        for n in range(self.len):
            values = [self.data.loc[n, key] for key in keys]
            if all(v == 1 for v in values):
                nodes_ind.append(n)
        
        # Prior evaluation of shared parents
        array = np.array(nodes_ind)
        for i in nodes_ind:
            array = np.delete(array, np.where(array == i))
            node_parent_i = self.evaluate_parents(i)
            if node_parent_i != []:
                for j in array:
                    node_parent_j = self.evaluate_parents(j)
                    if node_parent_j != []:               
                        for p_i in node_parent_i:
                            for p_j in node_parent_j:
                                if p_i == p_j:
                                    shared_parents.append(p_i)

        # # Determine which category to set as a compound
        # for parent in self.parents:
        #     if shared_parents.count(parent) > 5:
        #         compound_parents.append(parent)
  
        # Add nodes
        for i in nodes_ind:
            node_parent_i = self.evaluate_parents(i)
            self.elements.append(dict(
                data=dict(
                    id=self.data.loc[i, 'ID'],
                    label=self.data.loc[i, 'Name'],
                    parent=node_parent_i
                # grabbable=False
                )
            ))
        
        # Edge elements
        array = np.array(nodes_ind)
        for i in nodes_ind:
            array = np.delete(array, np.where(array == i))
            node_parent_i = self.evaluate_parents(i)

            # Continue if node doesn't have any parents 
            if node_parent_i == []:
                continue
            
            # Evaluate remaining installations for siblings
            for j in array:
                node_parent_j = self.evaluate_parents(j)                  

                n_p = len(set(node_parent_i) & set(node_parent_j))

                # Add Edges for Nodes with same parent
                if n_p > 0:
                    self.add_edge(i, j, node_parent_i[0])
                if n_p > 1:
                    self.add_edge(i, j, node_parent_i[1], " bezier")
                if n_p > 2:
                    self.add_edge(i, j, node_parent_i[2], " bezier1")

        # # Generate Compound Elements and Stylesheets
        # if compound_parents != []:
        #     for parent in compound_parents:
        #         self.elements.append(dict(
        #                             data=dict(
        #                                 id=parent
        #                             ), 
        #                         classes= self.colors[self.parents.index(parent)]
        #                         ))
        #         self.stylesheet.append(dict(
        #             selector = '$node > node' + self.colors[self.parents.index(parent)],
        #             style = {
        #                 'background-color': self.colors[self.parents.index(parent)],
        #                 'background-opacity': '0.2',
        #                 'shape': 'roundrectangle',
        #                 'text-background-color': self.colors[self.parents.index(parent)],
        #                 'text-background-opacity': '0.2',
        #                 'border-width': 0.2,
        #             }
        #         ))
                        
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
                'text-background-opacity': '0.7',
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

    def evaluate_parents(self, n):
        node_parent = []
        for col in self.parents:
            if self.data.loc[n, col] == 1:
                node_parent.append(col)
        return node_parent

    def add_edge(self, i, j, node_parent_i, classes = ""):
        self.elements.append(dict(
        data=dict(
            source=self.data.loc[i, 'ID'],
            target=self.data.loc[j, 'ID'],
            label=node_parent_i
        ),
        classes= self.colors[self.parents.index(node_parent_i)] + classes
        ))

