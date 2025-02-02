import pygame
import sys
import pygame
import pygame_menu

def game_over_menu():
    pygame.init()
  
 
    mytheme = pygame_menu.themes.Theme(
        background_color=(0, 0, 0, 0),
        title_background_color=(0, 0, 0),
        title_font_shadow=True,
        title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE
    )
    
    surface = pygame.display.set_mode((400, 500))
    pygame.display.set_caption("TETRIS GAME")
    
    def main_background() -> None:
        background = pygame_menu.BaseImage(image_path="GAME OVER IMG.jpg")
        background.draw(surface)
        
    menu = pygame_menu.Menu('', 400, 300, theme=mytheme)
    menu.add.button('Quit', pygame_menu.events.EXIT
)
    
    menu.mainloop(surface, main_background)

game_over_menu()