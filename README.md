# Q-Maze
With Q-learning algorithm you can define a reward function that gives a reward to each action that agent does. Base on these rewards and punishments, agent can find the correct way and gain the goal.
In this maze solver, two reward functions are defined which are named R1 and R2. In R1 neighbors of goal have 10 and the other cells have 0 points. In R2 neighbors of goal have a big positive point but cells which have just one valid neighbor have a big negative point.
You can choose your reward function in solve function in solver.py.
