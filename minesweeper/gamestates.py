import pygame as pg
import sys
from datetime import datetime
from UI import Button
from board import Board
import tkinter as tk
import json


class GameStateManager:
    def __init__(self, initial_state):
        self.state = initial_state
        self.state.manager = self  # pozwala stanowi znać managera

    def change_state(self, new_state):
        self.state = new_state
        self.state.manager = self

    def handle_events(self, events):
        self.state.handle_events(events)

    def update(self):
        self.state.update()

    def draw(self, screen):
        self.state.draw(screen)


class GameState:
    def __init__(self, manager, difficulty):
        self.manager = manager
        self.difficulty = difficulty
        self.font = pg.font.SysFont(None, 40)
        self.small_font = pg.font.SysFont(None, 20)

        # Ustawienia planszy wg trudności
        if "Łatwy" in difficulty:
            self.board = Board(6, 6, 7)
        elif "Trudny" in difficulty:
            self.board = Board(20, 20, 90)
        else:  # Customowy tryb
            self.board = Board(20, 20, 30)

        self.tile_size = 25
        self.board_width_px = self.board.width * (self.tile_size + 1) + 1
        self.board_height_px = self.board.height * (self.tile_size + 1) + 1
        self.margin_top = 50  # Miejsce na UI
        self.offset_x = (800 - self.board_width_px) // 2
        self.offset_y = self.margin_top + ((600 - self.margin_top - self.board_height_px) // 2)
        self.ui_font = pg.font.SysFont(None, 30)
        self.start_time = datetime.now()
        self.end_time = datetime.now()

        self.back_button = Button(
            rect=(20, 550, 100, 30),
            text="Menu",
            font=self.small_font,
            callback=lambda: self.manager.change_state(MenuState(self.manager)))
        self.text = None
        self.play_again_button = Button(
            rect=(300, 530, 300, 50),
            text="Zagraj jeszcze raz",
            font=self.font,
            callback=lambda: self.manager.change_state(GameState(self.manager, self.difficulty)))
        self.play_again_active = False

    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.manager.change_state(MenuState(self.manager))

            self.back_button.handle_event(event)
            if self.board.game_over:
                self.play_again_button.handle_event(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                grid_x = (mouse_x - self.offset_x) // self.tile_size
                grid_y = (mouse_y - self.offset_y) // self.tile_size

                if 0 <= grid_x < self.board.width and 0 <= grid_y < self.board.height:
                    if event.button == 1:  # Lewy przycisk
                        if self.board.handle_click(grid_x, grid_y): # dzieje sie to co w board.handle_click
                            pass
                    elif event.button == 3:  # Prawy przycisk
                        self.board.toggle_flag(grid_x, grid_y)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((50, 50, 50))

        # Rysowanie planszy
        for x in range(self.board.width):
            for y in range(self.board.height):
                element = self.board.grid[x][y]
                rect = pg.Rect(
                    self.offset_x + x * self.tile_size,
                    self.offset_y + y * self.tile_size,
                    self.tile_size - 2,
                    self.tile_size - 2
                )

                # Kolor w zależności od stanu
                if element.revealed:
                    color = (200, 200, 200)  # Odkryte
                    if element.bomb:
                        color = (255, 0, 0)  # Bomba
                else:
                    color = (100, 100, 100)  # Zakryte
                    if element.flagged:
                        color = (0, 255, 0)  # Flaga

                pg.draw.rect(screen, color, rect)
                pg.draw.rect(screen, (255, 255, 255), rect, 1)  # Obramowanie

                # Wyświetlanie wartości (liczby bomb wokół)
                if element.revealed and not element.bomb and element.value > 0:
                    text = self.ui_font.render(str(element.value), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

        # Rysowanie UI
        self.text = self.font.render(f"Tryb gry: {self.difficulty}", True, (255, 255, 255))
        screen.blit(self.text, (265, 30))

        # rysowanie czasu
        if not self.board.game_over:
            self.end_time = datetime.now()
        time_stamp = (self.end_time - self.start_time).total_seconds()
        time_formatted = format_time(time_stamp)
        time_icon = f" czas: {time_formatted} "
        time_surface = self.font.render(time_icon, True, (255, 255, 255))

        text_rect = time_surface.get_rect()
        text_rect.topleft = (500, 30)
        pg.draw.rect(screen, (50, 50, 50), text_rect)
        screen.blit(time_surface, text_rect)

        self.back_button.draw(screen)

        if self.board.game_over:
            self.play_again_button.draw(screen)
            self.play_again_active = True
        elif self.play_again_active:
            self.play_again_active = False

        if self.board.game_over and not self.board.won:
            pg.draw.rect(screen, (50, 50, 50), (265, 30, self.text.get_width(), self.text.get_height()))
            self.text = self.font.render(f"Przegrałeś", True, (255, 255, 255))
            text_rect = self.text.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(self.text, text_rect)

        if self.board.check_win():
            pg.draw.rect(screen, (50, 50, 50), (265, 30, self.text.get_width(), self.text.get_height()))
            self.text = self.font.render(f"Wygrałeś", True, (255, 255, 255))
            text_rect = self.text.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(self.text, text_rect)
            self.manager.change_state(WinState(self.manager, time_stamp, self.difficulty))


class CustomGame:
    def __init__(self):
        pass


class WinState:
    def __init__(self, manager, time_stamp, difficulty):
        self.manager = manager
        self.time_stamp = time_stamp
        self.font = pg.font.SysFont(None, 40)
        self.small_font = pg.font.SysFont(None, 20)
        self.back_button = Button(
            rect=(20, 550, 100, 30),
            text="Menu",
            font=self.small_font,
            callback=lambda: self.manager.change_state(MenuState(self.manager)))
        self.play_again_button = Button(
            rect=(300, 530, 300, 50),
            text="Zagraj jeszcze raz",
            font=self.font,
            callback=lambda: self.manager.change_state(GameState(self.manager, self.difficulty))
        )
        self.typed_name = False
        self.player_name = ""
        self.scores_file = "scores.json"
        self.difficulty = difficulty

    def handle_events(self, events):

        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.manager.change_state(MenuState(self.manager))

            self.back_button.handle_event(event)
            self.play_again_button.handle_event(event)

    def show_name_input(self):
        root = tk.Tk()
        root.title("Zwycięstwo!")

        tk.Label(root, text="Wpisz swoje imię/nazwę gracza").pack(padx=10, pady=5)
        name_entry = tk.Entry(root)
        name_entry.pack(padx=10, pady=5)

        def save_and_close():
            self.player_name = name_entry.get()
            self.save_score(self.player_name, self.time_stamp, self.difficulty)
            root.destroy()
            self.typed_name = True

        tk.Button(root, text="Zapisz", command=save_and_close).pack(pady=10)
        root.mainloop()

    def save_score(self, name, time, difficulty):
        # Ładujemy istniejące wyniki lub tworzymy nową strukturę
        try:
            with open(self.scores_file, 'r') as f:
                scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            scores = {
                "Łatwy": [],
                "Trudny": [],
                "Custom": []
            }

        # Dodajemy nowy wynik
        new_score = {
            "name": name,
            "time": self.time_stamp
        }

        scores[difficulty].append(new_score)

        # Zachowujemy tylko top 10 wyników
        scores[difficulty] = scores[difficulty][:10]

        # Zapisujemy z powrotem do pliku
        with open(self.scores_file, 'w') as f:
            json.dump(scores, f, indent=4)

    def draw(self, screen):
        screen.fill((40, 40, 40))
        text = self.font.render(f"Gratulację! Wygrałeś!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        self.back_button.draw(screen)
        self.play_again_button.draw(screen)

        if not self.typed_name:
            self.show_name_input()


    def update(self):
        pass


class MenuState:
    def __init__(self, manager):
        self.manager = manager
        self.font = pg.font.SysFont(None, 36)
        self.buttons = []

        difficulties = [
            ("Łatwy (6x6 8 bomb)", lambda: self.start_game("Łatwy")),
            ("Trudny (20x20 40 bomb)", lambda: self.start_game("Trudny")),
            ("Custom", lambda: self.start_game("Custom")),
        ]

        for i, (label, callback) in enumerate(difficulties):
            btn = Button(rect=(250, 150 + i * 70, 300, 50), text=label, font=self.font,
                         callback=callback)  # jeszcze musimy zdefiniować co robi ten przycisk
            self.buttons.append(btn)

        self.buttons.append(
            Button(rect=(250, 50, 300, 50), text="O autorze", font=self.font, callback=self.about_author))

        self.buttons.append(
            Button(rect=(250, 400, 300, 50), text="Najlepsze wyniki", font=self.font, callback=self.game_scores))
        self.buttons.append(Button(rect=(250, 470, 300, 50), text="Wyjście", font=self.font, callback=self.exit_game))

    def start_game(self, difficulty):

        self.manager.change_state(GameState(self.manager, difficulty))

    def game_scores(self):
        self.manager.change_state(ScoreState(self.manager))

    def about_author(self):
        self.manager.change_state(AboutAuth(self.manager))

    @staticmethod
    def exit_game():
        pg.quit()
        sys.exit()

    def handle_events(self, events):
        for event in events:
            for btn in self.buttons:
                btn.handle_event(event)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((30, 30, 30))
        for btn in self.buttons:
            btn.draw(screen)


class ScoreState:
    def __init__(self, manager):
        self.font = pg.font.SysFont(None, 30)
        self.small_font = pg.font.SysFont(None, 20)
        self.manager = manager
        self.back_button = Button(
            rect=(250, 450, 300, 50),
            text="Powrót do menu",
            font=self.font,
            callback=lambda: self.manager.change_state(MenuState(self.manager)))
        self.ready_scores_easy = None
        self.ready_scores_hard = None
        self.scores = None
        self.load_scores()

    def update(self):
        pass

    def load_scores(self):
        """Ładuje i formatuje wyniki z pliku JSON"""
        try:
            with open("scores.json", 'r') as file:
                data = json.load(file)

                # Sortujemy wyniki dla każdego poziomu trudności
                self.scores = {
                    'Łatwy': sorted(data.get('Łatwy', []), key=lambda x: x['time']),
                    'Trudny': sorted(data.get('Trudny', []), key=lambda x: x['time'])
                }
        except (FileNotFoundError, json.JSONDecodeError):
            self.scores = {
                'Łatwy': [],
                'Trudny': []
            }

    def draw(self, screen):
        screen.fill((40, 40, 40))

        easy = self.font.render(f"Poziom łatwy", True, (255, 255, 255))
        hard = self.font.render(f"Poziom trudny", True, (255, 255, 255))
        screen.blit(easy, (100, 100))
        screen.blit(hard, (500, 100))

        # Rysowanie wyników dla poziomu łatwego
        y_offset = 130
        for i, score in enumerate(self.scores['Łatwy'][:10]):  # Tylko top 10
            text = f"{i + 1}. {score['name']}: {format_time(score['time'])}"
            rendered_text = self.small_font.render(text, True, (200, 200, 255))
            screen.blit(rendered_text, (100, y_offset))
            y_offset += 30

        # Rysowanie wyników dla poziomu trudnego
        y_offset = 130
        for i, score in enumerate(self.scores['Trudny'][:10]):  # Tylko top 10
            text = f"{i + 1}. {score['name']}: {format_time(score['time'])}"
            rendered_text = self.small_font.render(text, True, (200, 200, 255))
            screen.blit(rendered_text, (500, y_offset))
            y_offset += 30

        # Przycisk powrotu
        self.back_button.draw(screen)

    def import_scores(self):
        pass  # chcemy aby pobierała ona najlepsze czasy z jakiegos pliku

    def handle_events(self, events):

        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.manager.change_state(MenuState(self.manager))

            self.back_button.handle_event(event)


class AboutAuth:
    def __init__(self, manager):
        self.font = pg.font.SysFont(None, 30)
        self.title_font = pg.font.SysFont(None, 30, bold=True)
        self.manager = manager

        self.back_button = Button(
            rect=(250, 450, 300, 50),
            text="Powrót do menu",
            font=self.font,
            callback=lambda: self.manager.change_state(MenuState(self.manager)))

        self.author_info = [
            "Autor: Karol Garbaczewski",
            "Wersja gry: 1.0",
            "Data stworzenia: 04.06.2025",
            "Technologie: Python, Pygame"
        ]

    def handle_events(self, events):

        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.manager.change_state(MenuState(self.manager))

            self.back_button.handle_event(event)

    def draw(self, screen):
        screen.fill((40, 40, 40))

        # Tytuł
        title = self.title_font.render("O Autorze", True, (255, 255, 255))
        screen.blit(title, (250, 50))

        # Informacje o autorze
        for i, line in enumerate(self.author_info):
            text = self.font.render(line, True, (200, 200, 255))
            screen.blit(text, (250, 150 + i * 40))

        # Przycisk powrotu
        self.back_button.draw(screen)

    def update(self):
        pass


def format_time(seconds):
    minutes = int(seconds // 60)
    seconds_remaining = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02d}:{seconds_remaining:02d}.{milliseconds:03d}"
