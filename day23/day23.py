def main():
    world = state_of_world()
    valid_moves = world.generate_valid_moves()
     

class state_of_world():
    def __init__(self):
        self.room_a = ["A", "D", "D", "D"]
        self.room_b = ["C", "C", "B", "A"]
        self.room_c = ["B", "B", "A", "D"]
        self.room_d = ["C", "A", "C", "B"]

        self.left_storage = [0,0]
        self.right_storage = [0,0]

        self.between_A_B = [0]
        self.between_B_C = [0]
        self.between_C_D = [0]
    
    def is_world_final(self):
        for elem in self.room_a:
            if elem != "A":
                return False
        for elem in self.room_b:
            if elem != "B":
                return False
        for elem in self.room_c:
            if elem != "C":
                return False
        for elem in self.room_d:
            if elem != "D":
                return False
        return True
    
    def generate_valid_moves(self):
        valid_moves = []
        # Generate moves from room A
        for i in range(4):
            if self.room_a != 0:
                animal_value = self.room_a[i]
                




    

    

main()
