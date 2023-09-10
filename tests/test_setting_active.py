from inspect import getsourcefile
import os.path
import sys
from collections import Counter

current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
parent_parent_dir = parent_dir[:parent_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_parent_dir)

from Simulation import setting_active  # noqa: E402


class TestSettingActive:
    def test_empty_arrays(self):
        vertices = {}
        adjacencyList={}
        res = setting_active(adjacencyList, vertices)
        assert len(res) == 0
    
    def test_simple_duet(self):
        vertices = {1, 2}
        adjacencyList={}
        for vertex in vertices:
            adjacencyList[vertex]=[]
        adjacencyList[1].append(2)
        adjacencyList[2].append(1)
        res = setting_active(adjacencyList, vertices)
        assert set(res.values()) == {0,1}

    def test_simple_triplet(self):
        vertices = {1, 2, 3}
        adjacencyList={}
        edges = {(1,2), (1,3), (3,2)}
        for vertex in vertices:
            adjacencyList[vertex]=[]
        for edge in edges:
            v1 = edge[0]
            v2 = edge[1]
            adjacencyList[v1].append(v2)
            adjacencyList[v2].append(v1)
        res = setting_active(adjacencyList, vertices)
        count = Counter(res.values())
        assert count[0] == 2 
        assert count[1] == 1

    def test_simple_3_nodes(self):
        vertices = {1, 2, 3}
        adjacencyList={}
        edges = {(1,2), (1,3)}
        for vertex in vertices:
            adjacencyList[vertex]=[]
        for edge in edges:
            v1 = edge[0]
            v2 = edge[1]
            adjacencyList[v1].append(v2)
            adjacencyList[v2].append(v1)
        res = setting_active(adjacencyList, vertices)
        count = Counter(res.values())
        assert count[0] == 1
        assert count[1] == 2
        assert res[1] == 0 

    def test_simple_isolate_nodes(self):
        vertices = {1, 2, 3}
        adjacencyList={}
        edges = {(1,2)}
        for vertex in vertices:
            adjacencyList[vertex]=[]
        for edge in edges:
            v1 = edge[0]
            v2 = edge[1]
            adjacencyList[v1].append(v2)
            adjacencyList[v2].append(v1)
        res = setting_active(adjacencyList, vertices)
        count = Counter(res.values())
        assert count[1] == 1
        assert -1  not in count.keys()
