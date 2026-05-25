import turtle
import random

screen = turtle.Screen()
screen.title("🏁 Ultimate Real Car Racing Championship 🏁")
screen.setup(width=650, height=450)
screen.bgcolor("#2c3e50")

car_images = [
    "car_red.gif", 
    "car_green.gif", 
    "car_blue.gif", 
    "car_orange.gif", 
    "car_yellow.gif"
]

for image in car_images:
    screen.register_shape(image)

drawer = turtle.Turtle()
drawer.speed(0)
drawer.hideturtle()
drawer.penup()

drawer.color("white")
drawer.pensize(4)
drawer.goto(-210, 160)
drawer.pendown()
drawer.goto(-210, -160)

drawer.penup()
drawer.color("#e74c3c")
drawer.pensize(5)
drawer.goto(220, 160)
drawer.pendown()
drawer.goto(220, -160)

drawer.pensize(1)
drawer.color("#7f8c8d")
for y in [-110, -50, 10, 70, 130]:
    drawer.penup()
    drawer.goto(-210, y)
    while drawer.xcor() < 220:
        drawer.pendown()
        drawer.forward(10)
        drawer.penup()
        drawer.forward(10)

user_bet = screen.textinput(
    title="Place Your Bet 🚗", 
    prompt="Which car color will win the race?\nEnter a color (red, green, blue, orange, yellow):"
)

color_names = ["red", "green", "blue", "orange", "yellow"]
y_positions = [-140, -80, -20, 40, 100]
all_cars = []

for index in range(0, 5):
    new_car = turtle.Turtle()
    new_car.shape(car_images[index]) 
    new_car.penup()
    new_car.goto(x=-240, y=y_positions[index])
    all_cars.append(new_car)

is_race_on = False
if user_bet:
    is_race_on = True

while is_race_on:
    for c in all_cars:
        if c.xcor() > 210: 
            is_race_on = False
            
            image_filename = c.shape()
            winning_index = car_images.index(image_filename)
            winning_color = color_names[winning_index]
            
            result_banner = turtle.Turtle()
            result_banner.hideturtle()
            result_banner.penup()
            result_banner.goto(0, -20)
            
            result_banner.color("#1abc9c" if winning_color == user_bet.lower() else "#e74c3c")
            
            if winning_color == user_bet.lower():
                result_banner.write(
                    f"🏆 WINNER: {winning_color.upper()} 🏆\nCongratulations! You won the bet!", 
                    align="center", 
                    font=("Courier", 20, "bold")
                )
            else:
                result_banner.write(
                    f"🏁 WINNER: {winning_color.upper()} 🏁\nOops! You lost the bet.", 
                    align="center", 
                    font=("Courier", 20, "bold")
                )
            break
                
        random_distance = random.randint(2, 12)
        c.forward(random_distance)

screen.exitonclick()