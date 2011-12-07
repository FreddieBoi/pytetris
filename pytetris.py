import pygame, random
from sys import exit

class Figure(object):
    #Constructor
    def __init__(self,shape):
        #The reference x and y coordinates of the figure
        self.x = 4
        self.y = 1
        #The coordinates to fill to create the specific shape
        self.coordinates = []
        #Create the specified shape
        self.create_shape(shape)
        #The current rotation index of the shape (random rotation initially)
        self.rotation = random.randint(0,len(self.coordinates)-1)
        #A unique number used to separate one figure from another
        self.random_id = random.random()
        #A boolean handling if the shape is in the "air" or not
        self.active = True
    
    #Setup the specified shape (color and coordinates)
    def create_shape(self, shape):
        #The tall (red) shape
        if shape == 1:
            self.color = (255,0,0)
            #This shape has two possible rotations (horizontal or vertical)
            #Horizontal coordinates
            self.coordinates.append([(self.x-1,self.y),
                                     (self.x,self.y),
                                     (self.x+1,self.y),
                                     (self.x+2,self.y)])
            #Vertical coordinates
            self.coordinates.append([(self.x,self.y-2),
                                     (self.x,self.y-1),
                                     (self.x,self.y),
                                     (self.x,self.y+1)])
        #The box (green) shape
        elif shape == 2:
            self.color = (0,255,0)
            #This shape looks the same always, rotation doesn't matter
            self.coordinates.append([(self.x,self.y),
                                     (self.x+1,self.y-1),
                                     (self.x+1,self.y),
                                     (self.x,self.y-1)])
        #T: The pyramid (blue) shape
        elif shape == 3:
            self.color = (0,0,255)
            #This shape looks different if rotated.
            #Four sets of coordinates needed.
            #Default coordinates (pyramid is pointing upwards)
            self.coordinates.append([(self.x-1,self.y),
                                     (self.x,self.y),
                                     (self.x+1,self.y),
                                     (self.x, self.y-1)])
            #Shape rotated 90 degrees left (pyramid is pointing to the left)
            self.coordinates.append([(self.x,self.y),
                                     (self.x-1,self.y),
                                     (self.x,self.y+1),
                                     (self.x,self.y-1)])
            #Shape rotated 180 degrees (pyramid is pointing downwards)  
            self.coordinates.append([(self.x-1,self.y),
                                     (self.x,self.y),
                                     (self.x+1,self.y),
                                     (self.x,self.y+1)])
            #Shape rotated 90 degrees right (pyramid is pointing to the right)
            self.coordinates.append([(self.x,self.y),
                                     (self.x+1,self.y),
                                     (self.x,self.y+1),
                                     (self.x,self.y-1)])

        #Z: The Z-shape (yellow)
        elif shape == 4:
            self.color = (255,240,0)
            #This shape has two possible rotations (horizontal or vertical)
            #The default Z-shape horizontal coordinates
            self.coordinates.append([(self.x-1,self.y-1),
                                     (self.x,self.y-1),
                                     (self.x,self.y),
                                     (self.x+1,self.y)])
            #Vertical coordinates
            self.coordinates.append([(self.x+1,self.y-1),
                                     (self.x+1,self.y),
                                     (self.x,self.y),
                                     (self.x,self.y+1)])
        #S: The S-shape (pink)
        elif shape == 5:
            self.color = (255,0,255)
            #This shape has two possible rotations (horizontal or vertical)
            #The default S-shape horizontal coordinates
            self.coordinates.append([(self.x-1,self.y),
                                     (self.x,self.y),
                                     (self.x,self.y-1),
                                     (self.x+1,self.y-1)])
            #Vertical coordinates
            self.coordinates.append([(self.x,self.y-1),
                                     (self.x,self.y),
                                     (self.x+1,self.y),
                                     (self.x+1,self.y+1)])
        #L: The L-shape (dark gray)
        elif shape == 6:
            self.color = (50,50,50)
            #This shape looks different if rotated.
            #Four sets of coordinates needed.
            #Default L-shape coordinates (vertical)
            self.coordinates.append([(self.x,self.y-1),
                                     (self.x,self.y),
                                     (self.x,self.y+1),
                                     (self.x+1,self.y+1)])
            #The shape is lying (horizontal with L-tip up right)
            self.coordinates.append([(self.x-1,self.y),
                                     (self.x,self.y),
                                     (self.x+1, self.y),
                                     (self.x+1, self.y-1)])
            #The L-shape is upside down (vertical) 
            self.coordinates.append([(self.x-1,self.y-1),
                                     (self.x,self.y-1),
                                     (self.x,self.y),
                                     (self.x,self.y+1)])
            #The shape is lying down (horizontal with L-tip down left)
            self.coordinates.append([(self.x-1,self.y),
                                     (self.x-1,self.y+1),
                                     (self.x,self.y),
                                     (self.x+1,self.y)])
        #J: The inverse L-shape (cyan)
        elif shape == 7:
            self.color = (0,255,255)
            #This shape looks different if rotated.
            #Four sets of coordinates needed.
            #Default inverse L-shape coordinates (vertical)
            self.coordinates.append([(self.x,self.y-1),
                                     (self.x,self.y),
                                     (self.x-1,self.y+1),
                                     (self.x,self.y+1)])
            #The shape is lying (horizontal with L-tip down right)
            self.coordinates.append([(self.x-1,self.y),
                                     (self.x,self.y),
                                     (self.x+1,self.y),
                                     (self.x+1,self.y+1)])
            #The inverse L-shape is upside down (vertical)
            self.coordinates.append([(self.x+1,self.y-1),
                                     (self.x,self.y-1),
                                     (self.x,self.y),
                                     (self.x, self.y+1)])
            #The shape is lying (horizontal with L-tip up left)
            self.coordinates.append([(self.x-1,self.y-1),
                                     (self.x-1,self.y),
                                     (self.x,self.y),
                                     (self.x+1,self.y)])

    #Move the figure in the specified direction on the specified board
    def move(self, board, direction):
        #Only allow movement if figure is active (in the "air").
        if self.active:
            #Only move the figure if the move is allowed
            if board.move_allowed(self.random_id,
                                 self.coordinates[self.rotation],
                                 direction):
                #Cover the current coordinates with background color
                board.cover_cells(self.coordinates[self.rotation])
                #Add the direction to all sets of coordinates (move the figure)
                for i in range(len(self.coordinates)):
                    c  = self.coordinates[i]
                    for j in range(len(c)):                
                        c[j] = (c[j][0]+direction[0],c[j][1]+direction[1])
                        if i == self.rotation:
                            x = c[j][0]
                            y = c[j][1]
                            #Fill cells with the current rotation coordinates 
                            board.set_cell(self.color,x,y,self.random_id)

            #Deactivate the figure if moving down isn't allowed
            #(the figure is in place)
            elif direction == (0,1):
                self.active = False
    
    #Rotate the figure
    def rotate(self,board):
        #The new rotation
        new_rotation = self.rotation
        #Rotate 90 degrees to the next step
        if self.rotation < len(self.coordinates)-1:
            new_rotation += 1
        #If rotated 360 degrees, reset rotation             
        else:
            new_rotation = 0
        #Only allow rotation if the figure is active
        if self.active and board.rotate_allowed(self.random_id,
                                 self.coordinates[new_rotation]):
            #Cover the current coordinates with background color
            board.cover_cells(self.coordinates[self.rotation])
            #Rotate the figure
            self.rotation = new_rotation
            #Move the figure "on the spot"
            self.move(board,(0,0))

