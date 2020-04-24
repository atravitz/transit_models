import unittest
import transit_model
import networkx as nx
import random
import numpy as np

class TestBasicSetup(unittest.TestCase):
    def test_import_CTA(self):
        g = nx.read_gml('cta.gml')


class TestSinglePassengers(unittest.TestCase):
    def test_work_home(self):
        g = nx.read_gml('cta.gml')
        transit_model.initialize(itinerary=None)


if __name__ == '__main__':
    unittest.main()