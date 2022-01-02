import ast
import math
import copy

def get_input():
    f = open("input.txt", "r")
    converted_instructions = []
    for i, j in enumerate(f):
        converted_instructions.append(ast.literal_eval(j.strip()))
    return converted_instructions

def main():
    instructions = get_input()
    part1(instructions)
    instructions = get_input()
    part2(instructions)

def part1(instructions):
    converted_to_trees = []
    for elem in instructions:
        converted_to_trees.append(MyTree(elem))
    initial_tree = converted_to_trees[0]
    for i in range(1, len(converted_to_trees)):
        initial_tree.add_new_tree(converted_to_trees[i])
        initial_tree.run_reduction_operations()
    print(initial_tree.calculate_magnitude(initial_tree.get_top_node()))
    return 0

def part2(instructions):
    converted_to_trees = []
    for elem in instructions:
        converted_to_trees.append(MyTree(elem))
    top_score = 0
    for i in range(len(converted_to_trees)):
        for j in range(len(converted_to_trees)):
            if i != j:
                temp_tree_1 = copy.deepcopy(converted_to_trees[i])
                temp_tree_2 = copy.deepcopy(converted_to_trees[j])
                temp_tree_1.add_new_tree(temp_tree_2)
                temp_tree_1.run_reduction_operations()
                temp_result = temp_tree_1.calculate_magnitude(temp_tree_1.get_top_node())
                if temp_result > top_score:
                    top_score = temp_result
    print(top_score)
    return 0

