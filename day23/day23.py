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
    valid_moves = world.generate_valid_moves()
     

class state_of_world():
    def __init__(self):
        self.total_movement_score = 0
        # self.all_animals = []

        self.room_a = room()
        self.room_b = room()
        self.room_c = room()
        self.room_d = room()
        
        
        # self.room_a = deque([],4)
        # self.room_b = deque([],4)
        # self.room_c = deque([],4)
        # self.room_d = deque([],4)

        # self.room_a_accepting_items = False
        # self.room_b_accepting_items = False
        # self.room_c_accepting_items = False
        # self.room_d_accepting_items = False

        self.all_rooms = [self.room_a, self.room_b, self.room_c, self.room_d]

        self.left_storage_left_item = deque([],1)
        self.left_storage_right_item = deque([],1)

        self.right_storage_left_item = deque([],1)
        self.right_storage_right_item = deque([],1)

        self.between_A_B = deque([],1)
        self.between_B_C = deque([],1)
        self.between_C_D = deque([],1)

        self.top_row = [self.left_storage_left_item, self.left_storage_right_item, self.room_a, self.between_A_B, self.room_b, self.between_B_C, self.room_c, self.between_C_D, self.room_d, self.right_storage_left_item, self.right_storage_right_item]
        
    def generate_valid_moves(self):
        # Part 1 generate valid moves from the rooms up
        # Check the top item on every single room
        valid_moves = []
        for checked_room in self.all_rooms:
            room_valid_moves = self.generate_valid_moves_from_room(checked_room)

    def generate_valid_moves_from_room(self, checked_room):
        current_room = checked_room
        room_status = checked_room.get_room_status()
        # If there are no items in the room, no movements are possible
        if len(checked_room) == 0:
            return []
        # If the room is ready to accept animals, no movements out are possible
        if room_status == True:
            return []
        else:
            top_item = current_room[0]
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

    def find_valid_moves_on_top_row(self, current_room, top_item, initial_top_row_position):
        valid_moves = []
        # Check to the left
        left_rider = initial_top_row_position - 1
        print(left_rider)
        while (left_rider >= 0):
            checked_position = self.top_row[left_rider]
            # Check if the checked position is a storage on the top. If so and it is occupied, break, because you cannot move further
            if checked_position.maxlen == 1 and len(checked_position) == 1:
                break
            # Otherwise add it as a possible position
            elif checked_position.maxlen == 1 and len(checked_position) == 0:
                valid_moves.append((current_room, checked_position))
            # Check if it is a room. If it accepts 
            elif checked_position.maxlen == 4:
                pass

            left_rider -= 1
            

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
        # self.animal_location = animal_location
        self.reached_destination = False
        # self.animal_location = animal_location

class room():
    def __init__ (self):
        self.accepting_animals = False
        self.room_content = deque([],4)
    
    def fill_room(self, room_animals):
        for elem in room_animals:
            created_animal = moving_animal(elem)
            self.room_content.append(created_animal)
    
    def get_room_status(self):
        return self.accepting_animals

main()
