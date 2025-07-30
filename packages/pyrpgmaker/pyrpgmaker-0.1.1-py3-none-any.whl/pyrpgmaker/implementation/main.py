import pygame

from pyrpgmaker.interface.gui import GUI


def main(gui: GUI) -> None:
    """
    Entry function for the game.
    """
    pygame.init()
    pygame.display.set_mode((gui.default_width, gui.default_height), pygame.RESIZABLE if gui.resizable else 0)
    pygame.display.set_caption(gui.title)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.update()
        clock.tick(gui.max_frames_per_second)
