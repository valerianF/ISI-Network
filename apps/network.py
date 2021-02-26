import pandas as pd
import numpy as np

class netObj:
    def __init__(self, data):
        self.data = data
        self.IDs = []
        self.net = {}
        self.len = len(self.data)
        self.elements = []

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

        # Initialize parents list
        for col in self.data:
            if parent in col:
                parents.append(col)

        # Node and Edge elements
        array = np.linspace(0, self.len-1, self.len, dtype=int)
        for i in range(self.len):
            values_i = [self.data.loc[i, key] for key in keys]
            for key in keys:
                values_i.append(self.data.loc[i, key])
            if all(v == 1 for v in values_i):
                array = np.delete(array, np.where(array == i))
                n_pi = 0

                # Evaluate Node's parent(s)
                for col in parents:
                    try:
                        if self.data.loc[i, col] == 1:
                            if n_pi == 0:
                                node_parent_i = col
                                n_pi += 1
                            else:
                                node_parent_i += " " + col 
                                if node_parent_i not in parents:
                                    parents.append(node_parent_i)
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
                                        node_parent_j = col
                                        n_pj += 1
                                    else:
                                        node_parent_j += " " + col 
                            except KeyError:
                                continue

                        # if (any([p in node_parent_i for p in node_parent_j.split()])):
                        if node_parent_j == node_parent_i:

                            # Add Edges for Nodes with same parent
                            self.elements.append(dict(
                            data=dict(
                                source=self.data.loc[i, 'ID'],
                                target=self.data.loc[j, 'ID'],
                                label='Node {x} to {y}'.format(x=self.data.loc[i, 'ID'],
                                                                y=self.data.loc[j, 'ID'])
                            ) 
                            ))

        # Add parent Nodes
        for p in parents:
            self.elements.append(dict(
                data=dict(
                    id=p, 
                    label=p
                )
            ))
