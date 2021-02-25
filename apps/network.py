import pandas as pd
import numpy as np

class netObj:
    def __init__(self, data):
        self.data = data
        self.IDs = []
        self.net = {}
        self.len = len(self.data)
        self.elements = []

    def initiate_network(self, keys):

        # Nodes elements
        for i in range(self.len):
            self.elements.append(dict(
                data=dict(
                    id=self.data.loc[i, 'ID'],
                    label=self.data.loc[i, 'Name']
                    ),
                # grabbable=False
                ))

        # Edge elements
        array = np.linspace(0, self.len-1, self.len, dtype=int)
        for i in range(self.len):
            values_i = [self.data.loc[i, key] for key in keys]
            for key in keys:
                values_i.append(self.data.loc[i, key])
            if all(v == 1 for v in values_i):
                array = np.delete(array, np.where(array == i))
                for j in array:
                    values_j = [self.data.loc[j, key] for key in keys]
                    if all(v == 1 for v in values_j):
                        self.elements.append(dict(
                           data=dict(
                               source=self.data.loc[i, 'ID'],
                               target=self.data.loc[j, 'ID'],
                               label='Node {x} to {y}'.format(x=self.data.loc[i, 'ID'],
                                                              y=self.data.loc[j, 'ID'])
                           ) 
                        ))
