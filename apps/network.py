import pandas as pd

class netObj:
    def __init__(self, data):
        self.data = data
        self.IDs = []
        self.net = {}

    def initiate_network(self):

        for i in range(len(self.data)):
            print(self.data.loc[i, 'Name'])