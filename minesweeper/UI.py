import pygame as pg


class Button:
    def __init__(self, rect, text, font, callback, bg_color=(150, 150, 150), text_color=(0, 0, 0)):
        self.rect = pg.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.bg_color = bg_color
        self.text_color = text_color

        self.rendered_text = self.font.render(self.text, True,
                                              self.text_color)  # render metoda generująca obraz tekstu w pg
        self.text_pos = self.rendered_text.get_rect(center=self.rect.center)  # określa pozycję tekstu na przycisku

    def draw(self, screen):
        pg.draw.rect(screen, self.bg_color, self.rect)
        pg.draw.rect(screen, (255, 255, 255), self.rect, 2)  # biała ramka
        screen.blit(self.rendered_text, self.text_pos)

    def handle_event(self, event):
        if event.type == pg.MOUSEMOTION and self.rect.collidepoint(event.pos):
            self.bg_color = (150, 100, 100)
        else:
            self.bg_color = (150, 150, 150)
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()
