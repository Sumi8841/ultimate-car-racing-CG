import turtle
import random
import winsound
import os
import time

def play_sound(sound_type):
    try:
        if sound_type == "beep":
            winsound.Beep(800, 150)
        elif sound_type == "go":
            winsound.Beep(1200, 400)
        elif sound_type == "nitro":
            winsound.Beep(1500, 100)
        elif sound_type == "coin":
            winsound.Beep(2000, 80)
        elif sound_type == "win":
            winsound.Beep(1000, 150)
            winsound.Beep(1200, 150)
            winsound.Beep(1500, 400)
        elif sound_type == "lose":
            winsound.Beep(400, 200)
            winsound.Beep(200, 300)
    except:
        pass

LEADERBOARD_FILE = "race_leaderboard.txt"
if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w") as f:
        f.write("red:0\ngreen:0\nblue:0\norange:0\nyellow:0")

player_wallet = 100

def load_leaderboard():
    scores = {}
    with open(LEADERBOARD_FILE, "r") as f:
        for line in f:
            color, score = line.strip().split(":")
            scores[color] = int(score)
    return scores

def update_leaderboard(winner):
    scores = load_leaderboard()
    scores[winner] += 1
    with open(LEADERBOARD_FILE, "w") as f:
        for color, score in scores.items():
            f.write(f"{color}:{score}\n")

screen = turtle.Screen()
screen.title("🏁 Grand Prix Racing Simulation Pro 🏁")
screen.setup(width=900, height=700)

car_images = ["car_red.gif", "car_green.gif", "car_blue.gif", "car_orange.gif", "car_yellow.gif"]
for image in car_images:
    screen.register_shape(image)

drawer = turtle.Turtle()
drawer.speed(0)
drawer.hideturtle()

hud_drawer = turtle.Turtle()
hud_drawer.speed(0)
hud_drawer.hideturtle()

weather_drawer = turtle.Turtle()
weather_drawer.speed(0)
weather_drawer.hideturtle()

def draw_podium(first, second, third):
    drawer.clear()
    hud_drawer.clear()
    weather_drawer.clear()
    screen.bgcolor("#1a252f")
    
    drawer.penup()
    drawer.color("#f1c40f")
    drawer.goto(0, 180)
    drawer.write("🏆 VICTORY PODIUM 🏆", align="center", font=("Courier", 26, "bold"))
    
    podiums = [
        {"pos": (-100, -100), "w": 80, "h": 120, "color": "#bdc3c7", "text": "2nd", "car": second, "car_pos": (-100, 30)},
        {"pos": (0, -100), "w": 80, "h": 180, "color": "#f1c40f", "text": "1st", "car": first, "car_pos": (0, 90)},
        {"pos": (100, -100), "w": 80, "h": 80, "color": "#e67e22", "text": "3rd", "car": third, "car_pos": (100, -10)}
    ]
    
    for p in podiums:
        drawer.penup()
        drawer.goto(p["pos"])
        drawer.color(p["color"])
        drawer.begin_fill()
        for _ in range(2):
            drawer.forward(p["w"])
            drawer.left(90)
            drawer.forward(p["h"])
            drawer.left(90)
        drawer.end_fill()
        
        drawer.color("white")
        drawer.goto(p["pos"][0] + p["w"]/2, p["pos"][1] + 20)
        drawer.write(p["text"], align="center", font=("Arial", 16, "bold"))
        
        p["car"].goto(p["car_pos"])
        p["car"].showturtle()

