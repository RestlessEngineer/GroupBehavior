# GroupBehavior

The main goal of this project is to explore a new method of managing a group of robots.

## Intuition

The goal is to avoid overloading the centralized control system and let the robots decide how to drive on their own based on the information they have.
It is assumed that robots can have an idea of where their nearest neighbors are looking and what their status is (pass or fail).
The idea behind the algorithm is to create a kind of game for each robot. The solution of the route optimization problem in such a game is reduced to obtaining the maximum gain at a given step. 
Thus, instead of searching for an optimal algorithm of robots' behavior at each step, it is enough to find such a game, which will be the most optimal.

## Current state

Right now, a very simple game strategy is suggested. It is assumed that the most favorable direction for the next step will give 2 points. The direction that is opposite to it will give 0. The others will give 1. How it all works can be seen in examples/simple_field


## Acknowledgements

Many thanks to the site https://www.redblobgames.com/pathfinding/a-star/ and Red Blob Games <redblobgames@gmail.com> for their work. My main data structures are based on their code