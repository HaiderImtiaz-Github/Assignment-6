import tkinter as tk
import random

# Initialize the game window
window = tk.Tk()
window.title("Breakout Game")
window.resizable(0, 0)
window.wm_attributes("-topmost", 1)

canvas = tk.Canvas(window, width=600, height=400, bd=0, highlightthickness=0)
canvas.pack()
window.update()

# Game variables
paddle_speed = 20
ball_speed = 3
ball_diameter = 20
paddle_width = 100
paddle_height = 10
paddle_color = "#0095DD"
brick_colors = ["#FF5733", "#33FF57", "#3357FF"]
bricks = []

# Paddle class
class Paddle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.paddle = canvas.create_rectangle(0, 0, paddle_width, paddle_height, fill=paddle_color)
        self.canvas.move(self.paddle, 250, 350)
        self.x = 0
        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)
    
    def draw(self):
        pos = self.canvas.coords(self.paddle)
        if pos[0] + self.x < 0:
            self.x = 0
        if pos[2] + self.x > 600:
            self.x = 0
        self.canvas.move(self.paddle, self.x, 0)
    
    def move_left(self, evt):
        self.x = -paddle_speed
    
    def move_right(self, evt):
        self.x = paddle_speed

# Ball class
class Ball:
    def __init__(self, canvas, paddle, bricks):
        self.canvas = canvas
        self.paddle = paddle
        self.bricks = bricks
        self.ball = canvas.create_oval(0, 0, ball_diameter, ball_diameter, fill="red")
        self.canvas.move(self.ball, 300, 200)
        self.x = random.choice([-ball_speed, ball_speed])
        self.y = -ball_speed
        self.hit_bottom = False
    
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.paddle)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def hit_brick(self, pos):
        for brick in self.bricks:
            brick_pos = self.canvas.coords(brick)
            if pos[2] >= brick_pos[0] and pos[0] <= brick_pos[2]:
                if pos[1] <= brick_pos[3] and pos[3] >= brick_pos[1]:
                    self.canvas.delete(brick)
                    self.bricks.remove(brick)
                    return True
        return False
    
    def draw(self):
        pos = self.canvas.coords(self.ball)
        if pos[1] <= 0:  # Top boundary
            self.y = ball_speed
        if pos[3] >= 400:  # Bottom boundary
            self.hit_bottom = True
        if pos[0] <= 0:  # Left boundary
            self.x = ball_speed
        if pos[2] >= 600:  # Right boundary
            self.x = -ball_speed

        if self.hit_paddle(pos):
            self.y = -ball_speed

        if self.hit_brick(pos):
            self.y = ball_speed

        self.canvas.move(self.ball, self.x, self.y)

# Brick class
def create_bricks(canvas, rows, cols):
    brick_width = 60
    brick_height = 20
    for row in range(rows):
        for col in range(cols):
            x1 = col * (brick_width + 5) + 25
            y1 = row * (brick_height + 5) + 25
            x2 = x1 + brick_width
            y2 = y1 + brick_height
            brick = canvas.create_rectangle(x1, y1, x2, y2, fill=random.choice(brick_colors), outline="black")
            bricks.append(brick)

# Main game function
def game_loop():
    if not ball.hit_bottom:
        ball.draw()
        paddle.draw()
        if len(bricks) == 0:
            canvas.create_text(300, 200, text="You Win!", font=("Arial", 30), fill="green")
            return
    else:
        canvas.create_text(300, 200, text="Game Over", font=("Arial", 30), fill="red")
        return
    window.after(10, game_loop)

# Initialize game objects
paddle = Paddle(canvas)
ball = Ball(canvas, paddle, bricks)
create_bricks(canvas, 5, 8)

# Start the game
game_loop()

# Run the Tkinter main loop
window.mainloop()
