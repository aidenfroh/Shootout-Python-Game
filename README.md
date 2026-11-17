# Shootout

### A Python penalty shootout game where you play against the computer.

#### How to Play:
Run the game file with Python. Keep shootout_constants.py in the same folder.
The game starts with a coin flip. Call heads/tails to se who shoots first. 
There are 5 rounds. Each round you shoot once and then defend once.
When you shoot, pick a side (left/right/center) and a power (1-5). 
The goalie dives to a random side. You score unless he dives to the same side you picked.
The higher powered shots are harder to save even if the goalie dives to the right side, but drain your energy. If you have higher fatigue, you will miss shots more often.
When you defend, pick a side to dive. The computer shoots to a random side with a random power. 
If the score is tied after 5 rounds, it goes to sudden death until someone wins.

#### Fatigue:
Fatigue is a unique factor that comes into play the more you shot at high levels. The following table lays out save and miss percentages for each power level. 

Power Level 1: 0% miss chance, 90% save chance

Power Level 2: 5% miss chance, 75% save chance

Power Level 3: 10% miss chance, 55% save chance

Power Level 4: 20% miss chance, 35% save chance

Power Level 5: 30% miss chance, 20% save chance

There is also an additional penalty of an increase in miss chance of 7% for higher fatigue levels. For example, fatigue level 2 means you have 14% more chance to miss. Fatigue level 4 means you have 28% more chance to miss. The computer faces the same fatigue issue. Power 1 and 2 shots lower your fatigue one point, power 3 remains the same, and 4-5 increase your fatigue one point.


#### How State Is Stored:

The game keeps track of the score, computer and player fatigue, and what round it is. It cycles through rounds until someone can't win, or the game is tied after 5 rounds.
The user state is tracked by the amount of times they use different power level shots. Same with the computer. Each round cycles through a player shot and computer shot. At the end of each round, the game checks whether the player or computer can still win. If they can, the game moves to the next round, otherwise it breaks and sends the
closing message. 