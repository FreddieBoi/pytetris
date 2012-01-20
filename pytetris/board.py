import pygame

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
