import tkinter as tk
import random

# Constants
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20
DELAY = 100

# Directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = DOWN
        self.head = self.canvas.create_rectangle(self.body[0][0] * CELL_SIZE, self.body[0][1] * CELL_SIZE,
                                                (self.body[0][0] + 1) * CELL_SIZE, (self.body[0][1] + 1) * CELL_SIZE,
                                                fill="green")
        self.length = 1

    def move(self):
        x, y = self.body[0]
        if self.direction == UP:
            y -= 1
        elif self.direction == DOWN:
            y += 1
        elif self.direction == LEFT:
            x -= 1
        elif self.direction == RIGHT:
            x += 1

        self.body.insert(0, (x, y))
        if len(self.body) > self.length:
            self.canvas.delete(self.body.pop())

        self.canvas.move(self.head, (x - self.body[0][0]) * CELL_SIZE, (y - self.body[0][1]) * CELL_SIZE)

    def change_direction(self, direction):
        if direction != self.direction and (self.direction + direction) % 2 != 0:
            self.direction = direction

class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = random.randint(0, WIDTH // CELL_SIZE - 1)
        self.y = random.randint(0, HEIGHT // CELL_SIZE - 1)
        self.oval = self.canvas.create_oval(self.x * CELL_SIZE, self.y * CELL_SIZE,
                                           (self.x + 1) * CELL_SIZE, (self.y + 1) * CELL_SIZE,
                                           fill="red")

    def respawn(self):
        self.x = random.randint(0, WIDTH // CELL_SIZE - 1)
        self.y = random.randint(0, HEIGHT // CELL_SIZE - 1)
        self.canvas.coords(self.oval, self.x * CELL_SIZE, self.y * CELL_SIZE,
                           (self.x + 1) * CELL_SIZE, (self.y + 1) * CELL_SIZE)

def game_over():
    canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", font=("Arial", 30), fill="red")
    window.update()

def on_key_press(event):
    if event.keysym in ["Up", "Down", "Left", "Right"]:
        snake.change_direction({
            "Up": UP,
            "Down": DOWN,
            "Left": LEFT,
            "Right": RIGHT
        }[event.keysym])

# Create the game window
window = tk.Tk()
window.title("Snake Game")
window.geometry(f"{WIDTH}x{HEIGHT}")

# Create the canvas
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Create the snake and food objects
snake = Snake(canvas)
food = Food(canvas)

# Bind key events
window.bind("<Left>", on_key_press)
window.bind("<Right>", on_key_press)
window.bind("<Up>", on_key_press)
window.bind("<Down>", on_key_press)

# Game loop
while True:
    if snake.body[0] in snake.body[1:]:
        game_over()
        break
    if snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH // CELL_SIZE or snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT // CELL_SIZE:
        game_over()
        break

    if snake.body[0] == (food.x, food.y):
        snake.length += 1
        food.respawn()

    snake.move()
    window.update()
    window.after(DELAY)