def start_race():
    global player_wallet
    drawer.clear()
    hud_drawer.clear()
    weather_drawer.clear()
    
    weather_modes = ["Sunny", "Rainy", "Night Mode"]
    current_weather = random.choice(weather_modes)
    
    if current_weather == "Sunny":
        screen.bgcolor("#2c3e50")
        track_color = "#7f8c8d"
    elif current_weather == "Rainy":
        screen.bgcolor("#34495e")
        track_color = "#95a5a6"
    else:
        screen.bgcolor("#111111")
        track_color = "#2c3e50"
        
    drawer.penup()
    drawer.color("white")
    drawer.pensize(4)
    drawer.goto(-250, 220)
    drawer.pendown()
    drawer.goto(-250, -220)

    drawer.penup()
    drawer.color("#e74c3c")
    drawer.pensize(5)
    drawer.goto(220, 220)
    drawer.pendown()
    drawer.goto(220, -220)

    drawer.pensize(1)
    drawer.color(track_color)
    for y in [-140, -60, 20, 100, 180]:
        drawer.penup()
        drawer.goto(-250, y)
        while drawer.xcor() < 220:
            drawer.pendown()
            drawer.forward(10)
            drawer.penup()
            drawer.forward(10)

    if current_weather == "Rainy":
        weather_drawer.color("#3498db")
        for _ in range(20):
            weather_drawer.penup()
            weather_drawer.goto(random.randint(-300, 300), random.randint(-200, 250))
            weather_drawer.write("💧", font=("Arial", 10))
    elif current_weather == "Night Mode":
        weather_drawer.color("#f1c40f")
        for _ in range(15):
            weather_drawer.penup()
            weather_drawer.goto(random.randint(-350, 350), random.randint(230, 300))
            weather_drawer.write("⭐", font=("Arial", 8))

    scores = load_leaderboard()
    hud_drawer.penup()
    hud_drawer.color("#f1c40f")
    hud_drawer.goto(-420, 310)
    hud_drawer.write(f"💰 Wallet: {player_wallet} Coins  |  🌦️ Weather: {current_weather}", font=("Arial", 13, "bold"))
    
    hud_drawer.goto(-420, 280)
    leaderboard_text = f"🏆 Wins -> R:{scores['red']} | G:{scores['green']} | B:{scores['blue']} | O:{scores['orange']} | Y:{scores['yellow']}"
    hud_drawer.write(leaderboard_text, font=("Arial", 11, "bold"))

    coins_x = [random.randint(-150, 150) for _ in range(5)]
    y_positions = [-180, -90, 0, 90, 180]

    for i in range(5):
        drawer.penup()
        drawer.color("#f1c40f")
        drawer.goto(coins_x[i], y_positions[i] + 15)
        drawer.write("🪙", align="center", font=("Arial", 12, "bold"))

    user_bet = screen.textinput(title="Place Your Bet 🚗", prompt=f"Wallet: {player_wallet} Coins\nChoose Winner (red, green, blue, orange, yellow):")
    if not user_bet or user_bet.lower() not in ["red", "green", "blue", "orange", "yellow"]:
        return

    bet_amount = screen.numinput(title="Bet Amount 💰", prompt=f"Enter bet amount (1 - {player_wallet}):", default=10, minval=1, maxval=player_wallet)
    if not bet_amount:
        bet_amount = 10
    bet_amount = int(bet_amount)

    color_names = ["red", "green", "blue", "orange", "yellow"]
    all_cars = []

    for index in range(0, 5):
        new_car = turtle.Turtle()
        new_car.shape(car_images[index])
        new_car.penup()
        new_car.goto(x=-280, y=y_positions[index])
        all_cars.append(new_car)

    for count in [3, 2, 1, "GO!"]:
        hud_drawer.penup()
        hud_drawer.goto(0, 240)
        hud_drawer.color("#e74c3c" if count != "GO!" else "#2ecc71")
        hud_drawer.write(count, align="center", font=("Impact", 36, "bold"))
        if count == "GO!":
            play_sound("go")
        else:
            play_sound("beep")
        time.sleep(0.5)
        hud_drawer.clear()
        
        hud_drawer.color("#f1c40f")
        hud_drawer.goto(-420, 310)
        hud_drawer.write(f"💰 Wallet: {player_wallet} Coins  |  🌦️ Weather: {current_weather}", font=("Arial", 13, "bold"))
        hud_drawer.goto(-420, 280)
        hud_drawer.write(leaderboard_text, font=("Arial", 11, "bold"))

    is_race_on = True
    has_hit_coin = [False] * 5
    finished_cars = []

    while is_race_on:
        for index, c in enumerate(all_cars):
            if c not in finished_cars and c.xcor() > 220:
                finished_cars.append(c)
                if len(finished_cars) == 3:
                    is_race_on = False
                    break

        if not is_race_on:
            break

        sorted_cars = sorted(all_cars, key=lambda car: car.xcor(), reverse=True)
        hud_drawer.clear()
        hud_drawer.color("#f1c40f")
        hud_drawer.goto(-420, 310)
        hud_drawer.write(f"💰 Wallet: {player_wallet} Coins  |  🌦️ Weather: {current_weather}", font=("Arial", 13, "bold"))
        hud_drawer.goto(-420, 280)
        hud_drawer.write(leaderboard_text, font=("Arial", 11, "bold"))
        
        hud_drawer.color("white")
        hud_drawer.goto(260, 100)
        hud_drawer.write("📊 LIVE RANKING", font=("Arial", 12, "bold"))
        for rank, car in enumerate(sorted_cars):
            car_color_str = color_names[car_images.index(car.shape())]
            hud_drawer.goto(260, 70 - (rank * 25))
            hud_drawer.write(f"{rank+1}. {car_color_str.upper()}", font=("Arial", 11, "bold"))

        for index, c in enumerate(all_cars):
            if c in finished_cars:
                continue
                
            base_min = 2 if current_weather != "Rainy" else 1
            base_max = 10 if current_weather != "Rainy" else 7
            speed = random.randint(base_min, base_max)
            
            if random.random() < 0.04:
                speed += 12
                play_sound("nitro")

            if c.xcor() >= coins_x[index] and not has_hit_coin[index]:
                speed += 18
                has_hit_coin[index] = True
                play_sound("coin")

            c.forward(speed)

    winning_color = color_names[car_images.index(finished_cars[0].shape())]
    update_leaderboard(winning_color)
    
    if winning_color == user_bet.lower():
        player_wallet += bet_amount
        play_sound("win")
        msg = f"🏆 WINNER: {winning_color.upper()} 🏆\nYou won {bet_amount} coins!"
        color_code = "#1abc9c"
    else:
        player_wallet -= bet_amount
        play_sound("lose")
        msg = f"🏁 WINNER: {winning_color.upper()} 🏁\nYou lost {bet_amount} coins."
        color_code = "#e74c3c"

    for c in all_cars:
        if c not in finished_cars:
            finished_cars.append(c)

    time.sleep(1.5)
    draw_podium(finished_cars[0], finished_cars[1], finished_cars[2])

    drawer.penup()
    drawer.goto(0, -220)
    drawer.color(color_code)
    drawer.write(msg, align="center", font=("Courier", 16, "bold"))

    if player_wallet <= 0:
        drawer.penup()
        drawer.goto(0, -260)
        drawer.color("#e74c3c")
        drawer.write("💥 GAME OVER! You ran out of coins. 💥", align="center", font=("Arial", 18, "bold"))
    else:
        ask_again = screen.textinput(title="Play Again? 🔄", prompt="Do you want to race again? (yes/no):")
        if ask_again and ask_again.lower() == "yes":
            for c in all_cars:
                c.hideturtle()
            start_race()
        else:
            drawer.penup()
            drawer.goto(0, -260)
            drawer.color("white")
            drawer.write("Thanks for playing! Click screen to exit.", align="center", font=("Arial", 14, "bold"))

start_race()
screen.exitonclick()
screen.exitonclick()