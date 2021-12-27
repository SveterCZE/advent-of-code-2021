import queue
from collections import deque

def main():
    room_a_animals = ["A", "D", "D", "D"]
    room_b_animals = ["C", "C", "B", "A"]
    room_c_animals = ["B", "B", "A", "D"]
    room_d_animals = ["C", "A", "C", "B"]
    world = state_of_world()
    world.room_a.fill_room(room_a_animals)
    world.room_b.fill_room(room_b_animals)
    world.room_c.fill_room(room_c_animals)
    world.room_d.fill_room(room_d_animals)
    # world.print_the_world()
    valid_moves = world.generate_valid_moves()
    print(valid_moves)
     

class state_of_world():
    def __init__(self):
        self.total_movement_score = 0
        # self.all_animals = []

        self.room_a = room("A")
        self.room_b = room("B")
        self.room_c = room("C")
        self.room_d = room("D")
        
        # self.room_a = deque([],4)
        # self.room_b = deque([],4)
        # self.room_c = deque([],4)
        # self.room_d = deque([],4)

        # self.room_a_accepting_items = False
        # self.room_b_accepting_items = False
        # self.room_c_accepting_items = False
        # self.room_d_accepting_items = False

        self.all_rooms = [self.room_a, self.room_b, self.room_c, self.room_d]

        self.left_storage_left_item = top_row_storage()
        self.left_storage_right_item = top_row_storage()

        self.right_storage_left_item = top_row_storage()
        self.right_storage_right_item = top_row_storage()

        self.between_A_B = top_row_storage()
        self.between_B_C = top_row_storage()
        self.between_C_D = top_row_storage()

        self.top_row = [self.left_storage_left_item, self.left_storage_right_item, self.room_a, self.between_A_B, self.room_b, self.between_B_C, self.room_c, self.between_C_D, self.room_d, self.right_storage_left_item, self.right_storage_right_item]
    
    def generate_valid_moves(self):
        # Part 1 generate valid moves from the rooms up
        # Check the top item on every single room
        all_valid_moves = []
        for checked_room in self.all_rooms:
            room_valid_moves = self.generate_valid_moves_from_room(checked_room)
            all_valid_moves += room_valid_moves
            # print("Room:", room_valid_moves)
        return all_valid_moves

    def generate_valid_moves_from_room(self, checked_room):
        current_room = checked_room
        room_status = checked_room.get_room_status()
        # If there are no items in the room, no movements are possible
        if checked_room.get_room_occupancy() == 0:
            return []
        # If the room is ready to accept animals, no movements out are possible
        if room_status == True:
            return []
        # In other cases, you can move animals out of the room
        else:
            top_item = current_room.get_top_animal()
            # Determine its position on the top row
            if (current_room == self.room_a):
                top_row_position = 2
            elif (current_room == self.room_b):
                top_row_position = 4
            elif (current_room == self.room_c):
                top_row_position = 6
            elif (current_room == self.room_d):
                top_row_position = 8
            # Determine possible moves along the top row
            room_valid_moves = self.find_valid_moves_on_top_row(current_room, top_item, top_row_position)
            # print(room_valid_moves)
            return room_valid_moves

    def calculate_distance_between_items(self, start_position, destination_position, initial_top_row_position):
        total_distance = 0
        # If the start position is a room --- calculate a distance to the top row
        if isinstance(start_position, room):
            distance_to_top = 5 - start_position.get_room_occupancy()
            total_distance += distance_to_top
        # Calculate a distance on the top row -- find the index of the destination position
        for i in range(11):
            if self.top_row[i] == destination_position:
                total_distance += abs(initial_top_row_position - i)
                break
        # If the destination is a room --- calculate a distance down to it
        if isinstance(destination_position, room):
            distance_to_bottom = 4 - destination_position.get_room_occupancy()
            total_distance += distance_to_bottom
        return total_distance


    def find_valid_moves_on_top_row(self, current_room, top_item, initial_top_row_position):
        valid_moves = []
        # Check to the left
        left_rider = initial_top_row_position - 1
        while (left_rider >= 0):
            checked_position = self.top_row[left_rider]
            # Check if the checked position is a storage on the top.
            if isinstance(checked_position, top_row_storage):
            # If so and it is occupied, break, because you cannot move further
                if checked_position.is_storage_occupied() == True:
                    break
                # Otherwise add it as a possible position
                elif checked_position.is_storage_occupied() == False:
                    journey_distance = self.calculate_distance_between_items(current_room, checked_position, initial_top_row_position)
                    valid_moves.append((current_room, checked_position, journey_distance))
            # Check if it is a room. 
            elif isinstance(checked_position, room):
                # Check if it accepts animals for insertion
                if checked_position.get_room_status() == True:
                    # If so, check if the animals fits into this room and if so, add it there
                    if checked_position.get_room_class() == top_item.get_animal_class():
                        # TODO - Calculate a distance as well
                        journey_distance = self.calculate_distance_between_items(current_room, checked_position, initial_top_row_position)
                        valid_moves.append((current_room, checked_position, journey_distance))
            left_rider -= 1

        # Check to the right
        right_rider = initial_top_row_position + 1
        while (right_rider <= 10):
            checked_position = self.top_row[right_rider]
            # Check if the checked position is a storage on the top. If so and it is occupied, break, because you cannot move further
            if isinstance(checked_position, top_row_storage):
                if checked_position.is_storage_occupied() == True:
                    break
                # Otherwise add it as a possible position
                elif checked_position.is_storage_occupied() == False:
                    journey_distance = self.calculate_distance_between_items(current_room, checked_position, initial_top_row_position)
                    valid_moves.append((current_room, checked_position, journey_distance))
            # Check if it is a room. 
            elif isinstance(checked_position, room):
                # Check if it accepts animals for insertion
                if checked_position.get_room_status() == True:
                    # If so, check if the animals fits into this room and if so, add it there
                    if checked_position.get_room_class() == top_item.get_animal_class():
                        journey_distance = self.calculate_distance_between_items(current_room, checked_position, initial_top_row_position)
                        valid_moves.append((current_room, checked_position, journey_distance))
            right_rider += 1
        return valid_moves

    def is_world_final(self):
        for elem in self.all_animals:
            if elem.reached_destination == False:
                return False
        return True

    # def fill_a_room(self, room_a_animals):
    #     for elem in room_a_animals:
    #         created_animal = moving_animal(elem, self.room_a)
    #         self.room_a.append(created_animal)
    #         self.all_animals.append(created_animal)
    
    # def fill_b_room(self, room_b_animals):
    #     for elem in room_b_animals:
    #         created_animal = moving_animal(elem, self.room_b)
    #         self.room_b.append(created_animal)
    #         self.all_animals.append(created_animal)
    
    # def fill_c_room(self, room_c_animals):
    #     for elem in room_c_animals:
    #         created_animal = moving_animal(elem, self.room_c)
    #         self.room_c.append(created_animal)
    #         self.all_animals.append(created_animal)
    
    # def fill_d_room(self, room_d_animals):
    #     for elem in room_d_animals:
    #         created_animal = moving_animal(elem, self.room_d)
    #         self.room_d.append(created_animal)
    #         self.all_animals.append(created_animal)


class moving_animal():
    def __init__ (self, animal_class):
        self.actions_taken = 0
        self.animal_class = animal_class
        self.reached_destination = False
    
    def get_animal_class(self):
        return self.animal_class

class room():
    def __init__ (self, room_class):
        self.accepting_animals = False
        self.room_class = room_class
        self.room_content = deque([],4)
    
    def get_room_occupancy(self):
        return len(self.room_content)
    
    def fill_room(self, room_animals):
        for elem in room_animals:
            created_animal = moving_animal(elem)
            self.room_content.append(created_animal)
    
    def get_room_status(self):
        return self.accepting_animals
    
    def get_top_animal(self):
        return self.room_content[0]

    def get_room_class(self):
        return self.room_class

class top_row_storage():
    def __init__ (self):
        self.storage_content = deque([],1)
    
    def is_storage_occupied(self):
        if len(self.storage_content) == 0:
            return False
        else:
            return True
    
    def get_inserted_animal(self):
        return self.storage_content[0]

main()
