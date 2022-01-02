import ast

def get_input():
    f = open("sample5.txt", "r")
    converted_instructions = []
    for i, j in enumerate(f):
        converted_instructions.append(ast.literal_eval(j.strip()))
    return converted_instructions

def main():
    instructions = get_input()
    part1(instructions)
    part2(instructions)

def part1(instructions):
    converted_to_trees = []
    for elem in instructions:
        converted_to_trees.append(MyTree(elem))
    for elem in converted_to_trees:
        elem.run_reduction_operations()
    for elem in converted_to_trees:
        print(elem)

def part2(instructions):
    pass

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
            had_there_been_splits = self.run_split_operations()
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
                left_exploded_figure = checked_item.get_left_item()
                right_exploded_figure = checked_item.get_right_item()
                # Determine whether the checked node is the left or right item of its parent
                if checked_item.get_parent_item().get_left_item() is checked_item:
                    checked_item.get_parent_item().set_left_item(0)
                    checked_item.get_parent_item().set_right_item(checked_item.get_parent_item().get_right_item() + right_exploded_figure)
                    # self.find_nearest_up_destination(left_exploded_figure, checked_item.get_parent_item().get_parent_item(), "left")
                    self.find_nearest_up_destination(left_exploded_figure, checked_item.get_parent_item(), "left")

                elif checked_item.get_parent_item().get_right_item() is checked_item:
                    checked_item.get_parent_item().set_right_item(0)
                    checked_item.get_parent_item().set_left_item(checked_item.get_parent_item().get_left_item() + left_exploded_figure)
                    # self.find_nearest_up_destination(right_exploded_figure, checked_item.get_parent_item().get_parent_item(), "right")
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
                # parent = checked_node.get_parent_item()
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
        
        # else:
        #     parent = checked_node.get_parent_item()
        #     if parent != None:
        #         self.find_nearest_up_destination(exploded_figure, parent, direction)

    def run_split_operations(self):
        return False

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
        
        elif isinstance(potential_target, 'Node'):
            self.find_nearest_down_destination(exploded_figure, potential_target, direction)

        
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
    
main()