import matplotlib.pyplot as plt
import numpy as np
import random

class Malom:
    def __init__(self):
        self.positions = [(-3, -3), (-3, 0), (-3, 3), (0, 3), (3, 3), (3, 0), (3, -3), (0, -3), # Külső négyzet
                          (-2, -2), (-2, 0), (-2, 2), (0, 2), (2, 2), (2, 0), (2, -2), (0, -2), # Középső négyzet
                          (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)] # Belső négyzet
        self.connections = [[(-3, -3), (-3, 0)], [(-3, 0), (-3, 3)], [(-3, 3), (0, 3)], [(0, 3), (3, 3)],
                            [(3, 3), (3, 0)], [(3, 0), (3, -3)], [(3, -3), (0, -3)], [(0, -3), (-3, -3)], # Külső négyzet vonalak
                            [(-2, -2), (-2, 0)], [(-2, 0), (-2, 2)], [(-2, 2), (0, 2)], [(0, 2), (2, 2)],
                            [(2, 2), (2, 0)], [(2, 0), (2, -2)], [(2, -2), (0, -2)], [(0, -2), (-2, -2)], # Középső négyzet vonalak
                            [(-1, -1), (-1, 0)], [(-1, 0), (-1, 1)], [(-1, 1), (0, 1)], [(0, 1), (1, 1)],
                            [(1, 1), (1, 0)], [(1, 0), (1, -1)], [(1, -1), (0, -1)], [(0, -1), (-1, -1)], # Belső négyzet vonalak
                            [(0, -3), (0, -2)], [(0, -2), (0, -1)], [(0, 3), (0, 2)], [(0, 2), (0, 1)],
                            [(-3, 0), (-2, 0)], [(-2, 0), (-1, 0)], [(3, 0), (2, 0)], [(2, 0), (1, 0)]] # Pici vonalak
        self.board = {pos: None for pos in self.positions}
        self.player_pieces = 0
        self.ai_pieces = 0
        self.turn = "Player" # Player kezd
        self.mills = [[(-3, -3), (-3, 0), (-3, 3)], [(-3, 3), (0, 3), (3, 3)], [(3, 3), (3, 0), (3, -3)], [(3, -3), (0, -3), (-3, -3)],
                      [(-2, -2), (-2, 0), (-2, 2)], [(-2, 2), (0, 2), (2, 2)], [(2, 2), (2, 0), (2, -2)], [(2, -2), (0, -2), (-2, -2)],
                      [(-1, -1), (-1, 0), (-1, 1)], [(-1, 1), (0, 1), (1, 1)], [(1, 1), (1, 0), (1, -1)], [(1, -1), (0, -1), (-1, -1)],
                      [(0, -3), (0, -2), (0, -1)], [(0, 3), (0, 2), (0, 1)], [(-3, 0), (-2, 0), (-1, 0)], [(3, 0), (2, 0), (1, 0)]]
    
    def draw_board(self):
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)
        fig.patch.set_facecolor('yellow') # Szép sárga háttér

        for conn in self.connections:
            x, y = zip(*conn)
            ax.plot(x, y, 'k', linewidth=3) # Fekete vonalak
        for pos, piece in self.board.items():
            if piece == "Player": # Fehér Player bábuk
                ax.plot(*pos, 'o', markersize=24, color='#F3E5AB', markeredgecolor='grey')
                ax.plot(*pos, 'o', markersize=16, color='#F3E5AB', markeredgecolor='grey')
                ax.plot(*pos, 'o', markersize=8, color='#F3E5AB', markeredgecolor='grey')
            elif piece == "AI": # Fekete AI bábuk
                ax.plot(*pos, 'o', markersize=24, color='black', markeredgecolor='grey')
                ax.plot(*pos, 'o', markersize=16, color='black', markeredgecolor='grey')
                ax.plot(*pos, 'o', markersize=8, color='black', markeredgecolor='grey')
            else: # Üres helyek
                ax.plot(*pos, 'ko', markersize=10)
        plt.show()

    def is_in_mill(self, player, position):
        possible_mills = [mill for mill in self.mills if position in mill]
        for mill in possible_mills:
            if all(self.board[pos] == player for pos in mill):
                return True
        return False

    def is_valid_removal(self, player, position):
        if self.board.get(position) == player:
            if self.is_in_mill(player, position):
                if all(self.is_in_mill(player, p) == True for p in self.board if self.board[p] == player): 
                    return True
                return False
            return True
        return False

    def remove_opponent_piece(self, opponent):
        if opponent == "AI":
            pos = tuple(map(int, input("Az ellenfél leveendő bábuja: ").split(",")))
            valid = self.is_valid_removal("AI", pos)
            while valid is not True:
                print("Ezt nem lehet! Próbáld újra!")
                self.draw_board()
                pos = tuple(map(int, input("Az ellenfél leveendő bábuja: ").split(",")))
                valid = self.is_valid_removal("AI", pos)
            self.board[pos] = None
            self.draw_board()
            self.ai_pieces -= 1
        else:
            pos = self.removing_strategy()
            self.board[pos] = None
            self.draw_board()
            self.player_pieces -= 1

    def empty_positions(self):
        return [pos for pos, piece in self.board.items() if piece is None]

    def place_piece(self, player):
        if player == "Player":
            pos = tuple(map(int, input("Pozíció (pl. 1,1): ").split(",")))
            while pos not in self.empty_positions():
                print("Ezt nem lehet! Próbáld újra!")
                pos = tuple(map(int, input("Pozíció (pl. 1,1): ").split(",")))
            self.board[pos] = "Player"
            self.player_pieces += 1
            self.draw_board()
            if self.is_in_mill("Player", pos) == True:
                self.remove_opponent_piece("AI")
            self.turn = "AI"
        else:
            pos = self.placing_strategy()
            self.board[pos] = "AI"
            self.ai_pieces += 1
            self.draw_board()
            if self.is_in_mill("AI", pos) == True:
                self.remove_opponent_piece("Player")
            self.turn = "Player"

    def is_valid_moving(self, player):
        old_pos = tuple(map(int, input("Mozgatandó bábu: ").split(",")))
        while self.board.get(old_pos) != player:
            print("Ezt nem lehet! Próbáld újra!")
            self.draw_board()
            old_pos = tuple(map(int, input("Mozgatandó bábu: ").split(","))) 
        new_pos = tuple(map(int, input("Új pozíció: ").split(",")))
        while new_pos not in self.empty_positions():
            print("Ezt nem lehet! Próbáld újra!")
            self.draw_board()
            new_pos = tuple(map(int, input("Új pozíció: ").split(",")))
        while [old_pos, new_pos] not in self.connections and [new_pos, old_pos] not in self.connections:
            print("Ezt nem lehet! Próbáld újra!")
            self.draw_board()
            old_pos = tuple(map(int, input("Mozgatandó bábu: ").split(",")))
            while self.board.get(old_pos) != player:
                print("Ezt nem lehet! Próbáld újra!")
                self.draw_board()
                old_pos = tuple(map(int, input("Mozgatandó bábu: ").split(","))) 
            new_pos = tuple(map(int, input("Új pozíció: ").split(",")))
            while new_pos not in self.empty_positions():
                print("Ezt nem lehet! Próbáld újra!")
                self.draw_board()
                new_pos = tuple(map(int, input("Új pozíció: ").split(",")))
        return old_pos, new_pos

    def move_piece(self, player):
        if player == "Player":
            old_pos, new_pos = self.is_valid_moving(player)
            self.board[old_pos] = None
            self.board[new_pos] = "Player"
            self.draw_board()
            if self.is_in_mill("Player", new_pos) == True:
                self.remove_opponent_piece("AI")
            self.turn = "AI"
        else:
            movable_pieces = [pos for pos, piece in self.board.items() if piece == "AI"]
            empty_pos = self.empty_positions()
            valid_moves = [(conn[0], conn[1]) for conn in self.connections if conn[0] in movable_pieces and conn[1] in empty_pos]
            valid_moves += [(conn[1], conn[0]) for conn in self.connections if conn[1] in movable_pieces and conn[0] in empty_pos]
            old_pos, new_pos = self.moving_strategy()
            self.board[old_pos] = None
            self.board[new_pos] = "AI"
            self.draw_board()
            if self.is_in_mill("AI", new_pos) == True:
                self.remove_opponent_piece("Player")
            self.turn = "Player"

    def is_valid_flying(self, player):
        old_pos = tuple(map(int, input("Mozgatandó bábu: ").split(",")))
        while self.board.get(old_pos) != player:
            print("Ezt nem lehet! Próbáld újra!")
            self.draw_board()
            old_pos = tuple(map(int, input("Mozgatandó bábu: ").split(","))) 
        new_pos = tuple(map(int, input("Új pozíció: ").split(",")))
        while new_pos not in self.empty_positions():
            print("Ezt nem lehet! Próbáld újra!")
            self.draw_board()
            new_pos = tuple(map(int, input("Új pozíció: ").split(",")))
        return old_pos, new_pos
    
    def fly_piece(self, player):
        if player == "Player":
            old_pos, new_pos = self.is_valid_flying(player)
            self.board[old_pos] = None
            self.board[new_pos] = "Player"
            self.draw_board()
            if self.is_in_mill("Player", new_pos) == True:
                self.remove_opponent_piece("AI")
            self.turn = "AI"
        else:
            old_pos = self.flying_strategy()[0]
            new_pos = self.flying_strategy()[1]
            self.board[old_pos] = None
            self.board[new_pos] = "AI"
            self.draw_board()
            if self.is_in_mill("AI", new_pos) == True:
                self.remove_opponent_piece("Player")
            self.turn = "Player"

    def game_over(self):
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)
        fig.patch.set_facecolor('yellow')

        for conn in self.connections:
            x, y = zip(*conn)
            ax.plot(x, y, 'k', linewidth=3)
        for pos, piece in self.board.items():
            if piece == "Player":
                ax.plot(*pos, 'o', markersize=24, color='#F3E5AB', markeredgecolor='grey')
                ax.plot(*pos, 'o', markersize=16, color='#F3E5AB', markeredgecolor='grey')
                ax.plot(*pos, 'o', markersize=8, color='#F3E5AB', markeredgecolor='grey')
            elif piece == "AI":
                ax.plot(*pos, 'o', markersize=24, color='black', markeredgecolor='grey')
                ax.plot(*pos, 'o', markersize=16, color='black', markeredgecolor='grey')
                ax.plot(*pos, 'o', markersize=8, color='black', markeredgecolor='grey')
            else:
                ax.plot(*pos, 'ko', markersize=10)
        
        plt.text(0, 0, 'Game Over!', fontsize=40, ha='center', va='center', fontweight='bold', color='red', 
                 bbox=dict(facecolor='black', alpha=0.75)) # Ez a sor az extra, amúgy egy draw_board    
        plt.show()

    def play_game(self):
        self.draw_board()
        for i in range(18): # 9-9 placing lépés
            self.place_piece(self.turn)
        while self.player_pieces >= 3 and self.ai_pieces >= 3:
            if self.turn == "Player":
                if self.player_pieces > 3:
                    self.move_piece(self.turn)
                else:
                    self.fly_piece(self.turn)
            else:
                if self.ai_pieces > 3:
                    self.move_piece(self.turn)
                else:
                    self.fly_piece(self.turn)
        self.game_over()



    # Strategy:
    def placing_make_mill(self):
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 2 and positions.count(None) == 1:
                return mill[positions.index(None)]
        return None

    def placing_block_opponent_mill(self):
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 2 and positions.count(None) == 1:
                return mill[positions.index(None)]
        return None

    def placing_block_opponent_diagonal(self):
        diagonals = [[(-3, -3), (3, 3), (-3, 3)], [(-3, -3), (3, 3), (3, -3)], [(3, -3), (-3, 3), (3, 3)], [(3, -3), (-3, 3), (-3, -3)],
                     [(-2, -2), (2, 2), (-2, 2)], [(-2, -2), (2, 2), (2, -2)], [(2, -2), (-2, 2), (2, 2)], [(2, -2), (-2, 2), (-2, -2)],
                     [(-1, -1), (1, 1), (-1, 1)], [(-1, -1), (1, 1), (1, -1)], [(1, -1), (-1, 1), (1, 1)], [(1, -1), (-1, 1), (-1, -1)],
                     [(0, -3), (-2, -2), (0, -2)], [(0, 3), (2, 2), (0, 2)], [(-3, 0), (-2, 2), (-2, 0)], [(3, 0), (2, -2), (2, 0)]] # L-alakú részek
        if self.placing_make_potential_mill() is None:
            for diagonal in diagonals:
                first_mill = [pos for mill in self.mills for pos in mill if diagonal[0] in mill and diagonal[2] in mill]
                second_mill = [pos for mill in self.mills for pos in mill if diagonal[1] in mill and diagonal[2] in mill] # Az L két malma
                first_mill_positions = [self.board[pos] for pos in first_mill]
                second_mill_positions = [self.board[pos] for pos in second_mill]
                if self.board[diagonal[0]] == "Player" and first_mill_positions.count(None) == 2 and second_mill_positions.count(None) == 3:
                    return diagonal[1]
                elif self.board[diagonal[1]] == "Player" and first_mill_positions.count(None) == 3 and second_mill_positions.count(None) == 2:
                    return diagonal[0]
            return None
        return None

    def placing_make_diagonal(self):
        diagonals = [[(-3, -3), (3, 3), (-3, 3)], [(-3, -3), (3, 3), (3, -3)], [(3, -3), (-3, 3), (3, 3)], [(3, -3), (-3, 3), (-3, -3)],
                     [(-2, -2), (2, 2), (-2, 2)], [(-2, -2), (2, 2), (2, -2)], [(2, -2), (-2, 2), (2, 2)], [(2, -2), (-2, 2), (-2, -2)],
                     [(-1, -1), (1, 1), (-1, 1)], [(-1, -1), (1, 1), (1, -1)], [(1, -1), (-1, 1), (1, 1)], [(1, -1), (-1, 1), (-1, -1)],
                     [(0, -3), (-2, -2), (0, -2)], [(0, 3), (2, 2), (0, 2)], [(-3, 0), (-2, 2), (-2, 0)], [(3, 0), (2, -2), (2, 0)]] # L-alakú részek
        possible_moves = []
        for diagonal in diagonals:
            first_mill = [pos for mill in self.mills for pos in mill if diagonal[0] in mill and diagonal[2] in mill]
            second_mill = [pos for mill in self.mills for pos in mill if diagonal[1] in mill and diagonal[2] in mill] # Az L két malma
            first_mill_positions = [self.board[pos] for pos in first_mill]
            second_mill_positions = [self.board[pos] for pos in second_mill]
            if self.board[diagonal[0]] == "AI" and self.board[diagonal[1]] == "AI" and first_mill_positions.count(None) == 2 and second_mill_positions.count(None) == 2:
                possible_moves.append(diagonal[2])
        if possible_moves:
            return random.choice(possible_moves)
        for diagonal in diagonals:
            first_mill = [pos for mill in self.mills for pos in mill if diagonal[0] in mill and diagonal[2] in mill]
            second_mill = [pos for mill in self.mills for pos in mill if diagonal[1] in mill and diagonal[2] in mill]
            first_mill_positions = [self.board[pos] for pos in first_mill]
            second_mill_positions = [self.board[pos] for pos in second_mill]
            if self.board[diagonal[0]] == "AI" and first_mill_positions.count(None) == 2 and second_mill_positions.count(None) == 3:
                possible_moves.append(diagonal[1])
            if self.board[diagonal[1]] == "AI" and first_mill_positions.count(None) == 3 and second_mill_positions.count(None) == 2:
                possible_moves.append(diagonal[0])
        if possible_moves:
            return random.choice(possible_moves)    
        if self.placing_make_potential_mill() is None:
            for diagonal in diagonals:
                first_mill = [pos for mill in self.mills for pos in mill if diagonal[0] in mill and diagonal[2] in mill]
                second_mill = [pos for mill in self.mills for pos in mill if diagonal[1] in mill and diagonal[2] in mill]
                first_mill_positions = [self.board[pos] for pos in first_mill]
                second_mill_positions = [self.board[pos] for pos in second_mill]
                if first_mill_positions.count(None) == 3 and second_mill_positions.count(None) == 3:
                    possible_moves.append(diagonal[0])
            if possible_moves:
                return random.choice(possible_moves)
            return None
        return None

    def placing_make_potential_mill(self):
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 1 and positions.count(None) == 2:
                return mill[positions.index(None)] #hát ez pont jól jön ki, de elég idióta, hogy az első None helyét adja vissza, nem az összes None helyet
        return None

    def placing_random_move(self):
        return random.choice(self.empty_positions())

    def placing_strategy(self):
        for strategy in [self.placing_make_mill(), self.placing_block_opponent_mill(), self.placing_block_opponent_diagonal(), 
                         self.placing_make_diagonal(), self.placing_make_potential_mill(), self.placing_random_move()]:
            if strategy is not None:
                return strategy
    


    def flying_make_mill(self):
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 2 and positions.count(None) == 1:
                old_new_pos = [pos for pos, piece in self.board.items() if piece == "AI" and pos not in mill]
                old_new_pos.append(mill[positions.index(None)])
                return old_new_pos
        return None

    def is_blocking_piece(self, pos):
        for mill in self.mills:
            if pos in mill:
                positions = [self.board[pos] for pos in mill]
                if positions.count("Player") == 2 and positions.count("AI") == 1:
                    return True
        return False

    def flying_block_opponent_mill(self):
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 2 and positions.count(None) == 1:
                possible_old_pos = [pos for pos, piece in self.board.items() if piece == "AI" and self.is_blocking_piece(pos) is False]
                if possible_old_pos:
                    old_new_pos = [random.choice(possible_old_pos), mill[positions.index(None)]]
                else:
                    ai_old_pos = [pos for pos, piece in self.board.items() if piece == "AI"]
                    old_new_pos = [random.choice(ai_old_pos), mill[positions.index(None)]]
                return old_new_pos
        return None    

    def flying_make_potential_mill(self):
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 1 and positions.count(None) == 2:
                possible_old_pos = [pos for pos, piece in self.board.items() if piece == "AI" and self.is_blocking_piece(pos) is False and pos not in mill]
                if possible_old_pos:
                    old_new_pos = [random.choice(possible_old_pos), mill[positions.index(None)]]
                    return old_new_pos
        return None

    def flying_random_move(self):
        possible_old_pos = [pos for pos, piece in self.board.items() if piece == "AI" and self.is_blocking_piece(pos) is False]
        if possible_old_pos:
            old_new_pos = [random.choice(possible_old_pos), random.choice(self.empty_positions())]
        else:
            ai_old_pos = [pos for pos, piece in self.board.items() if piece == "AI"]
            old_new_pos = [random.choice(ai_old_pos), random.choice(self.empty_positions())]
        return old_new_pos

    def flying_strategy(self):
        for strategy in [self.flying_make_mill(), self.flying_block_opponent_mill(), self.flying_make_potential_mill(), self.flying_random_move()]:
            if strategy is not None:
                return strategy # Ez egy pár: mit hova visz



    def moving_make_mill(self):
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 2 and positions.count(None) == 1:
                possible_old_pos = [pos for pos in self.neighbouring_pieces("AI", mill[positions.index(None)]) if pos not in mill]
                if possible_old_pos:
                    return [random.choice(possible_old_pos), mill[positions.index(None)]]
        return None

    def moving_block_opponent_mill(self):
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 2 and positions.count(None) == 1:
                neighbouring_pieces = self.neighbouring_pieces("Player", mill[0]) + self.neighbouring_pieces("Player", mill[1]) + self.neighbouring_pieces("Player", mill[2])
                for pos in mill:
                    if pos in neighbouring_pieces:
                        neighbouring_pieces.remove(pos)
                possible_old_pos = self.neighbouring_pieces("AI", mill[positions.index(None)])
                if neighbouring_pieces and possible_old_pos:
                    old_pos = [pos for pos in possible_old_pos if self.is_blocking_piece(pos) is False and self.is_in_mill("AI", pos) is False]
                    if old_pos:
                        return [random.choice(old_pos), mill[positions.index(None)]]
                    return [random.choice(possible_old_pos), mill[positions.index(None)]]
        return None    

    def moving_make_csikicsuki(self):
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 3:
                for other_mill in self.mills:
                    other_positions = [self.board[pos] for pos in other_mill]
                    if other_positions.count("AI") == 2 and other_positions.count(None) == 1 and set(other_mill).isdisjoint(set(mill)):
                        ai_positions = [pos for pos in other_mill if self.board[pos] == "AI"]
                        if ai_positions[0] in (self.neighbouring_pieces("AI", mill[0])+self.neighbouring_pieces("AI", mill[1])+self.neighbouring_pieces("AI", mill[2])):
                            return [ai_positions[0], other_mill[other_positions.index(None)]]
                        if ai_positions[1] in (self.neighbouring_pieces("AI", mill[0])+self.neighbouring_pieces("AI", mill[1])+self.neighbouring_pieces("AI", mill[2])):
                            return [ai_positions[1], other_mill[other_positions.index(None)]]
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 3:
                for other_mill in self.mills:
                    other_positions = [self.board[pos] for pos in other_mill]
                    if other_positions.count("AI") == 1 and other_positions.count(None) == 2 and set(other_mill).isdisjoint(set(mill)):
                        none_positions = [pos for pos in other_mill if self.board[pos] == None]
                        old_pos_0 = list(set(self.neighbouring_pieces("AI", none_positions[0])) - set(other_mill))
                        old_pos_1 = list(set(self.neighbouring_pieces("AI", none_positions[1])) - set(other_mill))
                        if none_positions[1] in (self.neighbouring_pieces(None, mill[0])+self.neighbouring_pieces(None, mill[1])+self.neighbouring_pieces(None, mill[2])) and old_pos_0:
                            return [random.choice(old_pos_0), none_positions[0]]
                        elif none_positions[0] in (self.neighbouring_pieces(None, mill[0])+self.neighbouring_pieces(None, mill[1])+self.neighbouring_pieces(None, mill[2])) and old_pos_1:
                            return [random.choice(old_pos_1), none_positions[1]]
        return None

    def moving_make_potential_mill(self):
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 2 and positions.count(None) == 1:
                possible_new_pos = self.neighbouring_pieces(None, mill[positions.index(None)])
                possible_old_new_pos = [[old_pos, new_pos] for new_pos in possible_new_pos for old_pos in self.neighbouring_pieces("AI", new_pos) 
                                        if self.is_blocking_piece(old_pos) is False and self.is_in_mill("AI", old_pos) is False]
                if possible_old_new_pos:
                    return random.choice(possible_old_new_pos)
        return None

    def moving_random_move(self):
        possible_old_pos = [pos for pos, piece in self.board.items() if piece == "AI" and self.is_blocking_piece(pos) is False]
        possible_old_new_pos = [[old_pos, new_pos] for old_pos in possible_old_pos for new_pos in self.neighbouring_pieces(None, old_pos)]
        if possible_old_new_pos:
            return random.choice(possible_old_new_pos)
        else:
            possible_old_pos = [pos for pos, piece in self.board.items() if piece == "AI"]
            possible_old_new_pos = [[old_pos, new_pos] for old_pos in possible_old_pos for new_pos in self.neighbouring_pieces(None, old_pos)]
            if possible_old_new_pos:
                return random.choice(possible_old_new_pos)
        return None

    def moving_strategy(self):
        for strategy in [self.moving_make_mill(), self.moving_block_opponent_mill(), self.moving_make_csikicsuki(), self.moving_make_potential_mill(), self.moving_random_move()]:
            if strategy is not None:
                return strategy # Ez egy pár: mit hova visz
        return None #ez az ha nem tud lépni



    def neighbouring_pieces(self, player, pos):
        neighbours1 = [conn[0] for conn in self.connections if conn[1] == pos]
        neighbours2 = [conn[1] for conn in self.connections if conn[0] == pos]
        neighbours = neighbours1 + neighbours2
        neighbouring_pieces = [neighbour for neighbour in neighbours if self.board[neighbour] == player]
        return neighbouring_pieces
    
    def removing_csikicsuki(self): # Szerintem a csiki-csukinak nincs is angol neve, amilyen bénák
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 3:
                for other_mill in self.mills:
                    other_positions = [self.board[pos] for pos in other_mill]
                    if other_positions.count("Player") == 2 and other_positions.count(None) == 1 and other_mill[other_positions.index(None)] in (
                        self.neighbouring_pieces(None, mill[0])+self.neighbouring_pieces(None, mill[1])+self.neighbouring_pieces(None, mill[2])):
                        removable_pieces = [pos for pos in other_mill if self.is_valid_removal("Player", pos) is True]
                        if removable_pieces:
                            return random.choice(removable_pieces)
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 3:
                for other_mill in self.mills:
                    other_positions = [self.board[pos] for pos in other_mill]
                    if other_positions.count("Player") == 2 and other_positions.count("AI") == 1 and other_mill[other_positions.index("AI")] in (
                        self.neighbouring_pieces("AI", mill[0])+self.neighbouring_pieces("AI", mill[1])+self.neighbouring_pieces("AI", mill[2])):
                        removable_pieces = [pos for pos in other_mill if self.is_valid_removal("Player", pos) is True]
                        if removable_pieces:
                            return random.choice(removable_pieces)
        return None
    
    def removing_potential_mill(self):
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 2 and positions.count(None) == 1:
                neighbouring_pieces = self.neighbouring_pieces("Player", mill[positions.index(None)])
                removable_pieces = []
                for pos in mill:
                    if pos in neighbouring_pieces:
                        neighbouring_pieces.remove(pos)
                    if self.board[pos] == "Player" and self.is_valid_removal("Player", pos) is True:
                        removable_pieces.append(pos)
                if neighbouring_pieces and removable_pieces:
                    if len(removable_pieces) == 2 and len(self.neighbouring_pieces("Player", removable_pieces[1])) > len(self.neighbouring_pieces("Player", removable_pieces[0])):
                        return removable_pieces[1]
                    else:
                        return removable_pieces[0]
        return None

    def removing_blocking_piece(self):
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 2 and positions.count("Player") == 1:
                neighbouring_pieces = self.neighbouring_pieces("AI", mill[positions.index("Player")])
                for pos in mill:
                    if pos in neighbouring_pieces:
                        neighbouring_pieces.remove(pos)
                if neighbouring_pieces:
                    return mill[positions.index("Player")]
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 2 and positions.count("Player") == 1:
                neighbouring_pieces = self.neighbouring_pieces("AI", mill[positions.index("Player")])
                for pos in neighbouring_pieces:
                    if pos not in mill:
                        neighbouring_pieces.remove(pos)
                two_neighbouring_pieces = []
                for piece in neighbouring_pieces:
                    two_neighbouring_pieces = two_neighbouring_pieces + self.neighbouring_pieces("AI", piece)
                for pos in mill:
                    if pos in two_neighbouring_pieces:
                        two_neighbouring_pieces.remove(pos)
                if two_neighbouring_pieces and self.is_valid_removal("Player", mill[positions.index("Player")]):
                    return mill[positions.index("Player")]
        return None
    
    def removing_most_neighbours(self):
        most_neighbours = [] #akiknek a legtöbb saját színű szomszédjuk van
        max = -1
        removable_pieces = []
        for pos in self.positions:
            if self.is_valid_removal("Player", pos) is True:
                removable_pieces.append(pos)
        for pos in removable_pieces:
            neighbouring_pieces = self.neighbouring_pieces("Player", pos)
            count = len(neighbouring_pieces)
            if count > max:
                max = count
                most_neighbours = [pos]
            elif count == max:
                most_neighbours.append(pos)
        return random.choice(most_neighbours)
    
    def removing_strategy(self):
        for strategy in [self.removing_csikicsuki(), self.removing_potential_mill(), self.removing_blocking_piece(), self.removing_most_neighbours()]:
            if strategy is not None:
                return strategy


    
game = Malom()
game.play_game()
