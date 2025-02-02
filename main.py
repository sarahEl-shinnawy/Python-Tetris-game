import pygame
import random
import sys
from pygame import mixer
import pygame_menu
pygame.init()

# adding background sound 
mixer.music.load("MenuTheme.wav")
mixer.music.play(-1)
 
#defining colors
colors = [
    (0, 102, 102),
(0, 153, 204),
(102, 0, 255),
(0, 204, 255),
(153, 255, 204),
(153, 153, 255),
(255, 153, 207)]
 # Adding background image 
bg_image = pygame.image.load('899.jpg') 
 
# Function for the start menu
def start_menu(button_label):
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
    button_rect = pygame.Rect((width - button_width) // 2, (height - button_height) // 2 + 35, button_width, button_height)
    button_color = (255, 0, 0)
    button_hover_color = (0, 255, 0)
    button_pressed = False

    # Font setup
    font = pygame.font.Font(None, 36)
    text = font.render(button_label, True, (255, 255, 255))

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

        if button_pressed:
            break


class tetrominos:
    x = 0
    y = 0
#defining game figures
    tetrominos = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]
#inializing the game figures
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.tetrominos) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0
#returning the image representation of a tetromino based on its type and rotation
    def img(self):
        return self.tetrominos[self.type][self.rotation]
#rotating the current tetromino.
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.tetrominos[self.type])
 
class Tetris:
#initializing the tetris game logic
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.tetrominos = None
    
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        #creating game grid
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)
  #Creates a new tetromino object and assigns it to the self.tetrominos variable.
    def new_tetrominos(self):
        self.tetrominos = tetrominos(3, 0)
#Checks for collisions between the current tetromino and the game board or other tetrominoes.
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tetrominos.img():
                    if i + self.tetrominos.y > self.height - 1 or \
                            j + self.tetrominos.x > self.width - 1 or \
                            j + self.tetrominos.x < 0 or \
                            self.field[i + self.tetrominos.y][j + self.tetrominos.x] > 0:
                        intersection = True
        return intersection
#Handles line clearing in the game.
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2
#Quickly moves the tetromino down until it collides with something.
    def go_space(self):
        while not self.intersects():
            self.tetrominos.y += 1
        self.tetrominos.y -= 1
        self.freeze()
#Moves the tetromino down one step.
    def go_down(self):
        self.tetrominos.y += 1
        if self.intersects():
            self.tetrominos.y -= 1
            self.freeze()
 
    def freeze(self):
        for i in range(4): #This loop iterates over a 4x4 grid, representing the shape of the current tetromino
            for j in range(4):
                if i * 4 + j in self.tetrominos.img():
                    self.field[i + self.tetrominos.y][j + self.tetrominos.x] = self.tetrominos.color
        self.break_lines() #break_lines method. This likely checks for and removes completed lines in the game field.
        self.new_tetrominos() #It generates a new tetromino after the current one has been frozen and processed.
        if self.intersects(): #It checks if the newly placed tetromino intersects with existing blocks in the game field. 
            self.state = "gameover" # it sets the game state to game over


    def go_side(self, dx):
        old_x = self.tetrominos.x #It stores the current x-coordinate of the tetromino before attempting to move it
        self.tetrominos.x += dx #then the tetromino is moved by distance dx
        if self.intersects(): # cheks if there's an intersection with new tetromino
            self.tetrominos.x = old_x # cheks if there's an intersection with new tetromino
    

    def rotate(self):
        old_rotation = self.tetrominos.rotation #This line stores the current rotation state of the tetromino in a variable named old_rotation
        self.tetrominos.rotate()  # this method is responsible for changing the rotation state of the tetromino.
        if self.intersects(): # checks if there's intersection occured
            self.tetrominos.rotation = old_rotation # return to the old place of the tetromino

# creating game over menu with a quit button
def game_over_menu():
    pygame.init()
  
     #customizing pygame_menu theme 
    mytheme = pygame_menu.themes.Theme(
        background_color=(0, 0, 0, 0),
        title_background_color=(0, 0, 0),
        title_font_shadow=True,
        title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE
    )
    #defining window size and name
    surface = pygame.display.set_mode((400, 500))
    pygame.display.set_caption("TETRIS GAME")
    # adding game over background image
    def main_background() -> None:
        background = pygame_menu.BaseImage(image_path="GAME OVER IMG.jpg")
        background.draw(surface)
        
    menu = pygame_menu.Menu('', 400, 300, theme=mytheme)
    #adding the quit button
    menu.add.button('Quit', pygame_menu.events.EXIT
)
    
    menu.mainloop(surface, main_background)

 
# Initialize the game engine
pygame.init()

# Define some colors for grid.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)



size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False
start_menu("Play")

 
while not done:    #it enters into agame loop that continues until the done variable is set to True
    
    if game.tetrominos is None: #withen the game loop,it checks if the game.tetrominous is None if it is,it creates
        game.new_tetrominos() 
    counter += 1 #it increments the counter variable by 1
    if counter > 100000:#if the counter exceeds 100,000, it resets the counter to 0
        counter = 0
    

    if counter % (fps // game.level // 2) == 0 or pressing_down: #it checks if the counter is division by the values of fps divided by game.level divided by 2 if it is 
        if game.state == "start":                                 #the game.state is "start" , it moves the tetromino down
            game.go_down()

    for event in pygame.event.get():  # it processes any events that occur during the game loop
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # rotating the teromino, moving it to the up
                game.rotate()
            if event.key == pygame.K_DOWN:  # rotating the teromino, moving it to the down
                pressing_down = True
            if event.key == pygame.K_LEFT:  # rotating the teromino, moving it to the left
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:  # rotating the teromino, moving it to the right
                game.go_side(1)
            if event.key == pygame.K_SPACE:  # k.SPACE it performs a specific action in the game e.g. dropping the tetromino to the bottom
                game.go_space()
            if event.key == pygame.K_ESCAPE:  # K.KSPACE it reinitializes the game
                game.__init__(20, 10)

        if event.type == pygame.KEYUP:  # if the key is released, it sets the pressing_down variable to False
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.blit(bg_image, (0, 0))  # Adding background image inside loop

    for i in range(game.height):  # draw.rect  it draws the game field which is represented by rectangles on the screen
        for j in range(game.width):
            pygame.draw.rect(screen, WHITE, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.tetrominos is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.tetrominos.img():
                    pygame.draw.rect(screen, colors[game.tetrominos.color],
                                     [game.x + game.zoom * (j + game.tetrominos.x) + 1,
                                      game.y + game.zoom * (i + game.tetrominos.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)  # It renders and displays the score on the screen using a specified font
    font1 = pygame.font.SysFont('Calibri', 37, True, False)
    text = font.render("Score: " + str(game.score), True, WHITE)
    text_game_over = font1.render("          Game Over", True, (204, 255, 255))  # If the game state is "gameover", it displays the "Game Over" message and the "Press ESC" message on the screen
    text_game_over1 = font1.render("Press ESC to play again", True, (204, 255, 255))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])
        #calling the game over menu
        game_over_menu()

    pygame.display.flip()  # It updates the display pygame.display.flip()) and limits the frame rate to a specified value clock.tick(fps)
    clock.tick(fps)

# Once the game loop is exited (when done is set to True), it calls pygame.quit() to uninitialize the Pygame modules and exits the program
pygame.quit()