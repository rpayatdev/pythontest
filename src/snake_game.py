from graph import *
from train import *
import random
from tkinter import Tk, Label, Canvas, Button
import sys

SQUARE_SIZE = 25
CANVAS_HEIGHT = 700
CANVAS_WIDTH = 900
FIELD_HEIGHT = int(CANVAS_HEIGHT / SQUARE_SIZE)
FIELD_WIDTH = int(CANVAS_WIDTH / SQUARE_SIZE)
INITIAL_DIRECTION = "down"
YELLOW = "#FFFB00"

class Snake:
    def __init__(self, game):
        self.body_size = 3
        self.coordinates = []
        self.squares = []
        self.colour = "#00FF00"

        for i in range(0, self.body_size):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = game.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=self.colour)
            self.squares.append(square)

class Food:
    def __init__(self, game, snake):
        count = 0
        is_on_snake = True
        while is_on_snake:
            count+=1
            if count > 1000:
                break
                #Spiel ist gewonnen Todoooo!!!!
            is_on_snake = False
            x = random.randint(0, FIELD_WIDTH - 1) * SQUARE_SIZE
            y = random.randint(0, FIELD_HEIGHT - 1) * SQUARE_SIZE
            for snake_x, snake_y in snake.coordinates:
                if snake_x == x and snake_y == y:
                    is_on_snake = True
            
        
        self.coordinates = [x, y]
        self.colour = "#FF0000"
        self.position = game.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=self.colour, tags="food")

class Game:
    def __init__(self, root, graph, train):
        self.root = root
        self.canvas = None
        self.label = None
        self.direction = INITIAL_DIRECTION
        self.score = 0
        self.graph = graph
        self.graph.show()
        self.train = train

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def gameover(self):

        self.train.add()

        self.canvas.delete("all")
        self.label.config(text=f"GAME OVER", fg="red")

        self.graph.add(self.score)
        self.graph.show()

        play_again = Button(self.root, text="Play Again", font=("Helvetica", 20), width=15, command=self.play)
        self.canvas.create_window(CANVAS_WIDTH/2, 370, window=play_again)
        self.canvas.create_text(CANVAS_WIDTH/2, 450, text=f"{self.score}",font=("Helvetica",20),fill="white")

    def next_turn(self, snake, food):
        x, y = snake.coordinates[0]

        if self.direction == 'up':
            y -= SQUARE_SIZE
        if self.direction == 'down':
            y += SQUARE_SIZE
        if self.direction == 'left':
            x -= SQUARE_SIZE
        if self.direction == 'right':
            x += SQUARE_SIZE

        snake.coordinates.insert(0, [x, y])
        square = self.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=snake.colour)
        snake.squares.insert(0, square)

        if x == food.coordinates[0] and y == food.coordinates[1]:
            self.score += 1
            snake.body_size +=1
            self.label.config(text=f"Score is : {self.score}")
            

            last_x, last_y = snake.coordinates[-1]
            snake.coordinates.insert(-1, [last_x, last_y])
            square = self.canvas.create_rectangle(last_x, last_y, last_x + SQUARE_SIZE, last_y + SQUARE_SIZE, fill=snake.colour)
            snake.squares.insert(-1, square)

            self.canvas.delete(food.position)
            food = Food(self, snake)

        del snake.coordinates[-1]
        self.canvas.delete(snake.squares[-1])
        del snake.squares[-1]

        if self.check_collision(snake):
            self.gameover()
        else:
            self.root.after(100, self.next_turn, snake, food)

    def change_direction(self, new_direction):
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        if new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        if new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        if new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction
    
    def get_distance_to_food(self, snake, food):
        # Get the coordinates of the snake's head
        snake_head_x, snake_head_y = snake.coordinates[0]
        # Get the coordinates of the food
        food_x, food_y = food.coordinates
        # Calculate the Manhattan distance between the snake's head and the food
        distance = (abs(snake_head_x - food_x) + abs(snake_head_y - food_y) / SQUARE_SIZE)
        return distance
    
    def get_food_direction(self, snake_head_x, snake_head_y, food_x, food_y):
        
        if snake_head_x == food_x:
            if snake_head_y - food_y == SQUARE_SIZE:
                return 'up'
            elif snake_head_y - food_y == -SQUARE_SIZE:
                return 'down'
        elif snake_head_y == food_y:
            if snake_head_x - food_x== SQUARE_SIZE:
                return 'left'
            elif snake_head_x - food_x == -SQUARE_SIZE:
                return 'right'
        else:
            return 'none'

    def check_collision(self, snake):
        x, y = snake.coordinates[0]

        for x_pos, y_pos in snake.coordinates[1:]:
            if x_pos == x and y_pos == y:
                return True

        if x >= CANVAS_WIDTH or y >= CANVAS_HEIGHT or x < 0 or y < 0:
            return True

        return False

    def play(self):
        # Reset the direction to the initial one
        self.direction = INITIAL_DIRECTION

        # Clear any previous canvas or label to avoid multiple instances
        if self.label:
            self.label.destroy()
        if self.canvas:
            self.canvas.destroy()

        # Reset score and create new label and canvas
        self.score = 0
        self.label = Label(self.root, text=f"Score is : {self.score}", font=('consolas', 50))
        self.label.pack()

        self.canvas = Canvas(self.root, bg="#000000", height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.pack()

        # Re-bind the arrow keys to control the snake
        self.root.bind('<Left>', lambda event: self.change_direction('left'))
        self.root.bind('<Right>', lambda event: self.change_direction('right'))
        self.root.bind('<Down>', lambda event: self.change_direction('down'))
        self.root.bind('<Up>', lambda event: self.change_direction('up'))

        # Create new instances of Food and Snake for the new game
        snake = Snake(self)
        food = Food(self, snake)

        #Todo!!!!
        snake_head_x, snake_head_y = snake.coordinates[0]
        food_x, food_y = food.coordinates
        distance_to_food = self.get_distance_to_food(snake_head_x, snake_head_y, food_x, food_y)
        food_direction = self.get_food_direction(snake_head_x, snake_head_y, food_x, food_y)
        self.status = Status(self.direction, food_direction, 
        
        # Start the next turn
        self.next_turn(snake, food)
    
    def on_closing(self):
        # Gracefully exit the Tkinter mainloop
        self.root.destroy()
        # Optionally close the Python process if needed
        sys.exit()


# Main game setup
root = Tk()
root.title("Snake Game")

graph = Graph()
train = Train()
game = Game(root, graph, train)
game.play()

root.mainloop()