#Board (a grid of cells).
#Each cell is containing a color, a rectangle (bounds) and a random ID number
#and is accessible using the cell coordinates
#Get the cell at specified x and y coordinate using: cells[(x,y)]
#Get the color of the cell using: cells[(x,y)][0]
#Get the rectangle (the bounds) using: cells[(x,y)][1]
#Get the random ID number using: cells[(x,y)][2]
class Board(object):
    #Constructor
    def __init__(self, color):
        #The grid (cells)
        self.cells = {}
        #The number of rows and columns 
        self.cols = 10
        self.rows = 24
        #The height/width of each grid-cell
        self.cell_width = 25
        self.cell_height = 25
        #The height/width of this board
        self.h = self.cell_height*self.rows
        self.w = self.cell_width*self.cols
        
        #Score and difficulty variables
        #The number of removed lines
        self.lines = 0
        #The current level
        self.level = 1
        #The current score
        self.score = 0
        #The speed (rate) of a figure's downfall
        self.wait_time = 450
        
        #The background (covering) color
        self.color = color
        #Setup an empty grid of cells with background color
        for x in range(self.cols):
            for y in range(self.rows):
                self.set_cell(self.color,x,y,0)
        
    #Make the board draw the grid on the specified screen
    def draw(self, screen):
        #For every cell draw a rectangle
        for i in self.cells:
            #Only needed for non-empty (occupied) cells (random ID > 0)
            if self.cells[i][2] > 0:
                pygame.draw.rect(screen,self.cells[i][0],self.cells[i][1])

    #Set the cell specified by x and y coordinates to the specified color.
    def set_cell(self,color, x, y, randomID):
        #Create the cell rectangle
        cellRect = pygame.Rect((x*self.cell_width+1,y*self.cell_height+1),
                        (self.cell_height-1,self.cell_width-1))
        #Set the cell color, rectangle (bounds) and random ID
        self.cells[(x,y)] = (color,cellRect,randomID)
    
    #Fill the specified coordinates with background color 
    #(used to avoid leaving traces of a figure behind)
    def cover_cells(self, coordinates):
        for i in range(len(coordinates)):
            #Set the cell to background color with the random ID to 0
            self.set_cell(self.color,coordinates[i][0],coordinates[i][1],0)

    #Check if moving in the specified direction from the specified
    #coordinates is allowed
    def move_allowed(self, randomID, coordinates, direction):
        #Check all tuples of coordinates in the direction
        for c in coordinates:
            #Save the position the figure wants to move to
            x = c[0]+direction[0]
            y = c[1]+direction[1]
            #Check if the position is within the grid
            if self.cells.has_key((x,y)):
                #Move is not allowed if the cell is occupied
                #(has another random ID > 0)
                if (self.cells[(x,y)][2] != randomID
                    and self.cells[(x,y)][2] != 0):
                    return False
            #Out of bounds
            else:
                return False
        #Move allowed
        return True

    def rotate_allowed(self, randomID, coordinates):
        #Check all tuples of coordinates
        for c in coordinates:
            #Save the position the figure will occupy when rotated
            x = c[0]
            y = c[1]
            #Check if the position is within the grid
            if self.cells.has_key((x,y)):
                #Rotation is not allowed if the cell already is occupied
                #(has another random ID > 0)
                if (self.cells[(x,y)][2] != randomID
                    and self.cells[(x,y)][2] != 0):
                    return False
            #Out of bounds
            else:
                return False
        #Rotation allowed
        return True
    
    #Check if any rows (lines) are completely filled
    def check_lines(self):
        #The number of filled cols for every row
        filled_cells = {}
        #Go through all cells
        for cell in self.cells:
            y = cell[1]
            #If y-value (row) isn't listed; make room for it
            if not filled_cells.has_key(y):
                filled_cells[y] = 0
            #The cell is occupied (randomID > 0)
            if self.cells[cell][2] > 0:
                #Add 1 to the number of filled cols at this row (y-coordinate)
                filled_cells[y] += 1
        #Temporary storage for the current cleared lines
        templines = self.lines
        #Check all rows
        for i in filled_cells:
            #The row got all cols filled
            if filled_cells[i] >= self.cols:
                #Remove the row
                self.remove_line(i)
                #Increase the number of cleared lines
                self.lines += 1
                #Check if the number of lines increases level
                if self.lines/10 >= self.level:
                    self.level += 1
                    if self.wait_time > 0:
                        self.wait_time -= 22.5
                #Move the cells above down
                self.drop_down_cells(i)
        #Increase the score
        diff = self.lines-templines
        if diff == 1:
            self.score += (self.level) * 40
        elif diff == 2:
            self.score += (self.level) * 100
        elif diff == 3:
            self.score += (self.level) * 300
        #Tetris!
        elif diff == 4:
            self.score += (self.level) * 1200

    #Reset the row at specified y value.
    def remove_line(self, y):
        #Set all cells with specified y-value to background color
        for i in range(self.cols):
            self.set_cell(self.color,i,y,0)
    
    #Move down all cells above the specified border (y-coordinate)
    def drop_down_cells(self,border):
        #A temporary dictionary used for saving the cells to be moved
        cellsToMove = {}
        #Check all cells
        for cell in self.cells:
            x = cell[0]
            y = cell[1]
            color = self.cells[cell][0]
            random_id = self.cells[cell][2]
            #If cell is above the specified border; put it into tempcells
            if y < border:
                #Cover the current cells with background color
                self.set_cell(self.color,x,y,random_id)
                #Create the cell bounds
                rect = pygame.Rect((x*self.cell_width+1,y*self.cell_height+1),
                            (self.cell_height,self.cell_width))
                #Increase all temporary cells y-coordinates (move them down)
                cellsToMove[(x,y+1)] = (color,rect,random_id)
        #Put the temporary cells into the real grid
        for c in cellsToMove:
            x = c[0]
            y = c[1]
            color = cellsToMove[c][0]
            random_id = cellsToMove[c][2]            
            self.set_cell(color,x,y,random_id)
    
    #Returns the y-value that currently is closest to the "game over line"       
    def get_top_y(self):
        top = self.rows
        #Check every cell's y-value
        for cell in self.cells:
            y = cell[1]
            #Save the y-value if it's closer to the top than the current
            if y < top and self.cells[cell][2] > 0:
                top = y
        #Return the top (lowest) value
        return top

#PyTetris. The main class.
class PyTetris(object):
    #Constructor
    def __init__(self):
        #Print info
        name = "PyTetris"
        version = "1.2b"
        print name + " v" + version

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
        pygame.display.set_caption(name + " v" + version)
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
    #Handle exiting actions
    def quit(self):
        print "terminating.."
        exit()

    #Restart the game
    def restart(self):
        print "restarting.."
        PyTetris().run()

    #Start the game loop
    def run(self):
        print "running.."
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
                    self.quit()
                #A key has been pressed, save it for later use
                if event.type == pygame.KEYDOWN: 
                    key = event.key
                #Escape-key is pressed; quit the game
                if key == pygame.K_ESCAPE:
                    self.quit()
                #P-key is pressed; pause/unpause the game
                if (key == pygame.K_p or key == pygame.K_PAUSE) and not self.game_over:
                    #Switch the boolean value
                    self.is_paused = not self.is_paused
                #R-key is pressed; restart the game
                if key == pygame.K_r:
                    self.restart()
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
#Start it up!
if __name__ == "__main__":
    py_tetris = PyTetris().run()