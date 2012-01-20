import random

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
