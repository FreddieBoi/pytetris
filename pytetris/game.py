import pygame, random
from pytetris import __package__, __version__, Board, Figure

#PyTetris. The main class.
class Game(object):
    #Constructor
    def __init__(self, main):
        self.main = main
        #The background color
        self.color = (255, 255, 255)
        #The game board (grid)
        self.board = Board(self.color)
        #Boolean to handle if game is over or not
        self.game_over = False
        #Boolean to handle if the game is paused or not
        self.is_paused = False
        #The current figure to fall down (dummy figure initially)
        self.figure = Figure(1)
        self.figure.active = False
        #A bag containing the next 7 figures to come down
        self.bag = []
        #The bag index; is used to localize the next figure from the bag
        self.bag_index = 7
        #Init pygame module (setup display/screen, title and font)
        pygame.init()
        self.size = (self.board.w + 1, self.board.h + 1)
        self.screen = pygame.display.set_mode(self.size, 0, 32)
        pygame.display.set_caption(__package__ + " v" + __version__)
        self.font = pygame.font.Font(None, 18)
    
    #Get the next figure to fall down
    def next_figure(self):
        #End of current bag; create a new bag of 7 figures
        if(self.bag_index > 6):
            #Reset bag index
            self.bag_index = 0
            #Create a bag and put 7 new figures into it
            bag = []
            for i in range(1,8):
                bag.append(Figure(i))
            #Shuffle the bag
            random.shuffle(bag)
            #Replace the current bag with the new one
            self.bag = bag
        #Create a new figure
        self.figure = self.bag[self.bag_index]
        #Increase the index
        self.bag_index += 1
    
    #Handle the graphics (draw background, board (grid), texts etc.)
    def draw(self):
        #Render screen background
        backgroundRect = pygame.Rect(0, 0, self.size[0], self.size[1])
        pygame.draw.rect(self.screen, self.color, backgroundRect)
        #Render the board (grid)
        self.board.draw(self.screen)
        #Show the score
        self.screen.blit(self.font.render("Score: " + str(self.board.score), 1,
                         (0, 0, 0)), pygame.Rect((1, 1), (self.size[0], 20)))
        self.screen.blit(self.font.render("Level: " + str(self.board.level), 1,
                         (0, 0, 0)), pygame.Rect((self.size[0] / 2 + self.size[0] / 5, 1),
                                        (self.size[0], 20)))
        #Let the user know if the game is over.
        if self.game_over:
            self.screen.blit(self.font.render("Game over!", 1,
                            (255, 0, 0)), pygame.Rect((1, 20), (self.size[0], 20)))
            self.screen.blit(self.font.render("Press 'R' to restart.", 1,
                            (0, 255, 0)), pygame.Rect((1, 40), (self.size[0], 40)))
        #Let the user know if the game is paused.
        if self.is_paused:
            self.screen.blit(self.font.render("Paused.", 1, (0, 0, 255)),
                       pygame.Rect((1, 20), (self.size[0], 20)))
        #Show a "game over line"
        pygame.draw.line(self.screen, (0, 0, 0), (1, 101), (self.size[0] - 2, 101), 1)
        #Update the display
        pygame.display.update()

    #Start the game loop
    def run(self):
        time_passed = 0
        self.clock = pygame.time.Clock()

        while True:
            #Handle graphics
            self.draw()

            #Tick the clock
            time_passed += self.clock.tick(60)

            #Handle keyboard commands
            key = ""
            for event in pygame.event.get():
                #The user wants to quit the game; terminate!
                if event.type == pygame.QUIT:
                    self.main.quit()
                #A key has been pressed, save it for later use
                if event.type == pygame.KEYDOWN: 
                    key = event.key
                #Escape-key is pressed; quit the game
                if key == pygame.K_ESCAPE:
                    self.main.quit()
                #P-key is pressed; pause/unpause the game
                if (key == pygame.K_p or key == pygame.K_PAUSE) and not self.game_over:
                    #Switch the boolean value
                    self.is_paused = not self.is_paused
                #R-key is pressed; restart the game
                if key == pygame.K_r:
                    self.main.restart()

            #Handle the game movement if the game isn't over and isn't paused
            if not self.game_over and not self.is_paused:

                #A figure is in the "air"
                if self.figure.active:
                    #Listen to keyboard commands and handle the figure movement
                    #Right-arrow; move the figure right
                    if key == pygame.K_RIGHT:
                        self.figure.move(self.board, (1, 0))
                    #Left-arrow; move the figure left
                    elif key == pygame.K_LEFT:
                        self.figure.move(self.board, (-1, 0))
                    #Down-arrow; move down the figure one step
                    elif key == pygame.K_DOWN:
                        self.figure.move(self.board, (0, 1))
                        
                    #Space; instantly drop down the figure all the way
                    elif key == pygame.K_SPACE:
                        #Move the figure down while still in the "air"
                        while self.figure.active:
                            self.figure.move(self.board, (0, 1))
                    #Up-arrow; rotate the figure
                    elif key == pygame.K_UP:
                        self.figure.rotate(self.board)
                    #Move the figure down
                    #if enough time has elapsed since last movement
                    if time_passed >= self.board.wait_time:
                        time_passed = 0
                        self.figure.move(self.board, (0, 1))
                #No active figure
                else:
                    #Check filled up lines (rows)
                    self.board.check_lines()
                    #Check if the game is over
                    if self.board.get_top_y() <= 3:
                        self.game_over = True
                    else:
                        #Create a new figure
                        self.next_figure()
                        #Start dropping the new figure instantly
                        time_passed = self.board.wait_time
