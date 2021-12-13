import copy

def main():
    cave_system = get_input()
    part1(cave_system)
    part2(cave_system)
    return 0

def get_input():
    f = open("input.txt", "r")
    cave_system = []
    for line in f:
        cave_system.append(line.strip().split("-"))
    return cave_system

def part1(cave_system):
    cave_graph = My_Graph(cave_system)
    cave_graph.build_graph()
    cave_graph.find_journeys()
    cave_graph.give_number_of_journeys()

def part2(cave_system):
    cave_graph_part2 = My_Graph(cave_system)
    cave_graph_part2.build_graph()
    cave_graph_part2.find_journeys_part2()
    cave_graph_part2.give_number_of_journeys()

class My_Graph():
    def __init__(self, cave_system):
        self.nodes = {}
        self.cave_system = cave_system
        # self.visited_small_caves = set()
        self.complete_journeys = []
    
    def build_graph(self):
        for elem in self.cave_system:
            self.build_graph_helper(elem)
    
    def build_graph_helper(self, current_edge):
        node1 = current_edge[0]
        node2 = current_edge[1]
        # Add first direction
        if node1 not in self.nodes:
            self.nodes[node1] = [node2]
        else:
            self.nodes[node1].append(node2)
        # Add second direction
        if node2 not in self.nodes:
            self.nodes[node2] = [node1]
        else:
            self.nodes[node2].append(node1)

    def find_journeys(self):
        journey = ['start']
        for next_step in self.nodes['start']:
            copied_journey = copy.deepcopy(journey)
            copied_journey.append(next_step)
            self.find_journey_recursive(copied_journey)

    def find_journeys_part2(self):
        journey = ['start']
        for next_step in self.nodes['start']:
            copied_journey = copy.deepcopy(journey)
            copied_journey.append(next_step)
            self.find_journey_recursive_part2(copied_journey)

    def find_journey_recursive(self, current_journey):
        # BASE CASE - Reached the end
        if current_journey[-1] == 'end':
            self.complete_journeys.append(current_journey)
            
        # Recursive case - find neigbouring nodes - 
        # do not visit small caves that have already been visited
        else:
            for next_step in self.nodes[current_journey[-1]]:
                # if next_step not in current_journey:
                    copied_journey = copy.deepcopy(current_journey)
                    if next_step.islower() == True and next_step in current_journey:
                        continue
                    copied_journey.append(next_step)
                    self.find_journey_recursive(copied_journey)

    def find_journey_recursive_part2(self, current_journey):
        # BASE CASE - Reached the end
        if current_journey[-1] == 'end':
            self.complete_journeys.append(current_journey)
        else:
            for next_step in self.nodes[current_journey[-1]]:                
                if next_step == "start":
                    continue
                elif next_step == "end":
                    copied_journey = copy.deepcopy(current_journey)
                    copied_journey.append(next_step)
                    self.find_journey_recursive_part2(copied_journey)
                elif next_step.isupper() == True:
                    copied_journey = copy.deepcopy(current_journey)
                    copied_journey.append(next_step)
                    self.find_journey_recursive_part2(copied_journey)
                elif self.can_small_cave_be_visited(current_journey, next_step) == True:
                    copied_journey = copy.deepcopy(current_journey)
                    copied_journey.append(next_step)
                    self.find_journey_recursive_part2(copied_journey)


    def can_small_cave_be_visited(self, current_journey, next_step):
        small_letters_count = {}
        for elem in current_journey:
            if elem.islower() == True:
                if elem not in small_letters_count:
                    small_letters_count[elem] = 1
                else:
                    small_letters_count[elem] += 1
        if next_step not in small_letters_count:
            return True
        
        for key, value in small_letters_count.items():
            if value > 1:
                return False
        return True

    def give_number_of_journeys(self):
        print(len(self.complete_journeys))


main()