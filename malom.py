import matplotlib.pyplot as plt
import random

class Malom:
    def __init__(self):
        self.positions = [(-3, -3), (-3, 0), (-3, 3), (0, 3), (3, 3), (3, 0), (3, -3), (0, -3), # Külső négyzet pozíciói
                          (-2, -2), (-2, 0), (-2, 2), (0, 2), (2, 2), (2, 0), (2, -2), (0, -2), # Középső négyzet pozíciói
                          (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)] # Belső négyzet pozíciói
        self.connections = [[(-3, -3), (-3, 0)], [(-3, 0), (-3, 3)], [(-3, 3), (0, 3)], [(0, 3), (3, 3)],
                            [(3, 3), (3, 0)], [(3, 0), (3, -3)], [(3, -3), (0, -3)], [(0, -3), (-3, -3)], # Külső négyzet vonalai
                            [(-2, -2), (-2, 0)], [(-2, 0), (-2, 2)], [(-2, 2), (0, 2)], [(0, 2), (2, 2)],
                            [(2, 2), (2, 0)], [(2, 0), (2, -2)], [(2, -2), (0, -2)], [(0, -2), (-2, -2)], # Középső négyzet vonalai
                            [(-1, -1), (-1, 0)], [(-1, 0), (-1, 1)], [(-1, 1), (0, 1)], [(0, 1), (1, 1)],
                            [(1, 1), (1, 0)], [(1, 0), (1, -1)], [(1, -1), (0, -1)], [(0, -1), (-1, -1)], # Belső négyzet vonalai
                            [(0, -3), (0, -2)], [(0, -2), (0, -1)], [(0, 3), (0, 2)], [(0, 2), (0, 1)],
                            [(-3, 0), (-2, 0)], [(-2, 0), (-1, 0)], [(3, 0), (2, 0)], [(2, 0), (1, 0)]] # Pici vonalak
        self.board = {pos: None for pos in self.positions} # A táblán melyik pozíción ki van épp
        self.player_pieces = 0 # A játékos bábuinak száma
        self.ai_pieces = 0 # A számítógép bábuinak száma
        self.turn = "Player" # Player kezd
        self.placing_phase = True
        self.remaining_player_pieces = 9
        self.remaining_ai_pieces = 9
        self.mills = [[(-3, -3), (-3, 0), (-3, 3)], [(-3, 3), (0, 3), (3, 3)], [(3, 3), (3, 0), (3, -3)], [(3, -3), (0, -3), (-3, -3)],
                      [(-2, -2), (-2, 0), (-2, 2)], [(-2, 2), (0, 2), (2, 2)], [(2, 2), (2, 0), (2, -2)], [(2, -2), (0, -2), (-2, -2)],
                      [(-1, -1), (-1, 0), (-1, 1)], [(-1, 1), (0, 1), (1, 1)], [(1, 1), (1, 0), (1, -1)], [(1, -1), (0, -1), (-1, -1)],
                      [(0, -3), (0, -2), (0, -1)], [(0, 3), (0, 2), (0, 1)], [(-3, 0), (-2, 0), (-1, 0)], [(3, 0), (2, 0), (1, 0)]] # Lehetséges malmok
    
    def draw_board(self): # Megrajzolja a táblát az aktuális állással
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
            ax.text(pos[0] + 0.1, pos[1] + 0.1, str(pos), fontsize=8, color='grey', fontstyle='italic') # Koordináták
        
        if self.placing_phase: # Megmondja, hány lerakható bábu van még
            plt.text(4, 4, f'Megmaradt bábuk (Player): {self.remaining_player_pieces}', fontsize=10, fontstyle='italic', weight='bold', ha='right', va='top')
            plt.text(-4, 4, f'Megmaradt bábuk (AI): {self.remaining_ai_pieces}', fontsize=10, fontstyle='italic', weight='bold', ha='left', va='top')
        plt.show()

    def is_in_mill(self, player, position): # Megmondja, hogy az adott pozíció az adott játékos egy malmához tartozik-e
        possible_mills = [mill for mill in self.mills if position in mill]
        for mill in possible_mills:
            if all(self.board[pos] == player for pos in mill):
                return True
        return False

    def is_valid_removal(self, player, position): # Megmondja, hogy az adott pozícióból levehető-e az adott játékos bábuja
        if self.board[position] == player: # A bábu az adott játékosé
            if self.is_in_mill(player, position): # A bábu malomban van
                if all(self.is_in_mill(player, pos) == True for pos in self.board if self.board[pos] == player): # A játékos minden bábuja malomban van
                    return True
                return False
            return True
        return False

    def remove_opponent_piece(self, opponent): # Leveszi az ellenfél egy bábuját
        if opponent == "AI":
            pos = tuple(map(int, input("Az ellenfél leveendő bábuja: ").split(",")))
            valid = self.is_valid_removal("AI", pos)
            while valid is not True:
                print("Ezt nem lehet! Próbáld újra!")
                self.draw_board()
                pos = tuple(map(int, input("Az ellenfél leveendő bábuja: ").split(",")))
                valid = self.is_valid_removal("AI", pos)
            self.board[pos] = None
            self.ai_pieces -= 1
            self.draw_board()
        else:
            pos = self.removing_strategy()
            self.board[pos] = None
            self.player_pieces -= 1
            self.draw_board()  

    def empty_positions(self): # Visszaadja az üres pozíciók listáját
        return [pos for pos, piece in self.board.items() if piece is None]

    def place_piece(self, player): # Lerak egy bábut (1. fázis - lerakás)
        if player == "Player":
            pos = tuple(map(int, input("Pozíció (pl. 1,1): ").split(",")))
            while pos not in self.empty_positions():
                print("Ezt nem lehet! Próbáld újra!")
                pos = tuple(map(int, input("Pozíció (pl. 1,1): ").split(",")))
            self.board[pos] = "Player"
            self.player_pieces += 1
            self.remaining_player_pieces -= 1
            self.draw_board()
            if self.is_in_mill("Player", pos) == True: # Ha malmot csinált a játékos, levetet vele egy bábut
                self.remove_opponent_piece("AI")
            self.turn = "AI"
        else:
            pos = self.placing_strategy()
            self.board[pos] = "AI"
            self.ai_pieces += 1
            self.remaining_ai_pieces -= 1
            self.draw_board()
            if self.is_in_mill("AI", pos) == True: # Ha malmot csinált a játékos, levetet vele egy bábut
                self.remove_opponent_piece("Player")
            self.turn = "Player"

    def is_valid_moving(self, player): # Megmondja, hogy az adott játékos egy lépése szabályos-e
        old_pos = tuple(map(int, input("Mozgatandó bábu: ").split(",")))
        new_pos = tuple(map(int, input("Új pozíció: ").split(",")))
        while self.board.get(old_pos) != player or new_pos not in self.empty_positions() or (
            [old_pos, new_pos] not in self.connections and [new_pos, old_pos] not in self.connections): # A régi pozíción saját bábu kell álljon, az új pozíció üres kell legyen, és a két pozíció szomszédos kell legyen
            print("Ezt nem lehet! Próbáld újra!")
            self.draw_board()
            old_pos = tuple(map(int, input("Mozgatandó bábu: ").split(","))) 
            new_pos = tuple(map(int, input("Új pozíció: ").split(",")))
        return old_pos, new_pos

    def move_piece(self, player): # Mozgat egy bábut (2. fázis - lépés)
        if player == "Player":
            old_pos, new_pos = self.is_valid_moving(player)
            self.board[old_pos] = None
            self.board[new_pos] = "Player"
            self.draw_board()
            if self.is_in_mill("Player", new_pos) == True: # Ha malmot csinált a játékos, levetet vele egy bábut
                self.remove_opponent_piece("AI")
            self.turn = "AI"
        else:
            old_pos, new_pos = self.moving_strategy()
            self.board[old_pos] = None
            self.board[new_pos] = "AI"
            self.draw_board()
            if self.is_in_mill("AI", new_pos) == True: # Ha malmot csinált a játékos, levetet vele egy bábut
                self.remove_opponent_piece("Player")
            self.turn = "Player"

    def is_valid_flying(self, player): # Megmondja, hogy az adott játékos egy ugrása szabályos-e
        old_pos = tuple(map(int, input("Mozgatandó bábu: ").split(",")))
        new_pos = tuple(map(int, input("Új pozíció: ").split(",")))
        while self.board.get(old_pos) != player or new_pos not in self.empty_positions(): # A régi pozíción saját bábu kell álljon, az új pozíció üres kell legyen
            print("Ezt nem lehet! Próbáld újra!")
            self.draw_board()
            old_pos = tuple(map(int, input("Mozgatandó bábu: ").split(",")))
            new_pos = tuple(map(int, input("Új pozíció: ").split(",")))
        return old_pos, new_pos
    
    def fly_piece(self, player): # Ugrik egy bábuval (3. fázis - ugrálás)
        if player == "Player":
            old_pos, new_pos = self.is_valid_flying(player)
            self.board[old_pos] = None
            self.board[new_pos] = "Player"
            self.draw_board()
            if self.is_in_mill("Player", new_pos) == True: # Ha malmot csinált a játékos, levetet vele egy bábut
                self.remove_opponent_piece("AI")
            self.turn = "AI"
        else:
            old_pos, new_pos = self.flying_strategy()
            self.board[old_pos] = None
            self.board[new_pos] = "AI"
            self.draw_board()
            if self.is_in_mill("AI", new_pos) == True: # Ha malmot csinált a játékos, levetet vele egy bábut
                self.remove_opponent_piece("Player")
            self.turn = "Player"

    def game_over(self): # Kiírja, hogy ki nyert
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
        
        if self.ai_pieces < 3: # Ez a rész az extra, amúgy egy draw_board
            plt.text(0, 0, 'Nyertél! :)', fontsize=40, ha='center', va='center', fontweight='bold', color='red', 
                 bbox=dict(facecolor='black', alpha=0.75))
        else:
            plt.text(0, 0, 'Vesztettél! :(', fontsize=40, ha='center', va='center', fontweight='bold', color='red', 
                 bbox=dict(facecolor='black', alpha=0.75))
        plt.show()

    def play_game(self): # Lejátszatja a játékot
        self.draw_board()
        for i in range(18): # 9-9 placing
            self.place_piece(self.turn)
        self.placing_phase = False
        while self.player_pieces >= 3 and self.ai_pieces >= 3: # Lépnek, amíg több mint 3 bábujuk van, ha csak 3, akkor ugranak
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
    def placing_make_mill(self): # Ha létezik, visszaad egy olyan pozíciót, ami malmot csinál (1. fázis)
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 2 and positions.count(None) == 1: # 2 helyen már ő van, a harmadik üres
                return mill[positions.index(None)]
        return None

    def placing_block_opponent_mill(self): # Ha létezik, visszaad egy olyan pozíciót, ami blokkolja az ellenfél malmát (1. fázis)
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 2 and positions.count(None) == 1:
                return mill[positions.index(None)]
        return None

    def placing_block_opponent_diagonal(self): # Ha létezik, visszaad egy olyan pozíciót, ami blokkolja az ellenfél diagonálisát (1. fázis)
        diagonals = [[[(-3, -3), (3, 3), (-3, 3), (3, -3)], [(-3, 0), (0, 3), (3, 0), (0, -3)]], # Külső négyzet pozíciói
                     [[(-2, -2), (2, 2), (-2, 2), (2, -2)], [(-2, 0), (0, 2), (2, 0), (0, -2)]], # Középső négyzet pozíciói
                     [[(-1, -1), (1, 1), (-1, 1), (1, -1)], [(-1, 0), (0, 1), (1, 0), (0, -1)]]] # Belső négyzet pozíciói
        for square in diagonals:
            positions0 = [self.board[pos] for pos in square[0]]
            positions1 = [self.board[pos] for pos in square[1]]
            if positions0.count("Player") == 1 and positions0.count(None) == 3 and positions1.count(None) == 4: # Ha a négyzetnek csak egy sarkában van Player bábu, szembe rak vele
                if positions0.index("Player") == 0:
                    return square[0][1]
                if positions0.index("Player") == 1:
                    return square[0][0]
                if positions0.index("Player") == 2:
                    return square[0][3]
                if positions0.index("Player") == 3:
                    return square[0][2]
        for mill in self.mills: # Ha egy diagonálist csinálna Player, az AI berak a metszetbe
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 1 and positions.count(None) == 2:
                for other_mill in self.mills:
                    other_positions = [self.board[pos] for pos in other_mill]
                    if other_positions.count("Player") == 1 and other_positions.count(None) == 2 and not set(other_mill).isdisjoint(set(mill)) and mill != other_mill: # A két malom metszi egymást és 1-1 Player bábu van benne
                        intersection = list(set(mill) & set(other_mill))[0]
                        if self.board[intersection] == None:
                            return intersection
        return None

    def placing_make_diagonal(self): # Ha tud, visszaad egy olyan pozíciót, ami diagonálist csinál (1. fázis)
        diagonals = [[[(-3, -3), (3, 3), (-3, 3), (3, -3)], [(-3, 0), (0, 3), (3, 0), (0, -3)]], # Külső négyzet pozíciói
                     [[(-2, -2), (2, 2), (-2, 2), (2, -2)], [(-2, 0), (0, 2), (2, 0), (0, -2)]], # Középső négyzet pozíciói
                     [[(-1, -1), (1, 1), (-1, 1), (1, -1)], [(-1, 0), (0, 1), (1, 0), (0, -1)]]] # Belső négyzet pozíciói
        for mill in self.mills: # A malmok metszetébe rak, ha a két szélén már ő van
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 1 and positions.count(None) == 2:
                for other_mill in self.mills:
                    other_positions = [self.board[pos] for pos in other_mill]
                    if other_positions.count("AI") == 1 and other_positions.count(None) == 2 and not set(other_mill).isdisjoint(set(mill)) and mill != other_mill:
                        intersection = list(set(mill) & set(other_mill))[0]
                        if self.board[intersection] == None:
                            return intersection
        for square in diagonals: # Ha a négyzetnek csak egy sarkában van AI bábu, szembe rak vele
            positions0 = [self.board[pos] for pos in square[0]]
            positions1 = [self.board[pos] for pos in square[1]]
            if positions0.count("AI") == 1 and positions0.count(None) == 3 and positions1.count(None) == 4:
                if positions0.index("AI") == 0:
                    return square[0][1]
                if positions0.index("AI") == 1:
                    return square[0][0]
                if positions0.index("AI") == 2:
                    return square[0][3]
                if positions0.index("AI") == 3:
                    return square[0][2]
        for mill in self.mills: # Ha a diagonális egyik malmában már van bábuja, rak a másikba is
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 1 and positions.count(None) == 2:
                for other_mill in self.mills:
                    other_positions = [self.board[pos] for pos in other_mill]
                    if other_positions.count(None) == 3 and not set(other_mill).isdisjoint(set(mill)) and mill != other_mill:
                        none_positions = [pos for pos in other_mill if pos not in mill]
                        return random.choice(none_positions)
        if self.placing_make_potential_mill() is None:
            for square in diagonals: # Elkezd egy újat, ha még nincs megkezdett
                positions0 = [self.board[pos] for pos in square[0]]
                positions1 = [self.board[pos] for pos in square[1]]
                if positions0.count(None) == 4 and positions1.count(None) == 4:
                    return random.choice(square[0])
            for mill in self.mills:
                positions = [self.board[pos] for pos in mill]
                if positions.count(None) == 3:
                    for other_mill in self.mills:
                        other_positions = [self.board[pos] for pos in other_mill]
                        if other_positions.count(None) == 3 and not set(other_mill).isdisjoint(set(mill)) and mill != other_mill:
                            none_positions = [pos for pos in other_mill if pos not in mill]
                            return random.choice(none_positions)
        return None

    def placing_make_potential_mill(self): # Ha tud, visszaad egy olyan pozíciót, ami potenciális malmot csinál (1. fázis)
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 1 and positions.count(None) == 2: # 1 helyen ő van, 2 üres
                return mill[positions.index(None)] # (hát ez pont jól jön ki, de elég idióta, hogy az első None helyét adja vissza, nem az összes None helyet)
        return None

    def placing_random_move(self): # Random lép valami szabályosat
        return random.choice(self.empty_positions())

    def placing_strategy(self): # A prioritási sorrend szerint végigpróbálja az 1. fázis lépéseit
        for strategy in [self.placing_make_mill(), self.placing_block_opponent_mill(), self.placing_block_opponent_diagonal(), 
                         self.placing_make_diagonal(), self.placing_make_potential_mill(), self.placing_random_move()]:
            if strategy is not None:
                return strategy
    


    def flying_make_mill(self): # Ha létezik, visszaad egy olyan ugrást, ami malmot csinál (3. fázis)
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 2 and positions.count(None) == 1: # 2 helyen már ő van, a harmadik üres
                old_new_pos = [pos for pos, piece in self.board.items() if piece == "AI" and pos not in mill]
                old_new_pos.append(mill[positions.index(None)])
                return old_new_pos
        return None

    def is_blocking_piece(self, pos): # Megmondja, hogy az adott pozíció blokkolja-e az ellenfél egy malmát
        for mill in self.mills:
            if pos in mill:
                positions = [self.board[pos] for pos in mill]
                if positions.count("Player") == 2 and positions.count("AI") == 1:
                    return True
        return False

    def flying_block_opponent_mill(self): # Ha létezik, visszaad egy olyan ugrást, ami blokkolja az ellenfél malmát (3. fázis)
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 2 and positions.count(None) == 1:
                possible_old_pos = [pos for pos, piece in self.board.items() if piece == "AI" and self.is_blocking_piece(pos) is False]
                if possible_old_pos: # Lehetőleg nem olyan bábuval lép, ami más malmot blokkol
                    old_new_pos = [random.choice(possible_old_pos), mill[positions.index(None)]]
                else:
                    ai_old_pos = [pos for pos, piece in self.board.items() if piece == "AI"]
                    old_new_pos = [random.choice(ai_old_pos), mill[positions.index(None)]]
                return old_new_pos
        return None    

    def flying_make_potential_mill(self): # Ha tud, visszaad egy olyan ugrást, ami potenciális malmot csinál (3. fázis)
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 1 and positions.count(None) == 2:
                possible_old_pos = [pos for pos, piece in self.board.items() if piece == "AI" and self.is_blocking_piece(pos) is False and pos not in mill]
                if possible_old_pos:
                    old_new_pos = [random.choice(possible_old_pos), mill[positions.index(None)]]
                    return old_new_pos
        return None

    def flying_random_move(self): # Random lép valami szabályosat
        possible_old_pos = [pos for pos, piece in self.board.items() if piece == "AI" and self.is_blocking_piece(pos) is False]
        if possible_old_pos: # Lehetőleg nem olyan bábuval lép, ami más malmot blokkol
            old_new_pos = [random.choice(possible_old_pos), random.choice(self.empty_positions())]
        else:
            ai_old_pos = [pos for pos, piece in self.board.items() if piece == "AI"]
            old_new_pos = [random.choice(ai_old_pos), random.choice(self.empty_positions())]
        return old_new_pos

    def flying_strategy(self): # A prioritási sorrend szerint végigpróbálja az 3. fázis lépéseit
        for strategy in [self.flying_make_mill(), self.flying_block_opponent_mill(), self.flying_make_potential_mill(), self.flying_random_move()]:
            if strategy is not None:
                return strategy



    def neighbouring_pieces(self, player, pos): # Visszadja az adott pozíció "player" színű szomszédainak listáját
        neighbours1 = [conn[0] for conn in self.connections if conn[1] == pos]
        neighbours2 = [conn[1] for conn in self.connections if conn[0] == pos]
        neighbours = neighbours1 + neighbours2
        neighbouring_pieces = [neighbour for neighbour in neighbours if self.board[neighbour] == player]
        return neighbouring_pieces
    
    def moving_make_mill(self): # Ha létezik, visszaad egy olyan lépést, ami malmot csinál (2. fázis)
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 2 and positions.count(None) == 1: # 2 helyen már ő van, a harmadik üres
                possible_old_pos = [pos for pos in self.neighbouring_pieces("AI", mill[positions.index(None)]) if pos not in mill] # Oda tud lépni az üres helyre
                if possible_old_pos:
                    return [random.choice(possible_old_pos), mill[positions.index(None)]]
        return None

    def moving_block_opponent_mill(self): # Ha létezik, visszaad egy olyan lépést, ami blokkolja az ellenfél malmát (2. fázis)
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 2 and positions.count(None) == 1:
                neighbouring_pieces = self.neighbouring_pieces("Player", mill[0]) + self.neighbouring_pieces("Player", mill[1]) + self.neighbouring_pieces("Player", mill[2])
                for pos in mill:
                    if pos in neighbouring_pieces:
                        neighbouring_pieces.remove(pos) # A malom pozícióinak külső "player" színű szomszédjai
                possible_old_pos = self.neighbouring_pieces("AI", mill[positions.index(None)])
                if neighbouring_pieces and possible_old_pos: # Ha a Playernek van bábuja, amivel 1-2 lépésben malmot csinálna, az AI belép a malomba, ha tud
                    old_pos = [pos for pos in possible_old_pos if self.is_blocking_piece(pos) is False and self.is_in_mill("AI", pos) is False]
                    if old_pos: # Lehetőleg nem olyan bábuval lép, ami más malmot blokkol
                        return [random.choice(old_pos), mill[positions.index(None)]]
                    return [random.choice(possible_old_pos), mill[positions.index(None)]]
        return None    

    def moving_make_csikicsuki(self): # Ha tud, visszaad egy olyan lépést, ami csiki-csukit csinál (2. fázis)
        for mill in self.mills: # Egy lépésből befejez egy csiki-csukit
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 3: # A csiki-csuki egyik malma
                for other_mill in self.mills:
                    other_positions = [self.board[pos] for pos in other_mill]
                    if other_positions.count("AI") == 2 and other_positions.count(None) == 1 and set(other_mill).isdisjoint(set(mill)): # A csiki-csuki másik malma
                        ai_positions = [pos for pos in other_mill if self.board[pos] == "AI"]
                        if ai_positions[0] in (self.neighbouring_pieces("AI", mill[0])+self.neighbouring_pieces("AI", mill[1])+self.neighbouring_pieces("AI", mill[2])):
                            return [ai_positions[0], other_mill[other_positions.index(None)]]
                        if ai_positions[1] in (self.neighbouring_pieces("AI", mill[0])+self.neighbouring_pieces("AI", mill[1])+self.neighbouring_pieces("AI", mill[2])):
                            return [ai_positions[1], other_mill[other_positions.index(None)]]
        for mill in self.mills: # Két lépésből befejez egy csiki-csukit
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 3: # A csiki-csuki egyik malma
                for other_mill in self.mills:
                    other_positions = [self.board[pos] for pos in other_mill]
                    if other_positions.count("AI") == 1 and other_positions.count(None) == 2 and set(other_mill).isdisjoint(set(mill)): # A csiki-csuki másik malma
                        none_positions = [pos for pos in other_mill if self.board[pos] == None]
                        old_pos_0 = list(set(self.neighbouring_pieces("AI", none_positions[0])) - set(other_mill)) # A csiki-csuki másik malmának egyik üres pozíciójának "AI" színű szomszédjai
                        old_pos_1 = list(set(self.neighbouring_pieces("AI", none_positions[1])) - set(other_mill)) # A csiki-csuki másik malmának másik üres pozíciójának "AI" színű szomszédjai
                        if none_positions[1] in (self.neighbouring_pieces(None, mill[0])+self.neighbouring_pieces(None, mill[1])+
                                                 self.neighbouring_pieces(None, mill[2])) and old_pos_0:
                            return [random.choice(old_pos_0), none_positions[0]]
                        elif none_positions[0] in (self.neighbouring_pieces(None, mill[0])+self.neighbouring_pieces(None, mill[1])+
                                                   self.neighbouring_pieces(None, mill[2])) and old_pos_1:
                            return [random.choice(old_pos_1), none_positions[1]]
        return None

    def moving_make_potential_mill(self): # Ha tud, visszaad egy olyan lépést, ami potenciális malmot csinál (2. fázis)
        for mill in self.mills: # Belép az üres pozíció szomszédjába, ha 2 helyen már ő van
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 2 and positions.count(None) == 1:
                possible_new_pos = self.neighbouring_pieces(None, mill[positions.index(None)])
                possible_old_new_pos = [[old_pos, new_pos] for new_pos in possible_new_pos for old_pos in self.neighbouring_pieces("AI", new_pos) 
                                        if self.is_blocking_piece(old_pos) is False and self.is_in_mill("AI", old_pos) is False]
                if possible_old_new_pos:
                    return random.choice(possible_old_new_pos)
        for mill in self.mills: # 1 lépésből csukható malmot csinál
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 1 and positions.count(None) == 2:
                none_positions = [pos for pos in mill if self.board[pos] == None]
                old_pos_0 = list(set(self.neighbouring_pieces("AI", none_positions[0])) - set(mill)) # Az egyik üres pozíció "AI" színű szomszédjai
                old_pos_1 = list(set(self.neighbouring_pieces("AI", none_positions[1])) - set(mill)) # A másik üres pozíció "AI" színű szomszédjai
                if old_pos_0 and old_pos_1: # Ha mindkét üres pozícióba be tud lépni, akkor belép az egyikbe
                    possible_old_new_pos = [[old_pos, new_pos] for new_pos in none_positions for old_pos in self.neighbouring_pieces("AI", new_pos) 
                                            if old_pos not in mill and self.is_blocking_piece(old_pos) is False and self.is_in_mill("AI", old_pos) is False]
                    if possible_old_new_pos:
                        return random.choice(possible_old_new_pos)
        return None

    def moving_open_mill(self): # Kinyitja a malmát (2. fázis)
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 3:
                possible_old_new_pos = [[old_pos, new_pos] for old_pos in mill for new_pos in self.neighbouring_pieces(None, old_pos) 
                                        if self.removing_potential_mill() is None and not self.neighbouring_pieces("Player", old_pos)] # Akkor nyitja ki, ha a Playernek nincs nyitott malma és belépni se fog tud a nyitott malmába
                if possible_old_new_pos:
                    return random.choice(possible_old_new_pos)
        return None
    
    def moving_random_move(self): # Random lép valami szabályosat
        possible_old_pos = [pos for pos, piece in self.board.items() if piece == "AI" and self.is_blocking_piece(pos) is False]
        possible_old_new_pos = [[old_pos, new_pos] for old_pos in possible_old_pos for new_pos in self.neighbouring_pieces(None, old_pos)]
        if possible_old_new_pos: # Lehetőleg nem olyan bábuval lép, ami más malmot blokkol
            return random.choice(possible_old_new_pos)
        else:
            possible_old_pos = [pos for pos, piece in self.board.items() if piece == "AI"]
            possible_old_new_pos = [[old_pos, new_pos] for old_pos in possible_old_pos for new_pos in self.neighbouring_pieces(None, old_pos)]
            if possible_old_new_pos:
                return random.choice(possible_old_new_pos)
        return None

    def moving_strategy(self): # A prioritási sorrend szerint végigpróbálja az 2. fázis lépéseit
        for strategy in [self.moving_make_mill(), self.moving_block_opponent_mill(), self.moving_make_csikicsuki(), 
                         self.moving_make_potential_mill(), self. moving_open_mill(), self.moving_random_move()]:
            if strategy is not None:
                return strategy
        return None # (ez az ha nem tud lépni)


    
    def removing_csikicsuki(self): # Csiki-csukiból vesz le bábut
        for mill in self.mills: # Működő csiki-csukiból vesz le
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 3: # A csiki-csuki egyik malma
                for other_mill in self.mills:
                    other_positions = [self.board[pos] for pos in other_mill]
                    if other_positions.count("Player") == 2 and other_positions.count(None) == 1 and set(other_mill).isdisjoint(set(mill)) and other_mill[other_positions.index(None)] in (
                        self.neighbouring_pieces(None, mill[0])+self.neighbouring_pieces(None, mill[1])+self.neighbouring_pieces(None, mill[2])): # A csiki-csuki másik malma
                        removable_pieces = [pos for pos in other_mill if self.is_valid_removal("Player", pos) is True]
                        if removable_pieces:
                            return random.choice(removable_pieces)
        for mill in self.mills: # Blokkolt csiki-csukiból vesz le
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 3: # A csiki-csuki egyik malma
                for other_mill in self.mills:
                    other_positions = [self.board[pos] for pos in other_mill]
                    if other_positions.count("Player") == 2 and other_positions.count("AI") == 1 and set(other_mill).isdisjoint(set(mill)) and other_mill[other_positions.index("AI")] in (
                        self.neighbouring_pieces("AI", mill[0])+self.neighbouring_pieces("AI", mill[1])+self.neighbouring_pieces("AI", mill[2])): # A csiki-csuki másik malma
                        removable_pieces = [pos for pos in other_mill if self.is_valid_removal("Player", pos) is True]
                        if removable_pieces:
                            return random.choice(removable_pieces)
        return None

    def removing_potential_mill(self): # Potenciális malomból vesz le bábut
        removable_pieces = []
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("Player") == 2 and positions.count(None) == 1:
                neighbouring_pieces = self.neighbouring_pieces("Player", mill[positions.index(None)])
                for pos in mill:
                    if pos in neighbouring_pieces:
                        neighbouring_pieces.remove(pos)
                if neighbouring_pieces: # Ha a Player be tudná fejezni a malmot, az AI levesz belőle, ha lehet
                    player_positions = [pos for pos in mill if self.board[pos] == "Player"]
                    potential_removable_pieces = neighbouring_pieces + player_positions
                    for pos in potential_removable_pieces:
                        if self.is_valid_removal("Player", pos):
                            removable_pieces.append(pos) # Beveszi a potenciális malom levehető bábuit
        if removable_pieces:
            return max(set(removable_pieces), key=removable_pieces.count) # Azt adja vissza, aki a legtöbb potenciális malomban van benne
        return None
    
    def removing_blocking_piece(self): # Blokkoló bábut vesz le
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 2 and positions.count("Player") == 1:
                neighbouring_pieces = self.neighbouring_pieces("AI", mill[positions.index("Player")])
                for pos in mill:
                    if pos in neighbouring_pieces:
                        neighbouring_pieces.remove(pos)
                if neighbouring_pieces: # Ha be tudná fejezni a malmot, leveszi a blokkoló bábut
                    return mill[positions.index("Player")]
        for mill in self.mills:
            positions = [self.board[pos] for pos in mill]
            if positions.count("AI") == 2 and positions.count("Player") == 1:
                neighbouring_pieces = self.neighbouring_pieces("AI", mill[positions.index("Player")])
                for pos in neighbouring_pieces:
                    if pos not in mill:
                        neighbouring_pieces.remove(pos)
                two_neighbouring_pieces = [] # Kiválogatja a másodszomszédokat
                for piece in neighbouring_pieces:
                    two_neighbouring_pieces = two_neighbouring_pieces + self.neighbouring_pieces("AI", piece)
                for pos in mill:
                    if pos in two_neighbouring_pieces:
                        two_neighbouring_pieces.remove(pos)
                if two_neighbouring_pieces and self.is_valid_removal("Player", mill[positions.index("Player")]): # Ha 2 lépésből be tudná fejezni a malmot, leveszi a blokkoló bábut
                    return mill[positions.index("Player")]
        return None
    
    def removing_most_neighbours(self): # Leszedi azt, akinek a legtöbb saját színű szomszédja van
        most_neighbours = [] # Akiknek a legtöbb saját színű szomszédjuk van
        max = -1
        removable_pieces = []
        for pos in self.positions:
            if self.is_valid_removal("Player", pos) is True:
                removable_pieces.append(pos) # Kiválogatja a levehető bábukat
        for pos in removable_pieces:
            neighbouring_pieces = self.neighbouring_pieces("Player", pos)
            count = len(neighbouring_pieces)
            if count > max:
                max = count
                most_neighbours = [pos]
            elif count == max:
                most_neighbours.append(pos)
        return random.choice(most_neighbours)
    
    def removing_strategy(self): # A prioritási sorrend szerint végigpróbálja a levevős lépéseket
        for strategy in [self.removing_csikicsuki(), self.removing_potential_mill(), self.removing_blocking_piece(), self.removing_most_neighbours()]:
            if strategy is not None:
                return strategy


    
game = Malom()
game.play_game()