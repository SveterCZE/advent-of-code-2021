from collections import deque
import copy
import time

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
    states_of_world = {}
    final_scores = set()
    check_possible_worlds(world, final_scores, states_of_world)
    print(final_scores)
    print("Minimum:")
    print(min(final_scores))
    print("Maximum:")
    print(max(final_scores))
    print("Various states explored:")
    print(len(states_of_world))

def check_possible_worlds(world, final_scores, states_of_world):
    # Base case --- We have found a world that was resolved successfully
    if world.is_finished() == True:
        achieved_score = world.total_movement_score
        if achieved_score not in final_scores:
            final_scores.add(achieved_score)
            print(achieved_score)
        return
    # Recursive case --- (1) generate possible valid moves, (2) generate a deep copy of each world, (3) apply the movement and (4) recursively call this function
    # Generate new worlds only if there are no final scores or the scores of the current world are lower than the minimum achieved score
    elif len(final_scores) == 0 or world.total_movement_score < min(final_scores):
        valid_moves = world.generate_valid_moves()
        valid_moves.sort(key = lambda x: x[2])
        if len(valid_moves) > 0:
            for applied_move in valid_moves:
                alternative_world = copy.deepcopy(world)
                alternative_world.make_movement(applied_move)
                current_state_of_world = alternative_world.export_state_of_world()
                if current_state_of_world not in states_of_world or states_of_world[current_state_of_world] > alternative_world.total_movement_score:
                    states_of_world[current_state_of_world] = alternative_world.total_movement_score
                    check_possible_worlds(alternative_world, final_scores, states_of_world)
    # print(valid_moves)


