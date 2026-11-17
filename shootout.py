import random 
from shootout_constants import SIDES, POWER_LEVELS, SAVE_CHANCE, MISS_CHANCE, FATIGUE_PENALTY, MAX_FATIGUE


def get_coin_call():
    """
    Ask for coin call until valid input is given. 
    """
    choice = input("Call the coin toss (heads/tails): ").lower().strip()
    while choice not in ["heads", "tails"]:
        print("Invalid choice. Please try again. (heads/tails)")
        choice = input("Call the coin toss (heads/tails): ").lower().strip()
    return choice

def coin_toss():
    """
    Simulate a coin toss and return whether the player or the computer goes first. 
    """
    call = get_coin_call()
    flip = random.choice(["heads", "tails"])
    print("The coin landed on", flip)
    if call == flip:
        print("You won the toss! You shoot first.")
        return True
    print("You lost the toss. The computer shoots first.")
    return False

def play_round(player_first, player_goals, computer_goals, player_fatigue, computer_fatigue):
    """
    Play one round (a shot per team) in the right order. Return the new scores and fatigue levels. 
    """
    if player_first:
        goal, player_fatigue = player_shoots(player_fatigue)
        scored, computer_fatigue = player_defends(computer_fatigue)
    else:
        scored, computer_fatigue = player_defends(computer_fatigue)
        goal, player_fatigue = player_shoots(player_fatigue)
    if goal:
        player_goals += 1
    if scored:
        computer_goals += 1
    return player_goals, computer_goals, player_fatigue, computer_fatigue

def get_side(prompt):
    """
    Ask for side until valid input is given. 
    """
    choice = input(prompt).lower().strip()
    while choice not in SIDES:
        print("Invalid choice. Please try again. (left/right/center)")
        choice = input(prompt).lower().strip()
    return choice

def get_power():
    """
    Get a power input from the user until it is valid (1-5)
    """
    power = input("Choose your power (1-5): ").strip()
    while power not in POWER_LEVELS:
        print("Invalid power. Please try again.")
        power = input("Choose your power (1-5): ").strip()
    return int(power)

def computer_side():
    """
    Generate a random side for the computer
    """
    return random.choice(SIDES)

def computer_power():
    """    
    Generate a random computer power level 1-5.
    """
    return int(random.choice(POWER_LEVELS))

def update_fatigue(power, fatigue):
    """
    Return the new fatigue level. Power 4-5 builds fatigue, and 1-2 recovers it. 
    Inputs:
    fatigue: current fatigue level (0-4)
    power: the power of the shot (1-5)

    Outputs: 
    new fatigue level (0-4)

    """
    if power >= 4 and fatigue < MAX_FATIGUE:
        fatigue += 1
    elif power <= 2 and fatigue >0:
        fatigue -= 1
    return fatigue


def shot_outcome(shot, keeper, power, fatigue):
    """
    Return "miss", "saved", or "goal". Higher power misses more but it harder to save when the goalie guesses right. 

    Inputs:
    shot: the side the player shot to (left/right/center)
    keeper: the side the keeper guessed (left/right/center)
    power: the power of the shot (1-5)
    fatigue: the current fatigue level (0-4)

    Outputs:
    "miss" if the shot missed, "saved" if the keeper saved it, or "goal" if it scored. 
    """
    miss_chance = MISS_CHANCE[power]
    if power >= 4:
        miss_chance = miss_chance + fatigue * FATIGUE_PENALTY

    if random.randint(1,100) <= miss_chance:
        return "miss"
    if shot == keeper and random.randint(1,100) <= SAVE_CHANCE[power]:
        return "saved"
    return "goal"

def player_shoots(player_fatigue):
    """
    Player's shot function. Returns (goal, new_fatigue) where goal is true if it scores
    """
    shot = get_side("Where do you want to shoot (left/right/center)? ")
    power = get_power()
    keeper = computer_side()
    print("The goalie dove to the", keeper)

    result = shot_outcome(shot, keeper, power, player_fatigue)
    new_fatigue = update_fatigue(power, player_fatigue)

    if result == "miss":
        print()
        print("MISSED! The ball sails over the goal!")
        print()
    elif result == "saved":
        print()
        print("SAVED by the keeper. The goalie is dancing in the net!")
        print()
    else:
        print()
        print("GOALLLLL! The crowd is going wild!")
        print()
    if new_fatigue >= 2:
        print("Your legs are getting heavy. Power shots will be harder to control.")
    return result == "goal", new_fatigue

def player_defends(computer_fatigue):
    """
    Player's dive. Returns (scored, new_computer_fatigue) where scored is True if the computer scores
    
    """
    dive = get_side("Where do you want to dive? (left/right/center)")
    shot = computer_side()
    power = computer_power()
    print("The computer shot to the", shot, "at power", power)

    result = shot_outcome(shot, dive, power, computer_fatigue)
    new_fatigue = update_fatigue(power, computer_fatigue)
    print()
    if result =="miss":
        print("The computer BLASTED IT WIDE! Huge break for you!")
        print()
        return False, new_fatigue
    elif result == "saved":
        print("You SAVED IT! What a way to track the ball!")
        print()
        return False, new_fatigue
    else:
        print("GOALLLLLL! Computer fans are going wild!")
        print()
        return result == "goal", new_fatigue

def team_can_catch_up(goal, opponent_goals, shots_left):
    """
    Returns True if a team can still win or tie the game. This assumes they score every remaining shot.
    """
    return goal + shots_left >= opponent_goals

def play_game():
    player_goals = 0
    computer_goals = 0
    player_fatigue = 0
    computer_fatigue = 0
    print("WELCOME TO SHOOTOUT!")
    print()
    player_first = coin_toss()

    for round_num in range(1,6):
        print()
        print("Round", round_num)
        player_goals, computer_goals, player_fatigue, computer_fatigue = play_round(
            player_first, player_goals, computer_goals, player_fatigue, computer_fatigue)
        print()
        print("Score: Player", player_goals, "- Computer", computer_goals)
        print()

        rounds_left = 5 - round_num
        if rounds_left >0: 
            if not team_can_catch_up(player_goals, computer_goals, rounds_left):
                print("The computer is too far ahead. You can't catch up!")
                break
            if not team_can_catch_up(computer_goals, player_goals, rounds_left):
                print("Wow, you killed it! The computer can't catch up!")
                break

    round_num = 5
    while player_goals == computer_goals:
        round_num += 1
        print()
        print("SUDDEN DEATH ROUND", round_num)
        player_goals, computer_goals, player_fatigue, computer_fatigue = play_round(
            player_first, player_goals, computer_goals, player_fatigue, computer_fatigue)
        print()
        print("Score: Player", player_goals, "- Computer", computer_goals)
        print()

    if player_goals > computer_goals:
        print("You WIN! Congratulations on beating the computer! Keep the good times rolling!")
    else:
        print("The computer wins. Better luck next time. Try again at beating the computer.")

if __name__ == "__main__":
    play_game()