class MyTree():
    def __init__(self, original_instructions):
        self.top_node = Node(None, None, None, 0)
        if isinstance(original_instructions[0], list):
            left_item = self.recursive_tree_builder_function(original_instructions[0], self.top_node, 1)
        else:
            left_item = original_instructions[0]
        if isinstance(original_instructions[1], list):
            right_item = self.recursive_tree_builder_function(original_instructions[1], self.top_node, 1)
        else:
            right_item = original_instructions[1]
        self.top_node.set_left_item(left_item)
        self.top_node.set_right_item(right_item)

    def recursive_tree_builder_function(self, provided_instruction, parent_node, depth_level):
        inserted_node = Node(None, None, parent_node, depth_level)
        if isinstance(provided_instruction[0], list):
            left_item = self.recursive_tree_builder_function(provided_instruction[0], inserted_node, depth_level + 1)
        else:
            left_item = provided_instruction[0]
        if isinstance(provided_instruction[1], list):
            right_item = self.recursive_tree_builder_function(provided_instruction[1], inserted_node, depth_level + 1)
        else:
            right_item = provided_instruction[1]
        inserted_node.set_left_item(left_item)
        inserted_node.set_right_item(right_item)
        return inserted_node
    
    def get_top_node(self):
        return self.top_node
    
    def run_reduction_operations(self):
        while True:
            had_there_been_explosion = self.run_explosion_operations()
            if had_there_been_explosion == True:
                continue
            had_there_been_splits = self.run_split_operations(self.top_node)
            if had_there_been_explosion == False and had_there_been_splits == False:
                break

    def run_explosion_operations(self):
        explosion_occurrence = self.run_explosion_operations_recursive_helper(self.top_node.get_left_item())
        if explosion_occurrence == False:
            explosion_occurrence = self.run_explosion_operations_recursive_helper(self.top_node.get_right_item())
        return explosion_occurrence
    
    def run_explosion_operations_recursive_helper(self, checked_item):
        if isinstance(checked_item, int) == True:
            return False
        else:
            if checked_item.get_depth() > 3:
                # TODO --- CHECK HOW TO PROPERLY MERGE UP
                left_exploded_figure = checked_item.get_left_item()
                right_exploded_figure = checked_item.get_right_item()
                # Determine whether the checked node is the left or right item of its parent
                if checked_item.get_parent_item().get_left_item() is checked_item:
                    checked_item.get_parent_item().set_left_item(0)
                    if isinstance(checked_item.get_parent_item().get_right_item(), int):
                        checked_item.get_parent_item().set_right_item(checked_item.get_parent_item().get_right_item() + right_exploded_figure)
                    else:
                        self.find_nearest_down_destination(right_exploded_figure, checked_item.get_parent_item(), "left")
                    self.find_nearest_up_destination(left_exploded_figure, checked_item.get_parent_item(), "left")

                elif checked_item.get_parent_item().get_right_item() is checked_item:
                    checked_item.get_parent_item().set_right_item(0)
                    if isinstance(checked_item.get_parent_item().get_left_item(), int):
                        checked_item.get_parent_item().set_left_item(checked_item.get_parent_item().get_left_item() + left_exploded_figure)
                    else:
                        self.find_nearest_down_destination(left_exploded_figure, checked_item.get_parent_item(), "right")
                    self.find_nearest_up_destination(right_exploded_figure, checked_item.get_parent_item(), "right")
                return True
            else:
                explosion_occurrence = self.run_explosion_operations_recursive_helper(checked_item.get_left_item())
                if explosion_occurrence == False:
                    explosion_occurrence = self.run_explosion_operations_recursive_helper(checked_item.get_right_item())
                return explosion_occurrence

    # TODO --- Improve all checks to make sure it goes properly up and down through the tree
    def find_nearest_up_destination(self, exploded_figure, checked_node, direction):
        parent_item = checked_node.get_parent_item()
        if parent_item != None:
            if direction == "left":
                potential_target = parent_item.get_left_item()
            elif direction == "right":
                potential_target = parent_item.get_right_item()
            
            if potential_target is checked_node:
                if parent_item != None:
                    self.find_nearest_up_destination(exploded_figure, parent_item, direction)

            elif isinstance(potential_target, int):
                if direction == "left":
                    parent_item.set_left_item(parent_item.get_left_item() + exploded_figure)
                elif direction == "right":
                    parent_item.set_right_item(parent_item.get_right_item() + exploded_figure)
            
            elif isinstance(potential_target, Node):
                if direction == "left":
                    converted_direction = "right"
                elif direction == "right":
                    converted_direction = "left" 
                self.find_nearest_down_destination(exploded_figure, potential_target, converted_direction)

    def run_split_operations(self, checked_node):
        left_node = checked_node.get_left_item()
        right_node = checked_node.get_right_item()
        if isinstance(left_node, int) == True:
            if (left_node >= 10):
                split_node = self.create_split_node(left_node, checked_node)
                checked_node.set_left_item(split_node)
                return True
        
        if isinstance(left_node, Node):
            split_operation_result_level_below = self.run_split_operations(left_node)
            if split_operation_result_level_below == True:
                return True

        if isinstance(right_node, int) == True:
            if (right_node >= 10):
                split_node = self.create_split_node(right_node, checked_node)
                checked_node.set_right_item(split_node)
                return True
        
        if isinstance(right_node, Node):
            split_operation_result_level_below = self.run_split_operations(right_node)
            if split_operation_result_level_below == True:
                return True
        return False

    def create_split_node(self, split_node_value, parent_node):
        left_figure = math.floor(split_node_value / 2)
        right_figure = math.ceil(split_node_value / 2)
        split_node = Node(left_figure, right_figure, parent_node, parent_node.get_depth() + 1)
        return split_node

    def find_nearest_down_destination(self, exploded_figure, checked_item, direction):
        if direction == "left":
            potential_target = checked_item.get_left_item()
        elif direction == "right":
            potential_target = checked_item.get_right_item()
        
        if isinstance(potential_target, int):
            if direction == "left":
                checked_item.set_left_item(checked_item.get_left_item() + exploded_figure)
            elif direction == "right":
                checked_item.set_right_item(checked_item.get_right_item() + exploded_figure)
        
        elif isinstance(potential_target, Node):
            self.find_nearest_down_destination(exploded_figure, potential_target, direction)
    
    def calculate_magnitude(self, checked_node):
        if isinstance(checked_node.get_left_item(), int):
            left_part = 3 * checked_node.get_left_item()
        elif isinstance(checked_node.get_left_item(), Node):
            left_part = 3 * self.calculate_magnitude(checked_node.get_left_item())
        
        if isinstance(checked_node.get_right_item(), int):
            right_part = 2 * checked_node.get_right_item()
        elif isinstance(checked_node.get_right_item(), Node):
            right_part = 2 * self.calculate_magnitude(checked_node.get_right_item())
        
        total_magnitude = left_part + right_part
        return total_magnitude
    
    def set_new_top_node(self, new_top_node):
        self.top_node = new_top_node
    
    def add_new_tree(self, added_tree):
        new_top_node = Node(self.get_top_node(), added_tree.get_top_node(), None, 0)
        former_self_parent = self.get_top_node()
        former_added_parent = added_tree.get_top_node()

        # Update the connections to the top figures
        former_self_parent.set_parent_item(new_top_node)
        former_added_parent.set_parent_item(new_top_node)
        self.set_new_top_node(new_top_node)

        # Update the depth figures
        self.update_depth_figures(self.get_top_node().get_left_item())
        self.update_depth_figures(self.get_top_node().get_right_item())

    def update_depth_figures(self, current_node):
        if isinstance(current_node, Node):
            current_node.set_depth(current_node.get_depth() + 1)
            self.update_depth_figures(current_node.get_left_item())
            self.update_depth_figures(current_node.get_right_item())
        
class Node():
    def __init__(self, left_item, right_item, parent_item, depth):
        self.left_item = left_item
        self.right_item = right_item
        self.parent_item = parent_item
        self.depth = depth
    
    def get_left_item(self):
        return self.left_item
    
    def get_right_item(self):
        return self.right_item
    
    def get_depth(self):
        return self.depth

    def get_parent_item(self):
        return self.parent_item

    def set_left_item(self, new_left_item):
        self.left_item = new_left_item
    
    def set_right_item(self, new_right_item):
        self.right_item = new_right_item
    
    def set_parent_item(self, new_parent):
        self.parent_item = new_parent
    
    def set_depth(self, new_depth):
        self.depth = new_depth
    
main()