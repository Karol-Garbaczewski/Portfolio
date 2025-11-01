import random


class BoardElement:
    def __init__(self, x, y, size=40):
        self.x = x
        self.y = y
        self.size = size
        self.bomb = False
        self.revealed = False
        self.flagged = False
        self.neighbors = []
        self.value = 0  # Liczba bomb w sąsiedztwie

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def calculate_value(self):
        self.value = sum(1 for neighbor in self.neighbors if neighbor.bomb)

    def reveal(self):
        self.revealed = True
        return self.bomb  # Zwraca True jeśli to bomba

    def toggle_flag(self):
        self.flagged = not self.flagged
        return self.flagged

    def __repr__(self):
        return f"Cell({self.x}, {self.y}, value = {self.value}, reavled = {self.revealed})"


class Board:
    def __init__(self, width, height, bomb_count):
        self.width = width
        self.height = height
        self.bomb_count = bomb_count
        self.grid = [[BoardElement(x, y) for y in range(height)] for x in range(width)]
        self.first_click = True
        self.game_over = False
        self.setup_neighbors()
        self.won = None

    def setup_neighbors(self):
        """Dodajemy sądiadów do każdego punktu"""
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        for x in range(self.width):
            for y in range(self.height):
                neighbors = []
                for dx, dy in directions:

                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        neighbors.append(self.grid[nx][ny])
                self.grid[x][y].set_neighbors(neighbors)

    def place_bombs(self, safe_x, safe_y):
        positions = [(x, y) for x in range(self.width)
                     for y in range(self.height)
                     if abs(x - safe_x) > 1 or abs(y - safe_y) > 1]

        bomb_positions = random.sample(positions, self.bomb_count)

        for x, y in bomb_positions:
            self.grid[x][y].bomb = True

        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y].calculate_value()

    def handle_click(self, x, y):
        if self.game_over or not (0 <= x < self.width and 0 <= y < self.height):
            return False

        element = self.grid[x][y]

        if element.flagged:
            return False

        if self.first_click:
            self.place_bombs(x, y)
            self.first_click = False

        if element.bomb:
            element.reveal()
            self.game_over = True
            for x in range(self.width):
                for y in range(self.height):
                    if self.grid[x][y].bomb and not self.grid[x][y].flagged:
                        self.grid[x][y].reveal()
            self.won = False
            return True

        if element.value == 0:
            self.reveal_empty(x, y)
        else:
            element.reveal()

        return False

    def reveal_empty(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return

        element = self.grid[x][y]

        if element.revealed:
            return

        if element.flagged:
            return

        element.revealed = True

        if element.value == 0:
            for neighbor in element.neighbors:
                self.reveal_empty(neighbor.x, neighbor.y)

    def toggle_flag(self, x, y):
        if not self.game_over and 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y].toggle_flag()
        return False

    def check_win(self):
        for row in self.grid:
            for element in row:
                if not element.bomb and not element.revealed:
                    return False
        self.game_over = True
        self.won = True
        return True
