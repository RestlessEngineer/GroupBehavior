
from Graph import SquareGrid, WeightedGraph, Location
from typing import Iterator

def parse_value(line: str, name: str) -> str:
    ind = line.index(name) + len(name)
    num = ''
    while line[ind].isdigit():
        num += line[ind]
        ind += 1
    return num


class RobotField(SquareGrid, WeightedGraph):


    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self._robots_locations: list[Location] = []


    def reset(self, width: int, height: int):
        super().reset(width, height)
        self._robots_locations = []


    def parse_from_file(self, file_name: str):
         with open(file_name) as f:
            line = f.readline()
            line = ''.join(line.split(sep=' '))
            row = int(parse_value(line, "row="))
            col = int(parse_value(line, "col="))
            self.reset(row, col)
            for i, line in enumerate(f):
                line = ''.join(line.split())
                if i >= row:
                    raise Exception(f'wrong amount of row. row must be {row},\
                                     current row = {i}')
                if not len(line) == col:
                    raise Exception(f'wnamerong amount of col. col must be {col},\
                                     current col = {len(line)}')
                #line parsing
                for j, s in enumerate(line):
                    if s == '#':
                        self.walls.append((i,j))


    def passrobots(self, id: Location) -> bool:
        return id not in self._robots_locations


    def push_robot_location(self, location: Location):
        self._robots_locations.append(location)
    

    def clear_robots_locations(self):
        self._robots_locations.clear()


    def neighbors(self, id: Location) -> Iterator[Location]:
        results = super().neighbors(id)
        results = filter(self.passrobots, results)
        return results


    def cost(self, from_id: Location, to_id: Location) -> float:
        return 1