from inspect import getsourcefile
import os.path
import sys

current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
parent_parent_dir = parent_dir[:parent_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_parent_dir)

from Strategy import NashStrategy
import numpy as np
import math

class TestNashStrategy:
    def test_pure_minmax(self):
        profit_mtx = np.array([[1, 2], [-1, -2]])
        stratey_num = NashStrategy().choose_strategy(profit_mtx)
        assert stratey_num == 0
    

    def test_pure_multiple_strategies(self):
        profit_mtx = np.array([[0, 0, 0, 0, -1, -2, -1],
                               [0, 0, 0, 0, -1, -2, -1],
                               [0, 0, 0, 0, -1, -2, -1],
                               [1, 1, 1, 1,  0, -1,  0],
                               [0, 0, 0, 0, -1, -2, -1],
                               [1, 1, 1, 1,  0, -1,  0],
                               [1, 1, 1, 1,  0, -2,  0]])
        
        _, probabilities = NashStrategy()._solve_strategy(profit_mtx)
        stratey_num = NashStrategy().choose_strategy(profit_mtx)
        num_strategies = len(list(filter(lambda x: x > 0, probabilities)))
        assert math.isclose(np.sum(probabilities), 1.0)
        assert stratey_num == 3 or stratey_num == 5 
        assert num_strategies == 2

    def test_mixed_strategies(self):
        profit_mtx = np.array([[6, -2, 3],
                               [-4, 5, 4]])
        
        _, probabilities = NashStrategy()._solve_strategy(profit_mtx)
        stratey_num = NashStrategy().choose_strategy(profit_mtx)
        num_strategies = len(list(filter(lambda x: x > 0, probabilities)))
        assert math.isclose(np.sum(probabilities), 1.0)
        assert math.isclose(probabilities[0], 9/17) and math.isclose(probabilities[1], 8/17) 
        assert num_strategies == 2

    