class state_of_world():
    def __init__(self):
        self.total_movement_score = 0
        # self.all_animals = []

        self.room_a = room("A")
        self.room_b = room("B")
        self.room_c = room("C")
        self.room_d = room("D")
        
        self.all_rooms = [self.room_a, self.room_b, self.room_c, self.room_d]

        self.left_storage_left_item = top_row_storage()
        self.left_storage_right_item = top_row_storage()

        self.right_storage_left_item = top_row_storage()
        self.right_storage_right_item = top_row_storage()

        self.between_A_B = top_row_storage()
        self.between_B_C = top_row_storage()
        self.between_C_D = top_row_storage()

        self.all_storages = [self.left_storage_left_item, self.left_storage_right_item, self.between_A_B, self.between_B_C, self.between_C_D, self.right_storage_left_item, self.right_storage_right_item]
        self.top_row = [self.left_storage_left_item, self.left_storage_right_item, self.room_a, self.between_A_B, self.room_b, self.between_B_C, self.room_c, self.between_C_D, self.room_d, self.right_storage_left_item, self.right_storage_right_item]
    
    def export_state_of_world(self):
        exported_state_of_world = (self.left_storage_left_item.get_representation(), self.left_storage_right_item.get_representation(), self.room_a.get_representation(), 
            self.between_A_B.get_representation(), self.room_b.get_representation(), self.between_B_C.get_representation(), self.room_c.get_representation(), self.between_C_D.get_representation(), 
            self.room_d.get_representation(), self.right_storage_left_item.get_representation(), self.right_storage_right_item.get_representation())
        return exported_state_of_world

    def is_finished(self):
        # If some of the rooms is not fully occupied, return false
        if self.room_a.get_room_occupancy() != 4 or self.room_b.get_room_occupancy() != 4 or self.room_c.get_room_occupancy() != 4 or self.room_d.get_room_occupancy() != 4:
            return False
        for elem in self.room_a.get_all_room_animals():
            if elem.get_animal_class() != "A":
                return False
        for elem in self.room_b.get_all_room_animals():
            if elem.get_animal_class() != "B":
                return False
        for elem in self.room_c.get_all_room_animals():
            if elem.get_animal_class() != "C":
                return False
        for elem in self.room_d.get_all_room_animals():
            if elem.get_animal_class() != "D":
                return False
        return True

    def make_movement(self, possible_movement):
        self.total_movement_score += possible_movement[2]
        moved_item = self.top_row[possible_movement[0]].extract_top_animal()
        self.top_row[possible_movement[1]].insert_new_animal(moved_item)

    def generate_valid_moves(self):
        # Part 1 generate valid moves from the rooms up
        # Check the top item on every single room
        all_valid_moves = []
        for checked_storage in self.all_storages:
            storage_valid_moves = self.generate_valid_moves_from_storage(checked_storage)
            all_valid_moves += storage_valid_moves
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

    def generate_valid_moves_from_storage(self, checked_storage):
        # If the storage is empty, return empty --- no movements will be possible
        if checked_storage.is_storage_occupied() == False:
            return []
        # If not empty, determine the letter of its animal
        else:
            valid_move = []
            animal_letter = checked_storage.get_top_animal().get_animal_class()
            # Determine if the corresponding room accepts new animals
            if self.accepts_animals(animal_letter) == True:
                # If so, check that there is a space between the storage and the target room
                top_row_position, target_position = self.determine_checked_storage_and_target_room_nos(checked_storage, animal_letter)
                # Check that there is a space between the two
                if self.can_insert_animal_from_storage(top_row_position, target_position) == True:
                    journey_distance = self.calculate_distance_between_items(checked_storage, self.top_row[target_position], top_row_position)
                    journey_weighted_value = self.calculate_weighted_value(journey_distance, top_row_position)
                    valid_move.append((top_row_position, target_position, journey_weighted_value))
            return valid_move

    def can_insert_animal_from_storage(self, start_position, target_position):
        if start_position < target_position:
            rider = start_position + 1
            while True:
                if isinstance(self.top_row[rider], top_row_storage):
                    if self.top_row[rider].is_storage_occupied() == True:
                        return False
                if rider == target_position:
                    return True
                rider +=1
        elif start_position > target_position:
            rider = start_position - 1
            while True:
                if isinstance(self.top_row[rider], top_row_storage):
                    if self.top_row[rider].is_storage_occupied() == True:
                        return False
                if rider == target_position:
                    return True
                rider -= 1

    def determine_checked_storage_and_target_room_nos(self, checked_storage, animal_letter):
        # Determine its number of the top row
                if checked_storage == self.left_storage_left_item:
                    top_row_position = 0
                elif checked_storage == self.left_storage_right_item:
                    top_row_position = 1
                elif checked_storage == self.between_A_B:
                    top_row_position = 3
                elif checked_storage == self.between_B_C:
                    top_row_position = 5
                elif checked_storage == self.between_C_D:
                    top_row_position = 7
                elif checked_storage == self.right_storage_left_item:
                    top_row_position = 9
                elif checked_storage == self.right_storage_right_item:
                    top_row_position = 10
                
                # Determine the top row number of the target
                if animal_letter == "A":
                    target_position = 2
                elif animal_letter == "B":
                    target_position = 4
                elif animal_letter == "C":
                    target_position = 6
                elif animal_letter == "D":
                    target_position = 8
                return top_row_position, target_position

    def accepts_animals(self, animal_letter):
        if animal_letter == "A":
            return self.room_a.get_room_status()
        elif animal_letter == "B":
            return self.room_b.get_room_status()
        elif animal_letter == "C":
            return self.room_c.get_room_status()
        elif animal_letter == "D":
            return self.room_d.get_room_status()

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

    def calculate_weighted_value(self, journey_distance, initial_top_row_position):
        moved_value = self.top_row[initial_top_row_position].get_top_animal().get_animal_class()
        if moved_value == "A":
            return journey_distance
        elif moved_value == "B":
            return journey_distance * 10
        elif moved_value == "C":
            return journey_distance * 100
        elif moved_value == "D":
            return journey_distance * 1000

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
                    journey_weighted_value = self.calculate_weighted_value(journey_distance, initial_top_row_position)
                    # valid_moves.append((current_room, checked_position, journey_weighted_value))
                    valid_moves.append((initial_top_row_position, left_rider, journey_weighted_value))
            # Check if it is a room. 
            elif isinstance(checked_position, room):
                # Check if it accepts animals for insertion
                if checked_position.get_room_status() == True:
                    # If so, check if the animals fits into this room and if so, add it there
                    if checked_position.get_room_class() == top_item.get_animal_class():
                        journey_distance = self.calculate_distance_between_items(current_room, checked_position, initial_top_row_position)
                        journey_weighted_value = self.calculate_weighted_value(journey_distance, initial_top_row_position)
                        # valid_moves.append((current_room, checked_position, journey_weighted_value))
                        valid_moves.append((initial_top_row_position, left_rider, journey_weighted_value))
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
                    journey_weighted_value = self.calculate_weighted_value(journey_distance, initial_top_row_position)
                    # valid_moves.append((current_room, checked_position, journey_weighted_value))
                    valid_moves.append((initial_top_row_position, right_rider, journey_weighted_value))
            # Check if it is a room. 
            elif isinstance(checked_position, room):
                # Check if it accepts animals for insertion
                if checked_position.get_room_status() == True:
                    # If so, check if the animals fits into this room and if so, add it there
                    if checked_position.get_room_class() == top_item.get_animal_class():
                        journey_distance = self.calculate_distance_between_items(current_room, checked_position, initial_top_row_position)
                        journey_weighted_value = self.calculate_weighted_value(journey_distance, initial_top_row_position)
                        # valid_moves.append((current_room, checked_position, journey_weighted_value))
                        valid_moves.append((initial_top_row_position, right_rider, journey_weighted_value))
            right_rider += 1
        return valid_moves

    def is_world_final(self):
        for elem in self.all_animals:
            if elem.reached_destination == False:
                return False
        return True

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
        if self.get_room_occupancy() == 0:
            self.accepting_animals = True
        return self.accepting_animals
    
    def get_top_animal(self):
        return self.room_content[0]

    def get_room_class(self):
        return self.room_class
    
    def get_all_room_animals(self):
        return self.room_content
    
    def extract_top_animal(self):
        return self.room_content.popleft()
    
    def insert_new_animal(self, inserted_animal):
        self.room_content.append(inserted_animal)
    
    def get_representation(self):
        temp_representation = []
        for elem in self.room_content:
            temp_representation.append(elem.get_animal_class())
        return (tuple(temp_representation))

class top_row_storage():
    def __init__ (self):
        self.storage_content = deque([],1)
    
    def is_storage_occupied(self):
        if len(self.storage_content) == 0:
            return False
        else:
            return True
    
    def get_top_animal(self):
        return self.storage_content[0]
    
    def extract_top_animal(self):
        return self.storage_content.popleft()

    def insert_new_animal(self, inserted_animal):
        self.storage_content.append(inserted_animal)
    
    def get_representation(self):
        if len(self.storage_content) == 0:
            return "."
        else:
            return self.get_top_animal().get_animal_class()

start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
