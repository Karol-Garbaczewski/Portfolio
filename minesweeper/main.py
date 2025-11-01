from gamestates import GameStateManager, MenuState
import pygame as pg
import sys


# ---------- Main loop ----------
def main():
    pg.init()

    # muzyka bedzie się odtwarzać w nieskończoność
    pg.mixer.init()
    pg.mixer.music.load("saper_sound.mp3")
    pg.mixer.music.play(loops=-1)

    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Saper")
    clock = pg.time.Clock()

    icon = pg.image.load("icon_saper.png")
    pg.display.set_icon(icon)

    manager = GameStateManager(MenuState(None))

    running = True
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False

        manager.handle_events(events)
        manager.update()
        manager.draw(screen)

        pg.display.flip()
        clock.tick(60)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
