import pygame
import sys

pygame.init()

# Set up display
width, height = 400, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Over")

# Uploading image and resizing
background_image = pygame.image.load('menu background 2.png').convert()
background_image = pygame.transform.scale(background_image, (width, height))

# Button properties and location
button_width, button_height = 110, 50
button_rect = pygame.Rect((width - button_width) // 2, (height - button_height) // 2 +35, button_width, button_height)
button_color = (255, 0, 0)
button_hover_color = (0, 255, 0)
button_pressed = False

# Font setup
font = pygame.font.Font(None, 36)
text = font.render('Play', True, (255, 255, 255))

# Main menu loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                button_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            button_pressed = False

    # Background image
    screen.blit(background_image, (0, 0))

    # Button specs
    button_color_to_use = button_hover_color if button_rect.collidepoint(pygame.mouse.get_pos()) else button_color
    pygame.draw.rect(screen, button_color_to_use, button_rect)

    # Draw text on the button
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    # Updating display
    pygame.display.flip()
    
    